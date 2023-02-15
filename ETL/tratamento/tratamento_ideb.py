import numpy as np
import pandas as pd

def matriculas_por_tipo_escola_municipio(df_censo_basica, ano):
    # Total de matrículas no ensino médio por município e tipo de escola (pública/privada) para o ano de 2019
    df_censo_basica["ANO"] = df_censo_basica["ANO"].astype(str)
    df_mat_med_rede = df_censo_basica[(df_censo_basica['ANO'] == ano)&(df_censo_basica['TIPO_ESCOLA'].isin([2,4]))&\
                                 (df_censo_basica['QT_TOT_MAT_MED'] > 0)].groupby(['COD_MUN','TIPO_ESCOLA'], as_index=False)\
                                ['QT_TOT_MAT_MED'].sum()

    return df_mat_med_rede

def calcular_prop_rede_escolar(df_mat_med_rede):
    # Calculando a proporção da rede escolar (pública e privada) de Ensino Médio
    df_mat_prop_med_rede = pd.pivot_table(df_mat_med_rede, values='QT_TOT_MAT_MED', columns=['TIPO_ESCOLA'], index=['COD_MUN']).rename_axis(None, axis=1)
    df_mat_prop_med_rede.reset_index(inplace=True)
    df_mat_prop_med_rede.rename(columns={2:'ESCOLA_PUBLICA',4:'ESCOLA_PRIVADA'}, inplace=True)   
    df_mat_prop_med_rede.fillna(0, inplace=True)

    # Obs: Nem todos os municípios ofertam o Ensino Médio
    df_mat_prop_med_rede['PROP_PUBLICA']=df_mat_prop_med_rede['ESCOLA_PUBLICA']/(df_mat_prop_med_rede['ESCOLA_PUBLICA']+df_mat_prop_med_rede['ESCOLA_PRIVADA'])
    df_mat_prop_med_rede['PROP_PRIVADA']=1-df_mat_prop_med_rede['PROP_PUBLICA']

    return df_mat_prop_med_rede

def selecionar_colunas_ideb(path_ideb_med, ano):
    # Lendo dados do Ideb por município (ano de 2019)
    #importando os dados da pasta local
    cols_names=['UF','COD_MUN','MUNICIPIO','TIPO_REDE','IDEB']
    dict= {'UF':str, 'COD_MUN':str, 'MUNICIPIO':str, 'TIPO_REDE':str,'IDEB':np.float64}
    if ano == 2019:
        usecols=[0,1,2,3,23]
    else:
        usecols=[0,1,2,3,13]
    df_ideb_med = pd.read_excel(path_ideb_med, dtype=str,skiprows=9, skipfooter=3, usecols=usecols, na_values='-', names=cols_names)
    df_ideb_med.dropna(subset = ['IDEB'],inplace=True)
    df_ideb_med.reset_index(inplace=True)

    # Pivoteando o DF por tipo de escola
    df_ideb_med['IDEB'] = df_ideb_med['IDEB'].astype(np.float64)
    df_ideb_med_rede = pd.pivot_table(df_ideb_med[df_ideb_med['TIPO_REDE'].isin(['Estadual','Pública'])], values='IDEB', columns=['TIPO_REDE'], index=['COD_MUN']).rename_axis(None, axis=1)
    df_ideb_med_rede.reset_index(inplace=True)
    df_ideb_med_rede.rename(columns={'Estadual':'IDEB_ESCOLA_PRIVADA','Pública':'IDEB_ESCOLA_PUBLICA'}, inplace=True)   
    # df_mat_prop_med_rede.fillna(0, inplace=True)
    return df_ideb_med_rede

def ajusta_ideb_na (priv, pub, tipo):
    if tipo == 'pub':
        if pd.isna(pub):
            return (priv)
        else:
            return (pub)
    elif tipo == 'priv':
        if pd.isna(priv):
            return (pub)
        else:
            return (priv)

