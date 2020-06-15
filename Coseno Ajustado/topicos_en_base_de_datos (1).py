# -*- coding: utf-8 -*-
"""Topicos en Base de datos

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vgwWklkiZ8zn8Bse6nqLoHLzG01r4Exa
"""

import pandas as pd
import numpy as np
import math
from time import time
import csv
import os.path
from os import path
#from google.colab import drive
#drive.mount('/content/drive')

"""Cargando base de datos"""

#df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Movie_Ratings.csv')
#archivo = 'BX-Book-Ratings'
#df = df.rename({'Unnamed: 0':'peliculas'}, axis=1)

archivo = 'ratings'
#path.exists('guru99.txt')
Cache_Item = None
Cache_usuarios_peliculas1=None
Cache_peliculas1=None

def cargar(ubicacion,delimit,heade=None):
    pd_chunk = pd.read_csv(ubicacion, chunksize= 1000000, delimiter=delimit,header=heade,error_bad_lines=False)
    list_chunk = []

    for chunk in pd_chunk:
        list_chunk.append(chunk)
    df_concat = pd.concat(list_chunk)
    return df_concat

df = cargar(archivo+".csv",',')
"""
seleciono pelicula
obtengo usuarios con rating a mi pelicula
Agarro a esos usuarios y consulto a que peliculas han puntuado
Comparo la pelicula con las peliculas que han rakiado mis usuarios

"""
def peliculas(item1):
  peliculas1 = df.loc[df.loc[:,1] == item1 ]
  usuarios_peliculas1 = peliculas1[0].to_numpy()
  peliculas = df.loc[df.loc[:,0].isin(usuarios_peliculas1)][1].drop_duplicates()

  return peliculas.values

def preprocesamiento_movie(item1,item2):

  peliculas1 = df.loc[df.loc[:,1] == item1]
  peliculas2 = df.loc[df.loc[:,1] == item2]
  usuarios_peliculas1 = peliculas1[0].to_numpy()
  usuarios_peliculas2 = peliculas2[0].to_numpy()
  usuarios_comunes = usuarios_peliculas1[np.in1d(usuarios_peliculas1, usuarios_peliculas2)]
  peliculas1 = peliculas1.loc[peliculas1.loc[:,0].isin(usuarios_comunes) ][2].to_numpy()
  peliculas2 = peliculas2.loc[peliculas2.loc[:,0].isin(usuarios_comunes) ][2].to_numpy()
  Cache_usuarios_peliculas1=usuarios_peliculas1
  Cache_peliculas1=peliculas1
  Cache_Item=item1
  return peliculas1, peliculas2 , usuarios_comunes


def preprocesamiento_movie2(peliculas1,usuarios_peliculas1,item2):
  peliculas2 = df.loc[df.loc[:,1] == item2]
  usuarios_peliculas2 = peliculas2[0].to_numpy()
  usuarios_comunes = usuarios_peliculas1[np.in1d(usuarios_peliculas1, usuarios_peliculas2)]
  peliculas1 = peliculas1.loc[peliculas1.loc[:,0].isin(usuarios_comunes) ][2].to_numpy()
  peliculas2 = peliculas2.loc[peliculas2.loc[:,0].isin(usuarios_comunes) ][2].to_numpy()
  return peliculas1, peliculas2 , usuarios_comunes

def coseno_ajustado(pelicula1, pelicula2):
    columna1,columna2,columnas = preprocesamiento_movie(pelicula1,pelicula2)
    acumulador = 0
    op1=0 
    op2 = 0
    suma = 0
    div1 = 0
    div2 =0
    if(columna1.size==0):
        return 0
    for iterador in range(columna1.size):
        usuarios = columnas[iterador] 
        avg = df.loc[df.loc[:,0] == usuarios][2].mean()
        op1 = columna1[iterador] - avg
        op2 = columna2[iterador] - avg
        suma += op1*op2
        div1 += pow(op1,2)
        div2 += pow(op2,2)
    if(div2 and div1):
        resultado = suma/(math.sqrt(div1*div2))
        return resultado
    return -1


def coseno_ajustado2(pelicula1, pelicula2):
    if Cache_Item==None or Cache_Item!=pelicula1:
        columna1,columna2,columnas = preprocesamiento_movie(pelicula1,pelicula2)
    else:
        columna1,columna2,columnas = preprocesamiento_movie2(Cache_peliculas1,Cache_usuarios_peliculas1,pelicula1,pelicula2)

    acumulador = 0
    op1=0 
    op2 = 0
    suma = 0
    div1 = 0
    div2 =0
  
    if(columna1.size==0):
        return -1
    flagPr=True
    try:
        Promedios = pd.read_csv(archivo+"Promedios.csv",delimiter=';',header=None)
    except:
        flagPr = False


    for iterador in range(columna1.size):
        usuarios = columnas[iterador]
        if flagPr:
            if Promedios.loc[Promedios.loc[:,0]==usuarios].shape[0]>0:
                avg=Promedios.loc[Promedios.loc[:,0]==usuarios][1].values
                #print(avg)
                avg=avg[0]
            else:
                avg = df.loc[df.loc[:,0] == usuarios][2].mean()
                with open(archivo+'Promedios.csv', 'a') as employee_file:
                    employee_writer = csv.writer(employee_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                    employee_writer.writerow([str(usuarios),avg])
                    
        else:
            avg = df.loc[df.loc[:,0] == usuarios][2].mean()
            with open(archivo+'Promedios.csv', 'a') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                employee_writer.writerow([str(usuarios),avg])
                
        op1 = columna1[iterador] - avg
        op2 = columna2[iterador] - avg
        suma += op1*op2
        div1 += pow(op1,2)
        div2 += pow(op2,2)
    if(div2 and div1):
        resultado = suma/(math.sqrt(div1*div2))
        return resultado
    return -1

#print(coseno_ajustado2('0451167317','0451454952'))
