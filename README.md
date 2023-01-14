# TFM
En este repositorio se encuentra el código empleado durante el TFM.\
El objetivo de este estudio es analizar los cambios metabólicos y transcripcionales que subyacen a la colestasis infantil desde un abordaje poliómico. Para ello, se ha escrito código en R, Python y Bash. 

## Table of Contents
* [Información General](#general-information)
* [Setup](#Setup)
* [Scripts](#features)
* [Ejemplo](#technologies-used)
* [Contacto](#contacto)

## General Information
- Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->

## ¿Cómo utilizar el código?
Primero se debe clonar el repositorio:
```console
git clone https://github.com/ericmaciasfassio/TFM_colestasis.git

```
También se deberán instalar los paquetes de R y las librerías de Python siguientes:
```R
install.packages("BiocManager")
BiocManager::install("biomaRt")
BiocManager::install("ComplexHeatmap")
BiocManager::install("DESeq2")
BiocManager::install("EnhancedVolcano")
install.packages("RColorBrewer")
```
```console
pip install pandas
pip install numpy
pip install scipy
pip install matplotlib
```

Para poder ejecutar los scripts debemos darles permiso.

```console
chmod u+x Biomart.sh
```
Ejecutamos el script de Biomart.sh:

```console
./Biomart.sh ./Resultado_biomart ./csv_ejemplos/biomart.csv
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio Resultado_biomart se guardará el csv de salida.

```
Script Biomart.sh finalizado
```
Ejecutamos el script de analisis_transcriptoma.sh:

```console
./analisis_transcriptoma.sh ./resultados_transcriptoma ./csv_ejemplos/genes.csv genes
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio ./resultados_transcriptoma se guardarán los csv de salida y las figuras.

```
Script analisis_transcriptoma.sh finalizado 
```

Ejecutamos el script de correlaciones.sh:

```console
./correlaciones.sh ./resultado_correlaciones ./csv_ejemplos/genes_correlacion.csv ./csv_ejemplos/mirnas_correlacion.csv 
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio ./resultado_correlaciones se guardarán los csv de salida y las figuras.

```
Script correlaciones.sh finalizado 
```
Ejecutamos el script de lipidoma.sh:

```console
./lipidoma.sh ./resultado_lipidoma_2 ./csv_ejemplos/datos_lipidoma.csv lipidoma
```
Al finalizar la ejecución obtenemos un mensaje por pantalla y en el directorio ./resultado_correlaciones se guardarán los csv de salida y las figuras.

```
Script lipidoma.sh finalizado 
```
## Scripts
Todos los scripts se ejecutan por terminal de una forma no interactiva.
Todos piden 3 parámetros:
1.archivo.csv: Con los datos
2.Nombre de un directorio: Se creará un directorio un directorio nuevo
3.Tipo de datos analizados: En el nombre de los archivos que se crearán durante la ejecución de los script se añadirá

Encontramos un total de 4 scripts:

1. Biomart.R: Este script permite clasificar los genes en función de la categoría a la que pertenecen (codificantes de proteínas, de lncRNA...). Además, permite cambiar el Ensembl id por el Gene Symbol. 

2. Analisis_transcriptoma.sh: Dentro de este script encontramos un script en R y otro en Python, necesarios para realizar las figuras (PCA, dendrograma y heatmaps) y el análisis de expresión diferencial. Estos scripts son:
  -analisis_miRNA_TFM.R
  -hierarchical_clustering.py
  
3.Analisis_lipidoma.sh: Dentro de este script encontramos 
  -lipidoma_final_repetido.py
  -heatmap_lipidoma.py
  -lipidoma_final.R
  -hierarchical_clustering.py
  
4.Correlaciones
 


