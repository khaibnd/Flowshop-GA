# -*- coding: utf-8 -*-

import random
import copy


class Poblacion(object):
    """docstring for Poblacion"""
    cromosomas = []

    def __init__(self, tamano=128):
        super(Poblacion, self).__init__()
        #self.cromosomas = cromosomas
        self.tamano = tamano

    def generar(self, tamano_cromosoma):
        """Genera Poblacion Inicial"""
        for i in range(self.tamano):
            cromosoma_actual = Cromosoma(tamano_cromosoma)
            cromosoma_actual.generar_secuencia()
            #cromosoma_actual.evaluar_fitness()
            self.cromosomas.append(cromosoma_actual)

    def mostrar(self):
        for c in self.cromosomas:
            print (c.secuencia)
            print (c.fitness)
            print('----------------------')


class Cromosoma(object):
    fitness = 0
    secuencia = []
    tamano = 0

    def __init__(self, tamano):
        self.tamano = tamano

    def generar_secuencia(self):
        self.secuencia = [i for i in range(0, self.tamano)]
        random.shuffle(self.secuencia)


class Selection(object):
    def __init__(self):
        pass


class DBT(Selection):
    """docstring for Deterministic Binary Tournament
        Dados dos cromosomas devuelve el de mejor fitness"""
    def __init__(self):
        super(DBT, self).__init__()

    def seleccionar(self, cromosoma1, cromosoma2):
        #Tomo el mejor fitness
        rta = None
        if cromosoma1.fitness >= cromosoma2.fitness:
            rta = cromosoma1
        else:
            rta = cromosoma2
        return rta


class Crossover(object):
    """docstring for Crossover"""
    def __init__(self):
        super(Crossover, self).__init__()


class PMXa(Crossover):
    """docstring for PMXa"""
    def __init__(self):
        super(PMXa, self).__init__()

    def cruzar(self, cromosoma1, cromosoma2):
        lista_respuesta = []
        h1 = Cromosoma(cromosoma1.tamano)
        h2 = Cromosoma(cromosoma2.tamano)
        h1.secuencia = copy.deepcopy(cromosoma1.secuencia)
        h2.secuencia = copy.deepcopy(cromosoma2.secuencia)
        #Genero dos posiciones al azar teniendo en cuenta el tamano del cromo
        pos1 = random.randint(0, cromosoma1.tamano)
        pos2 = random.randint(0, cromosoma2.tamano)
        if pos1 <= pos2:
            pos_inicial = pos1
            pos_final = pos2
        else:
            pos_inicial = pos2
            pos_final = pos1
        i = 0
        for i in range(pos_inicial, pos_final):
            replace = [h1.secuencia[i], h2.secuencia[i]]
            j = 0
            for j, el in enumerate(h1.secuencia):
                if el in replace:
                    if el == replace[0]:
                        h1.secuencia[j] = replace[1]
                    else:
                        h1.secuencia[j] = replace[0]
            j = 0
            for j, el in enumerate(h2.secuencia):
                if el in replace:
                    if el == replace[0]:
                        h2.secuencia[j] = replace[1]
                    else:
                        h2.secuencia[j] = replace[0]
        lista_respuesta.append(h1)
        lista_respuesta.append(h2)
        return lista_respuesta


