import xgboost as xgboost
from selecao_variaveis import dividir_banco_tx_ocupacao, dividir_banco_tx_conclusao
from diagnostico import calcular_diagnosticos_regressao, calcular_diagnostico_classificacao, calcular_importancia_variaveis
from sklearn.model_selection import GridSearchCV

# TAXA DE OCUPAÇÃO - REG

X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv")
modelo = xgboost.XGBRegressor(eval_metric='rmse')
regressor = xgboost.XGBRegressor(learning_rate = 0.6,
                           n_estimators  = 20,
                           max_depth     = 9)

regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)

calcular_diagnosticos_regressao(y_test, predictions)
calcular_importancia_variaveis(regressor, X_train, y_train)

# TAXA DE OCUPAÇÃO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_ocupacao("ES_cursos_presenciais_2021.csv", classificacao=True)

classifier = xgboost.XGBClassifier(learning_rate = 0.5,
                           n_estimators  = 5,
                           max_depth     = 9)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(classifier, X_train, y_train)

# TAXA DE CONCLUSÃO DE CURSO - REGRESSÃO

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv")

modelo = xgboost.XGBRegressor(eval_metric='rmse')

regressor = xgboost.XGBRegressor(learning_rate = 0.3,
                           n_estimators  = 100,
                           max_depth     = 3)

regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)

calcular_diagnosticos_regressao(y_test, predictions)
calcular_importancia_variaveis(regressor, X_train, y_train)


# TAXA DE CONCLUSÃO DE CURSO - CLASSIFICAÇÃO

# 0 - ruim
# 1 - razoavel
# 2 - bom

X_train, X_test, y_train, y_test = dividir_banco_tx_conclusao("ES_cursos_presenciais_2021.csv", classificacao=True)

classifier = xgboost.XGBClassifier(learning_rate = 0.5,
                           n_estimators  = 50,
                           max_depth     = 20)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

calcular_diagnostico_classificacao(y_test, predictions)
calcular_importancia_variaveis(classifier, X_train, y_train)

