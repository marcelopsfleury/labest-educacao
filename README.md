
# Projeto Educação Superior - Labest
Análise dos fatores determinantes da taxa de ocupação e conclusão no ensino superior no Brasil.

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