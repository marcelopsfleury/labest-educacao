## 1.7) Dados do Enad - CPC - notas por curso

#### Fonte dos dados: INEP - ENADE CPC 2015, 2016, 2017, 2018 e 2019 (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior) - <acesso em: 1/8/2022>

##### Obs: A frequência de avaliação do ENADE é a cada três anos (por isso, para abranger todos os cursos, utilizou-se 
##### as cinco últimas avaliações disponíveis, considerando a última avaliação válida do curso.
##### Serão considerados nesse trabalho cursos que possuam avaliação (válida) quanto ao CPC-ENADE (97%)

##### Obs2: Para correspondência do CPC-Contínuo com CPC-Faixa, observou-se o disposto na NOTA TÉCNICA Nº 58/2020/CGCQES/DAES/INEP - Tabela1- pg.11 (https://download.inep.gov.br/educacao_superior/enade/notas_tecnicas/2019/NOTA_TECNICA_N_58-2020_CGCQES-DAES_Metodologia_de_calculo_do_CPC_2019.pdf)

###### Obs3: Tabela de correspondência de cursos (CINE e MEC): https://download.inep.gov.br/pesquisas_estatisticas_indicadores_educacionais/cinebrasil/documentos/Tabela_de_correspondencia_entre_as_denominacoes_dos_cursos_e_as_sugestoes_de_rotulos_16092021.pdf

import pandas as pd
import numpy as np
from tratamento import selecionar_colunas_enade_2019, selecionar_colunas_enade_2018, selecionar_colunas_enade_2015, selecionar_colunas_enade_2016, selecionar_colunas_enade_2017, criar_dataframe_de_saida_enade, aplicar_enade_grau_academico, calcular_media_enade, calcular_media_ponderada_enade,ler_enade_arquivo_1_31_32, tratar_tabelas_enade

# Lendo dados do Enade (anos de 2015, 2016, 2017, 2018, 2019, 2021) - considera-se a mais recente avaliação do curso no período

df_enade_ano_2015 = selecionar_colunas_enade_2015("./extracao/dados_zip/cpc_2015_portal_atualizado_03_10_2017.xls")
df_enade_ano_2016 = selecionar_colunas_enade_2016("./extracao/dados_zip/Resultado_CPC_2016_portal_23_02_2018.xls")
df_enade_ano_2017 = selecionar_colunas_enade_2017("./extracao/dados_zip/resultado_cpc_2017.xlsx")
df_enade_ano_2018 = selecionar_colunas_enade_2018("./extracao/dados_zip/portal_CPC_edicao2018.xlsx")
df_enade_ano_2019 = selecionar_colunas_enade_2019("./extracao/dados_zip/resultados_cpc_2019.xlsx")

df_enade = pd.concat([df_enade_ano_2015, df_enade_ano_2016, df_enade_ano_2017, df_enade_ano_2018, df_enade_ano_2019])

# Criando dataFrame de saída
df_enade_curso_ultima_avaliacao = criar_dataframe_de_saida_enade(df_enade)

# Trabalhando os dados da Enade para comparar com os dados do Censo Superior
# com os nomes correspondentes na tabela de correspondência de cursos do INEP
df_enade_curso_ultima_avaliacao = aplicar_enade_grau_academico(df_enade_curso_ultima_avaliacao)

# Calculando a média do Enade-CPC por IES e Município
df_enade_ies_mun_med = calcular_media_enade(df_enade_curso_ultima_avaliacao)

# Agrupando e calculando a Mediana Ponderada (Weighted Median) do CPC-Enade por IES e Município
df_enade_ies_mun_md = calcular_media_ponderada_enade(df_enade_curso_ultima_avaliacao)

# Merge para Média e Mediana por IES e Município

df_enade_ies_mun =df_enade_ies_mun_md.merge(df_enade_ies_mun_med,on=['COD_IES','COD_MUN'],how='inner',suffixes=(None, '_y'))\
                                                    [['COD_IES','COD_MUN','TOT_PART_IES_MUN',\
                                                      'MEDIA_IES_MUN_CPC_CONTINUO','MEDIA_IES_MUN_CPC_FAIXA',\
                                                      'MEDIANA_IES_MUN_CPC_CONTINUO','MEDIANA_IES_MUN_CPC_FAIXA']]