def aplicar_ajusta_ideb_na(df_ideb_med_rede):
    df_ideb_med_rede['IDEB_ESCOLA_PUBLICA']=df_ideb_med_rede[['IDEB_ESCOLA_PRIVADA','IDEB_ESCOLA_PUBLICA']].apply(lambda x: ajusta_ideb_na(x['IDEB_ESCOLA_PRIVADA'],x['IDEB_ESCOLA_PUBLICA'],'pub'), axis=1)
    df_ideb_med_rede['IDEB_ESCOLA_PRIVADA']=df_ideb_med_rede[['IDEB_ESCOLA_PRIVADA','IDEB_ESCOLA_PUBLICA']].apply(lambda x: ajusta_ideb_na(x['IDEB_ESCOLA_PRIVADA'],x['IDEB_ESCOLA_PUBLICA'],'priv'), axis=1)
    return df_ideb_med_rede

def calcular_ideb(df_ideb_med_rede, df_mat_prop_med_rede):
    # Calcular a IDEB proporcional à quantidade de matrículas para redes públicas e privadas
    df_mat_prop_med_rede['COD_MUN'] = df_mat_prop_med_rede['COD_MUN'].astype(str)
    df_ideb_prop = df_ideb_med_rede.merge(df_mat_prop_med_rede,on='COD_MUN',how='inner',suffixes=(None, '_y'))\
                [['COD_MUN','ESCOLA_PUBLICA','PROP_PUBLICA','ESCOLA_PRIVADA','PROP_PRIVADA','IDEB_ESCOLA_PUBLICA','IDEB_ESCOLA_PRIVADA']]
    df_ideb_prop['IDEB_MUN']=round(df_ideb_prop['PROP_PUBLICA']*df_ideb_prop['IDEB_ESCOLA_PUBLICA'] + \
                            df_ideb_prop['PROP_PRIVADA']*df_ideb_prop['IDEB_ESCOLA_PRIVADA'],2)
    df_ideb_prop['QTD_MAT_MUN']=df_ideb_prop['ESCOLA_PUBLICA']+df_ideb_prop['ESCOLA_PRIVADA']
    df_ideb_prop.drop(['ESCOLA_PUBLICA', 'ESCOLA_PRIVADA'], axis=1)
    df_ideb_prop = df_ideb_prop[['COD_MUN','QTD_MAT_MUN','PROP_PUBLICA','IDEB_ESCOLA_PUBLICA','IDEB_ESCOLA_PRIVADA','IDEB_MUN']]
    return df_ideb_prop

def ideb_por_rgi(df_ideb_prop, df_rgi):
    # IDEB por RGI (proporcional à qtd Matrícula) - merge das tabelas
    df_ideb_prop_merged = df_ideb_prop.merge(df_rgi, on='COD_MUN',how='right',suffixes=(None, '_y'))[['COD_MUN','MUNICIPIO','COD_RGI','QTD_MAT_MUN',\
                                                        'PROP_PUBLICA','IDEB_ESCOLA_PUBLICA','IDEB_ESCOLA_PRIVADA','IDEB_MUN']]
    df_ideb_prop_merged.sort_values(by=['COD_RGI','COD_MUN'], inplace=True, ascending = [True, True],ignore_index=True)
    return df_ideb_prop_merged

def ajusta_ideb_rgi_na (prop_pub):
    if pd.isna(prop_pub):
        return (1.0)
    else:
        return (prop_pub)

def aplicar_ajusta_ideb_rgi_na(df_ideb_prop_merged):
    df_ideb_prop_merged['PROP_PUBLICA']=df_ideb_prop_merged['PROP_PUBLICA'].apply(lambda x: ajusta_ideb_rgi_na(x))
    df_ideb_prop_merged.fillna(0,inplace=True)
    return df_ideb_prop_merged


def my_agg_ideb(x):
    names = {
        'TOT_MATRICULA': x['QTD_MAT_MUN'].sum(),
        'MAT_X_IDEB': (x['QTD_MAT_MUN']*x['IDEB_MUN']).sum(),
        }
    return pd.Series(names)

def aplicar_my_agg_ideb(df_ideb_prop_merged):
    df_ideb_rgi = df_ideb_prop_merged.groupby('COD_RGI', as_index=False)['COD_MUN','COD_RGI','QTD_MAT_MUN','IDEB_MUN'].apply(my_agg_ideb)
    df_ideb_rgi['IDEB_RGI']=round(df_ideb_rgi['MAT_X_IDEB']/df_ideb_rgi['TOT_MATRICULA'],2)
    return df_ideb_rgi