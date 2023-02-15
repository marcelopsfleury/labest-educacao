#%%
from selecao_variaveis import dividir_banco_tx_ocupacao, dividir_banco_tx_conclusao
from diagnostico import calcular_diagnosticos_regressao, calcular_diagnostico_classificacao, calcular_importancia_variaveis
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", random_forest=True)
regressor = RandomForestRegressor(n_estimators  = 100, max_depth = 100)

regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)

calcular_diagnosticos_regressao(y_test, predictions)
calcular_importancia_variaveis(regressor, X_train, y_train)

# TAXA DE OCUPAÇÃO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", classificacao=True, random_forest=True)
classifier = RandomForestClassifier(n_estimators  = 100, max_depth = 100)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(classifier, X_train, y_train)

# TAXA DE CONCLUSÃO DE CURSO - REGRESSÃO

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", random_forest=True)
regressor = RandomForestRegressor(n_estimators  = 100, max_depth = 100)

regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)

calcular_diagnosticos_regressao(y_test, predictions)
calcular_importancia_variaveis(regressor, X_train, y_train)


# TAXA DE CONCLUSÃO DE CURSO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", classificacao=True, random_forest=True)
classifier = RandomForestClassifier(n_estimators  = 100, max_depth = 100)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(classifier, X_train, y_train)

# %%
