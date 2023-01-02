import pandas as pd
import numpy as np

def selecionar_colunas_censo_sup_enade(path_censo_enade):
    dict={'COD_MUN':str, 'COD_IES':str,'CD_CURSO':str,'GRAU_ACADEMICO':str, 'MODALIDADE':str,'TP_REDE':str,'ANO_AVALIACAO':str}
    df_censo_sup_enade = pd.read_excel(path_censo_enade,  dtype=dict)
    df_censo_sup_enade=df_censo_sup_enade[df_censo_sup_enade['MODALIDADE']=='1']
    return df_censo_sup_enade


def agregar_prop_rendimento(path_ibge_rend, df_censo_sup_enade):
    # Agregar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb),
    # de acordo com o RGI ao qual o curso pertence
    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI']

    df_ibge_rend = pd.read_excel(path_ibge_rend, dtype=dict)
    # Calculando a proproção do rednimento (mediano) em relação ao SM de 2010 (R$ 510,00), 
    # para colocar numa escala compatível com outras variáveis
    df_ibge_rend['VLR_REND_W_MD_RGI'] = df_ibge_rend['VLR_REND_W_MD_RGI'].astype(np.float64)
    df_ibge_rend['VLR_REND_PROP_RGI']=round(df_ibge_rend['VLR_REND_W_MD_RGI']/510.0,2)

    breakpoint()

    df_educ_superior = df_censo_sup_enade.merge(df_ibge_rend, on='COD_MUN',how='left',suffixes=(None, '_y'))[output_cols]

    return df_educ_superior

def agregar_pop_rgi_mun(path_ibge_pop, path_ibge_rgi, df_educ_superior):
    # Agragar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb),
    # de acordo com o RGI ao qual o curso pertence

    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI', 'POPULACAO_2019_RGI']

    # População (estimativa) por município e rgi
    dict={'COD_MUN':str}
    df_ibge_pop = pd.read_excel(path_ibge_pop, dtype=dict)

    dict={'COD_MUN':str,'COD_RGI':str}
    df_ibge_rgi = pd.read_excel(path_ibge_rgi, dtype=dict)


    df_pop_rgi = df_ibge_pop.merge(df_ibge_rgi,on='COD_MUN',how='left',suffixes=(None, '_y'))
    df_pop_rgi_agg = df_pop_rgi.groupby('COD_RGI', as_index=False)['POPULACAO_2019'].sum()
    df_pop_rgi_agg.rename(columns={'POPULACAO_2019':'POPULACAO_2019_RGI'}, inplace=True)                                   
    df_pop_rgi_tot = df_pop_rgi.merge(df_pop_rgi_agg, how='left',suffixes=(None, '_y'))
    df_pop_rgi_tot.sort_values(by=['COD_RGI','COD_MUN'], inplace=True,
                ascending = [True, True])
    df_pop_rgi_tot.reset_index(inplace=True, drop=True)
    df_educ_superior = df_educ_superior.merge(df_pop_rgi_tot, on='COD_MUN',how='left',suffixes=(None, '_y'))[output_cols]
    df_educ_superior['FAIXA_POPULACAO_RGI']=\
            ["PQ" if x <= 300000 else ("MD" if (x > 300000 and x <= 3000000) else "GD")\
            for x in (df_educ_superior['POPULACAO_2019_RGI'])] 
    df_educ_superior['POPULACAO_2019_RGI'] = round(df_educ_superior['POPULACAO_2019_RGI']/1000000,2) # População em milhões
    output_cols=output_cols+['FAIXA_POPULACAO_RGI']


    return df_educ_superior


def agregar_matricula_ensino_medio(path_inep_mat_ens_med, df_educ_superior):
    # Agragar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb),
    # de acordo com o RGI ao qual o curso pertence
    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI', 'POPULACAO_2019_RGI', 'PERC_MAT_RGI_2019']

    # Matrículas no Ensino Médio (proporcionalmente à população) por RGI
    dict={'COD_MUN':str, 'COD_RGI':str}
    df_mat_ens_med = pd.read_excel(path_inep_mat_ens_med, dtype=dict)

    df_educ_superior = df_educ_superior.merge(df_mat_ens_med, on='COD_MUN',how='left',suffixes=(None, '_y'))[output_cols]
    return df_educ_superior


def agregar_ideb_por_rgi(path_inep_ideb, df_educ_superior):
    # Agregar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb),
    # de acordo com o RGI ao qual o curso pertence
    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI', 'POPULACAO_2019_RGI', 'PERC_MAT_RGI_2019', 'IDEB_RGI']

    # Ideb no Ensino Médio por RGI
    dict={'COD_MUN':str, 'COD_RGI':str}
    df_ideb = pd.read_excel(path_inep_ideb, dtype=dict)

    df_educ_superior = df_educ_superior.merge(df_ideb, on='COD_MUN',how='left',suffixes=(None, '_y'))[output_cols]
    return df_educ_superior


