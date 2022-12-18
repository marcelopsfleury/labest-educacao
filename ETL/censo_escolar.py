from .tratamento import selecionar_colunas_censo_escolar, selecionar_escolas_em_atividade, total_matriculas_por_mun_ano, linhas_para_colunas, percentual_matricula_por_municipio, percentual_matricula_por_rgi, merge_matriculas_mun_rgi
import pandas as pd

# Lendo dados do Enem (anos de 2018, 2019, 2020 e 2021)
path_inep_censo = []
df_censo_basica_ano = []

for path in path_inep_censo:
    df_censo_basica_ano.append(selecionar_colunas_censo_escolar(path))

df_censo_basica = pd.concat(df_censo_basica_ano)

df_censo_basica = selecionar_escolas_em_atividade(df_censo_basica)

path_output = ''
df_censo_basica.to_excel(path_output, index=False)

df_censo_basica_mun = total_matriculas_por_mun_ano(df_censo_basica)

df_censo_basica_mat = linhas_para_colunas(df_censo_basica_mun)

# lendo tabela de estimativa populacional dos municípios para os anos de 2018, 2019, 2020 e 2021
path_ibge_pop = ''
df_estimativa_pop = pd.read_excel(path_ibge_pop, dtype={'COD_MUN':object})

# Calculando percentual de matrícula (ensino médio) em relação à população do município
# para os anos de 2018, 2019, 2020 e 2021
df_mat_prop_mun = percentual_matricula_por_municipio(df_estimativa_pop, df_censo_basica_mat)

# lendo tabela de Regiões Geográficas Imediatas (RGI)
path_ibge_rgi = ''
df_rgi = pd.read_excel(path_ibge_rgi, dtype={'COD_MUN':object,'COD_RGI':object})

df_prop_mat_rgi, df_prop_mat_merged = percentual_matricula_por_rgi(df_mat_prop_mun, df_rgi)

df_mat_mun_rgi = merge_matriculas_mun_rgi(df_prop_mat_merged, df_prop_mat_rgi)

# Exportando os dados da pasta local
path_output = ''
df_mat_mun_rgi.to_excel(path_output, index=False)