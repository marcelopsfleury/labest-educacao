## 1.7) Dados do Enad - CPC - notas por curso

#### Fonte dos dados: INEP - ENADE CPC 2015, 2016, 2017, 2018 e 2019 (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior) - <acesso em: 1/8/2022>

##### Obs: A frequência de avaliação do ENADE é a cada três anos (por isso, para abranger todos os cursos, utilizou-se 
##### as cinco últimas avaliações disponíveis, considerando a última avaliação válida do curso.
##### Serão considerados nesse trabalho cursos que possuam avaliação (válida) quanto ao CPC-ENADE (97%)

##### Obs2: Para correspondência do CPC-Contínuo com CPC-Faixa, observou-se o disposto na NOTA TÉCNICA Nº 58/2020/CGCQES/DAES/INEP - Tabela1- pg.11 (https://download.inep.gov.br/educacao_superior/enade/notas_tecnicas/2019/NOTA_TECNICA_N_58-2020_CGCQES-DAES_Metodologia_de_calculo_do_CPC_2019.pdf)

###### Obs3: Tabela de correspondência de cursos (CINE e MEC): https://download.inep.gov.br/pesquisas_estatisticas_indicadores_educacionais/cinebrasil/documentos/Tabela_de_correspondencia_entre_as_denominacoes_dos_cursos_e_as_sugestoes_de_rotulos_16092021.pdf

import pandas as pd
import numpy as np
from tratamento import selecionar_colunas_enade_2019, selecionar_colunas_enade_2018, selecionar_colunas_enade_2015, selecionar_colunas_enade_2016, selecionar_colunas_enade_2017, criar_dataframe_de_saida_enade, aplicar_enade_grau_academico, calcular_media_enade, calcular_media_ponderada_enade

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
path_ibge_rgi = './dados_saida/regiao_geografica_municipios.xlsx'
df_rgi = pd.read_excel(path_ibge_rgi, dtype={'COD_MUN':object,'COD_RGI':object})

# Fazendo merge com CPC_Enade por IES e Município
df_enade_rgi = df_enade_ies_mun.merge(df_rgi,on='COD_MUN',how='left',suffixes=(None, '_y'))[['COD_IES','COD_MUN','COD_RGI',\
                                                                'TOT_PART_IES_MUN','MEDIA_IES_MUN_CPC_CONTINUO','MEDIA_IES_MUN_CPC_FAIXA',\
                                                                'MEDIANA_IES_MUN_CPC_CONTINUO','MEDIANA_IES_MUN_CPC_FAIXA']]

df_enade_rgi.groupby(['COD_IES','COD_RGI'], as_index=False)['TOT_PART_IES_MUN'].sum()

# Exportando os dados da pasta local
path_output = './dados_saida/enade_cpc_cursos.xlsx'
df_enade_curso_ultima_avaliacao.to_excel(path_output, index=False)


# Recuperando dados dos participantes do Enade (2019)

# Lendo dados do Enade 2019 (arquivo 1: dados do curso e ies)
dict= {'NU_ANO':str, 'CO_CURSO':str, 'CO_IES':str, 'CO_CATEGAD':str,'CO_ORGACAD':str,\
       'CO_GRUPO':str,'CO_MODALIDADE':np.int64,'CO_MUNIC_CURSO':str,'CPC_FAIXA':str}

path_enade_aluno = './extracao/dados_zip/microdados2019_arq1.txt'
df_enade_aluno = pd.read_csv(path_enade_aluno,  dtype=dict, usecols=[0,1,2,3,4,6,7],sep=';')

# Lendo dados do Enade 2019 (arquivo 31 e 32 - questões 25 e 26: questionário sobre motivo de opção pelo curso e ies)
path_enade_qi25 = './extracao/dados_zip/microdados2019_arq31.txt'
df_enade_qi25 = pd.read_csv(path_enade_qi25,  dtype=str, sep=';')
df_enade_qi25.dropna(subset = ['QE_I25'],inplace=True)
df_enade_qi25.reset_index(inplace=True, drop=True)

# Lendo dados do Enade 2019 (arquivo 31 e 32: questionário sobre motivo de opção pelo curso e ies)
path_enade_qi26 = './extracao/dados_zip/microdados2019_arq32.txt'
df_enade_qi26 = pd.read_csv(path_enade_qi26,  dtype=str, sep=';')
df_enade_qi26.dropna(subset = ['QE_I26'],inplace=True)
df_enade_qi26.reset_index(inplace=True, drop=True)

# Agrupando as tabelas com resposta às QE I26  (escolha da IES)
# Motivações agrupadas por: Opção por qualidade (interesses/vocação) ou por facilidade (oportunidade, conveniência)
df_enade_qi25['ESCOLHA_QUALI']=[1 if x in ('ABCDE') else 0 for x in df_enade_qi25['QE_I25'] ]
df_enade_qi26['ESCOLHA_QUALI']=[1 if x in ('F') else 0 for x in df_enade_qi26['QE_I26'] ]

df_enade_esc_quali = df_enade_qi26.groupby(['CO_CURSO']).agg({'QE_I26': 'count','ESCOLHA_QUALI':'sum'}).reset_index()
df_enade_esc_quali['TX_ESC_QUALI_IES']=round(df_enade_esc_quali['ESCOLHA_QUALI']/df_enade_esc_quali['QE_I26'],2)

# Recuperando dados da IES
df_curso_ies = df_enade_aluno.groupby(['CO_CURSO','CO_IES','CO_MUNIC_CURSO','CO_MODALIDADE'], as_index=False).agg({'NU_ANO':'count'}).rename(columns={'NU_ANO':'QTD'})
df_enade_esc_quali_ies = df_enade_esc_quali.merge(df_curso_ies,on='CO_CURSO',how='left')[['CO_CURSO','CO_MODALIDADE','CO_IES','CO_MUNIC_CURSO','TX_ESC_QUALI_IES']]
df_enade_esc_quali_ies.rename(columns={'CO_CURSO':'COD_CURSO','CO_IES':'COD_IES','CO_MUNIC_CURSO':'COD_MUN'},inplace=True)

df_enade_curso_ult_aval_quali_ies = df_enade_curso_ultima_avaliacao.merge(df_enade_esc_quali_ies,on=['COD_MUN','COD_CURSO','COD_IES'],how='left')\
    [['COD_MUN','COD_CURSO','CURSO','COD_IES','GRAU_ACADEMICO','COD_AREA','AREA','NUM_PART','CPC_CONTINUO',\
     'CPC_FAIXA','ANO_AVALIACAO','QT_AVALIAÇÕES','TX_ESC_QUALI_IES']]
df_enade_curso_ult_aval_quali_ies['TX_ESC_QUALI_IES'].fillna(0.5,inplace=True)

# Exportando os dados da pasta local
path_output = './dados_saida/enade_cpc_cursos_quali_ies.xlsx'
df_enade_curso_ult_aval_quali_ies.to_excel(path_output, index=False)