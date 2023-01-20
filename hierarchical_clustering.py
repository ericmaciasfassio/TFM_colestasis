import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import sys


#función para realizar el hierarchical clustering
def hierarchical_clustering(file, path, type):
    df = pd.read_csv(file, header = None)
    df = df.transpose()
    
    #quitamos la primera fila que son los ids
    df = df.iloc[1:, :]
    df = df.fillna(0)


    labelList = df.loc[:, 0]
    lista = []
    
    #Metemos en una lista todas las etiquetas para renombrarlas en controles o colestasis
    for i in range(len(labelList)):
        lista.append(labelList.iloc[i])

    lista_rectificada = []
    for i in range(len(lista)):
        if 'Control' in lista[i] or 'CONTR' in lista[i] :
            lista_rectificada.append('control')
        else:
            lista_rectificada.append('colestasis')
    lista_rectificada

    pca = PCA(n_components=2)
    X_r= pca.fit(df.iloc[: , 1:]).transform(df.iloc[: , 1:])



    #print(X_r[11,:])
    #print(X_r.shape)
    print('explained variance ratio (first 16 components): %s'
        % str(pca.explained_variance_ratio_))
    #y = df.loc[1:, 0]
    df_prueba = pd.DataFrame(lista_rectificada)

    y = (df_prueba.values[ 0:, 0 ] == 'control').astype(np.int)
   
    #PCA opcional
    plt.figure()
    comp1=0; #first component to visualize, you can modify it
    comp2=1; #second component to visualize, you can modify it

    # plot the two components selected above for both malign and benign tumors
    plt.scatter(X_r[y == 1, comp1], X_r[y == 1, comp2], color='g', alpha=.7, lw=1,
                    label='control')

    plt.scatter(X_r[y == 0, comp1], X_r[y == 0, comp2], color='r', alpha=.7, lw=1,
                    label='colestasis')

    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('PCA ARNm dataset')

    plt.xlabel(pca.explained_variance_ratio_[0])
    plt.ylabel(pca.explained_variance_ratio_[1])

    #plt.show()

    # creamos dendrograma
    #creamos un array como está especificado en la documentación con labels y datos
    matriz2 = np.ones([1,1])
    for i in range(len(lista)):
        matriz2 = np.append(matriz2, [[lista[i]]], axis = 0)
        #print(matriz2)
    matriz1 = np.array(X_r)
    matriz2 = np.delete(matriz2, (0), axis = 0)


    matriz_final = np.concatenate((matriz2, matriz1), axis=1)
    #print(matriz_final)  #dataframe unido con todo

    indices_lista = []
    
    #debemos eliminar los controles del dataset
    for i in range(len(matriz_final)):
        if 'Control' in matriz_final[i][0] or 'CONTR' in matriz_final[i][0]:
            indices_lista.append(i)
    matriz_final = np.delete(matriz_final, (indices_lista), axis = 0)
    #print(matriz_final)
	
    #matriz final sin controles
    matriz_final = np.delete(matriz_final, 0, axis = 1)
    #print(matriz_final)

    linked = linkage(matriz_final, 'single')
 
     #quitamos los controles de la lista de labels
    lista_colestasis = []
    for i in range(len(lista)):
        if 'Control' not in lista[i] and 'CONT' not in lista[i] :
            lista_colestasis.append(lista[i])

    plt.figure(figsize=(20, 10))
    dendrogram(linked,
                orientation='top',
                labels=lista_colestasis,
                distance_sort='descending',
                leaf_rotation=90,
                leaf_font_size= 8
            )
    plt.title('Dendrograma', fontsize = 25)
    #plt.show()

    filename = f'{path}{type}_dendrograma.png'
    plt.savefig(filename, dpi=100, facecolor='w', edgecolor='w',
            orientation='portrait', papertype='legal', format=None,
            transparent=True, bbox_inches=None, pad_inches=0.2,
            frameon=None)
    return(print('Python Script finalizado')) 


dendrogram = hierarchical_clustering(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
#'/home/eric/Escritorio/TFM/Resultado_lipidoma/lipidoma_vst.csv','/home/eric/Escritorio/TFM/Resultado_lipidoma/figuras','/lipidoma'
#str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
