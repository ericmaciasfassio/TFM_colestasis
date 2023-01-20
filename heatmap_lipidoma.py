# libraries
import seaborn as sns
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sys

#'/home/eric/Escritorio/TFM/lipidoma/heatmap_final.csv'
#print(str(sys.argv))

#función para crear el heatmap
def heatmap_lipidoma(file, path, type):
    df = pd.read_csv(file, index_col= 0)
    print(df)      
    df = df[df['t_student']< 0.05]
    df = df.sort_values('Log2FC', ascending=False)
    df1 = df.iloc[:,7:8]
    print(len(df1))
      
    df2 = df.iloc[:,9:10]
    print(len(df2))

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    fig.subplots_adjust(wspace=0.01)
    # creating a colormap
    colormap = sns.color_palette("BuGn_r")

    sns.heatmap(df2, annot=True, annot_kws={"size": 10}, linewidths=1, linecolor='white', ax=ax1, yticklabels = True, cmap='coolwarm')
    sns.heatmap(df1, annot=True, annot_kws={"size": 10}, linewidths=1, linecolor='white', ax=ax2, yticklabels=False)

    ax2.yaxis.tick_right()

    fig.subplots_adjust(wspace=0.001)
    #plt.show()
    filename = f'{path}{type}_heatmap.png'
    plt.savefig(filename, dpi=100, facecolor='w')

heatmap_lipidoma = heatmap_lipidoma(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
