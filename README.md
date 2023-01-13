# TFM
> En este repositorio se encuentra el código empleado durante el TFM.
> El objetivo de este estudio es analizar los cambios metabólicos y transcripcionales que subyacen a la colestasis infantil desde un abordaje poliómico. Para ello, se ha escrito código en R, Python y Bash. 

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General Information
- Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->

## ¿Cómo utilizar el código?
- Tech 1 - version 1.0
- Tech 2 - version 2.0
- Tech 3 - version 3.0

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
 


