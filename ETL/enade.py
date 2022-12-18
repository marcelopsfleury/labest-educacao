
import pandas as pd
from tratamento import selecionar_colunas_enade, criar_dataframe_de_saida_enade, aplicar_enade_grau_academico, calcular_media_enade, calcular_media_ponderada_enade

# Lendo dados do Enade (anos de 2015, 2016, 2017, 2018, 2019, 2021) - considera-se a mais recente avaliação do curso no período

path_enade_inep = []
df_enade_ano = []

for path in path_enade_inep:
    df_enade_ano.append(selecionar_colunas_enade(path))

df_enade = pd.concat(df_enade_ano)

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
path_ibge_rgi = ''
df_rgi = pd.read_excel(path_ibge_rgi, dtype={'COD_MUN':object,'COD_RGI':object})

# Fazendo merge com CPC_Enade por IES e Município
df_enade_rgi = df_enade_ies_mun.merge(df_rgi,on='COD_MUN',how='left',suffixes=(None, '_y'))[['COD_IES','COD_MUN','COD_RGI',\
                                                                'TOT_PART_IES_MUN','MEDIA_IES_MUN_CPC_CONTINUO','MEDIA_IES_MUN_CPC_FAIXA',\
                                                                'MEDIANA_IES_MUN_CPC_CONTINUO','MEDIANA_IES_MUN_CPC_FAIXA']]

df_enade_rgi.groupby(['COD_IES','COD_RGI'], as_index=False)['TOT_PART_IES_MUN'].sum()

# Exportando os dados da pasta local
path_output = ''
df_enade_curso_ultima_avaliacao.to_excel(path_output, index=False)


# Recuperando dados dos participantes do Enade (2019)

# Lendo dados do Enade 2019 (arquivo 1: dados do curso e ies)
dict= {'NU_ANO':str, 'CO_CURSO':str, 'CO_IES':str, 'CO_CATEGAD':str,'CO_ORGACAD':str,\
       'CO_GRUPO':str,'CO_MODALIDADE':np.int64,'CO_MUNIC_CURSO':str,'CPC_FAIXA':str}

path_enade_aluno = 'C://DadosTCC/microdados2019_arq1.txt'
df_enade_aluno = pd.read_csv(path_enade_aluno,  dtype=dict, usecols=[0,1,2,3,4,6,7],sep=';')

# Lendo dados do Enade 2019 (arquivo 31 e 32 - questões 25 e 26: questionário sobre motivo de opção pelo curso e ies)
path_enade_qi25 = 'C://DadosTCC/microdados2019_arq31.txt'
df_enade_qi25 = pd.read_csv(path_enade_qi25,  dtype=str, sep=';')
df_enade_qi25.dropna(subset = ['QE_I25'],inplace=True)
df_enade_qi25.reset_index(inplace=True, drop=True)

# Lendo dados do Enade 2019 (arquivo 31 e 32: questionário sobre motivo de opção pelo curso e ies)
path_enade_qi26 = 'C://DadosTCC/microdados2019_arq32.txt'
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
path_output = ''
df_enade_curso_ult_aval_quali_ies.to_excel(path_output, index=False)