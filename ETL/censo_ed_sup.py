## 1.8) Dados do Censo Educação Superior - INEP (2019, 2020 e 2021)

#### Fonte dos dados: INEP - Censo Superior 2019, 2020 e 2021 (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior) - <acesso em: 3/6/2022>

from tratamento import selecionar_colunas_censo_sup_2019, selecionar_colunas_censo_sup_2020, selecionar_colunas_censo_sup_2021, aplicar_filtros_censo_sup, formatando_grau_academico, match_tabela_correspondencia, recuperar_info_enade_cpc, remover_duplicatas
import pandas as pd

# Lendo dados da Educação Superior (anos de 2019, 2020 e 2021)
path_censo_es_inep_2019 = './extracao/dados_zip/MICRODADOS_CADASTRO_CURSOS_2019.CSV'
path_censo_es_inep_2020 = './extracao/dados_zip/MICRODADOS_CADASTRO_CURSOS_2020.CSV'
path_censo_es_inep_2021 = './extracao/dados_zip/MICRODADOS_CADASTRO_CURSOS_2021.CSV'

df_censo_2019 = selecionar_colunas_censo_sup_2021(path_censo_es_inep_2021)
df_censo_2020 = selecionar_colunas_censo_sup_2021(path_censo_es_inep_2021)
df_censo_2021 = selecionar_colunas_censo_sup_2021(path_censo_es_inep_2021)

# Aplicar filtros: cursos com ingressantes, concluintes e matriculas no período
# Neste traballho intersessam cursos ativos e que já tenham concluintes (cursos recentes não são considerados)
# Considera-se tb os curos com num. matrículados maior do que o num de ingressantes (cursos que estão ativos)

# Carregando dados do Enade-CPC
# Utilizando a Tabela de correspondência de cursos (INEP) para obter informações do Enade-CPC dos cursos
path_enade_cpc = './dados_saida/enade_cpc_cursos_quali_ies.csv'
dict={'COD_MUN':str,'COD_CURSO':str, 'COD_IES':str,'COD_AREA':str,'ANO_AVALIACAO':str,'GRAU_ACADEMICO':str}
df_enade_curso_ult_aval = pd.read_csv(path_enade_cpc, dtype=dict)

# Utilizando a Tabela de correspondência de cursos (INEP) para obter informações do Enade-CPC dos cursos
path_tab_corresp = './extracao/dados_zip/tabela_correspondencia_cursos.xlsx'
df_tab_corresp = pd.read_excel(path_tab_corresp)

df_censo_anos = ["2019","2020","2021"]

lista_df_censo_enade_unique = []

for df_censo, ano in zip([df_censo_2019, df_censo_2020, df_censo_2021], df_censo_anos):

    df_censo_filtered = aplicar_filtros_censo_sup(df_censo)

    # Formatando o campo 'GRAU_ACADEMICO' para compatibilizar com codfificação dos dados do Censo Superior
    df_tab_corresp = formatando_grau_academico(df_tab_corresp)

    # Fazendo o match da tabela de correspondência com dados do Censo Superior
    # (mais de uma possibilidade de denominação por curso, o que não representa problema na recuperação de dados do Enade-CPC)
    df_corresp = match_tabela_correspondencia(df_censo_filtered, df_tab_corresp)

    # Recuperando informações do Enade-CPC para utilizá-la como variável do modelo de ML
    df_censo_enade = recuperar_info_enade_cpc(df_corresp, df_enade_curso_ult_aval, ano)

    # Removendo duplicatas(pegando a mais recente/alta avaliação do curso)
    lista_df_censo_enade_unique.append(remover_duplicatas(df_censo_enade, ano))

# Obs: Apenas 1.201 cursos EAD (que constam do censo 2019) tem avaliação Enade-CPC (cerca de 4% de cursos dessa modalidade),
# enquanto que temos mais de 13 mil presenciais que tem avaliação (82% de cursos dessa modalidade)
# 65% dos cursos (considerados no filtro) são EaD e outros 35% são presenciais.

df_censo_enade_unique = lista_df_censo_enade_unique[0].merge(lista_df_censo_enade_unique[1], on=['COD_MUN','COD_IES','CD_CURSO','MODALIDADE','ANO_AVALIACAO'], how='left', suffixes=(None, '_y'))
df_censo_enade_unique = df_censo_enade_unique.merge(lista_df_censo_enade_unique[2], on=['COD_MUN','COD_IES','CD_CURSO','MODALIDADE','ANO_AVALIACAO'], how='left', suffixes=(None, '_y'))

# Gravar saída : Censo Educ Superior (com avaliação Enade-CPC)
# exportando os dados da pasta local
path_output = './dados_saida/censo_sup_enade_cursos.csv'
df_censo_enade_unique.to_csv(path_output, index=False, sep=',')
