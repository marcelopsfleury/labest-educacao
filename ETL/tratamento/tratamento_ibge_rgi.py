import pandas as pd

def selecionar_colunas_ibge_rgi(path_ibge_regioes):
    # Lendo arquivo das regiões geográficas (RGIs - Regiões Geográficas Imediatas e RGInts - Regiões Geográficas Intermediárias) - IBGE - 2017
    # renomeia, seleciona e reordena as colunas de interesse: Cod.Município, Nome Município, Cod. Região Geográfica Imediata e Nome Região Geográfica Imediata
    cols_names = ['MUNICIPIO','COD_MUN','COD_RGI','NOME_RGI','COD_RGINT','NOME_RGINT']
    df_reg_muni = pd.read_excel(path_ibge_regioes, dtype=str, names=cols_names)
    df_reg_muni=df_reg_muni[['COD_MUN','MUNICIPIO','COD_RGI','NOME_RGI']]

    return df_reg_muni


def testar_polo(muni, rgi):
  if muni in rgi:
     return('S')
  else:
     return('N')         

def aplicar_testar_polo(df_reg_muni):
    # Incluir informação se município é Pólo de seu RGI
    # se string 'MUNICIPIO' está contida na string 'NOME_RGI'
    df_reg_muni['POLO'] = df_reg_muni[['MUNICIPIO','NOME_RGI']].apply(lambda x: testar_polo(x['MUNICIPIO'],x['NOME_RGI']), axis=1)
    return df_reg_muni 