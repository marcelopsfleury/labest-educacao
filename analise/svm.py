#%%
from selecao_variaveis import dividir_banco_tx_ocupacao, dividir_banco_tx_conclusao
from diagnostico import calcular_diagnosticos_regressao, calcular_diagnostico_classificacao, calcular_importancia_variaveis_svm
from sklearn import svm

# TAXA DE OCUPAÇÃO - REG

# X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", random_forest=True)
# modelo = svm.SVR()

# modelo.fit(X_train, y_train)
# predictions = modelo.predict(X_test)

# calcular_diagnosticos_regressao(y_test, predictions)

# TAXA DE OCUPAÇÃO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", classificacao=True, random_forest=True)

modelo = svm.SVC()

modelo.fit(X_train, y_train)
predictions = modelo.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
# calcular_importancia_variaveis_svm(modelo.coef_, X_train.columns)

# TAXA DE CONCLUSÃO DE CURSO - REGRESSÃO

# X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", random_forest=True)

# modelo = svm.SVR()

# modelo.fit(X_train, y_train)
# predictions = modelo.predict(X_test)

# calcular_diagnosticos_regressao(y_test, predictions)

# TAXA DE CONCLUSÃO DE CURSO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", classificacao=True, random_forest=True)

modelo = svm.SVC()

modelo.fit(X_train, y_train)
predictions = modelo.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
# calcular_importancia_variaveis(classifier, X_train, y_train)
# %%
