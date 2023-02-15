#%%
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from selecao_variaveis import dividir_banco_tx_ocupacao, dividir_banco_tx_conclusao
from diagnostico import calcular_diagnosticos_regressao, calcular_diagnostico_classificacao, calcular_importancia_variaveis
import pandas as pd

df = pd.read_csv("ES_cursos_presenciais_2021.csv", delimiter=';')
df = df.assign(
    TARGET_TX_OCUP_REG = lambda dataframe: round(dataframe['QT_MAT']/(dataframe['QT_TOTAL_VAGAS']),2)
)

df = df.rename(columns={"população.rgi": "POPULACAO_RGI"})

# Tirei 'IDEB_RGI' por conta dos NAs
X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
        'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
        'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
        'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
        'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
        'PERC_MAT_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])
y = df["TARGET_TX_OCUP_REG"]

def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(30, input_shape=(30,), kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

estimator = KerasRegressor(model=baseline_model, epochs=100, batch_size=5, verbose=0)
kfold = KFold(n_splits=10)
results = cross_val_score(estimator, X, y, cv=kfold, scoring='neg_mean_squared_error')
print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))
# %%
