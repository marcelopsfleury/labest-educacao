## 1.2) Dados de Regiões Geográficas por município - IBGE - 2017
#### Nessa pesquisa trabalhamos com dados agregados por "Regiões Geográficas Imediatas (RGI)", assim definido pelo IBGE: 
##### "Têm na rede urbana o seu principal elemento de referência. As RGIs são estruturas a partir de centros urbanos próximos para a satisfação das necessidades imediatas das populações, tais como compras de bens de consumo duráveis e não duráveis, busca de trabalho, procura por serviços de saúde e de educaçãoo, e a prestação de serviços públicos, tais como postos de atendimento do INSS, do Ministério do Trabalho e Emprego e do Judiciário, entre outros".
#### Fonte dos dados: IBGE - (https://www.ibge.gov.br/geociencias/organizacao-do-territorio/divisao-regional/15778-divisoes-regionais-do-brasil.html?=&t=downloads) - <acesso em: 21/7/2022>

from tratamento import selecionar_colunas_ibge_rgi, aplicar_testar_polo

path_ibge_regioes = './extracao/dados_zip/regioes_geograficas_composicao_por_municipios_2017_20180911.xlsx'

df_reg_muni = selecionar_colunas_ibge_rgi(path_ibge_regioes)

df_reg_muni = aplicar_testar_polo(df_reg_muni)

# Exportando os dados da pasta local
path_output = './dados_saida/regiao_geografica_municipios.xlsx'
df_reg_muni.to_excel(path_output, index=False)

