# -*- coding: utf-8 -*-

#from ..geneticos import metaheuristicas
from metaheuristicas import *
import sys
import copy


## ESQUEMA DE REPRESENTACION

""" 3 maquinas y 3 trabajos

      m1      m2    m3
t1    14      23    34
t2    16      12    10
t3    23      07    29


datos [[j1], [j2], [j3] ]

datos = [[j1m1, j1m2, j1m3], [j2m1, j2m2, j2m3], [j3m1, j3m2, j3m3]]


datos = [[14, 23, 34], [16, 12, 10], [23, 7, 29]]

"""


class Problema(object):
    """docstring for Problema"""

    datos = []
    jobs = 0
    maquinas = 0
    upper_bound = 0
    lower_bound = 0
    max_iterations = 500
    tamano_poblacion = 128
    iteracion = 0
    best_makespan = 999999
    best_iteration = 0

    poblacion_inicial = []

    def __init__(self):
        super(Problema, self).__init__()

    def parsear(self, archivo):
        """ Toma la entrada de Tailard y la transforma en algo
        con el formato lista de listas que podamos utilizar """

        with open(archivo, "r") as f:

            lines = map(str.strip, f.readlines())
            data = [map(int, line.split()) for line in lines]

        info = data.pop(0)
        self.jobs = info[0]
        self.maquinas = info[1]
        self.upper_bound = info[2]
        self.lower_bound = info[3]

        return data

    def evolucionar():
        padres = []
        hijos = []
        hijos_finales = []
        lista_final = []
        dbt = DBT()
        while len(hijos_finales) < 128:
            #-----------  SELECCION -----------
            #Armo una lista con 2 padres(Ver como vaciar la lista)
            for i in range(2):
                crom1 = self.poblacion_inicial.cromosomas(
                    random.randint(0, tamano_poblacion - 1))
                crom2 = self.poblacion_inicial.cromosomas(
                    random.randint(0, tamano_poblacion - 1))
                padres.append(dbt.seleccionar(crom1, crom2))
            # Analizo si voy a cruzar o no
            probabilidad_cruce = random.randint(0, 100)
            if probabilidad_cruce >= 35:

                #-----------  CROSSOVER  ----------

                # Analizo el método de cruce seteado
                if metodo_crossover == 1:
                    # Utilizo PMX
                    crossover = PMX()
                    hijos.append(crossover.cruzar(padres[0], padres[1]))
                else:
                    # Utilizo CX
                    crossover = CX()
                    hijos.append(crossover.cruzar(padres[0], padres[1]))

            else:
                #No Hacemos CrossOver
                hijos = copy.deepcopy(padres)

            # Vamos a contemplar que los padres pueden mutar
            # Analizo si voy mutar o no cada uno de los hijos
            for i in range(len(hijos)):
                probabilidad_mutacion = random.random()
                if probabilidad_mutacion <= (1 / self.jobs):
                    #-----------  MUTACIÓN  -----------

                    # Analizo el método de mutacion seteado
                    if metodo_mutacion == 1:
                        # Utilizo INVERTION
                        mutacion = Invertion()
                        # SE PUEDE HACER ESTA ASIGNACION ?
                        hijos[i] = mutacion.mutar(hijos[i])
                    else:
                        # Utilizo DISPLACEMENT
                        mutacion = Displacement()
                        hijos[i] = mutacion.mutar(hijos[i])
            #Agrego los dos hijos a la poblacion de hijos finales
            for i in range(len(hijos)):
                hijos_finales.append(hijos[i])
        # Termina while, estan creados los hijos finales
        #-----------  REEMPLAZO  ----------
        r = Remplazo()
        lista_final = r.reemplazar(self.poblacion_inicial, hijos_finales)

        # Creada la poblacion final, de los cuales solo interesa el primer
        # elemento, dado que la lista esta ordenada en forma descendente

        # Comparamos con el makespan actual
        if lista_final[0].fitness < self.best_makespan:
            self.best_makespan = lista_final[0].fitness
            self.best_iteration = self.iteracion

        #Finalmente Reasignamos poblacion inicial
        self.poblacion_inicial = copy.deepcopy(lista_final)

    def resolver():

        problema = self

        if len(sys.argv) == 2:
            problema.datos = problema.parsear(sys.argv[1])
        else:
            print ("\nUsage: python flow.py <Taillard problem file>\n")
            sys.exit(0)

        #-----------  GENERACIÓN POBLACIÓN INICIAL  ----------
        # Genero los primeros padres segun la cristiandad

        adan_y_eva = Poblacion(tamano_poblacion)
        adan_y_eva.generar(problema.jobs)
        adan_y_eva.mostrar()

        self.poblacion_inicial = adan_y_eva
        #self.padres = Poblacion(tamano_poblacion / 2)
        #self.hijos = Poblacion(tamano_poblacion)
        #self.hijos_mutados = Poblacion(tamano_poblacion)
        while self.iteracion < self.max_iterations:
            evolucionar()
            self.iteracion += 1

if __name__ == "__main__":
    p = Problema()
    p.resolver()