import glfw
import numpy as np
import grafica.transformations as tr
import random as rd

class Player():
    # Clase que contiene al modelo del player
    def __init__(self, size, p):
        self.pos = [0,-0.65] # Posicion en el escenario
        self.vel = [0.75,0.75] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo 
        self.radio = size*0.5 # distancia para realizar los calculos de colision
        self.p = p # Probabilidad de transformarse
        self.human = True # Variable de estado, humano o zombie
        self.infected = False # Variable de estado, contagiado o no
        self.inf_time = glfw.get_time() # Tiempo en que fue infectado

    def set_model(self, new_model):
        # Se obtiene una referencia a un nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def update(self, delta, tex_pipeline, tex_green_pipeline, googles, time, move):
        # Se actualiza la posicion del jugador

        # Si detecta la tecla [D] presionada y no se ha salido de la pantalla se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] < (1 - self.size/2):
            self.pos[0] += self.vel[0] * delta
        # Si detecta la tecla [A] presionada y no se ha salido de la pantalla se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] > -(1 - self.size/2):
            self.pos[0] -= self.vel[0] * delta
        # Si detecta la tecla [W] presionada y esta en la mitad inferior de la pantalla se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] < 0:
            self.pos[1] += self.vel[1] * delta
            self.controller.distance += self.vel[1] * delta
        # Si detecta la tecla [S] presionada y no se ha salido de la pantalla se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] > (-1 + self.size/2):
            self.pos[1] -= self.vel[1] * delta
            self.controller.distance -= self.vel[1] * delta

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        # Se dibuja con uno u otro shader dependiendo de su estado de infeccion y si se usan los lentes
        if self.infected and googles:
            self.model.curr_pipeline = tex_green_pipeline
        elif not googles:
            self.model.curr_pipeline = tex_pipeline

        # Actualiza el tono de verde que tendra siendo infectado
        self.green(time)

    def collision(self, colision_list):
        # Retorna todas las entidades dentro de collision_list con las que colisiona
        collided_with = []
        # Se recorren las entidades
        for obj in colision_list:
            # si la distancia al objeto es menor que la suma de los radios ha ocurrido en la colision
            if obj == self:
                continue
            elif (self.radio+obj.radio)**2 > ((self.pos[0]- obj.pos[0])**2 + (self.pos[1]-obj.pos[1])**2):
                collided_with += [obj]
        return collided_with

    def changeDirection(self):
        # Metodo vacio, pues se llama changeDirection de todas las entidades, pero player no lo necesita
        pass

    def changeState(self):
        # Se genera un numero al azar, y si es menor a p, se transforma en zombie si ya estaba infectado
        if self.infected == True:
            chance = rd.randint(0, 100)
            if chance < self.p * 100:
                self.human = False

    def green(self, time):
        # Controla el tono de verde que tendr al estar infectado
        self.model.green = min(1, self.p + (time - self.inf_time)*0.05)

class Zombie:
    def __init__(self, size, pos, vel):
        self.pos = pos # Posicion
        self.vel = vel # Velocidad maxima
        self.model = None # Nodo de grafo de escena asociado
        self.size = size # Tamaño del modelo
        self.radio = size*0.3 # Radio de colision
        self.direction = rd.randint(0,100) * 0.01 # Velocidad vertical inicial
        self.infected = True # Variable de estado, infectado o no
        self.human = False # Variable de estado, humano o zombie
        self.coin = rd.randint(0,1) # Se mueve a la izquierda o la derecha

    def setModel(self, newModel):
        # Se obtiene una referencia a un nodo
        self.model = newModel

    def update(self, delta, tex_pipeline, tex_green_pipeline, googles, time, move):
        # Se actualiza la posicion del zombie
        y_dir = self.direction
        vel = self.vel * delta

        x_dir = (1-self.direction) * 0.2
        if self.coin:
            x_dir *= -1

        if not move:
            self.pos[0] += vel * x_dir
            self.pos[1] += vel * y_dir 

        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])
        
        # Se dibuja con el pipeline de textura normal, no se ve verde
        self.model.curr_pipeline = tex_pipeline
    
    def changeDirection(self):
        # Cambia su velocidad y direccion a una al azar
        self.direction = rd.randint(0,100) * 0.01
        self.coin = rd.randint(0,1)

    def changeState(self):
        # Su estado no cambia
        return
    
    def collision(self, colision_list):
        # No le ocurre nada a zombie al colisionar con otras entidades
        return []