def agregar_enem_por_rgi(path_inep_enem, df_educ_superior):
    # Agregar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb),
    # de acordo com o RGI ao qual o curso pertence
    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI', 'POPULACAO_2019_RGI', 'PERC_MAT_RGI_2019', 'IDEB_RGI',
            'PROP_CAND_RGI_2019','MEDIA_NOTAS_RGI_2019']

    # Enem (Propporção de candidatos e média das notas) por RGI
    dict={'COD_MUN':str, 'COD_RGI':str}
    df_inep_enem = pd.read_excel(path_inep_enem, dtype=dict)

    df_educ_superior = df_educ_superior.merge(df_inep_enem, on='COD_MUN',how='left',suffixes=(None, '_y'))[output_cols]
    df_educ_superior.rename(columns={'PROP_CAND_RGI_2019':'PERC_CAND_ENEM_RGI_2019',
                                    'MEDIA_NOTAS_RGI_2019':'MEDIA_CAND_ENEM_RGI_2019'}, inplace=True)
    # Normalização das variáveis (para compatibilizar ordem de grandez no demais variáveis)
    df_educ_superior['PERC_CAND_ENEM_RGI_2019']=round(df_educ_superior['PERC_CAND_ENEM_RGI_2019']*100,2)
    df_educ_superior['MEDIA_CAND_ENEM_RGI_2019']=round(df_educ_superior['MEDIA_CAND_ENEM_RGI_2019']/100,4)
    output_cols=output_cols[0:-2]+['PERC_CAND_ENEM_RGI_2019','MEDIA_CAND_ENEM_RGI_2019']

    return df_educ_superior

def agregar_duracao_minima_cursos(path_dur_cursos, df_educ_superior):
    # Agragar demais informações para o modelo: renda, população, enem, ensino médio (mat e ideb) e duração do curso (em anos)
    # de acordo com o RGI ao qual o curso pertence
    # Dados sobre duração (mínima) dos cursos obtidos por meio de consulta às resoluções do MEC
    output_cols = ['COD_MUN','COD_RGI','COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','POLO',\
            'QT_TOTAL_VAGAS', 'QT_INSC_TOTAL','QT_MAT','QT_CONC','QT_ING',\
            'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL','FAIXA_ETARIA_ING',\
            'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','CPC_CONTINUO','CPC_FAIXA',\
            'TX_ESC_QUALI_IES','VLR_REND_PROP_RGI', 'POPULACAO_2019_RGI', 'PERC_MAT_RGI_2019', 'IDEB_RGI',
            'PROP_CAND_RGI_2019','MEDIA_NOTAS_RGI_2019', 'DUR_CURSO']

    # Enem (Propporção de candidatos e média das notas) por RGI
    # dict={'COD_MUN':str, 'COD_RGI':str}
    df_dur_cursos = pd.read_excel(path_dur_cursos)

    breakpoint()

    df_educ_superior = df_educ_superior.merge(df_dur_cursos, on='CURSO',how='left',suffixes=(None, '_y'))[output_cols]

    return df_educ_superior


def definir_targets(df_educ_superior):
    # Definindo os targets:
    # a) Taxa de ocupação (inicial): ocupação das vagas ofertadas (problema mais relevante para IES privadas)
    # b) Taxa de conclusão de curso: "equivalente" à taxa de sucesso (que tem outra metodologia de apuração - não sendo possível utilizá-la aqui)
    # Obs1: baseia-se a taxa de conclusão como proporção para o num de matrículas no ano do censo ao invés de matriculados,
    # (divide-se o num de matriculados pela duração do curso, para se poder comparar cursos com durações diferentes. 
    # Obs2: Para cursos EAD irá usar-se como Target a proporção em relação ao número de ingressantes (devido à indisponibilidade da informação)
    df_educ_superior['TARGET_TX_OCUP_INI']=round(df_educ_superior['QT_ING']/df_educ_superior['QT_TOTAL_VAGAS'],2)
    df_educ_superior['TARGET_TX_CONC_VAGAS']=round(df_educ_superior['QT_CONC']/df_educ_superior['QT_TOTAL_VAGAS'],2)
    df_educ_superior['TARGET_TX_CONC_ING']=round(df_educ_superior['QT_CONC']/df_educ_superior['QT_ING'],2)
    df_educ_superior['TARGET_TX_OCUP']=round(df_educ_superior['QT_MAT']/(df_educ_superior['QT_TOTAL_VAGAS']*df_educ_superior['DUR_CURSO']),2)
    return df_educ_superior
    