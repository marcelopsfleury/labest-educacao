
# Projeto Educação Superior - Labest
Análise dos fatores determinantes da taxa de ocupação e conclusão no ensino superior no Brasil.

## PARTE 1: ETL (Extração-Carga-Tratamento dos dados)

### Fonte de dados (na ordem em que foram tratados):

### 1.1) Estimativa Populacional por muncípio (2018, 2019 e 2020) - Fonte: IBGE
### 1.2) Dados de Regiões Geográficas por município - Fonte: IBGE - 2017
##### Nessa pesquisa trabalhamos com dados agregados por "Regiões Geográficas Imediatas (RGI)", assim definidas pelo IBGE: 
##### "Têm na rede urbana o seu principal elemento de referência. As RGIs são estruturas a partir de centros urbanos próximos para a satisfação das necessidades imediatas das populações, tais como compras de bens de consumo duráveis e não duráveis, busca de trabalho, procura por serviços de saúde e de educaçãoo, e a prestação de serviços públicos, tais como postos de atendimento do INSS, do Ministério do Trabalho e Emprego e do Judiciário, entre outros".

### 1.3) Dados do Censo - Rendimento mensal (per capta) - Fonte: IBGE (Censo 2010)
### 1.4) Dados do Censo Escolar - Percentual de Matrículas no Ensino Médio (2018, 2019, 2020) - Fonte: INEP
### 1.5) Dados do Ideb - Ensino Médio (2019) - Fonte: INEP
### 1.6) Dados do Enem - notas e num. candidatos (2018, 2019, 2020) - Fonte: INEP
### 1.7) Dados do Enade - CPC (2015 a 2019) - Fonte: INEP
### 1.8) Dados do Censo Educação Superior - INEP (2018, 2019 e 2020)


### Saídas:
### 1.9) Cursos Presenciais (com avaliação Enade-CPC)
###        Agregado com informação de Renda, População, Ensino Médio (matrículas e Ideb),
###        Enem (num candidatos e média das notas).



##### Obs: os arquivos foram baixados dos links indicados e carregados a partir da pasta local (formatos .cvs e .xlsx) por questões práticas. 

## Execução do projeto

Ao clonar o repositório, execute `python3 -m pip install --user virtualenv` se for usuário de linux ou `py -m pip install --user virtualenv` se for usuário de windows para a instalação do ambiente virtual. É necessário possuir Python 3.8+ para este projeto.

Antes de começar a instalar ou usar pacotes em seu ambiente virtual, você precisará ativá-lo. Execute `source env/bin/activate` se for usuário de linux ou `.\env\Scripts\activate` se for usuário de windows.

#### Comandos

## Banco de dados

### IBGE

Para criar a query das requests acessar `https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-bq`
## Análises


### Estrutura de pastas

| Pastas                 | Descrição                                            |
|:-----------------------|:-----------------------------------------------------|
|📦 PROJETO              | Raiz do projeto                                      |
| ┣ 📂 .vscode           | Arquivos de configuração do vscode                   |
| ┣ 📂 env               | Arquivos de configuração do ambiente virtual         |
| ┣ 📂 ETL               | Diretório base dos scripts do ETL                    |
|   ┣ 📂 ...             | Scripts de extração, limpeza e análise dos dados     |