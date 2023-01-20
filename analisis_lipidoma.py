#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:56:55 2022

@author: eric
"""
#importamos las liberías
import pandas as pd
from scipy import stats
import numpy as np
import math
import sys

#función para el análisis del lipidoma
def analisis_lipidoma(file, path, type):
    #cargamos el dataset
    data = pd.read_csv(file, header = 'infer', sep = ',')
    #print(data)
    data = data.fillna(0)
    #inicializamos unos contadores
    contador = 0
    suma = 0
    contador_controles = 0
    suma_controles = 0
    
    #a partir del primer dataframe se crearán dos dataframes, uno para las muestras colestásicas y otro para los controles
    df_colestasis = pd.DataFrame(columns = ['value'])
    df_controles = pd.DataFrame(columns = ['value'])
    
    #dataframe que recogerá los resultados de los análisis estadísticos
    resultados = pd.DataFrame(columns = ['control_mean', 'dt_controles','shapiro_test_controles','colestasis_mean', 'dt_colestasis', 'shapiro_test_colestasis','levenne', 't_student', 'wilcoxon','Log2FC'], index = data.iloc[:, 0])

    #bucle para recorrer el dataset inicial
    for i in range(data.shape[0]): #filas

        for j in range(data.shape[1]): #columnas
            #j > 0 pq la primera columna es el id
            #print(data.columns[j])
            
            #dataframe con las colestasis
            if j > 0 and 'CONT' not in data.columns[j] and 'Cont' not  in data.columns[j]:
                contador = contador + 1
                #print(data.iloc[i][j])
                #print(data.iloc[i][0])
                suma = suma + int(data.iloc[i][j])
                datos_añadir = data.iloc[i][j].tolist()
                df_colestasis.loc[contador-1] = datos_añadir
            #dataframe con los controles
            elif j > 0 and 'CONT' in data.columns[j] or 'Cont' in data.columns[j]:
                contador_controles = contador_controles + 1
                #print(i)
                #print(j)
                #print(data.iloc[i][j])
                suma_controles = suma_controles + data.iloc[i][j]
                datos_añadir = data.iloc[i][j].tolist()
                df_controles.loc[contador_controles-1] = datos_añadir
        
        #print(df_colestasis)
        #print(df_controles)
    

        #calcular shapiro test

        shapiro_test = stats.shapiro(df_colestasis)
        #print('NO CONTROLES', shapiro_test)
        
        shapiro_test_controles = stats.shapiro(df_controles)
        #print('CONTROLES', shapiro_test_controles)
        
        #desviacion típica
        desviacion_tipica = df_colestasis['value'].std()
        desviacion_tipica_controles = df_controles['value'].std()
        #print('la desviación tipica es', desviacion_tipica)
        #print('la desviacion tipica en controles es', desviacion_tipica_controles)
        
        
        #test de levene homocedasticidad
        levenne = stats.levene(df_controles['value'], df_colestasis['value'])
        #print('el test de levene', levenne)

        #t student
        t_student = stats.ttest_ind(a=df_controles, b=df_colestasis, equal_var=True)
        #print('el pvalor de la t_student es', t_student[1])


        #wilcoxon
        wilcoxon = stats.ranksums(df_colestasis['value'], df_controles['value'])
        #print(wilcoxon)
        #fold change
        
        fold_change = df_colestasis.mean()/df_controles.mean()
        #print('Fold_change', fold_change[0])
        fold_2_change = math.log(fold_change[0], 2)
        #print(fold_2_change)
        #print(df_controles.mean())
        resultados.iloc[i][0] = df_controles.mean()
        resultados.iloc[i][1] = desviacion_tipica_controles
        resultados.iloc[i][2] = shapiro_test_controles
        resultados.iloc[i][3] = df_colestasis.mean()
        resultados.iloc[i][4] = desviacion_tipica
        resultados.iloc[i][5] = shapiro_test 
        resultados.iloc[i][6] = levenne
        resultados.iloc[i][7] = "".join(str(x) for x in t_student[1])
        resultados.iloc[i][8] = wilcoxon
        resultados.iloc[i][9] = fold_2_change
        
        df_colestasis = pd.DataFrame(columns = ['value'])
        df_controles = pd.DataFrame(columns = ['value'])
    path = f'{path}{type}_resultado.csv'
    resultados.to_csv(path, index=True, header=True,)
    print(path)
   

analisis_lipidoma = analisis_lipidoma(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))

#'/home/eric/Escritorio/TFM/lipidoma/datos_por_clase.csv', '/home/eric/Escritorio/TFM/Resultado_lipidoma',  'lipidoma'
#str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
