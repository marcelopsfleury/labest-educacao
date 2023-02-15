## 1.9) Cursos Presenciais (com avaliação Enade-CPC)

## Agregar informação de Renda, População, Ensino Médio (matrículas e Ideb), Enem (num candidatos e média das notas)

#### Baseada nas informações geradas anteriormente

from tratamento import selecionar_colunas_censo_sup_enade, agregar_prop_rendimento, agregar_pop_rgi_mun, agregar_matricula_ensino_medio, agregar_ideb_por_rgi, agregar_enem_por_rgi, agregar_duracao_minima_cursos, definir_targets

# Carregar aquivo com informações do Censo de Educação superior (acrescida da avaliação do Enade-CPC)
# Ano = 2019 (ano do censo superior) - cursos presenciais
path_censo_enade = './dados_saida/censo_sup_enade_cursos.csv'
df_censo_sup_enade = selecionar_colunas_censo_sup_enade(path_censo_enade)

# Rendimento per capita (censo 2010)
path_ibge_rend = './dados_saida/rgi_rendimento_mensal_med_md_pond.csv'
df_educ_superior = agregar_prop_rendimento(path_ibge_rend, df_censo_sup_enade)

# População (estimativa) por município e rgi
path_ibge_pop = './dados_saida/estimativa_pop_municipios.csv'
path_ibge_rgi = './dados_saida/regiao_geografica_municipios.csv'
df_educ_superior = agregar_pop_rgi_mun(path_ibge_pop, path_ibge_rgi, df_educ_superior)

# Matrículas no Ensino Médio (proporcionalmente à população) por RGI
path_inep_mat_ens_med = './dados_saida/perc_mat_ensino_medio.csv'
df_educ_superior = agregar_matricula_ensino_medio(path_inep_mat_ens_med, df_educ_superior)

# Ideb no Ensino Médio por RGI
path_inep_ideb= './dados_saida/ideb_ensino_medio_mun_rgi.csv'
df_educ_superior = agregar_ideb_por_rgi(path_inep_ideb, df_educ_superior)

# Enem (Propporção de candidatos e média das notas) por RGI
path_inep_enem = './dados_saida/enem_cand_notas_mun_rgi.csv'
df_educ_superior = agregar_enem_por_rgi(path_inep_enem, df_educ_superior)

# Dados sobre duração (mínima) dos cursos obtidos por meio de consulta às resoluções do MEC
path_dur_cursos = './extracao/dados_zip/cursos_duracao.xlsx'
df_educ_superior = agregar_duracao_minima_cursos(path_dur_cursos, df_educ_superior)

df_educ_superior = definir_targets(df_educ_superior)

# Gravar saída : Dados da Educação Superior em 2019 para utilizar no Modelo de ML
# exportando os dados da pasta local
# reordenando as colunas para gravar resultado
# output_cols=['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','DUR_CURSO','GRAU_ACADEMICO','TP_REDE','POLO',
#              'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC',
#              'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',
#              'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',
#              'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI','POPULACAO_2019_RGI',
#              'FAIXA_POPULACAO_RGI',
#              'PERC_MAT_RGI_2019','IDEB_RGI','PERC_CAND_ENEM_RGI_2019','MEDIA_CAND_ENEM_RGI_2019',
#              'TARGET_TX_OCUP_INI','TARGET_TX_CONC_VAGAS','TARGET_TX_CONC_ING','TARGET_TX_OCUP']

path_output = './dados_saida/ES_cursos_presenciais.csv'
df_educ_superior.to_csv(path_output, index=False, sep=',')
# df_educ_superior[output_cols].to_excel(path_output, index=False)

#%%

import pandas as pd

df_colunas = pd.read_csv('./dados_saida/ES_cursos_presenciais.csv', delimiter=',')
df_linhas = pd.read_csv('./dados_saida/ES_cursos_presenciais_2021.csv', delimiter=',', encoding="Latin-1")
# %%
