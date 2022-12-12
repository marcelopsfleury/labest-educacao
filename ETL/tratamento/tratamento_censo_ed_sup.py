import pandas as pd

def selecionar_colunas_censo_sup_2018(path_censo_es_inep):
    cols_names=['ANO','MUNICIPIO','COD_MUN','IN_CAPITAL','TP_ORG','TP_REDE','COD_IES','CURSO','CD_CURSO',\
                'CD_AREA_GERAL','AREA_GERAL','CD_AREA_ESPECIFICA','AREA_ESPECIFICA','CD_AREA_DETALHADA','AREA_DETALHADA',\
                'GRAU_ACADEMICO','MODALIDADE','NIVEL_ACADEMICO','QT_TOTAL_VAGAS','QT_VAGAS_DIURNO','QT_VAGAS_NOTURNO','QT_VAGAS_EAD',\
                'QT_VAGAS_NOVAS','QT_VAGAS_PROC_SEL','QT_VAGAS_REMANESC','QT_INSC_TOTAL','QT_INSC_DIURNO','QT_INSC_NOT','QT_INSC_EAD',\
                'QT_INSC_VAGA_NOVA','QT_INSC_PROC_SEL','QT_INSC_VAGA_REMANESC','QT_ING','QT_ING_FEM','QT_ING_MASC',\
                'QT_ING_DIURNO','QT_ING_NOTURNO','QT_ING_VG_NOVA','QT_ING_VEST','QT_ING_ENEM','QT_ING_SER','QT_ING_SIMP','QT_ING_EGR',\
                'QT_ING_OUTROS_TP','QT_ING_PROC_SEL','QT_ING_VAGAS_REMANESC','QT_ING_OUTRAS',\
                'QT_ING_0_17','QT_ING_18_24','QT_ING_25_29','QT_ING_30_34','QT_ING_35_39','QT_ING_40_49','QT_ING_50_59','QT_ING_60_MAIS',\
                'QT_MAT','QT_MAT_FEM','QT_MAT_MASC','QT_MAT_DIURNO','QT_MAT_NOTURNO',\
                'QT_CONC','QT_CONC_DIURNO','QT_CONC_NOTURNO','QT_MAT_FINANC','QT_MAT_FINANC_REEMB','QT_MAT_FIES','QT_MAT_RPFIES',\
                'QT_MAT_PROUNI','QT_MAT_NRPFIES','QT_MAT_RESERVA_VAGA','QT_MAT_ESC_PUB','QT_MAT_ESC_PRIV','QT_MAT_ESC_NI',\
                'QT_MAT_ASIST_EST','QT_MAT_ATIV_EXTRA']
    cols_selected=[0,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35,36,37,38,39,41,42,43,44,45,46,\
                47,48,49,50,51,52,53,54,56,71,72,73,74,75,76,77,78,79,80,81,82,83,90,93,94,129,130,131,132,135,137,155,174,175,176,186,190]

    dict= {'ANO':str,'COD_MUN':str, 'IN_CAPITAL':str,'TP_ORG': str,'TP_REDE':str,'COD_IES':str,'CD_CURSO':str,\
        'GRAU_ACADEMICO':str, 'QT_ING': np.int64,'QT_MAT':np.int64,'QT_CONC':np.int64}

    df_censo_2018 = pd.read_csv(path_censo_es_inep,    sep=';', dtype=dict, encoding="Latin-1",\
                   names=cols_names, usecols=cols_selected, skiprows=1)
    
    return df_censo_2018

