
#%%

import numpy as np
import pandas as pd
import re
import math

# Lendo dados do Enade (anos de 2015, 2016, 2017, 2018 e 2019) - considera-se a mais recente avaliação do curso no período
#importando os dados da pasta local
cols_names=['ANO','COD_IES','SIGLA_IES','COD_CURSO','MODALIDADE','COD_AREA','AREA','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
dict= {'ANO':str, 'COD_IES':str, 'SIGLA_IES':str, 'COD_CURSO':str,'MODALIDADE':str,\
       'COD_MUN':str,'NUM_PART':np.int64,'CPC_CONTINUO':np.float64,'CPC_FAIXA':str}

def selecionar_colunas_enade_2015(path_enade_inep):
       # Ano = 2015
       cols_names_ano=['ANO','COD_IES','SIGLA_IES','COD_CURSO','COD_AREA','AREA','MODALIDADE','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
       df_enade_ano = pd.read_excel(path_enade_inep,  dtype=dict, usecols=[0,1,3,6,7,8,9,10,14,35,36],\
                            names=cols_names_ano, na_values=['-','SC'])
       df_enade_ano.dropna(subset = ['CPC_CONTINUO'],inplace=True)
       df_enade_ano.reset_index(inplace=True)
       df_enade_ano = df_enade_ano[cols_names]
       return df_enade_ano

def selecionar_colunas_enade_2016(path_enade_inep):
       # Ano = 2016
       cols_names_ano=['ANO','COD_IES','SIGLA_IES','COD_CURSO','COD_AREA','AREA','MODALIDADE','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
       df_enade_ano = pd.read_excel(path_enade_inep,  dtype=dict, usecols=[0,1,3,6,7,8,9,10,14,35,36],\
                            names=cols_names_ano, na_values=['-','SC'])
       df_enade_ano.dropna(subset = ['CPC_CONTINUO'],inplace=True)
       df_enade_ano.reset_index(inplace=True)
       df_enade_ano = df_enade_ano[cols_names]
       return df_enade_ano

def selecionar_colunas_enade_2017(path_enade_inep):
       # Ano = 2017
       cols_names_ano=['ANO','COD_AREA','AREA','COD_IES','SIGLA_IES','COD_CURSO','MODALIDADE','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
       df_enade_ano = pd.read_excel(path_enade_inep,  dtype=dict, usecols=[0,1,2,3,4,8,9,10,14,35,36],\
                            names=cols_names_ano, na_values='SC')
       df_enade_ano.dropna(subset = ['CPC_CONTINUO'],inplace=True)
       df_enade_ano.reset_index(inplace=True)
       df_enade_ano = df_enade_ano[cols_names]
       return df_enade_ano

def selecionar_colunas_enade_2018(path_enade_inep):
       # Ano = 2018
       cols_names_ano=['ANO','COD_IES','SIGLA_IES','COD_CURSO','COD_AREA','AREA','MODALIDADE','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
       df_enade_ano = pd.read_excel(path_enade_inep,  dtype=dict, usecols=[0,1,3,6,7,8,9,10,14,36,37],\
                            names=cols_names_ano, na_values=['-','SC'])
       df_enade_ano.dropna(subset = ['CPC_CONTINUO'],inplace=True)
       df_enade_ano.reset_index(inplace=True)
       df_enade_ano = df_enade_ano[cols_names]
       return df_enade_ano

def selecionar_colunas_enade_2019(path_enade_inep):
       # Ano = 2019
       cols_names_ano=['ANO','COD_AREA','AREA','COD_IES','SIGLA_IES','COD_CURSO','MODALIDADE','COD_MUN','NUM_PART','CPC_CONTINUO','CPC_FAIXA']
       df_enade_ano = pd.read_excel(path_enade_inep,  dtype=dict, usecols=[0,1,2,3,5,8,9,10,14,36,37],
                            names=cols_names_ano, na_values='SC')
       df_enade_ano.dropna(subset = ['CPC_CONTINUO'],inplace=True)
       df_enade_ano.reset_index(inplace=True)
       df_enade_ano = df_enade_ano[cols_names]
       return df_enade_ano

def criar_dataframe_de_saida_enade(df_enade):
       df_enade_curso_ultima_avaliacao = pd.DataFrame({'COD_MUN': pd.Series(dtype='object'),
                                                'COD_CURSO': pd.Series(dtype='object'),
                                                'COD_IES':pd.Series(dtype='object'),
                                                'SIGLA_IES':pd.Series(dtype='object'),
                                                'COD_AREA': pd.Series(dtype='object'),
                                                'AREA': pd.Series(dtype='object'),
                                                'NUM_PART': pd.Series(dtype='int'),
                                                'CPC_CONTINUO': pd.Series(dtype='float64'),
                                                'CPC_FAIXA':pd.Series(dtype='object'),
                                                'ANO_AVALIACAO': pd.Series(dtype='object'),
                                                'QT_AVALIAÇÕES': pd.Series(dtype='int'),})
       ## Fazendo o agrupamento por ano e curso
       by_ano =  df_enade.groupby('COD_CURSO', as_index=False)

       ## Iterando com o GroupByDataFrame (pra cada curso)
       for cd_curso, frame in by_ano:
              frame.sort_values(by=['ANO'],inplace=True)
              ## Selecionando dados da última linha (última avaliação feita)
              new_row = {'COD_MUN':frame.iloc[-1,7],\
                            'COD_CURSO':cd_curso,\
                            'COD_IES':frame.iloc[-1,1],\
                            'SIGLA_IES':frame.iloc[-1,2],\
                            'COD_AREA':frame.iloc[-1,5],\
                            'NUM_PART':frame.iloc[-1,8],\
                            'AREA':frame.iloc[-1,6],\
                            'CPC_CONTINUO':frame.iloc[-1,9],\
                            'CPC_FAIXA':frame.iloc[-1,10],\
                            'ANO_AVALIACAO':frame.iloc[-1,0],\
                            'QT_AVALIAÇÕES':frame['ANO'].count()}
              df_enade_curso_ultima_avaliacao = df_enade_curso_ultima_avaliacao.append(new_row, ignore_index=True)

       return df_enade_curso_ultima_avaliacao


def enade_grau_academico(s):
       # Tirar o parênteses onde tem LICENCIATURA ou BACHARELADO ou ainda a expressão "TECNOLOGIA EM", colocar na Coluna de Grau Acadêmico
       # 1- Bacharelado, 2 - Licenciatura e 3- Tecnológico
       good_chars = 'a-zA-Z0-9\s\'áéíóúüÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ\-'
       if re.search('['+ good_chars+']*(\(.*\))', s['AREA']):
              grau_acad = re.search('['+ good_chars+']*\((.*)\)', s['AREA']).group(1)
              nm_curso = re.search('['+ good_chars+']*(?=\(.*\))', s['AREA']).group(0).strip()        
       else:
              if s['AREA'].find('TECNOLOGIA EM')>=0:
                     grau_acad = 'TECNOLOGICO' 
                     nm_curso = re.search('TECNOLOGIA EM (.*)',s['AREA']).group(1) 
              else:
                     grau_acad = 'BACHARELADO'
                     nm_curso = s['AREA']
       # colocando na mesma codificação adotada no Censo Superior e ajustando o nome (espaços entre hífen e nome dos cursos)
       if grau_acad == 'BACHARELADO':
              grau = '1'
       elif grau_acad == 'LICENCIATURA':
              grau = '2'
              
       elif grau_acad == 'TECNOLOGICO':
              grau = '3'
       else:
              grau = '4'
       nm_curso=re.sub('\-|\s\-\s',' - ',nm_curso)

       return pd.Series([grau,nm_curso],index=['grau','nm_curso'])

def aplicar_enade_grau_academico(df_enade_curso_ultima_avaliacao):
       # Aplicando função enade_grau_academico
       df_enade_curso_ultima_avaliacao[['GRAU_ACADEMICO','CURSO']] = df_enade_curso_ultima_avaliacao.apply(lambda x: enade_grau_academico(x),axis=1)
       return df_enade_curso_ultima_avaliacao

def my_agg_enade(x):
    names = {
        'TOT_PART_IES_MUN': x['NUM_PART'].sum(),
        'PROD_PART_CPC_CONTINUO': (x['NUM_PART']*x['CPC_CONTINUO']).sum(),
        'PROD_PART_CPC_FAIXA': (x['NUM_PART']*x['CPC_FAIXA'].astype('int64')).sum(),
        }
    return pd.Series(names)

def calcular_media_enade(df_enade_curso_ultima_avaliacao):
       # Calculando a média do Enade-CPC por IES e Município
       df_enade_ies_mun_med = df_enade_curso_ultima_avaliacao.groupby(['COD_IES','COD_MUN'], as_index=False)['COD_IES','COD_MUN',\
                                                        'NUM_PART','CPC_CONTINUO','CPC_FAIXA'].apply(my_agg_enade)


       df_enade_ies_mun_med['MEDIA_IES_MUN_CPC_CONTINUO']=df_enade_ies_mun_med['PROD_PART_CPC_CONTINUO']/df_enade_ies_mun_med['TOT_PART_IES_MUN']
       df_enade_ies_mun_med['MEDIA_IES_MUN_CPC_FAIXA']=round(df_enade_ies_mun_med['PROD_PART_CPC_FAIXA']/df_enade_ies_mun_med['TOT_PART_IES_MUN'],2)
       df_enade_ies_mun_med['MEDIA_IES_MUN_CPC_FAIXA']=df_enade_ies_mun_med['MEDIA_IES_MUN_CPC_FAIXA'].apply(lambda x: math.floor(x))

       df_enade_ies_mun_med= df_enade_ies_mun_med[['COD_IES','COD_MUN','TOT_PART_IES_MUN','MEDIA_IES_MUN_CPC_CONTINUO','MEDIA_IES_MUN_CPC_FAIXA']]
       return df_enade_ies_mun_med

def calcular_media_ponderada_enade(df_enade_curso_ultima_avaliacao):
       # Agrupando e calculando a Mediana Ponderada (Weighted Median) do CPC-Enade por IES e Município
       df_enade_ies_mun_md = pd.DataFrame({'COD_IES': pd.Series(dtype='object'),
                                    'COD_MUN':pd.Series(dtype='object'),
                                    'TOT_PART_IES_MUN':pd.Series(dtype='int64'),
                                    'MEDIANA_IES_MUN_CPC_CONTINUO': pd.Series(dtype='int64'),
                                    'MEDIANA_IES_MUN_CPC_FAIXA':pd.Series(dtype='int64')})
       ## Fazendo o agrupamento por IES e Município
       by_ies_mun =  df_enade_curso_ultima_avaliacao.groupby(['COD_IES','COD_MUN'], as_index=False)

       ## Iterando com o GroupByDataFrame (pra cada grupo de ies e municípios)
       for ies_mun, frame in by_ies_mun:
              frame.sort_values(by=['CPC_CONTINUO'],inplace=True)
              frame['CumSum']=frame['NUM_PART'].cumsum()
              cutoff = frame['NUM_PART'].sum() / 2.0
              median_cont = frame[frame['CumSum'] > cutoff].iloc[0,7]
              median_faixa = float(frame[frame['CumSum'] > cutoff].iloc[0,8])
              ## Adicionando nova linha do DataFrame de saída para o RGI corrente 
              new_row = {'COD_IES':frame.iloc[0,2],
                            'COD_MUN':frame.iloc[0,0],
                            'TOT_PART_IES_MUN':frame['NUM_PART'].sum(),
                            'MEDIANA_IES_MUN_CPC_CONTINUO':median_cont,
                            'MEDIANA_IES_MUN_CPC_FAIXA':median_faixa}
              df_enade_ies_mun_md = df_enade_ies_mun_md.append(new_row, ignore_index=True)
                  
       return df_enade_ies_mun_md


def ler_enade_arquivo_1_31_32(path_enade_qi25, path_enade_qi26):
       # Lendo dados do Enade (arquivo 1: dados do curso e ies)

       # Lendo dados do Enade (arquivo 31 e 32 - questões 25 e 26: questionário sobre motivo de opção pelo curso e ies)
       df_enade_qi25 = pd.read_csv(path_enade_qi25,  dtype=str, sep=';')
       df_enade_qi25.dropna(subset = ['QE_I25'],inplace=True)
       df_enade_qi25.reset_index(inplace=True, drop=True)

       # Lendo dados do Enade (arquivo 31 e 32: questionário sobre motivo de opção pelo curso e ies)
       df_enade_qi26 = pd.read_csv(path_enade_qi26,  dtype=str, sep=';')
       df_enade_qi26.dropna(subset = ['QE_I26'],inplace=True)
       df_enade_qi26.reset_index(inplace=True, drop=True)

       return df_enade_qi25, df_enade_qi26

def tratar_tabelas_enade(path_enade_aluno, df_enade_qi25, df_enade_qi26):
       # Agrupando as tabelas com resposta às QE I26  (escolha da IES)
       # Motivações agrupadas por: Opção por qualidade (interesses/vocação) ou por facilidade (oportunidade, conveniência)
       dict= {'NU_ANO':str, 'CO_CURSO':str, 'CO_IES':str, 'CO_CATEGAD':str,'CO_ORGACAD':str,\
              'CO_GRUPO':str,'CO_MODALIDADE':np.int64,'CO_MUNIC_CURSO':str,'CPC_FAIXA':str}
       
       df_enade_aluno = pd.read_csv(path_enade_aluno,  dtype=dict, usecols=[0,1,2,3,4,6,7],sep=';')

       df_enade_qi25['ESCOLHA_QUALI']=[1 if x in ('ABCDE') else 0 for x in df_enade_qi25['QE_I25'] ]
       df_enade_qi26['ESCOLHA_QUALI']=[1 if x in ('F') else 0 for x in df_enade_qi26['QE_I26'] ]

       df_enade_esc_quali = df_enade_qi26.groupby(['CO_CURSO']).agg({'QE_I26': 'count','ESCOLHA_QUALI':'sum'}).reset_index()
       df_enade_esc_quali['TX_ESC_QUALI_IES']=round(df_enade_esc_quali['ESCOLHA_QUALI']/df_enade_esc_quali['QE_I26'],2)

       # Recuperando dados da IES
       df_curso_ies = df_enade_aluno.groupby(['CO_CURSO','CO_IES','CO_MUNIC_CURSO','CO_MODALIDADE'], as_index=False).agg({'NU_ANO':'count'}).rename(columns={'NU_ANO':'QTD'})
       df_enade_esc_quali_ies = df_enade_esc_quali.merge(df_curso_ies,on='CO_CURSO',how='left')[['CO_CURSO','CO_MODALIDADE','CO_IES','CO_MUNIC_CURSO','TX_ESC_QUALI_IES']]
       df_enade_esc_quali_ies.rename(columns={'CO_CURSO':'COD_CURSO','CO_IES':'COD_IES','CO_MUNIC_CURSO':'COD_MUN'},inplace=True)

       return df_enade_esc_quali_ies