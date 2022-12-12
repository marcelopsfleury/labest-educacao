from .extracao import extrair_estimativa_pop_por_municipio
from .tratamento import transformar_resposta, tratamento_colunas

# Dados de Estimativa Populacional por município para os anos de 2018, 2019 e 2020

resposta_api = extrair_estimativa_pop_por_municipio()

df_mun_uf = transformar_resposta(resposta_api)
df_mun_uf = tratamento_colunas(df_mun_uf)

# Exportando os dados da pasta local
path_output = ''
df_mun_uf.to_excel(path_output, index=False)

# Dados de Regiões Geográficas por município - IBGE - 2017
