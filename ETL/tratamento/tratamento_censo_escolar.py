import pandas as pd

def selecionar_colunas_censo_escolar(path_inep_censo):
    cols_names=['ANO','COD_MUN','COD_ESCOLA','NOME_ESCOLA','TIPO_ESCOLA','TIPO_LOCAL','SITUACAO','QT_MAT_MED','QT_MAT_PROF','QT_MAT_EJA_MED']
    df_censo_basica_ano = pd.read_csv(path_inep_censo, dtype=str, usecols=[0,7,13,14,15,17,26,305,307,310] ,names=cols_names, delimiter=';')
    df_censo_basica_ano = df_censo_basica_ano.iloc[1:,:] # removendo primeira linha dos nomes originais das colunas.
    return df_censo_basica_ano

def selecionar_escolas_em_atividade(df_censo_basica):
    df_censo_basica = df_censo_basica [df_censo_basica ['SITUACAO']=='1']
    df_censo_basica.fillna(0, inplace=True)
    df_censo_basica = df_censo_basica.astype({'QT_MAT_MED': 'int64','QT_MAT_PROF': 'int64', 'QT_MAT_EJA_MED': 'int64'})
    df_censo_basica['QT_TOT_MAT_MED']=df_censo_basica['QT_MAT_MED']+df_censo_basica['QT_MAT_PROF']+df_censo_basica['QT_MAT_EJA_MED']
    return df_censo_basica

def total_matriculas_por_mun_ano(df_censo_basica):
    return df_censo_basica.groupby(['ANO','COD_MUN'], as_index=False)['QT_TOT_MAT_MED'].sum()

def linhas_para_colunas(df_censo_basica_mun):
    df_censo_basica_mat = pd.pivot_table(df_censo_basica_mun, values='QT_TOT_MAT_MED', columns=['ANO'], index=['COD_MUN']).rename_axis(None, axis=1)
    df_censo_basica_mat.reset_index(inplace=True)
    df_censo_basica_mat.rename(columns={'2019':'QT_TOT_MAT_2019','2020':'QT_TOT_MAT_2020','2021':'QT_TOT_MAT_2021'}, inplace=True)
    return df_censo_basica_mat

def percentual_matricula_por_municipio(df_estimativa_pop, df_censo_basica_mat):
    # Calculando percentual de matrícula (ensino médio) em relação à população do município
    # para os anos de 2019, 2020 e 2021
    df_mat_prop_mun = df_estimativa_pop.merge(df_censo_basica_mat, on='COD_MUN',how='inner')[['COD_MUN','UF', 'MUNICIPIO','POPULACAO_2019', 'POPULACAO_2020','POPULACAO_2021',
                                                                        'QT_TOT_MAT_2019', 'QT_TOT_MAT_2020', 'QT_TOT_MAT_2021']] 
    df_mat_prop_mun['PERC_MAT_MUN_2019']=df_mat_prop_mun['QT_TOT_MAT_2019']/df_mat_prop_mun['POPULACAO_2019']*100
    df_mat_prop_mun['PERC_MAT_MUN_2020']=df_mat_prop_mun['QT_TOT_MAT_2020']/df_mat_prop_mun['POPULACAO_2020']*100
    df_mat_prop_mun['PERC_MAT_MUN_2021']=df_mat_prop_mun['QT_TOT_MAT_2021']/df_mat_prop_mun['POPULACAO_2021']*100
    return df_mat_prop_mun

def percentual_matricula_por_rgi(df_mat_prop_mun, df_rgi):
    # Fazendo merge e calculando o percentual de matrículas no ensino médio por RGI (em relação à população)
    df_prop_mat_merged = df_mat_prop_mun.merge(df_rgi, on='COD_MUN',how='inner',suffixes=(None, '_y'))[['COD_MUN','UF','COD_RGI','MUNICIPIO','POPULACAO_2019', 'POPULACAO_2020','POPULACAO_2021',
                                                            'QT_TOT_MAT_2019', 'QT_TOT_MAT_2020', 'QT_TOT_MAT_2021',
                                                            'PERC_MAT_MUN_2019', 'PERC_MAT_MUN_2020', 'PERC_MAT_MUN_2021']]
    df_prop_mat_merged.sort_values(by=['COD_RGI','COD_MUN'], inplace=True, ascending = [True, True])
    df_prop_mat_rgi = df_prop_mat_merged.groupby('COD_RGI',as_index=False)['POPULACAO_2019','QT_TOT_MAT_2019','POPULACAO_2020','QT_TOT_MAT_2020',
                                                            'POPULACAO_2021','QT_TOT_MAT_2021'].sum()
    df_prop_mat_rgi['PERC_MAT_RGI_2019']=df_prop_mat_rgi['QT_TOT_MAT_2019']/df_prop_mat_rgi['POPULACAO_2019']*100
    df_prop_mat_rgi['PERC_MAT_RGI_2020']=df_prop_mat_rgi['QT_TOT_MAT_2020']/df_prop_mat_rgi['POPULACAO_2020']*100
    df_prop_mat_rgi['PERC_MAT_RGI_2021']=df_prop_mat_rgi['QT_TOT_MAT_2021']/df_prop_mat_rgi['POPULACAO_2021']*100
    return df_prop_mat_rgi, df_prop_mat_merged

def merge_matriculas_mun_rgi(df_prop_mat_merged, df_prop_mat_rgi):
    df_mat_mun_rgi = df_prop_mat_merged.merge(df_prop_mat_rgi,on='COD_RGI',how='left',suffixes=(None, '_y'))[['COD_MUN','UF','COD_RGI','MUNICIPIO',
                                                        'QT_TOT_MAT_2019', 'QT_TOT_MAT_2020', 'QT_TOT_MAT_2021',
                                                        'PERC_MAT_MUN_2019', 'PERC_MAT_MUN_2020', 'PERC_MAT_MUN_2021',
                                                        'PERC_MAT_RGI_2019','PERC_MAT_RGI_2020','PERC_MAT_RGI_2021']]
    return df_mat_mun_rgi