#%%
## 1.3) Dados do Censo - Rendimento mensal (per capta) agrupado por Município/RGI

#### Fonte dos dados: IBGE - Censo 2010 (https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-2020-censo4.html?=&t=downloads) - <acesso em: 21/7/2022> indicadores sociais municipais Brasil.zip

##### Obs: O censo de 2010 contava com 5565 municípios

import pandas as pd
from tratamento import selecionar_colunas_censo_rend_mensal, selecionar_colunas_censo_pop, merge_pop_renda, merge_rendimento_pop_rgi, aplicar_my_agg, merge_rgi_renda_media, calcular_media_ponderada_por_rgi, merge_renda_media_ponderada

path_censo_2010_renda = './extracao/dados_zip/tab8.xls'
path_censo_2010_pop = './extracao/dados_zip/tab1.xls'

# Lendo dados do Censo 2010 - Rendimento mensal per capta (Tabela 8)
# Deleta os subtotais da tabela importada
df_censo_2010_renda = selecionar_colunas_censo_rend_mensal(path_censo_2010_renda)

# Lendo dados do Censo 2010 - População (Tabela 1)
# Deleta os subtotais da tabela importada
df_censo_2010_pop = selecionar_colunas_censo_pop(path_censo_2010_pop)

df_censo_2010_pop_renda = merge_pop_renda(df_censo_2010_renda, df_censo_2010_pop)

# Lendo dados de população por RGI
path_ibge_rgi_muni = './dados_saida/regiao_geografica_municipios.xlsx'
df_reg_muni = pd.read_excel(path_ibge_rgi_muni)

# Fazendo o merge das informações de redimento (per capta) e população dos municípios por RGI
df_rgi_merged = merge_rendimento_pop_rgi(df_reg_muni, df_censo_2010_pop_renda)

# Agrupando e calculando o Rendimento Médio Mensal (per capta) por RGI
df_rgi_rend_medio = aplicar_my_agg(df_rgi_merged)

df_rgi_rend_mean_md = merge_rgi_renda_media(df_reg_muni, df_rgi_rend_medio)

# Agrupando e calculando a Mediana Ponderada (Weighted Median) dos rendimentos mensais (per capta) por RGI

### Código exemplificativo
###
### wages = [598, 650, 660, 680, 712, 830]
### pop = [230000,300000,120000,1500000,600000,330000]
### d = {'Wages':wages,'Populacao':pop}
### df = pd.DataFrame(d)
### df['CumSum'] = df['Populacao'].cumsum()
### cutoff = df['Populacao'].sum() / 2.0
### median = df[df['CumSum'] > cutoff].iloc[0,0]
###

df_rgi_rend_w_md = calcular_media_ponderada_por_rgi(df_rgi_merged)

df_rgi_rend_mean_md = merge_renda_media_ponderada(df_rgi_rend_mean_md, df_rgi_rend_w_md)

# Exportando os dados da pasta local
path_output = './dados_saida/rgi_rendimento_mensal_med_md_pond.xlsx'
df_rgi_rend_mean_md.to_excel(path_output, index=False)
# %%