class Human:
    def __init__(self, size, pos, vel, p):
        self.pos = pos # Posicion
        self.vel = vel # Velocidad maxima
        self.model = None # Nodo de grafo de escena asociado
        self.size = size # Tamaño del modelo
        self.radio = size*0.5 # Radio de colision
        self.direction = rd.randint(0,100) * 0.01 # Velocidad inicial
        self.p = p # Probabilidad de transformarse en zombie si esta contagiado
        self.coin = rd.randint(0,1) # Se mueve a la derecha o izquierda
        self.coin_infection = rd.randint(0, 1) # 0.5 de probabilidad de estar infectado al aparecer
        self.infected = False # Variable de estado, infectado o no
        if self.coin_infection:
            self.infected = True
        self.human = True # Variable de estado, zombie o humano
        self.inf_time = glfw.get_time() # Tiempo de infeccion

    def setModel(self, newModel):
        # Se asocia un nuevo nodo de grafo de escena
        self.model = newModel

    def update(self, delta, tex_pipeline, tex_green_pipeline, googles, time, move):
        # Se actualiza su posicion
        y_dir = self.direction
        vel = self.vel * delta

        x_dir = (1-self.direction) * 0.2
        if self.coin:
            x_dir *= -1

        if not move:
            self.pos[0] += vel * x_dir
            self.pos[1] += vel * y_dir 

        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        # Se dibuja con uno u otro shader dependiendo de su estado de infeccion y si se usan los lentes
        if self.infected and googles:
            self.model.curr_pipeline = tex_green_pipeline
        elif not googles:
            self.model.curr_pipeline = tex_pipeline

        # Se controla el tono de verde que tendra si esta infectado
        self.green(time)
    
    def changeDirection(self):
        # Cambio de velocidad
        self.direction = rd.randint(0,100) * 0.01

    def changeState(self):
        # Si se obtiene al azar un numero menor a p y esta infectado, se transforma en zombie
        if self.infected == True:
            chance = rd.randint(0, 100)
            if chance < self.p * 100:
                self.human = False
    
    def collision(self, colision_list):
        # Retorna una lista con entidades de collision_list con las que colisiona

        collided_with = []
        for obj in colision_list:
            # si la distancia al objeto es menor que la suma de los radios ha ocurrido en la colision
            if obj == self:
                continue
            elif (self.radio+obj.radio)**2 > ((self.pos[0]- obj.pos[0])**2 + (self.pos[1]-obj.pos[1])**2):
                collided_with += [obj]
        return collided_with

    def green(self, time):
        # Se regula el tono de verde que tendra si esta infectado
        self.model.green = min(1, self.p + (time - self.inf_time)*0.05)

class Store:
    def __init__(self, pos):
        self.pos = pos # Posicion
        self.radio = 0.4 # Radio de colision
        self.model = None # Nodo de grafo de escena asociado

    def setModel(self, newModel):
        # Se asocia un nuevo nodo de un grafo de escena
        self.model = newModel

    def update(self):
        # Se actualiza su posicion
        self.model.transform = tr.translate(self.pos[0], self.pos[1], 0)
    
    def collisionPlayer(self, player):
        # Retorna true si colisiona con el jugador
        if (self.radio+player.radio)**2 > ((self.pos[0]- player.pos[0])**2 + (self.pos[1]-player.pos[1])**2):
            return True
        return False
            