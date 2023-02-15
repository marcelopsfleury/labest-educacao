#%%
from lazypredict.Supervised import LazyRegressor
from sklearn.utils import all_estimators
from sklearn.model_selection import train_test_split
import pandas as pd


df = pd.read_csv("ES_cursos_presenciais_2021.csv", delimiter=';')

df = df.assign(
    TARGET_TX_OCUP_REG = lambda dataframe: round(dataframe['QT_MAT']/dataframe["QT_TOTAL_VAGAS"],2)
)

df = df.assign(
    TARGET_TX_CONC_ING_REG = lambda dataframe: round(dataframe['QT_CONC']/dataframe['QT_INSCRITO_TOTAL'],2)
)

X = df[['COD_MUN', 'COD_RGI', 'COD_IES', 'DUR_CURSO', 'POLO', 'GRAU_ACADEMICO', 
        'TP_REDE','QT_TOTAL_VAGAS', 'QT_INSCRITO_TOTAL', 'QT_MAT', 'QT_CONC',
        'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
        'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
        'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'população.rgi',
        'PERC_MAT_RGI', 'IDEB_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI','CD_CURSO']]

X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI','CD_CURSO'])

y = df["TARGET_TX_OCUP_REG"]

# split data into train and test sets
seed = 7
test_size = 0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric = None)

models,predictions = clf.fit(X_train, X_test, y_train, y_test)
# %%
