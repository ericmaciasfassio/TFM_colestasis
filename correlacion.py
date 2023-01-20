"""
Created on Wed Oct 19 12:51:33 2022
@author: eric
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
plt.style.use('ggplot')
import csv
import pandas as pd
import numpy as np
from scipy import stats
import sys



#función para realizar las correlaciones
def correlacion(genes, mirnas, path):
    genes_df = pd.read_csv(genes, header='infer') 
    miRNA_df = pd.read_csv(mirnas , header='infer') 
    #dimension of data
    x = len(miRNA_df)
    y = len(genes_df)

    #creamos dos arrays para guardar el pvalor y el valor del estadístico
    valor_estadistico_z = np.zeros([y, x])
    p_value = np.zeros([y, x])

    #recorremos los dataframes de genes y mirnas
    contador = 0
    for i in range(len(genes_df)):
        a = genes_df.loc[i]   #devuelve la file i del dataframe de genes
    
        for j in range(len(miRNA_df)):
            contador = contador + 1
            b= miRNA_df.loc[j]  #devuelve la file j del dataframe de miRNA
        
            datos = pd.DataFrame(pd.concat([a, b], axis = 1))  #concatenamos las dos filas i, j por columnas en un nuevo dataframe, por lo que tenemos genes y mirnas
            
           
            #la primera fila no se selecciona, porque corresponde con los ids
            #x = se selecciona la primera columna que corresponde con la columna de los genes
            #y = se selecciona la segunda columna que corresponde con la columna de mirnas
            x=datos.iloc[1:,0].astype('float') 
        
            y=datos.iloc[1:,1].astype('float')
        
            
            z=stats.spearmanr(x, y)
            
        
            valor_estadistico_z[i][j]= z[0]
            p_value[i][j]= z[1]
            
        
        
            #plot de las z más significativas
            """ if -1 < z[0] < -0.85 or 1 > z[0] > 0.85:
                
                fig, ax = plt.subplots(1, 1 , figsize = (6, 4))
                ax.scatter(x, y, alpha= 0.8)
                ax.set_xlabel(datos.iloc[0,0])
                ax.set_ylabel(datos.iloc[0,1])
                b1, a1 = np.polyfit(x, y, deg=1)

                #máximo del eje x
                maximum=0
                for p in datos.iloc[1:,0]:
                    if p > maximum:
                        maximum = p
                xseq = np.linspace(0, maximum+30, num=10)
                
                maximum_y=0
                for k in datos.iloc[1:,1]:
                    if k > maximum_y:
                        maximum_y = k
                # Plot regression line
                ax.plot(xseq, a1 + b1 * xseq, color="k", lw=2.5)
                plt.title('Spearman correlation')
                valor = round(z[0], 4)
                plt.text(x = maximum-50, y = maximum_y-10, s = f'Z = {round(z[0], 4)}')
                
                plot = f'{datos.iloc[0,0]}_{datos.iloc[0,1]}'
                nombre = f'{path}/{plot}.pdf'
                plt.savefig(nombre, dpi=300, bbox_inches='tight')"""
                

    #id de los genes
    lista_1 = []
    for i in genes_df['id']: 
        lista_1.append(i)
        
    #id de los mirnas
    lista_2 = []
    for i in miRNA_df['id']:
        lista_2.append(i)
     
     #guardamos un csv con los pvalores y los estadísticos
    df_miARN = pd.DataFrame(valor_estadistico_z, index=lista_1, columns = lista_2)
    df_miARN.to_csv(f'{path}/z_correlaciones.csv', index=True, header=True, sep=',')

    df_miARN_pvalor= pd.DataFrame(p_value, index=lista_1, columns = lista_2 )

    df_miARN_pvalor.to_csv(f'{path}/p_value_correlaciones.csv', index=True, header=True, sep=',')
    return [f'{path}/z_correlaciones.csv', f'{path}/p_value_correlaciones.csv']

# a partir de la función anterior calculamos los FDR y las correlaciones significativas
def calculo_FDR(genes, mirnas, z_correlaciones, p_correlaciones, path):
    genes_df = pd.read_csv(genes, header='infer') 
    miRNA_df = pd.read_csv(mirnas, header='infer') 

    
    p_value = pd.read_csv(p_correlaciones, sep = ',', header='infer', index_col=0)
    valor_estadistico_z = pd.read_csv(z_correlaciones, header='infer', sep = ',', index_col=0) #este archivo sirve para diferenciar correlacione positivas y negativas

    df_nuevo = pd.DataFrame(columns=['p-valor', 'posición i', 'posicion j'])

    cont = 1

    #creamos un df con cada p-valor en una fila y guardando la posición inicial con una columna i + otro columna j
    for i in range(len(genes_df)):
    
        for j in range(len(miRNA_df)):
            valor = p_value.iloc[i][j]
    
            #Lista = {'p-valor': valor , 'posicion i': i , 'posicion j': j}
            Lista = [valor, i, j]
            df_nuevo.loc[cont] = Lista
            
            #df = df.append(Lista, ignore_index=True)
            Lista = []
            cont = cont + 1


    df1_nuevo = df_nuevo.sort_values('p-valor')  #ordenamos las filas en función del p-valor
    print(df1_nuevo)

    lista_numeros = []
    z = len(genes_df)* len(miRNA_df)
    for k in range(1, z+1):
        lista_numeros.append(k)
    
    df1_nuevo.loc[:,'rank '] = lista_numeros  #añadimos una nueva columna que corresponde con el ranking de los p-valor

    print(df1_nuevo)


    m = len(df1_nuevo)   #número total de p-valores necesario para poder calcular el FDR

    Q = 0.05   #el alfa
    cont = 1
    lista_FDR = []
    for k in range(0, z):
        i = df1_nuevo.iloc[k,3]   #i corresponde con la posición en el ranking 
    
    
        fdr = (i/m)*Q  #formula para calcular el FDR

        lista_FDR.append(fdr)

    df1_nuevo.loc[:,'FDR'] = lista_FDR    #añadimos una columna con el FDR al df
    print(df1_nuevo)    

    FDR_matriz = np.zeros([len(genes_df),len(miRNA_df)])
    cont=0
    df1_nuevo = df1_nuevo.sort_index()  #IMPORTANTE, reordenamos el df en función del index inicial


    #construimos el df final 
    for i in range(len(genes_df)):
        for j in range(len(miRNA_df)):
            
            FDR_matriz[i][j]=df1_nuevo.iloc[cont, 4]
            cont = cont + 1

    lista_1 = []
    for i in genes_df['id']: 
        lista_1.append(i)
        
    lista_2 = []
    for i in miRNA_df['id']:
        lista_2.append(i)
        
    FDR_genes_miRNA = pd.DataFrame(FDR_matriz, index=lista_1, columns = lista_2)
    FDR_genes_miRNA.to_csv(f'{path}/FDR.csv', index=True, header=True, sep=',')


    # 0 no es significativo
    # 1 es significativo con una z positiva
    #-1 es significativa con una z negativa
    matriz_0_1 = np.zeros([len(genes_df),len(miRNA_df)])
    for i in range(len(genes_df)):
    
        for j in range(len(miRNA_df)):
            if  p_value.iloc[i][j]<= FDR_matriz[i][j] and valor_estadistico_z.iloc[i][j] > 0:
                
                matriz_0_1[i][j]= 1
            elif p_value.iloc[i][j]<= FDR_matriz[i][j] and valor_estadistico_z.iloc[i][j] < 0:
                matriz_0_1[i][j]= -1
            else:
                matriz_0_1[i][j]= 0
                
    FDR_significativo_miARN = pd.DataFrame(matriz_0_1, index=lista_1, columns = lista_2)

    FDR_significativo_miARN.to_csv(f'{path}/FDR_significativo.csv', index=True, header=True, sep=',')

    print('final')

#str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
#'/home/eric/Escritorio/github/genes_correlacion.csv', '/home/eric/Escritorio/github/mirnas_correlacion.csv', '/home/eric/Escritorio/github'
correlacion = correlacion(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))

calculo_fdr = calculo_FDR(str(sys.argv[1]), str(sys.argv[2]), correlacion[0], correlacion[1], str(sys.argv[3]))
