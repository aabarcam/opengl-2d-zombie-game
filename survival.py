import glfw
import random as rd
import OpenGL.GL.shaders
import numpy as np
import math
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import sys, os.path

import custom_modules.custom_shaders as csh
from shapes import *
from models import *

SIZE_IN_BYTES = 4

class Controller:
    def __init__(self):
        self.googles_toggle = False
        self.distance = 0
        self.end = False
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False

controller = Controller()

def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se activan / desactivan los lentes
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.googles_toggle = not controller.googles_toggle

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)

# Funcion que mueve el nodo name de la escena scene hacia abajo
def moveSceneDown(scene, name, pos, vel, delta, fixed_pos):
    x = csg.findNode(scene, name)
    newpos = ((pos - vel*delta)%-4) + fixed_pos
    if newpos < -2:
        newpos += 4
    x.transform = tr.translate(0, newpos, 0)
    return newpos - fixed_pos


# Función que crea N zombies
def createNZombies(gpuZombie, entModList, entList, vel, N, x_range):
    for i in range(N):
        zombieNode = csg.CustomSceneGraphNode("zombie"+str(i))
        zombieNode.childs = [gpuZombie]
        x = rd.randint(-x_range * 100, x_range * 100) * 0.01
        y = -1
        up_or_down = rd.randint(0, 1)
        new_vel = rd.randint(0, vel*100)*0.01

        if up_or_down:
            y *= -1
            new_vel *= -1

        while ((player.pos[0]-x)**2 + (player.pos[1]-y)**2) < 0.5:
            x = rd.randint(-x_range * 100, x_range * 100) * 0.01

        entModList += [zombieNode]
        zombie = Zombie(sprite_size, [x, y], new_vel)
        zombie.setModel(zombieNode)

        entList += [zombie]

