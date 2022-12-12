#%%

import numpy as np
import pandas as pd

def selecionar_colunas_enem(path_enem_med):
       cols_names=['ANO','SIT_CONC','ANO_CONC','TREINEIRO','COD_MUN_PROVA','NOTA_CN','NOTA_CH','NOTA_LC','NOTA_MT','NOTA_REDACAO']
       dict= {'ANO':str, 'SIT_CONC':str, 'ANO_CONC':str, 'TREINEIRO':str,'COD_MUN_PROVA':str,\
              'NOTA_CN':np.float64,'NOTA_CH':np.float64,'NOTA_LC':np.float64,'NOTA_MT':np.float64,'NOTA_REDACAO':np.float64}
       df_enem_ano = pd.read_csv(path_enem_med, skiprows=1, dtype=dict, usecols=[1,7,8,11,19,31,32,33,34,50],\
                            names=cols_names, encoding='latin-1', sep=';')
       # Selecionando candidatos não treineiros, os que tem notas válidas em todas as provas e concluintes dos últimos 3 anos 
       df_enem_ano = df_enem_ano[(df_enem_ano['TREINEIRO']=='0') & (df_enem_ano['ANO_CONC'].isin(['0','1','2','3']))&\
              (df_enem_ano['NOTA_CN'].notna())&(df_enem_ano['NOTA_CH'].notna())&\
              (df_enem_ano['NOTA_LC'].notna())&(df_enem_ano['NOTA_MT'].notna())&(df_enem_ano['NOTA_REDACAO'].notna())]
       return df_enem_ano


def calcular_media_por_municipio(df_enem):
       # Calculando a média das notas e agrupando por ano e município
       df_enem['MEDIA_NOTAS'] = (df_enem['NOTA_CN'] + df_enem['NOTA_CH'] + df_enem['NOTA_LC'] + df_enem['NOTA_MT'] +\
                            df_enem['NOTA_REDACAO'])/5   

       df_enem_mun = df_enem.groupby(['ANO','COD_MUN_PROVA'], as_index=False).agg({'SIT_CONC':'count',\
                                                               'MEDIA_NOTAS':'mean'})
       df_enem_mun.rename(columns={'SIT_CONC':'QTD_CANDIDATOS'}, inplace=True)                                   
       return df_enem_mun


def pivotear_ano_qtd_candidatos(df_enem_mun):
       # Pivoteando por ano para quantidade de candidatos por município da prova
       df_enem_qtd = pd.pivot_table(df_enem_mun, values='QTD_CANDIDATOS', columns=['ANO'], index=['COD_MUN_PROVA']).rename_axis(None, axis=1)
       df_enem_qtd.reset_index(inplace=True)
       df_enem_qtd.rename(columns={'COD_MUN_PROVA':'COD_MUN','2018':'QT_CAND_2018','2019':'QT_CAND_2019','2020':'QT_CAND_2020'}, inplace=True)                                   
       return df_enem_qtd


def pivotear_ano_media_notas(df_enem_mun):
       # Pivoteando por ano para média das notas por município da provadf_enem_qtd = pd.pivot_table(df_enem_mun, values='QTD_CANDIDATOS', columns=['ANO'], index=['COD_MUN_PROVA']).rename_axis(None, axis=1)
       df_enem_nota = pd.pivot_table(df_enem_mun, values='MEDIA_NOTAS', columns=['ANO'], index=['COD_MUN_PROVA']).rename_axis(None, axis=1)
       df_enem_nota.reset_index(inplace=True)
       df_enem_nota.rename(columns={'COD_MUN_PROVA':'COD_MUN','2018':'MEDIA_NOTAS_2018','2019':'MEDIA_NOTAS_2019','2020':'MEDIA_NOTAS_2020'}, inplace=True)                                   
       return df_enem_nota


