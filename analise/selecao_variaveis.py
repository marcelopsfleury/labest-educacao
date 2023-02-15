from sklearn.model_selection import train_test_split
import pandas as pd

seed = 7

def dividir_treino_teste(X, y):
    test_size = 0.33
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    return X_train, X_test, y_train, y_test

def dividir_banco_tx_ocupacao(path, classificacao = False, logistic = False, random_forest=False):
    df = pd.read_csv(path, delimiter=';')
    df = df.assign(
        TARGET_TX_OCUP_REG = lambda dataframe: round(dataframe['QT_MAT']/(dataframe['QT_TOTAL_VAGAS']),2)
    )

    df = df.rename(columns={"população.rgi": "POPULACAO_RGI"})

    X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'IDEB_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

    X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])

    if random_forest:
        X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

        X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])


    if classificacao:
        df["TARGET_TX_OCUP_CLASSIFICACAO"] = [0 if x <= 0.87 else (1 if ((x > 0.87 and x <= 1.64)) else 2) for x in (df['TARGET_TX_OCUP_REG'])]
        if logistic:
            X = df[['TP_REDE','DUR_CURSO','VLR_REND_PROP_RGI','POPULACAO_RGI',
             'CPC_CONTINUO','TX_ORIG_ESC_PUBL','TX_ING_ENEM','FAIXA_ETARIA_ING','TX_CONCORRENCIA',
             'TX_MAT_FINANC','TX_MAT_NOTURNO','POLO']]
            X = pd.get_dummies(X, columns=['POLO'])
        
        if random_forest:
            X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

            X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])
            
        y = df["TARGET_TX_OCUP_CLASSIFICACAO"].astype("category")
        X_train, X_test, y_train, y_test = dividir_treino_teste(X,y)
        return X_train, X_test, y_train, y_test

    y = df["TARGET_TX_OCUP_REG"]
    X_train, X_test, y_train, y_test = dividir_treino_teste(X,y)

    return X_train, X_test, y_train, y_test

def dividir_banco_tx_conclusao(path, classificacao = False, logistic = False, random_forest=False):
    df = pd.read_csv(path, delimiter=';')
    df = df.query("QT_INSCRITO_TOTAL != 0")
    df = df.assign(
        TARGET_TX_CONC_ING_REG = lambda dataframe: round(dataframe['QT_CONC']/dataframe['QT_INSCRITO_TOTAL'],2)
    )
    df = df.rename(columns={"população.rgi": "POPULACAO_RGI"})

    X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_MAT', 'QT_TOTAL_VAGAS',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'IDEB_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

    X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])

    if random_forest:
        X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

        X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])

    if classificacao:
        df["TARGET_TX_CONC_ING_CLASSIFICACAO"] = [0 if x <= 0.06 else (1 if ((x > 0.06 and x <=0.15)) else 2) for x in (df['TARGET_TX_CONC_ING_REG'])]
        if logistic:
            X = df[['TP_REDE','DUR_CURSO','VLR_REND_PROP_RGI','POPULACAO_RGI',
             'CPC_CONTINUO','TX_ORIG_ESC_PUBL','TX_ING_ENEM','FAIXA_ETARIA_ING','TX_CONCORRENCIA',
             'TX_MAT_FINANC','TX_MAT_NOTURNO','POLO']]
            X = pd.get_dummies(X, columns=['POLO'])

        if random_forest:
            X = df[['COD_MUN', 'COD_RGI', 'DUR_CURSO', 'COD_IES', 'POLO', 'GRAU_ACADEMICO', 
            'TP_REDE', 'QT_INSCRITO_TOTAL', 'QT_CONC',
            'TX_MAT_FEM', 'TX_MAT_COTA', 'TX_MAT_NOTURNO', 'TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL', 
            'FAIXA_ETARIA_ING', 'TX_CONCORRENCIA','TX_ING_ENEM', 'TX_ORIG_ESC_PUBL', 'TX_ATIV_EXTRA',
            'CPC_CONTINUO','CPC_FAIXA', 'TX_ESC_QUALI_IES', 'VLR_REND_PROP_RGI', 'POPULACAO_RGI',
            'PERC_MAT_RGI', 'PERC_CAND_ENEM_RGI','MEDIA_CAND_ENEM_RGI', 'FAIXA_POPULACAO_RGI']]

            X = pd.get_dummies(X, columns=['GRAU_ACADEMICO','POLO','FAIXA_POPULACAO_RGI'])

        y = df["TARGET_TX_CONC_ING_CLASSIFICACAO"].astype("category")
        X_train, X_test, y_train, y_test = dividir_treino_teste(X,y)
        return X_train, X_test, y_train, y_test

    y = df["TARGET_TX_CONC_ING_REG"]
    X_train, X_test, y_train, y_test = dividir_treino_teste(X,y)

    return X_train, X_test, y_train, y_test