def selecionar_colunas_censo_sup_2019(path_censo_es_inep):
    cols_names=['ANO','MUNICIPIO','COD_MUN','IN_CAPITAL','TP_ORG','TP_REDE','COD_IES','CURSO','CD_CURSO',\
                'CD_AREA_GERAL','AREA_GERAL','CD_AREA_ESPECIFICA','AREA_ESPECIFICA','CD_AREA_DETALHADA','AREA_DETALHADA',\
                'GRAU_ACADEMICO','MODALIDADE','NIVEL_ACADEMICO','QT_TOTAL_VAGAS','QT_VAGAS_DIURNO','QT_VAGAS_NOTURNO','QT_VAGAS_EAD',\
                'QT_VAGAS_NOVAS','QT_VAGAS_PROC_SEL','QT_VAGAS_REMANESC','QT_INSC_TOTAL','QT_INSC_DIURNO','QT_INSC_NOT','QT_INSC_EAD',\
                'QT_INSC_VAGA_NOVA','QT_INSC_PROC_SEL','QT_INSC_VAGA_REMANESC','QT_ING','QT_ING_FEM','QT_ING_MASC',\
                'QT_ING_DIURNO','QT_ING_NOTURNO','QT_ING_VG_NOVA','QT_ING_VEST','QT_ING_ENEM','QT_ING_SER','QT_ING_SIMP','QT_ING_EGR',\
                'QT_ING_OUTROS_TP','QT_ING_PROC_SEL','QT_ING_VAGAS_REMANESC','QT_ING_OUTRAS',\
                'QT_ING_0_17','QT_ING_18_24','QT_ING_25_29','QT_ING_30_34','QT_ING_35_39','QT_ING_40_49','QT_ING_50_59','QT_ING_60_MAIS',\
                'QT_MAT','QT_MAT_FEM','QT_MAT_MASC','QT_MAT_DIURNO','QT_MAT_NOTURNO',\
                'QT_CONC','QT_CONC_DIURNO','QT_CONC_NOTURNO','QT_MAT_FINANC',\
                'QT_MAT_RESERVA_VAGA','QT_MAT_ESC_PUB','QT_MAT_ESC_PRIV','QT_MAT_ESC_NI',\
                'QT_MAT_ASIST_EST','QT_MAT_ATIV_EXTRA']
                
    cols_selected=[0,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35,36,37,38,39,41,42,43,44,45,46,\
                47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,71,72,73,74,75,90,93,94,129,155,174,175,176,186,190]

    dict= {'ANO':str,'COD_MUN':str, 'IN_CAPITAL':str,'TP_ORG': str,'TP_REDE':str,'COD_IES':str,'CD_CURSO':str,\
        'GRAU_ACADEMICO':str,'MODALIDADE':str, 'QT_ING': np.int64,'QT_MAT':np.int64,'QT_CONC':np.int64}

    df_censo_2019 = pd.read_csv(path_censo_es_inep,    sep=';', dtype=dict, encoding="Latin-1",\
                    names=cols_names, usecols=cols_selected, skiprows=1)

    return df_censo_2019

def aplicar_filtros_censo_sup_2019(df_censo_2019):
    df_censo_filtered= df_censo_2019[(df_censo_2019['QT_CONC']>0) & (df_censo_2019['QT_ING']>0)&(df_censo_2019['QT_MAT']>0)&
                                    (df_censo_2019['QT_MAT']>df_censo_2019['QT_ING'])&
                                    (df_censo_2019['QT_MAT']>df_censo_2019['QT_VAGAS_NOVAS'])&
                                    ((df_censo_2019['MODALIDADE']=='2')|((df_censo_2019['MODALIDADE']=='1') & (df_censo_2019['QT_TOTAL_VAGAS']>= 20)))&
                                    ((df_censo_2019['MODALIDADE']=='2')|((df_censo_2019['MODALIDADE']=='1') & ((df_censo_2019['QT_ING']*5)>=
                                                                                                        (df_censo_2019['QT_MAT']*0.5))))]
    df_censo_filtered.dropna(subset=['COD_MUN'],inplace=True)
    # df_censo_filtered.reset_index(inplace=True)

    # Calculando a Faixa Etaria dos ingressantes 
    df_censo_filtered['FAIXA_ETARIA_ING']=round(((df_censo_filtered['QT_ING_0_17']*2)+\
                                        (df_censo_filtered['QT_ING_18_24']*3)+\
                                        (df_censo_filtered['QT_ING_25_29']*4)+\
                                        (df_censo_filtered['QT_ING_30_34']*5)+\
                                        (df_censo_filtered['QT_ING_35_39']*6)+\
                                        (df_censo_filtered['QT_ING_40_49']*7)+\
                                        (df_censo_filtered['QT_ING_50_59']*8)+\
                                        (df_censo_filtered['QT_ING_60_MAIS']*9))/\
                                        (df_censo_filtered['QT_ING_0_17']+\
                                        df_censo_filtered['QT_ING_18_24']+\
                                        df_censo_filtered['QT_ING_25_29']+\
                                        df_censo_filtered['QT_ING_30_34']+\
                                        df_censo_filtered['QT_ING_35_39']+\
                                        df_censo_filtered['QT_ING_40_49']+\
                                        df_censo_filtered['QT_ING_50_59']+\
                                        df_censo_filtered['QT_ING_60_MAIS']),1)

    df_censo_filtered['TX_MAT_FEM']= round(df_censo_filtered['QT_MAT_FEM']/df_censo_filtered['QT_MAT'],2)
    df_censo_filtered['TX_MAT_COTA']=round(df_censo_filtered['QT_MAT_RESERVA_VAGA']/df_censo_filtered['QT_MAT'],2)
    df_censo_filtered['TX_MAT_NOTURNO']=round(df_censo_filtered['QT_MAT_NOTURNO']/(df_censo_filtered['QT_MAT_DIURNO']+df_censo_filtered['QT_MAT_NOTURNO']),2)
    df_censo_filtered['TX_MAT_FINANC']=round(df_censo_filtered['QT_MAT_FINANC']/df_censo_filtered['QT_MAT'],2)
    df_censo_filtered['TX_ASSIST_ESTUDANTIL']=round(df_censo_filtered['QT_MAT_ASIST_EST']/df_censo_filtered['QT_MAT'],2)
    df_censo_filtered['TX_CONCORRENCIA']=round(df_censo_filtered['QT_INSC_TOTAL']/df_censo_filtered['QT_TOTAL_VAGAS'],2)
    df_censo_filtered['TX_ING_ENEM']=round(df_censo_filtered['QT_ING_ENEM']/df_censo_filtered['QT_ING'],2)
    df_censo_filtered['TX_ORIG_ESC_PUBL']=round(df_censo_filtered['QT_MAT_ESC_PUB']/df_censo_filtered['QT_MAT'],2)
    df_censo_filtered['TX_ATIV_EXTRA']=round(df_censo_filtered['QT_MAT_ATIV_EXTRA']/df_censo_filtered['QT_MAT'],2)

    # Cursos EAD são balanceados quanto ao turno para evitar interferência desse variável pra essa modalidade
    df_censo_filtered['TX_MAT_NOTURNO'].fillna(0.5,inplace=True)
    df_censo_filtered.reset_index(drop=True, inplace=True)

    return df_censo_filtered