def calcular_media_por_rgi(df_pop, df_rgi, df_enem_qtd_notas):
       # Fazendo merge para calcular proporção de candidatos pela população e média (para cada RGI)
       # Obs: nesse caso não faz sentido calcular por município, pois as provas não são realizadas em todos os municípios
       df_pop_rgi = df_pop.merge(df_rgi,on='COD_MUN',how='inner',suffixes=(None, '_y'))[['COD_MUN','UF','MUNICIPIO','COD_RGI',\
                                                               'POPULACAO_2018', 'POPULACAO_2019','POPULACAO_2020']]
       df_enem_mun_qtd_notas = df_pop_rgi.merge(df_enem_qtd_notas, on='COD_MUN', how='left',suffixes=(None, '_y'))[['COD_MUN','MUNICIPIO','COD_RGI',\
                                                 'POPULACAO_2018','POPULACAO_2019','POPULACAO_2020',\
                                                 'QT_CAND_2018','QT_CAND_2019','QT_CAND_2020',\
                                                 'MEDIA_NOTAS_2018','MEDIA_NOTAS_2019','MEDIA_NOTAS_2020']]
       df_enem_mun_qtd_notas.fillna(0,inplace=True)
       df_enem_mun_qtd_notas.sort_values(by=['COD_RGI','COD_MUN'], inplace=True,
                     ascending = [True, True],ignore_index=True)

       return df_enem_mun_qtd_notas, df_pop_rgi

def my_agg_enem(x):
       # Agrupamento pra calcular proporção de candidatos em relação à população e a média das notas do RGI
       # (ponderada pela qtd de candidatos em cada município foi aplicada prova)
       names = {
              'TOT_POPULACAO_2018': x['POPULACAO_2018'].sum(),
              'TOT_POPULACAO_2019': x['POPULACAO_2019'].sum(),
              'TOT_POPULACAO_2020': x['POPULACAO_2020'].sum(),
              'TOT_CAND_2018': x['QT_CAND_2018'].sum(),
              'TOT_CAND_2019': x['QT_CAND_2019'].sum(),
              'TOT_CAND_2020': x['QT_CAND_2020'].sum(),
              'PROD_MEDIA_CAND_2018': (x['QT_CAND_2018']*x['MEDIA_NOTAS_2018']).sum(),
              'PROD_MEDIA_CAND_2019': (x['QT_CAND_2019']*x['MEDIA_NOTAS_2019']).sum(),
              'PROD_MEDIA_CAND_2020': (x['QT_CAND_2020']*x['MEDIA_NOTAS_2020']).sum()
              }
       return pd.Series(names)

def calcular_proporcao_candidatos(df_enem_mun_qtd_notas):
       df_enem_mun_rgi = df_enem_mun_qtd_notas.groupby('COD_RGI', as_index=False)['COD_MUN','COD_RGI',\
                                                    'POPULACAO_2018','POPULACAO_2019','POPULACAO_2020',\
                                                    'QT_CAND_2018','QT_CAND_2019','QT_CAND_2020',\
                                                    'MEDIA_NOTAS_2018','MEDIA_NOTAS_2019','MEDIA_NOTAS_2020'].apply(my_agg_enem)

       df_enem_mun_rgi['PROP_CAND_RGI_2018']=df_enem_mun_rgi['TOT_CAND_2018']/df_enem_mun_rgi['TOT_POPULACAO_2018']
       df_enem_mun_rgi['PROP_CAND_RGI_2019']=df_enem_mun_rgi['TOT_CAND_2019']/df_enem_mun_rgi['TOT_POPULACAO_2019']
       df_enem_mun_rgi['PROP_CAND_RGI_2020']=df_enem_mun_rgi['TOT_CAND_2020']/df_enem_mun_rgi['TOT_POPULACAO_2020']
       df_enem_mun_rgi['MEDIA_NOTAS_RGI_2018']=df_enem_mun_rgi['PROD_MEDIA_CAND_2018']/df_enem_mun_rgi['TOT_CAND_2018']
       df_enem_mun_rgi['MEDIA_NOTAS_RGI_2019']=df_enem_mun_rgi['PROD_MEDIA_CAND_2019']/df_enem_mun_rgi['TOT_CAND_2019']
       df_enem_mun_rgi['MEDIA_NOTAS_RGI_2020']=df_enem_mun_rgi['PROD_MEDIA_CAND_2020']/df_enem_mun_rgi['TOT_CAND_2020']

       return df_enem_mun_rgi

# %%