# lendo tabela de Regiões Geográficas Imediatas (RGI)
path_ibge_rgi = './dados_saida/regiao_geografica_municipios.csv'
df_rgi = pd.read_csv(path_ibge_rgi, dtype={'COD_MUN':object,'COD_RGI':object})

# Fazendo merge com CPC_Enade por IES e Município
df_enade_rgi = df_enade_ies_mun.merge(df_rgi,on='COD_MUN',how='left',suffixes=(None, '_y'))[['COD_IES','COD_MUN','COD_RGI',\
                                                                'TOT_PART_IES_MUN','MEDIA_IES_MUN_CPC_CONTINUO','MEDIA_IES_MUN_CPC_FAIXA',\
                                                                'MEDIANA_IES_MUN_CPC_CONTINUO','MEDIANA_IES_MUN_CPC_FAIXA']]

df_enade_rgi.groupby(['COD_IES','COD_RGI'], as_index=False)['TOT_PART_IES_MUN'].sum()

# Exportando os dados da pasta local
path_output = './dados_saida/enade_cpc_cursos.xlsx'
df_enade_curso_ultima_avaliacao.to_excel(path_output, index=False)


# Recuperando dados dos participantes do Enade (2015 a 2019)

lista_path_enade_aluno = ['./extracao/dados_zip/microdados2015_arq1.txt',
                          './extracao/dados_zip/microdados2016_arq1.txt',
                          './extracao/dados_zip/microdados2017_arq1.txt',
                          './extracao/dados_zip/microdados2018_arq1.txt',
                          './extracao/dados_zip/microdados2019_arq1.txt']

lista_path_enade_qi25 = ['./extracao/dados_zip/microdados2015_arq31.txt',
                         './extracao/dados_zip/microdados2016_arq31.txt',
                         './extracao/dados_zip/microdados2017_arq31.txt',
                         './extracao/dados_zip/microdados2018_arq31.txt',
                         './extracao/dados_zip/microdados2019_arq31.txt']

lista_path_enade_qi26 = ['./extracao/dados_zip/microdados2015_arq32.txt',
                         './extracao/dados_zip/microdados2016_arq32.txt',
                         './extracao/dados_zip/microdados2017_arq32.txt',
                         './extracao/dados_zip/microdados2018_arq32.txt',
                         './extracao/dados_zip/microdados2019_arq32.txt']

lista_df_enade_esc_quali_ies = []

for path_enade_aluno, path_enade_qi25, path_enade_qi26 in zip(lista_path_enade_aluno, lista_path_enade_qi25, lista_path_enade_qi26):
       df_enade_qi25, df_enade_qi26 = ler_enade_arquivo_1_31_32(path_enade_qi25, path_enade_qi26)
       lista_df_enade_esc_quali_ies.append(tratar_tabelas_enade(path_enade_aluno, df_enade_qi25, df_enade_qi26))

df_enade_esc_quali_ies = pd.concat(lista_df_enade_esc_quali_ies)

df_enade_curso_ult_aval_quali_ies = df_enade_curso_ultima_avaliacao.merge(df_enade_esc_quali_ies,on=['COD_MUN','COD_CURSO','COD_IES'],how='left')[['COD_MUN','COD_CURSO','CURSO','COD_IES','GRAU_ACADEMICO','COD_AREA','AREA','NUM_PART','CPC_CONTINUO',
       'CPC_FAIXA','ANO_AVALIACAO','QT_AVALIAÇÕES','TX_ESC_QUALI_IES']]
#df_enade_curso_ult_aval_quali_ies['TX_ESC_QUALI_IES'].fillna(0.5,inplace=True)

# Pegar somente os valores mais atualizados segundo ano
df_enade_curso_ult_aval_quali_ies.dropna(subset=['TX_ESC_QUALI_IES']).sort_values('ANO_AVALIACAO').drop_duplicates(subset=['COD_MUN','COD_IES','COD_CURSO'])

# Exportando os dados da pasta local
path_output = './dados_saida/enade_cpc_cursos_quali_ies.csv'
df_enade_curso_ult_aval_quali_ies.to_csv(path_output, index=False, sep=',')