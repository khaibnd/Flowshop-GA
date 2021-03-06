# -*- coding: utf-8 -*-

#from ..geneticos import metaheuristicas
from metaheuristicas import *
import sys
import copy
import time
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
    best_makespan_time = 0
    tiempo_ejecucion = 0
    tiempo_inicial = 0
    mejores_fitness = []
    fit_prom = 0
    poblacion_inicial = []

    def __init__(self):
        super(Problema, self).__init__()

    def ordenardatos(self, matrix, width, height):
        a = [[matrix[row][col] for row in range(0, height)]
            for col in range(0, width)]
        return a

    def cmakespan(self, datos, secuencia):
        t = [0] * len(datos[0])
        for j in secuencia:
            for m in range(len(datos[j])):
                if m == 0:
                    t[m] = t[m] + datos[j][m]
                else:
                    if t[m - 1] > t[m]:
                        t[m] = t[m - 1] + datos[j][m]
                    else:
                        t[m] = t[m] + datos[j][m]
        return t[-1]

    def parsear(self, archivo):
        """ Toma la entrada de Tailard y la transforma en algo
        con el formato lista de listas que podamos utilizar """

        with open(archivo, "r") as f:

            lines = map(str.strip, f.readlines())
            data = [list(map(int, line.split())) for line in lines]

        info = data.pop(0)
        self.jobs = info[0]
        self.maquinas = info[1]
        self.upper_bound = info[2]
        self.lower_bound = info[3]

        data = self.ordenardatos(data, self.jobs, self.maquinas)
        return data

    def evolucionar(self, metodo_crossover, metodo_mutacion):
        padres = []
        hijos = []
        hijos_finales = []
        lista_final = []
        dbt = DBT()
        while len(hijos_finales) < self.tamano_poblacion:
            #-----------  SELECCION -----------
            #Armo una lista con 2 padres
            for i in range(2):
                crom1 = self.poblacion_inicial.cromosomas[
                    random.randint(0, self.tamano_poblacion - 1)]
                crom2 = self.poblacion_inicial.cromosomas[
                    random.randint(0, self.tamano_poblacion - 1)]
                padres.append(dbt.seleccionar(crom1, crom2))
            # Analizo si voy a cruzar o no
            probabilidad_cruce = random.randint(0, 100)
            if probabilidad_cruce >= 35:
                #-----------  CROSSOVER  ----------
                # Analizo el metodo de cruce seteado
                if metodo_crossover == 1:
                    # Utilizo PMX
                    crossover = PMXa()
                    childs = crossover.cruzar(padres[0], padres[1])
                    hijos.append(childs[0])
                    hijos.append(childs[1])
                else:
                    # Utilizo CX
                    crossover = CX()
                    childs = crossover.cruzar(padres[0], padres[1])
                    hijos.append(childs[0])
                    hijos.append(childs[1])

            else:
                #No Hacemos CrossOver
                hijos = copy.deepcopy(padres)

            # Vamos a contemplar que los padres pueden mutar
            # Analizo si voy mutar o no cada uno de los hijos
            i = 0
            for i in range(len(hijos)):
                probabilidad_mutacion = random.random()
                if probabilidad_mutacion <= ((1.0 / self.jobs)):
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
                        #print (("Sec antes de mutar: ", hijos[i].secuencia))
                        hijos[i] = mutacion.mutar(hijos[i])
                        #print (("Sec desp de mutar: ", hijos[i].secuencia))

            #Agrego los dos hijos a la poblacion de hijos finales
            i = 0
            for i in range(len(hijos)):
                hijos_finales.append(hijos[i])
                # print(hijos_finales[i].secuencia)
            padres = []
            hijos = []
        # Termina while, estan creados los hijos finales
        #-----------  REEMPLAZO  ----------
        for i, elem in enumerate(hijos_finales):
            #print("Antes mp: ", elem.secuencia)
            hijos_finales[i].fitness = self.cmakespan(self.datos,
                    elem.secuencia)
        r = Reemplazo()

        lista_final = r.reemplazar(self.poblacion_inicial.cromosomas,
            hijos_finales)

        # Creada la poblacion final, de los cuales solo interesa el primer
        # elemento, dado que la lista esta ordenada en forma descendente

        # Comparamos con el makespan actual
        if lista_final[0].fitness < self.best_makespan:
            self.best_makespan = lista_final[0].fitness
            self.best_iteration = self.iteracion
            self.best_makespan_time = time.time() - self.tiempo_inicial

        # Agrego este mejor makespan a la lista para calcular promedio
        self.mejores_fitness.append(lista_final[0].fitness)
        #Finalmente Reasignamos poblacion inicial
        self.poblacion_inicial.cromosomas = copy.deepcopy(lista_final)

    def mostrar_solucion(self):
        print("Mejor costo:" + str(self.best_makespan))
        print("Promedio de los mejores costos: " + str(self.fit_prom))
        print("Tiempo Mejor Costo: " + str(self.best_makespan_time))
        print("Tiempo Total Ejecucion: " + str(self.tiempo_ejecucion))
        print("Mejor Iteracion: " + str(self.best_iteration))
        print("Total Iteraciones: " + str(self.max_iterations))

    def resolver(self, metodo_crossover, metodo_mutacion, iterations=500):
        self.max_iterations = iterations
        problema = self
        if len(sys.argv) == 2:
            problema.datos = problema.parsear(sys.argv[1])
        else:
            print ("\nUsage: python flowshop.py <Taillard problem file>\n")
            sys.exit(0)

        #-----------  GENERACIÓN POBLACIÓN INICIAL  ----------
        # Genero los primeros padres segun la cristiandad
        self.tiempo_inicial = time.time()

        adan_y_eva = Poblacion(self.tamano_poblacion)
        adan_y_eva.generar(problema.jobs)
        for crom in adan_y_eva.cromosomas:
            crom.fitness = self.cmakespan(self.datos, crom.secuencia)

        #adan_y_eva.mostrar()
        self.poblacion_inicial = copy.deepcopy(adan_y_eva)
        #self.padres = Poblacion(tamano_poblacion / 2)
        #self.hijos = Poblacion(tamano_poblacion)
        #self.hijos_mutados = Poblacion(tamano_poblacion)
        while self.iteracion < self.max_iterations:
            self.evolucionar(metodo_crossover, metodo_mutacion)
            self.iteracion += 1
        self.fit_prom = (sum(self.mejores_fitness) /
            float(len(self.mejores_fitness)))
        self.tiempo_ejecucion = time.time() - self.tiempo_inicial

    def grabar_solucion(self):
        # Mejor costo
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}\t".format(self.best_makespan))
            text_file.write("{0:.2f}\t".format(self.fit_prom))
            text_file.write("{0:.2f}\t".format(self.best_makespan_time))
            text_file.write("{0:.2f}\t".format(self.tiempo_ejecucion))
            text_file.write("{}\t".format(self.best_iteration))
            text_file.write("{}\n".format(self.max_iterations))

    def resolverTodos(self, cant_ejecuciones, iterations=500):
        with open("Resultados.txt", "a") as text_file:
            text_file.write("\n{}".format("=============== INICIO DE "))
            text_file.write("{}".format(sys.argv[1]))
            text_file.write("{}\n".format(" ==============="))
        #PMX e INVERTION
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}\n".format("***** PMX e INVERTION *****"))
        print("***** PMX e INVERTION *****")
        for i in range(cant_ejecuciones):
            self.resolver(1, 1, iterations)
            porc = (i / float(cant_ejecuciones)) * 100
            print ("Fase 1: %.2f %% completado" % porc)
            rest = ((self.tiempo_ejecucion * (cant_ejecuciones - i) +
                self.tiempo_ejecucion * cant_ejecuciones * 3) / 60)
            print("Tiempo estimado restante total: %.2f minutos" % rest)
            self.grabar_solucion()
            self = Problema()

        #PMX y DISPLACEMENT
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}\n".format("***** PMX y DISPLACEMENT *****"))
        print("***** PMX y DISPLACEMENT *****")
        for i in range(cant_ejecuciones):
            self.resolver(1, 0, iterations)
            porc = (i / float(cant_ejecuciones)) * 100
            print ("Fase 2: %.2f %% completado" % porc)
            rest = ((self.tiempo_ejecucion * (cant_ejecuciones - i) +
                self.tiempo_ejecucion * cant_ejecuciones * 2) / 60)
            print("Tiempo estimado restante total: %.2f minutos" % rest)
            self.grabar_solucion()
            self = Problema()
        #CX e INVERTION
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}\n".format("***** CX e INVERTION *****"))
        print("***** CX e INVERTION *****")
        for i in range(cant_ejecuciones):
            self.resolver(0, 1, iterations)
            porc = (i / float(cant_ejecuciones)) * 100
            print ("Fase 3: %.2f %% completado" % porc)
            rest = ((self.tiempo_ejecucion * (cant_ejecuciones - i) +
                self.tiempo_ejecucion * cant_ejecuciones) / 60)
            print("Tiempo estimado restante total: %.2f minutos" % rest)
            self.grabar_solucion()
            self = Problema()
        #CX y DISPLACEMENT
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}\n".format("***** CX y DISPLACEMENT *****"))
        print("***** CX y DISPLACEMENT *****")
        for i in range(cant_ejecuciones):
            self.resolver(0, 0, iterations)
            porc = (i / float(cant_ejecuciones)) * 100
            print ("Fase 4: %.2f %% completado" % porc)
            rest = ((self.tiempo_ejecucion * (cant_ejecuciones - i)) / 60)
            print("Tiempo estimado restante total: %.2f minutos" % rest)
            self.grabar_solucion()
            self = Problema()
        with open("Resultados.txt", "a") as text_file:
            text_file.write("\n{}".format("=============== FIN DE "))
            text_file.write("{}".format(sys.argv[1]))
            text_file.write("{}\n".format(" ==============="))
        print("\a")

    def resolverUno(self, cross, mut, iterations=500):
        print("Calculando...")
        self.resolver(cross, mut, iterations)
        self.grabar_solucion()

    def resolverXVeces(self, cross, mut, cant_ejecuciones, iterations=500):
        with open("Resultados.txt", "a") as text_file:
            text_file.write("{}".format("***** "))
            if(cross == 1):
                text_file.write("{}".format("PMX & "))
            else:
                text_file.write("{}".format("CX & "))
            if(mut == 1):
                text_file.write("{}".format("INVERTION "))
            else:
                text_file.write("{}".format("DISPLACEMENT "))
            text_file.write("{}\n".format(" *****"))
        for i in range(cant_ejecuciones):
            self.resolver(cross, mut, iterations)
            porc = (i / float(cant_ejecuciones)) * 100
            print ("%.2f %% completado" % porc)
            rest = ((self.tiempo_ejecucion * (cant_ejecuciones - i) / 60))
            print("Tiempo estimado restante total: %.2f minutos" % rest)
            self.grabar_solucion()
            self = Problema()
        print("\a")

if __name__ == "__main__":
    p = Problema()
    p.resolverTodos(30, 500)
    #p.resolverUno(1, 1)
    #p.resolverXVeces(1, 1, 4)
    p.mostrar_solucion()