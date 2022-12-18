import pandas as pd
import re

def transformar_resposta(resposta):
    # Transformando a resposta da request em dataframe
    lista_de_linhas_df = resposta.json()[0]['resultados'][0]['series']
    return pd.json_normalize(lista_de_linhas_df)

def tratamento_colunas(df_mun_uf):
    df = df_mun_uf.rename(columns={
        'localidade.id': 'COD_MUN', 
        'localidade.nome': 'MUNICIPIO',
        'serie.2018': 'POPULACAO_2018',
        'serie.2019': 'POPULACAO_2019',
        'serie.2020': 'POPULACAO_2020'})

    df['UF'] = df['MUNICIPIO'].transform(lambda x: re.sub(r'.+ - ','', x))

    df['MUNICIPIO'] = df['MUNICIPIO'].transform(lambda x: re.sub(r'(.+)-.+','\\1', x))

    return df
