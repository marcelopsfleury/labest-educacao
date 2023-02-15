## 1.1) Dados de Estimativa Populacional por município para os anos de 2018, 2019 e 2020

from extracao import extrair_estimativa_pop_por_municipio
from tratamento import transformar_resposta, tratamento_colunas

# Dados de Estimativa Populacional por município para os anos de 2018, 2019 e 2020

resposta_api = extrair_estimativa_pop_por_municipio()

df_mun_uf = transformar_resposta(resposta_api)
df_mun_uf = tratamento_colunas(df_mun_uf)

# Exportando os dados da pasta local
path_output = './dados_saida/estimativa_pop_municipios.csv'
df_mun_uf.to_csv(path_output, index=False, sep=',')