from tratamento import selecionar_colunas_censo_sup_2018, selecionar_colunas_censo_sup_2019, aplicar_filtros_censo_sup_2019, formatando_grau_academico, match_tabela_correspondencia, recuperar_info_enade_cpc, remover_duplicatas
import pandas as pd

# Lendo dados da Educação Superior (anos de 2018, 2019 e 2020) 
path_censo_es_inep_2018 = ''
path_censo_es_inep_2019 = ''

df_censo_2018 = selecionar_colunas_censo_sup_2018(path_censo_es_inep_2018)
df_censo_2019 = selecionar_colunas_censo_sup_2019(path_censo_es_inep_2019)

# Aplicar filtros: cursos com ingressantes, concluintes e matriculas no período
# Neste traballho intersessam cursos ativos e que já tenham concluintes (cursos recentes não são considerados)
# Considera-se tb os curos com num. matrículados maior do que o num de ingressantes (cursos que estão ativos)
df_censo_filtered = aplicar_filtros_censo_sup_2019(df_censo_2019)

# Utilizando a Tabela de correspondência de cursos (INEP) para obter informações do Enade-CPC dos cursos
path_tab_corresp = ''
df_tab_corresp = pd.read_excel(path_tab_corresp)

# Formatando o campo 'GRAU_ACADEMICO' para compatibilizar com codfificação dos dados do Censo Superior
df_tab_corresp = formatando_grau_academico(df_tab_corresp)

# Fazendo o match da tabela de correspondência com dados do Censo Superior
# (mais de uma possibilidade de denominação por curso, o que não representa problema na recuperação de dados do Enade-CPC)
df_corresp = match_tabela_correspondencia(df_censo_filtered, df_censo_filtered)

# Carregando dados do Enade-CPC
# Utilizando a Tabela de correspondência de cursos (INEP) para obter informações do Enade-CPC dos cursos
path_enade_cpc = ''
dict={'COD_MUN':str,'COD_CURSO':str, 'COD_IES':str,'COD_AREA':str,'ANO_AVALIACAO':str,'GRAU_ACADEMICO':str}
df_enade_curso_ult_aval = pd.read_excel(path_enade_cpc, dtype=dict)

# Recuperando informações do Enade-CPC para utilizá-la como variável do modelo de ML
df_censo_enade = recuperar_info_enade_cpc(df_corresp, df_enade_curso_ult_aval)

# Removendo duplicatas(pegando a mais recente/alta avaliação do curso)
df_censo_enade_unique = remover_duplicatas(df_censo_enade)

# Obs: Apenas 1.201 cursos EAD (que constam do censo 2019) tem avaliação Enade-CPC (cerca de 4% de cursos dessa modalidade),
# enquanto que temos mais de 13 mil presenciais que tem avaliação (82% de cursos dessa modalidade)
# 65% dos cursos (considerados no filtro) são EaD e outros 35% são presenciais.

# Gravar saída : Censo Educ Superior (com avaliação Enade-CPC)
# exportando os dados da pasta local
path_output = ''
df_censo_enade_unique.to_excel(path_output, index=False)
