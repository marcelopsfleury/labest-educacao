import requests

def extrair_estimativa_pop_por_municipio():
    resposta = requests.get("https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2019|2020|2021/variaveis/9324?localidades=N6[all]")
    return resposta