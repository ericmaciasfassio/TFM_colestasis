#!/bin/bash
# -*- ENCODING: UTF-8 -*-
FICHERO=$1 	#/home/eric/Escritorio/github/prueba
GEN=$2	#/home/eric/Escritorio/github/genes_correlacion.csv
MIRNA=$3	#/home/eric/Escritorio/github/genes_correlacion.csv		

#comprobar que se han introducido 3 argumentos
if [ "$#" != "3" ]; then
    echo "Debe introducir 3 argumentos"
    echo "Argumento 1 = Nombre de un directorio para crearlo y guardar los resultados"
    echo "Argumento 2 = Archivo CSV con los datos de los genes"
    echo "Argumento 3 = Archivo CSV con los datos de los miRNAs"
    exit
else
    echo "Se han introducido 3 argumentos"
fi

#Comprobamos que el directorio no existe y lo creamos
if [ -d ./$FICHERO ]
then
	echo "El fichero $FICHERO existe"
	exit
else
	mkdir $FICHERO
   	echo "El fichero $FICHERO se ha creado"
fi


#Script de python que realiza el calculos de los coeficientes de Spearman
python3 correlacion.py $GEN $MIRNA $FICHERO

echo 'Script correlaciones.sh finalizado'