class PMX(Crossover):
    """docstring for PMX"""
    def __init__(self):
        super(PMX, self).__init__()

    def eliminar_transitividad(self, lista):
        cambio = False
        seguir = True
        while seguir:
            for i in lista:
                for j in lista:
                    if j[0] == i[1]:
                        i[1] = j[1]
                        lista.remove(j)
                        cambio = True
            if cambio:
                seguir = True
                cambio = False
            else:
                seguir = False

    def mapear(self, protochild, lista_m, pos_inicial, pos_final):
        for i in range(len(protochild)):
            if (i < pos_inicial) or (i > pos_final):
                for j in range(len(lista_m)):
                    if protochild[i] in lista_m[j]:
                        if protochild[i] == lista_m[j][0]:
                            protochild[i] = lista_m[j][1]
                        else:
                            protochild[i] = lista_m[j][0]
        return protochild

    def cruzar(self, cromosoma1, cromosoma2):
        lista_respuesta = []
        padre1_secuencia = cromosoma1.secuencia
        padre2_secuencia = cromosoma2.secuencia
        #Genero dos posiciones al azar teniendo en cuenta el tamano del cromo
        pos1 = random.randint(0, cromosoma1.tamano)
        pos2 = random.randint(0, cromosoma1.tamano)
        if pos1 >= pos2:
            pos_inicial = pos2
            pos_final = pos1
        else:
            pos_inicial = pos1
            pos_final = pos2
        #Intercambio substrings entre los padres
        #---------------------------------------
        #1) Armo Substrings
        substring1 = padre1_secuencia[pos_inicial:pos_final + 1]
        substring2 = padre2_secuencia[pos_inicial:pos_final + 1]
        #2)Armo Protochilds
        padre1_secuencia[pos_inicial:pos_final + 1] = substring2
        padre2_secuencia[pos_inicial:pos_final + 1] = substring1
        #3)Armo Lista de Mapeo con los substrings
        lista_mapeo = []
        for i in range(len(substring1)):
            #print("Subs 1: ", substring1 )
            #print("Subs 2: ", substring2 )
            lista_mapeo.append([substring1[i], substring2[i]])
            #print("Lista Mapeo: ", lista_mapeo)
            #lista_mapeo = list(flatten(lista_mapeo))
        #4)Elimino Transitividad de la Lista de Mapeo
        self.eliminar_transitividad(lista_mapeo)
        #5)Reemplazo Final con Lista De Mapeo
        sec_hijo1 = self.mapear(padre1_secuencia, lista_mapeo, pos_inicial,
        pos_final)
        sec_hijo2 = self.mapear(padre2_secuencia, lista_mapeo, pos_inicial,
        pos_final)
        #6) Creo 2 hijos y les asigno la secuencia
        h1 = Cromosoma(cromosoma1.tamano)
        h2 = Cromosoma(cromosoma1.tamano)
        h1.secuencia = sec_hijo1
        h2.secuencia = sec_hijo2
        # QUE HACEMOS CON EL FITNESS ACÁ ????
        lista_respuesta.append(h1)
        lista_respuesta.append(h2)
        return lista_respuesta


class CX(Crossover):
    """docstring for CX"""
    def __init__(self):
        super(CX, self).__init__()

    def esta_en_lista(self, elemento, lista):
        """Devuelve verdadero si un elemento pertenece a una lista de listas"""
        rta = False
        for sublista in lista:
            if elemento in sublista:
                rta = True
        return rta

    def armar_ciclo(self, pos, secuencia1, secuencia2):
        """Funcion que encuentra el ciclo (en caso de existir )para
        el elemnto de la posicion recibida y agrega ese ciclo a la lista
        de ciclos"""

        # Setea el valor inicial para el corte
        inicio_ciclo = secuencia1[pos]
        ciclo = []
        i = pos
        seguir = True
        # Recorre la secuencia1
        while seguir:
            valor2 = secuencia2[i]
            ciclo.append(i)
            for j in range(len(secuencia1)):
                if secuencia1[j] == valor2:
                    i = j
            if secuencia2[i] == inicio_ciclo:
                ciclo.append(i)
                seguir = False
        return ciclo

    def generar_hijos(self, lista_ciclos, padre1, padre2):
        lista_hijos = []
        #print ("lista ciclos" + str(lista_ciclos))
        if len(lista_ciclos) == 1:
            h1 = Cromosoma(len(padre1))
            h2 = Cromosoma(len(padre1))
            h1.secuencia = copy.deepcopy(padre1)
            h2.secuencia = copy.deepcopy(padre2)
            lista_hijos.append(h1)
            lista_hijos.append(h2)
        else:
            ciclo_actual = lista_ciclos[0]
            hijo1 = Cromosoma(len(padre1))
            hijo2 = Cromosoma(len(padre1))
            hijo1.secuencia = []
            hijo2.secuencia = []
            # Genero offspring 1
            for i, el in enumerate(padre1):
                if i in ciclo_actual:
                    hijo1.secuencia.append(padre1[i])
                else:
                    hijo1.secuencia.append(padre2[i])
            # Genero offspring 2
            for i, el in enumerate(padre2):
                if i in ciclo_actual:
                    hijo2.secuencia.append(padre2[i])
                else:
                    hijo2.secuencia.append(padre1[i])

            lista_hijos.append(hijo1)
            lista_hijos.append(hijo2)
        #print "lista hijos: " + str(lista_hijos)
        return lista_hijos

    def buscar_ciclos(self, secuencia1, secuencia2):
        """ Esta funcion arma una lista de listas donde cada sublista
        esta formada, por las posiciones de los elementos que forman
        parte de un ciclo.De esta manera obtendremos:
        [[p1c1,p2c1,pnc1],[p1c2,p2c2,pnc2],....,[p1cn,p2cn,pncn]]
        Donde pncn representa la posición n del ciclo n
        """
        lista_ciclos = []
        for i in range(len(secuencia1)):
            # Revisamos que dos elementos en la misma posicion sean !=
            # if secuencia2[i] != secuencia1[i]:
            if not self.esta_en_lista(i, lista_ciclos):
                c = self.armar_ciclo(i, secuencia1, secuencia2)
                lista_ciclos.append(c)
        return lista_ciclos

    def cruzar(self, cromosoma1, cromosoma2):
        lista_rta = []
        #Reviso que los padres sean diferentes
        # if cromosoma1.secuencia != cromosoma2.secuencia:
            #Busco ciclos entre los dos padres
        lista_ciclos = self.buscar_ciclos(cromosoma1.secuencia,
        cromosoma2.secuencia)
        lista_rta = self.generar_hijos(lista_ciclos, cromosoma1.secuencia,
        cromosoma2.secuencia)
        # Si los padres son iguales los hijos iguales
        """
        else:
            h1 = Cromosoma(cromosoma1.tamano)
            h2 = Cromosoma(cromosoma1.tamano)
            h1.secuencia = cromosoma1.secuencia
            h2.secuencia = cromosoma1.secuencia
            lista_rta.append(h1)
            lista_rta.append(h2)
        """
        return lista_rta