# Funcion que crea N humanos
def createNHumans(gpuHuman, entModList, entList, N, vel, x_range, p):
    for i in range(N):
        humanNode = csg.CustomSceneGraphNode("human"+str(i))
        humanNode.curr_pipeline = tex_pipeline
        humanNode.childs = [gpuHuman]
        x = rd.randint(-x_range * 100, x_range * 100) * 0.01
        y = -1
        up_or_down = rd.randint(0, 1)
        new_vel = rd.randint(0, vel*100)*0.01

        if up_or_down:
            y *= -1
            new_vel *= -1

        while ((player.pos[0]-x)**2 + (player.pos[1]-y)**2) < 0.5:
            x = rd.randint(-x_range * 100, x_range * 100) * 0.01
        entModList += [humanNode]

        human = Human(sprite_size, [x, y], new_vel, p)
        human.setModel(humanNode)

        entList += [human]

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 800
    height = 800
    title = "Zombies"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()
    # Pipeline personalizado para fondo estático
    statictex_pipeline = csh.StaticTransformShaderProgram()
    # Pipeline personalizado para lentes detectores de infeccion
    tex_green_pipeline = csh.SimpleGreenTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
  
    # Variables
    flag = True
    flag_2 = True
    cd = True
    cd_dir = True
    Z = int(sys.argv[1])
    H = int(sys.argv[2])
    T = int(sys.argv[3])
    P = float(sys.argv[4])
    dist_to_store = 10

    treeN = 12

    # Posiciones de escenas
    dec_current_pos_1 = 0
    dec_current_pos_2 = 0
    dec_pos_1 = 0
    dec_pos_2 = 2

    scene_current_pos_1 = 0
    scene_current_pos_2 = 0
    scene_pos_1 = 0
    scene_pos_2 = 2

    game_over_pos = 1.5
    victory_pos = 1.5

    # Atributos entidades
    entities_current_pos = 0
    entities_pos = 0
    zombie_vel = 1
    human_vel = 1

    # Tamaño entidades
    sprite_size = 0.2


    # Creacion de escenas
    decorations = createDecorations(pipeline, statictex_pipeline, 0.6, [-1,1], treeN, 1)
    decorations_2 = createDecorations(pipeline, statictex_pipeline, 0.6, [-1,1], treeN, 2)
    decorations_2.transform = tr.translate(0, 2, 0)

    decoration_scene = csg.CustomSceneGraphNode("decoration_node")
    decoration_scene.childs = [decorations, decorations_2]

    scene = createBackground(pipeline, 0)
    scene_2 = createBackground(pipeline, 1)
    scene_2.transform = tr.translate(0, 2, 0)

    full_scene = sg.SceneGraphNode("full_scene")
    full_scene.childs = [scene, scene_2]

    # Creacion jugador
    player = Player(sprite_size, P)
    
    playerModel = createPlayerModel(tex_pipeline)

    player.set_model(playerModel)
    player.set_controller(controller)

    entityList = [player]
    entityModelsList = [playerModel]

    # Creacion zombies
    gpuZombie = createZombieModel(tex_pipeline)
    
    # Creacion humanos
    gpuHuman = createHumanModel(tex_pipeline)

    # Creacion tienda
    store_scene = createStoreModel(pipeline)
    store = Store([-0.8, 1.5])

    store.setModel(store_scene)

    fullStoreNode = csg.CustomSceneGraphNode("fullStore")
    fullStoreNode.childs = [store_scene]

    # Creacion texto victoria y derrota
    textScene = createText(tex_pipeline)
    
    gameOverScene = sg.findNode(textScene, "gameOver")
    gameOverScene.transform = tr.translate(game_over_pos, 0, 0)
    victoryScene = sg.findNode(textScene, "victory")


    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    ### Test

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Measuring performance
        glfw.set_window_title(window, title)
        # Using GLFW to check for input events
        glfw.poll_events()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Filling or not the shapes depending on the controller state

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Intervalo T
        interval = t1%T
        if interval < T/2 and flag:
            cd = True
            flag = False
        if interval > T/2 and not flag:
            flag = True

        # Intervalo cambio de direcciones de zombies / humanos
        dir_interval = t1%2
        if dir_interval < 1 and flag_2:
            cd_dir = True
            flag_2 = False
        if dir_interval > 1 and not flag_2:
            flag_2 = True

        # Lista de entidades aun dentro de la pantalla
        interationEntities = []
        iterationModels = []
        for entity in entityList:
            if entity.pos[0] > -1.2 and entity.pos[0] < 1.2 and entity.pos[1] > -1.2 and entity.pos[1] < 1.2:
                interationEntities += [entity]
                iterationModels += [entity.model]

        # Se dibujan los grafos de escena principales
        glUseProgram(pipeline.shaderProgram)

        sg.drawSceneGraphNode(full_scene, pipeline, "transform")

        csg.drawCustomSceneGraphNode(decoration_scene, pipeline, "transform")

        # Cuando el jugador avanza luego de estar a cierta altura, se mueve la escena en lugar del jugador
        if controller.is_w_pressed and player.pos[1] >= -0.05 and player.human == True:
            controller.distance += player.vel[1] * delta
            if controller.distance > dist_to_store:
                store.pos[1] -= player.vel[1] * delta
            dec_current_pos_1 = moveSceneDown(decoration_scene, "decorations1", dec_current_pos_1, player.vel[0], delta, dec_pos_1)
            dec_current_pos_2 = moveSceneDown(decoration_scene, "decorations2", dec_current_pos_2, player.vel[0], delta, dec_pos_2)
            scene_current_pos_1 = moveSceneDown(full_scene, "final0", scene_current_pos_1, player.vel[0], delta, scene_pos_1)
            scene_current_pos_2 = moveSceneDown(full_scene, "final1", scene_current_pos_2, player.vel[0], delta, scene_pos_2)
            for k in range(len(interationEntities)-1):
                interationEntities[k+1].pos[1] -= player.vel[1] * delta
      
        # Se actualizan todas las entidades activas
        for i in range(len(interationEntities)):
            interationEntities[i].update(delta, tex_pipeline, tex_green_pipeline, controller.googles_toggle, t1, controller.end)
            if not interationEntities[i].human and type(interationEntities[i]) != Zombie:
                newZombieNode = csg.CustomSceneGraphNode("zombie"+str(i))
                newZombieNode.childs = [gpuZombie]
                newPos = interationEntities[i].pos
                newZombieNode.transform = interationEntities[i].model.transform

                newZombie = Zombie(sprite_size, newPos, zombie_vel)
                newZombie.setModel(newZombieNode)

                interationEntities[i] = newZombie
                iterationModels[i] = newZombieNode
            if cd and not controller.end: # Esto ocurre cada T segundos
                interationEntities[i].changeState()
                    
            if cd_dir:
                interationEntities[i].changeDirection()

        # Se dibujan todas las entidades activas
        entityModelsNode = csg.CustomSceneGraphNode("entities")
        entityModelsNode.childs = iterationModels
        csg.drawCustomSceneGraphNode(entityModelsNode, tex_pipeline, "transform")

        # Se crean Z zombies y H humanos cada T segundos
        if cd and not controller.end: # Esto ocurre cada T segundos
            createNHumans(gpuHuman, iterationModels, interationEntities, H, human_vel, 1, P)
            createNZombies(gpuZombie, iterationModels, interationEntities, zombie_vel, Z, 1)
        
        # Se resetean las variables que indican cuando han pasado T segundos
        cd = False
        cd_dir = False

        # Si el jugador ha avanzado mas que la cantidad dist_to_store, se dibuja la tienda
        # controller.distance es controlado por el objeto player
        if controller.distance > dist_to_store:
            glUseProgram(pipeline.shaderProgram)
            csg.drawCustomSceneGraphNode(fullStoreNode, pipeline, "transform")
            store.update()

        # Se revisan las colisiones de todas las entidades activas
        for entity in interationEntities:
            for collisions in entity.collision(interationEntities):
                # Si entity colisiona con un zombie, se transforma en uno
                if not collisions.human:
                    entity.human = False
                # Si entity colisiona con un humano infectado, se infecta
                if collisions.infected and not entity.infected:
                    entity.infected = True
                    entity.inf_time = glfw.get_time()

        # Si hay una colision entre la tienda y el jugador, se termina el juego
        if store.collisionPlayer(player) and not controller.end:
            controller.end = True

        # Se crea una espiral mediante modificaciones de vertices segun el tiempo y transformaciones en CPU
        spiral = createSpiral(50, t1)
        for m in range(0, len(spiral.vertices), 6):
            current_vert = [spiral.vertices[m], spiral.vertices[m+1],spiral.vertices[m+2], 1]
            new_vert = tr.matmul([tr.scale(0.02, 0.02, 1), current_vert])
            spiral.vertices[m] = new_vert[0]
            spiral.vertices[m+1] = new_vert[1]
            spiral.vertices[m+2] = new_vert[2]
        GPUspiral = es.GPUShape().initBuffers()
        pipeline.setupVAO(GPUspiral)
        GPUspiral.fillBuffers(spiral.vertices, spiral.indices, GL_STREAM_DRAW)

        # Si el jugador esta infectado, aparece una espiral rotando encima de su modelo y se distoricona la vision
        if player.infected:
            for entity in entityList:
                entity.pos[0] += math.cos(t1) * delta * 0.2 * entity.pos[1]
            full_scene.transform = tr.shearing(math.cos(t1)*0.2, 0, 0, 0, 0, 0)
            decoration_scene.transform = tr.shearing(math.cos(t1)*0.2, 0, 0, 0, 0, 0)
            fullStoreNode.transform = tr.shearing(math.cos(t1)*0.2, 0, 0, 0, 0, 0)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([tr.translate(player.pos[0],player.pos[1] + 0.1,0), tr.rotationZ(t1)]))
            pipeline.drawCall(GPUspiral, GL_LINE_STRIP)

        # Se quitan de la lista de entidades aquellas que salieron de la pantalla esta iteracion
        entityList = interationEntities
        entityModelsList = iterationModels

        # Si el jugador se transforma en zombie, se acaba el juego y se dibuja la escena de game over
        if not player.human:
            if game_over_pos > 0:
                game_over_pos -= 1.2 * delta
                gameOverScene.transform = tr.translate(game_over_pos, 0, 0)
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(gameOverScene, tex_pipeline, "transform")

        # Si el jugador ha ganado y sigue siendo humano, se acaba el juego y se dibuja la escena de victoria
        if controller.end and player.human:
            if victory_pos > 0:
                victory_pos -= 1.2 * delta
                victoryScene.transform = tr.translate(victory_pos, 0, 0)
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(victoryScene, tex_pipeline, "transform")



        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # Se libera memoria de GPU
    full_scene.clear()
    decoration_scene.clear()
    entityModelsNode.clear()
    victoryScene.clear()
    gameOverScene.clear()
    GPUspiral.clear()
    fullStoreNode.clear()

    glfw.terminate()