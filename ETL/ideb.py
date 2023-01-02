## 1.5) Dados do Ideb - Ensino Médio (por município/RGI)

#### Fonte dos dados: INEP - Ideb Ensino Médio de 2019 (https://download.inep.gov.br/educacao_basica/portal_ideb/planilhas_para_download/2019/divulgacao_ensino_medio_municipios_2019.zip) - <acesso em: 27/7/2022>

##### Ideb ponderado segundo proporção de matrículas no Ensino Médio do município entre escolas públicas e privadas

from tratamento import matriculas_por_tipo_escola_municipio, calcular_prop_rede_escolar, selecionar_colunas_ideb, aplicar_ajusta_ideb_na, calcular_ideb, ideb_por_rgi, aplicar_ajusta_ideb_rgi_na, aplicar_my_agg_ideb
import pandas as pd

path_df_censo_basica = './dados_saida/df_censo_basica.csv'

df_censo_basica = pd.read_csv(path_df_censo_basica)

# Total de matrículas no ensino médio por município e tipo de escola (pública/privada) para o ano de ...
df_mat_med_rede = matriculas_por_tipo_escola_municipio(df_censo_basica)

# Calculando a proporção da rede escolar (pública e privada) de Ensino Médio
df_mat_prop_med_rede = calcular_prop_rede_escolar(df_mat_med_rede)

# Lendo dados do Ideb por município (ano de 2019)
path_ideb_med = './extracao/dados_zip/divulgacao_ensino_medio_municipios_2019.xlsx'
df_ideb_med_rede = selecionar_colunas_ideb(path_ideb_med)

# Ajuste para valores faltantes de IDEB (para evitar distorções)
df_ideb_med_rede = aplicar_ajusta_ideb_na(df_ideb_med_rede)

# Calcular a IDEB proporcional à quantidade de matrículas para redes públicas e privadas
df_ideb_prop = calcular_ideb(df_ideb_med_rede, df_mat_prop_med_rede)

# Lendo tabela de Regiões Geográficas Imediatas (RGI)
path_ibge_rgi = './dados_saida/regiao_geografica_municipios.xlsx'
df_rgi = pd.read_excel(path_ibge_rgi, dtype={'COD_MUN':object,'COD_RGI':object})

# IDEB por RGI (proporcional à qtd Matrícula) - merge das tabelas
df_ideb_prop_merged = ideb_por_rgi(df_ideb_prop, df_rgi)

# Ajustes para municípios sem oferta de ensino médio (valores NaN)
df_ideb_prop_merged = aplicar_ajusta_ideb_rgi_na(df_ideb_prop_merged)

# IDEB por RGI (proporcional à qtd Matrícula) - cálculo propriamente dito
df_ideb_rgi = aplicar_my_agg_ideb(df_ideb_prop_merged)

# IDEB Por Município e RGI
df_ideb_mun_rgi  = df_ideb_prop_merged.merge(df_ideb_rgi, on='COD_RGI',how='left',suffixes=(None, '_y'))[['COD_MUN','MUNICIPIO','COD_RGI','QTD_MAT_MUN',\
                                        'PROP_PUBLICA','IDEB_ESCOLA_PUBLICA','IDEB_ESCOLA_PRIVADA','IDEB_MUN','IDEB_RGI']]

# Exportando os dados da pasta local
path_output = './dados_saida/ideb_ensino_medio_mun_rgi.xlsx'
df_ideb_mun_rgi.to_excel(path_output, index=False)