class Mutation(object):
    """docstring for Mutation"""
    def __init__(self):
        pass

    def mutar():
        pass


class Invertion(Mutation):
    """This is a very simple mutation operator.
    Select two random points (i.e.; positions 2 through 5)
    and reverse the genes between them.

    0 1 2 3 4 5 6 7

    becomes

    0 4 3 2 1 5 6 7

    """
    def __init__(self):
        super(Invertion, self).__init__()

    def mutar(self, cromosoma):
        pos1 = random.randint(0, cromosoma.tamano - 1)
        pos2 = random.randint(0, cromosoma.tamano - 1)
        if pos1 < pos2:
            revlist = cromosoma.secuencia[pos1:pos2 + 1]
            revlist = revlist[::-1]
            cromosoma.secuencia[pos1:pos2 + 1] = revlist
        else:
            revlist = cromosoma.secuencia[pos2:pos1 + 1]
            revlist = revlist[::-1]
            cromosoma.secuencia[pos2:pos1 + 1] = revlist
        return cromosoma


class Displacement(Mutation):
    """Select two random points (i.e.; positions 4 and 6),
    grab the genes between them as a group, then reinsert
    the group at a random position displaced from the original.

    0 1 2 3 4 5 6 7

    becomes

    0 3 4 5 1 2 6 7
    """
    def __init__(self):
        super(Displacement, self).__init__()

    def mutar(self, cromosoma):
        pos1 = random.randint(0, cromosoma.tamano - 1)
        pos2 = random.randint(0, cromosoma.tamano - 1)
        if pos1 < pos2:
            group = cromosoma.secuencia[pos1:pos2 + 1]
            del(cromosoma.secuencia[pos1:pos2 + 1])
            randpos = random.randint(0, len(cromosoma.secuencia))
            cromosoma.secuencia.insert(randpos, group)
        if pos2 < pos1:
            group = cromosoma.secuencia[pos2:pos1 + 1]
            del(cromosoma.secuencia[pos2:pos1 + 1])
            randpos = random.randint(0, len(cromosoma.secuencia))
            cromosoma.secuencia.insert(randpos, group)
        cromosoma.secuencia = list(flatten(cromosoma.secuencia))
        return cromosoma


def flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x


class Reemplazo(object):

    def __init__(self):
        super(Reemplazo, self).__init__()

    def reemplazar(self, poblacion1, poblacion2):
        #Junto Listas
        poblacion_rta = poblacion1 + poblacion2
        # Ordeno por fitness de manera descendente
        poblacion_rta.sort(key=lambda x: x.fitness, reverse=False)
        # Elimino la parte que no me interesa quedandome con los mejores
        del poblacion_rta[len(poblacion_rta) // 2:]

        return poblacion_rta

    def reemplazarwe(self, poblacion1, poblacion2, tamano_poblacion):
        #Junto Listas
        poblacion_rta = [0] * tamano_poblacion
        poblacion = poblacion1 + poblacion2
        # Ordeno por fitness de manera descendente
        poblacion.sort(key=lambda x: x.fitness, reverse=False)
        poblacion_rta[0] = poblacion[0]
        for i in range(1, tamano_poblacion):
            c1 = random.choice(poblacion1)
            c2 = random.choice(poblacion2)
            if c1.fitness >= c2.fitness:
                poblacion_rta[i] = c1
            else:
                poblacion_rta[i] = c2
        return poblacion_rta