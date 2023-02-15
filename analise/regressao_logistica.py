#%%
from selecao_variaveis import dividir_banco_tx_ocupacao, dividir_banco_tx_conclusao
from diagnostico import calcular_diagnostico_classificacao, calcular_importancia_variaveis
from sklearn.linear_model import LogisticRegression

# TAXA DE OCUPAÇÃO

X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", classificacao=True, logistic=True)

modelo = LogisticRegression(multi_class='multinomial', solver='newton-cg')
# Coordinate Descent (CD) algorithm that solves optimization problems by successively performing approximate minimization

modelo.fit(X_train, y_train)

predictions = modelo.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(modelo, X_train, y_train, top_n=13)


# TAXA DE CONCLUSÃO

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", classificacao=True, logistic=True)

modelo = LogisticRegression(multi_class='multinomial', solver='newton-cg')
# Coordinate Descent (CD) algorithm that solves optimization problems by successively performing approximate minimization

modelo.fit(X_train, y_train)

predictions = modelo.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(modelo, X_train, y_train, top_n=13)
# %%