def formatando_grau_academico(df_tab_corresp):
    # Formatando o campo 'GRAU_ACADEMICO' para compatibilizar com codfificação dos dados do Censo Superior
    df_tab_corresp['GRAU_ACADEMICO_DESC']=df_tab_corresp['GRAU_ACADEMICO']
    df_tab_corresp['GRAU_ACADEMICO']=['1' if str.upper(x)=='BACHARELADO' else ('2' if str.upper(x) == 'LICENCIATURA' else '3')\
                                        for x in df_tab_corresp['GRAU_ACADEMICO_DESC']]
    df_tab_corresp['CURSO']=df_tab_corresp['ROTULO_SUGERIDO']
    return df_tab_corresp

def match_tabela_correspondencia(df_censo_filtered,df_tab_corresp):
    # Fazendo o match da tabela de correspondência com dados do Censo Superior
    # (mais de uma possibilidade de denominação por curso, o que não representa problema na recuperação de dados do Enade-CPC)
    output_cols =['COD_MUN', 'COD_IES','CD_CURSO','CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','DENOMINACAO_CURSO',
                'QT_TOTAL_VAGAS','QT_INSC_TOTAL','QT_MAT','QT_ING','QT_CONC',
                'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL',
                'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','FAIXA_ETARIA_ING']
    df_corresp =  df_censo_filtered.merge(df_tab_corresp, on=['CURSO','GRAU_ACADEMICO'], how='left',suffixes=(None, '_y'))\
                            [output_cols]
    df_corresp['DENOMINACAO_CURSO']=df_corresp['DENOMINACAO_CURSO'].str.upper()
    df_corresp.sort_values(by=['COD_MUN','COD_IES','DENOMINACAO_CURSO','GRAU_ACADEMICO'], inplace=True,
                ascending = [True, True,True,True])
    # Alterar nome de colunas para match com dados do Enade-CPC
    df_corresp.rename(columns={'CURSO':'NM_CURSO'}, inplace=True)                                   
    df_corresp.rename(columns={'DENOMINACAO_CURSO':'CURSO'}, inplace=True)
    return df_corresp


def recuperar_info_enade_cpc(df_corresp, df_enade_curso_ult_aval):
    # Recuperando informações do Enade-CPC para utilizá-la como variável do modelo de ML
    df_censo_enade = df_corresp.merge(df_enade_curso_ult_aval,on=['COD_IES','COD_MUN','CURSO'],how='inner',suffixes=(None, '_y'))\
        [['COD_MUN', 'COD_IES','CD_CURSO','NM_CURSO','GRAU_ACADEMICO','MODALIDADE','TP_REDE','ANO_AVALIACAO',
        'QT_TOTAL_VAGAS','QT_INSC_TOTAL','QT_MAT','QT_ING','QT_CONC',
        'TX_MAT_FEM','TX_MAT_COTA','TX_MAT_NOTURNO','TX_MAT_FINANC','TX_ASSIST_ESTUDANTIL',
        'TX_CONCORRENCIA','TX_ING_ENEM','TX_ORIG_ESC_PUBL','TX_ATIV_EXTRA','FAIXA_ETARIA_ING','CPC_CONTINUO','CPC_FAIXA','TX_ESC_QUALI_IES']]    
    return df_censo_enade

def remover_duplicatas(df_censo_enade):
    # Removendo duplicatas(pegando a mais recente/alta avaliação do curso)
    df_censo_enade.sort_values(by=['COD_MUN','COD_IES','CD_CURSO','MODALIDADE','ANO_AVALIACAO','CPC_CONTINUO'], inplace=True,
                ascending = [True, True, True, True, True,True])
    df_censo_enade_unique =df_censo_enade.drop_duplicates(
                            subset = ['COD_MUN', 'COD_IES','CD_CURSO','MODALIDADE'],
                            keep = 'last').reset_index(drop = True)
    df_censo_enade_unique.rename(columns={'NM_CURSO':'CURSO'}, inplace=True)                                   
    return df_censo_enade_unique