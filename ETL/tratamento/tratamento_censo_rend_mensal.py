import pandas as pd
import numpy as np

def selecionar_colunas_censo_rend_mensal(path_censo_2010_renda):
    # Lendo dados do Censo 2010 - Rendimento mensal per capta (Tabela 8)
    # Deleta os subtotais da tabela importada
    cols_names = ['COD_MUN','UF','MUNICIPIO','VLR_MEDIO_REND','VLR_QUARTIL_1','VLR_MEDIANA_REND','VALOR_QUARTIL_3']
    dict= {'COD_MUN':str, 'UF':str, 'MUNICIPIO':str, 'VLR_MEDIO_REND':np.int64,'VLR_MEDIANA_REND':np.int64}
    df_censo_2010_renda = pd.read_excel(path_censo_2010_renda, skiprows=10, index_col=None, dtype=dict, names=cols_names)
    df_censo_2010_renda.dropna(subset=['COD_MUN'], inplace=True)

    return df_censo_2010_renda

def selecionar_colunas_censo_pop(path_censo_2010_pop):
    # Lendo dados do Censo 2010 - População (Tabela 1)
    # Deleta os subtotais da tabela importada
    cols_names = ['COD_MUN','UF','MUNICIPIO','POPULACAO','URBANA','RURAL','HOMEM','MULHER','RAZÃO_SEXO']
    dict= {'COD_MUN':str, 'UF':str, 'MUNICIPIO':str, 'POPULACAO':np.float64}
    df_censo_2010_pop = pd.read_excel(path_censo_2010_pop, skiprows=8, index_col=None, dtype=dict , names=cols_names)
    df_censo_2010_pop.dropna(subset=['COD_MUN'], inplace=True)

    return df_censo_2010_pop

def merge_pop_renda(df_censo_2010_renda, df_censo_2010_pop):
    df_censo_2010_pop_renda = df_censo_2010_renda.merge(df_censo_2010_pop, on='COD_MUN', how='inner',suffixes=(None, '_y'))[['COD_MUN','UF', 'MUNICIPIO','POPULACAO', 'VLR_MEDIO_REND','VLR_MEDIANA_REND']] 
    return df_censo_2010_pop_renda

def merge_rendimento_pop_rgi(df_reg_muni, df_censo_2010_pop_renda):
    # Fazendo o merge das informações de redimento (per capta) e população dos municípios por RGI
    colunas_df_reg_muni = {'COD_MUN':str, 'MUNICIPIO':str, 'COD_RGI':np.int64, 'NOME_RGI':str, 'POLO':str}
    colunas_df_censo_2010_pop_renda = {'COD_MUN':str, 'UF':str, 'MUNICIPIO':str, 'POPULACAO':np.float64, 'VLR_MEDIO_REND': np.float64, 'VLR_MEDIANA_REND': np.float64}
    df_reg_muni = df_reg_muni.astype(colunas_df_reg_muni)
    df_censo_2010_pop_renda = df_censo_2010_pop_renda.astype(colunas_df_censo_2010_pop_renda)
    
    df_rgi_merged = df_reg_muni.merge(df_censo_2010_pop_renda, on='COD_MUN', how='inner',suffixes=(None, '_y'))[['COD_MUN', 'MUNICIPIO','COD_RGI','NOME_RGI','POLO','POPULACAO', 'VLR_MEDIO_REND','VLR_MEDIANA_REND']] 
    df_rgi_merged.sort_values(by=['COD_RGI','COD_MUN'], inplace=True,
                ascending = [True, True])

    return df_rgi_merged

def my_agg(x):
    names = {
        'TOT_POPULACAO': x['POPULACAO'].sum(),
        'TOT_VLR_REND_POND': (x['POPULACAO']*x['VLR_MEDIO_REND']).sum(),
        }
    return pd.Series(names)

def aplicar_my_agg(df_rgi_merged):
    # Agrupando e calculando o Rendimento Médio Mensal (per capta) por RGI
    df_rgi_rend_medio = df_rgi_merged.groupby('COD_RGI', as_index=False)['COD_MUN','COD_RGI','POPULACAO','VLR_MEDIO_REND'].apply(my_agg)
    df_rgi_rend_medio['VLR_REND_MEDIO']=round(df_rgi_rend_medio['TOT_VLR_REND_POND']/df_rgi_rend_medio['TOT_POPULACAO'],2)
    return df_rgi_rend_medio

def merge_rgi_renda_media(df_reg_muni, df_rgi_rend_medio):
    df_rgi_rend_mean_md = df_reg_muni.merge(df_rgi_rend_medio, on='COD_RGI', how='left',suffixes=(None, '_y')) [['COD_MUN', 'MUNICIPIO','COD_RGI','NOME_RGI','POLO', 'VLR_REND_MEDIO']] 
    df_rgi_rend_mean_md.rename(columns={'VLR_REND_MEDIO':'VLR_REND_MEDIO_RGI'}, inplace=True)                                   
    return df_rgi_rend_mean_md

def calcular_media_ponderada_por_rgi(df_rgi_merged):
    ## Criando dataFrame de saída
    df_rgi_rend_w_md = pd.DataFrame({'COD_RGI': pd.Series(dtype='object'),
                                    'VLR_REND_W_MD_RGI': pd.Series(dtype='int64')})
    ## Fazendo o agrupamento por RGI
    by_rgi =  df_rgi_merged.groupby('COD_RGI', as_index=False)

    ## Iterando com o GroupByDataFrame (pra cada grupo de municípios de um dado RGI)
    for rgi, frame in by_rgi:
        frame.sort_values(by=['VLR_MEDIANA_REND'],inplace=True)
        frame['CumSum']=frame['POPULACAO'].cumsum()
        cutoff = frame['POPULACAO'].sum() / 2.0
        median = frame[frame['CumSum'] > cutoff].iloc[0,7]
        ## Adicionando nova linha do DataFrame de saída para o RGI corrente 
        new_row = {'COD_RGI':rgi, 'VLR_REND_W_MD_RGI':median}
        df_rgi_rend_w_md = df_rgi_rend_w_md.append(new_row, ignore_index=True)
        
    return df_rgi_rend_w_md

def merge_renda_media_ponderada(df_rgi_rend_mean_md, df_rgi_rend_w_md):
    df_rgi_rend_mean_md = df_rgi_rend_mean_md.merge(df_rgi_rend_w_md, on='COD_RGI', how='left',suffixes=(None, '_y')) [['COD_MUN', 'MUNICIPIO','COD_RGI','NOME_RGI','POLO', 'VLR_REND_MEDIO_RGI','VLR_REND_W_MD_RGI']] 
    return df_rgi_rend_mean_md