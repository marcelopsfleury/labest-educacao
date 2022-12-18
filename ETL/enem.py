import pandas as pd
from tratamento import selecionar_colunas_enem, calcular_media_por_municipio, pivotear_ano_media_notas, pivotear_ano_qtd_candidatos, calcular_media_por_rgi, calcular_proporcao_candidatos

# Lendo dados do Enem (anos de 2018, 2019 e 2020)
path_enem_med = []
df_enem_ano = []

for path in path_enem_med:
    df_enem_ano.append(selecionar_colunas_enem(path))

df_enem = pd.concat(df_enem_ano)

# Calculando a média das notas e agrupando por ano e município
df_enem_mun = calcular_media_por_municipio(df_enem)

# Pivoteando por ano para quantidade de candidatos por município da prova
df_enem_qtd = pivotear_ano_qtd_candidatos(df_enem_mun)

# Pivoteando por ano para média das notas por município da provadf_enem_qtd = pd.pivot_table(df_enem_mun, values='QTD_CANDIDATOS', columns=['ANO'], index=['COD_MUN_PROVA']).rename_axis(None, axis=1)
df_enem_nota = pivotear_ano_media_notas(df_enem_mun)

# Fazendo o merge das duas tabelas pivoteadas para obter qtd de candidatos e média das notas
# por município de realização das provas (df_enem_qtd e df_enem_nota)
df_enem_qtd_notas = df_enem_qtd.merge(df_enem_nota, on='COD_MUN',how='left',suffixes=(None, '_y'))[['COD_MUN',\
                                        'QT_CAND_2018','QT_CAND_2019','QT_CAND_2020',\
                                        'MEDIA_NOTAS_2018','MEDIA_NOTAS_2019','MEDIA_NOTAS_2020']]


# Lendo dados sobre região geográfica e estimativa populacional dos municípios (2018, 2019 e 2020)
path_ibge_rgi = 'C://DadosTCC/Saida/regiao_geografica_municipios.xlsx'
df_rgi = pd.read_excel(path_ibge_rgi, dtype={'COD_MUN':str,'COD_RGI':str})

path_ibge_pop = 'C://DadosTCC/Saida/estimativa_pop_municipios.xlsx'
df_pop = pd.read_excel(path_ibge_pop, dtype={'COD_MUN':str})


# Fazendo merge para calcular proporção de candidatos pela população e média (para cada RGI)
# Obs: nesse caso não faz sentido calcular por município, pois as provas não são realizadas em todos os municípios
df_enem_mun_qtd_notas, df_pop_rgi = calcular_media_por_rgi(df_pop, df_rgi, df_enem_qtd_notas)

# Agrupamento pra calcular proporção de candidatos em relação à população e a média das notas do RGI
# (ponderada pela qtd de candidatos em cada município foi aplicada prova)
df_enem_mun_rgi = calcular_proporcao_candidatos(df_enem_mun_qtd_notas)

df_enem_mun_rgi_saida =df_pop_rgi.merge(df_enem_mun_rgi,on='COD_RGI',how='left',suffixes=(None, '_y'))[['COD_MUN','UF','MUNICIPIO','COD_RGI',\
                                                        'PROP_CAND_RGI_2018','PROP_CAND_RGI_2019','PROP_CAND_RGI_2020',\
                                                        'MEDIA_NOTAS_RGI_2018','MEDIA_NOTAS_RGI_2019','MEDIA_NOTAS_RGI_2020']]
df_enem_mun_rgi_saida.fillna(0,inplace=True)

# Exportando os dados da pasta local
path_output = ''
df_enem_mun_rgi_saida.to_excel(path_output, index=False)