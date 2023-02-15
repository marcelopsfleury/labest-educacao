from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
from yellowbrick.features import FeatureImportances
from matplotlib import pyplot as plt

def calcular_diagnosticos_regressao(y_test, predictions):
    RMSE = mean_squared_error(y_test, predictions)
    print("RMSE: %.5f" % RMSE)

    R2 = r2_score(y_test, predictions)
    print("R2: %.5f" % R2)

def calcular_diagnostico_classificacao(y_test, predictions):
    print ('Acurácia:',  accuracy_score(y_test, predictions))
    print ('Precisão:',  precision_score(y_test, predictions,average='weighted'))
    print ('Recall:', recall_score(y_test, predictions,average='weighted'))
    print ('F1:',f1_score(y_test, predictions,average='weighted'))

def calcular_importancia_variaveis(regressor, X_train, y_train, top_n=15):
    visualizacao = FeatureImportances(regressor, topn=top_n, colors=['gray'], relative=True)
    visualizacao.fit(X_train, y_train)
    visualizacao.show()

def calcular_importancia_variaveis_svm(coef, names):
    imp = coef
    imp,names = zip(*sorted(zip(imp,names)))
    plt.barh(range(len(names)), imp, align='center')
    plt.yticks(range(len(names)), names)
    plt.show()