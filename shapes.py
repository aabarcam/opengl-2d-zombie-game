import numpy as np
import math
import random as rd
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import sys, os.path

import custom_modules.custom_scenegraph as csg

def getAssetPath(filename):
    """Convenience function to access assets files regardless from where you run the example script."""

    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    parentFolderPath = os.path.dirname(thisFolderPath)
    assetsDirectory = os.path.join(parentFolderPath, "T1/sprites")
    requestedPath = os.path.join(assetsDirectory, filename)
    return requestedPath


def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createColorTriangle(r, g, b):
    # Funcion para crear un triangulo con un color personalizado

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.0,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)

def createTriangle():
    # Se crea un triangulo solo con informacion de posicion de sus vertices
    vertices = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0]

    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)

def createQuad():
    # Se crea un quad solo con informacion de posicion de sus vertices
    vertices = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.5,  0.5, 0.0,
        -0.5,  0.5, 0.0]

    indices = [
        0, 1, 2,
        2, 3, 0]

    return bs.Shape(vertices, indices)

def createSpiralVert(N, r, g, b, mult):
    # Se crean los vertices de una espiral con colores personalizados
    vertices = []

    dtheta = 2 * math.pi / N

    for i in range(N * 3):
        theta = i * dtheta
        
        # La posicion de los vertices oscila dependiendo de mult, se normaliza con N para mantener el tamaño contante a distintos N
        vertices += [1/N * i * math.cos(theta) * abs(math.cos(mult)), 1/N * i * math.sin(theta) * abs(math.cos(mult)), 0, r, g, b]
    
    return vertices


def createSpiral(N, mult):
    
    # Se crean los vertices de una espiral con la funcion anterior
    vertices = createSpiralVert(N, 1, 1, 1, mult)
    indices = []

    for i in range(0, N * 3, 2):
        # Se unen los vertices de dos en dos para modo de dibujo GL_LINE_STRIP
        indices += [i, i+1]

    return bs.Shape(vertices, indices)

def createUmbrellaCircle():
    vertices = []
    indices = []

    dtheta = 2 * math.pi / 8

    for i in range(8):
        # Se crean 8 triangulos
        theta = i * dtheta
        theta_prime = theta + dtheta
        # Los triangulos son blancos y rojos intercaladamente
        mod = (i+1)%2 * 0.9

        # Tres vertices por triangulo
        vertices += [0, 0, 0, 0.9, mod, mod, 
        0.5 * math.cos(theta), 0.5 * math.sin(theta), 0, 0.9, mod, mod,
        0.5 * math.cos(theta_prime), 0.5 * math.sin(theta_prime), 0, 0.9, mod, mod]

        # Se unen de a 3 vertices para modo de dibujo GL_TRIANGLES
        curr = 3 * i
        indices += [curr, curr+1, curr+2]

    return bs.Shape(vertices, indices)

def height(node):
    # Retorna la coordenada y del nodo para usar sort en listas de nodos
    transform = node.transform
    return transform[1][3]

def createBackground(pipeline, i):
    # Se crea el fondo con un grafo de escena de shapes
    greenQuad = bs.createColorQuad(0.0, 0.6, 0.0)
    greyQuad = bs.createColorQuad(0.6, 0.6, 0.6)
    whiteQuad = bs.createColorQuad(255/255, 242/255, 0)


    gpuGrass = createGPUShape(greenQuad, pipeline)
    gpuStreet = createGPUShape(greyQuad, pipeline)
    gpuLine = createGPUShape(whiteQuad, pipeline)


    grassNode = sg.SceneGraphNode("grass")
    grassNode.transform = tr.scale(4, 2, 1)
    grassNode.childs = [gpuGrass]

    streetNode = sg.SceneGraphNode("street")
    streetNode.transform = tr.scale(1, 2, 1)
    streetNode.childs = [gpuStreet]

    lineNode = sg.SceneGraphNode("line")
    lineNode.transform = tr.scale(0.1, 0.25, 1)
    lineNode.childs = [gpuLine]

    trLineNode1 = sg.SceneGraphNode("trline1")
    trLineNode1.transform = tr.identity()
    trLineNode1.childs = [lineNode]

    trLineNode2 = sg.SceneGraphNode("trline2")
    trLineNode2.transform = tr.translate(0, 0.4, 0)
    trLineNode2.childs = [lineNode]

    trLineNode3 = sg.SceneGraphNode("trline3")
    trLineNode3.transform = tr.translate(0, -0.4, 0)
    trLineNode3.childs = [lineNode]

    trLineNode4 = sg.SceneGraphNode("trline4")
    trLineNode4.transform = tr.translate(0, -0.8, 0)
    trLineNode4.childs = [lineNode]

    trLineNode5 = sg.SceneGraphNode("trline5")
    trLineNode5.transform = tr.translate(0, 0.8, 0)
    trLineNode5.childs = [lineNode]

    lineGroupNode = sg.SceneGraphNode("lineGroup")
    lineGroupNode.transform = tr.translate(0, 0, 0)
    lineGroupNode.childs = [trLineNode1, trLineNode2, trLineNode3, trLineNode4, trLineNode5]

    finalNode = sg.SceneGraphNode("final"+str(i))
    finalNode.childs = [grassNode, streetNode, lineGroupNode]

    return finalNode

def createDecorations(pipeline, tex_pipeline, x_range, y_range, n, i_z):
    # Se crean las decoraciones con un grafo de escena que admite shapes y texturas
    triangleShape = createTriangle()
    quadShape = createQuad()
    whiteQuad = bs.createColorQuad(1, 1, 1)
    greyQuad = bs.createColorQuad(0.8,0.8,0.8)
    umbrellaShape = createUmbrellaCircle()

    gpuLeaves = createTextureGPUShape(triangleShape, tex_pipeline, getAssetPath("hojas_arboles.jpg"))
    gpuTrunk = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("tronco.jpeg"))
    gpuWhiteQuad = createGPUShape(whiteQuad, pipeline)
    gpuGreyQuad = createGPUShape(greyQuad, pipeline)
    gpuUmbrella = createGPUShape(umbrellaShape, pipeline)

    leavesNode = csg.CustomSceneGraphNode("hojas")
    leavesNode.transform = tr.translate(0, 0.5, 0)
    leavesNode.childs = [gpuLeaves]

    trunkNode = csg.CustomSceneGraphNode("tronco")
    trunkNode.transform = tr.matmul([tr.translate(0, -0.25, 0), tr.scale(0.3, 0.5, 1)])
    trunkNode.childs = [gpuTrunk]

    scaledTreeNode = csg.CustomSceneGraphNode("arbol_escalado")
    scaledTreeNode.transform = tr.uniformScale(0.3)
    scaledTreeNode.childs = [trunkNode, leavesNode]
    
    treeGroupNode = csg.CustomSceneGraphNode("grupo_arboles")

    # Se crean arboles en posiciones generadas al azar
    for i in range(n):
        x = 100 - x_range * 100
        x_rand = rd.randint(0, x)*0.01
        r_x = x_rand + x_range
        coin = rd.randint(0,1)
        if coin:
            r_x *= -1
        r_y = rd.randint(y_range[0]*100, y_range[1]*100)*0.01
        treeNode = csg.CustomSceneGraphNode("arbol_"+str(i))
        treeNode.transform = tr.translate(r_x, r_y, 0)
        treeNode.childs = [scaledTreeNode]

        treeGroupNode.childs += [treeNode]
    

    treeGroupNode.childs.sort(reverse=True, key=height)

    
    cartBodyNode = csg.CustomSceneGraphNode("ej")
    cartBodyNode.transform = tr.scale(0.3, 0.5, 1)
    cartBodyNode.childs = [gpuWhiteQuad]

    cartInsideNode = csg.CustomSceneGraphNode("inside")
    cartInsideNode.transform = tr.scale(0.2, 0.3, 1)
    cartInsideNode.childs = [gpuGreyQuad]

    umbrellaNode = csg.CustomSceneGraphNode("umbrella")
    umbrellaNode.transform = tr.rotationZ(math.pi/8)
    umbrellaNode.childs = [gpuUmbrella]

    umbrellaScaled = csg.CustomSceneGraphNode("umbrellaS")
    umbrellaScaled.transform = tr.scale(0.3, 0.3, 1)
    umbrellaScaled.childs = [umbrellaNode]

    umbrellaTranslated = csg.CustomSceneGraphNode("umbrellaT")
    umbrellaTranslated.transform = tr.translate(-0.1, 0.1, 0)
    umbrellaTranslated.childs = [umbrellaScaled]

    cartNode = csg.CustomSceneGraphNode("cart")
    cartNode.transform = tr.translate(0.8, -0.5, 0)
    cartNode.childs = [cartBodyNode, cartInsideNode, umbrellaTranslated]

    regularNode = csg.CustomSceneGraphNode("regular")
    regularNode.transform = tr.identity()
    regularNode.childs = [cartNode]
    regularNode.curr_pipeline = pipeline
    
    texNode = csg.CustomSceneGraphNode("tex")
    texNode.childs = [treeGroupNode]
    texNode.curr_pipeline = tex_pipeline
    
    decNode = csg.CustomSceneGraphNode("decorations"+str(i_z))
    decNode.childs = [regularNode, texNode]

    return decNode

def createPlayerModel(tex_pipeline):
    # Se crea el nodo del modelo del jugador
    quadShape = bs.createTextureQuad(1, 1)

    gpuQuad = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("hinata_cut_transparent.png"))

    playerNode = csg.CustomSceneGraphNode("player")
    playerNode.childs = [gpuQuad]

    return playerNode

def createZombieModel(tex_pipeline):
    # Se crea un cuadrado con textura de zombie en gpu
    quadShape = bs.createTextureQuad(1, 1)

    gpuQuad = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("zombie_sprite.png"))

    return gpuQuad

def createHumanModel(tex_pipeline):
    # Se crea un cuadrado con textura de humano en gpu
    quadShape = bs.createTextureQuad(1, 1)

    gpuQuad = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("human_sprite.png"))

    return gpuQuad

def createStoreModel(pipeline):
    # Se crea la tiendo con un grafo de escena a base de shapes
    redQuadShape = bs.createColorQuad(255/255, 105/255, 105/255)
    lBlueQuadShape = bs.createColorQuad(133/255, 255/255, 253/255)
    darkGreenQuadShape = bs.createColorQuad(0, 125/255, 0)
    blackQuadShape = bs.createColorQuad(0, 0, 0)

    gpuRedQuad = createGPUShape(redQuadShape, pipeline)
    gpuLBlueQuad = createGPUShape(lBlueQuadShape, pipeline)
    gpuDarkGreenQuad = createGPUShape(darkGreenQuadShape, pipeline)
    gpuBlackQuad = createGPUShape(blackQuadShape, pipeline)

    frontNode = csg.CustomSceneGraphNode("front")
    frontNode.transform = tr.scale(0.3, 0.6, 1)
    frontNode.childs = [gpuRedQuad]

    windowNode = csg.CustomSceneGraphNode("window")
    windowNode.transform = tr.scale(0.1, 0.2, 1)
    windowNode.childs = [gpuLBlueQuad]

    windowDoorNode = csg.CustomSceneGraphNode("door")
    windowDoorNode.transform = tr.matmul([tr.translate(0.024, 0.1, 0), tr.scale(0.15, 0.1, 1)])
    windowDoorNode.childs = [gpuLBlueQuad]

    windowNode1 = csg.CustomSceneGraphNode("window2")
    windowNode1.transform = tr.translate(0,-0.15, 0)
    windowNode1.childs = [windowNode]

    windowGroupNode = csg.CustomSceneGraphNode("windowGroup")
    windowGroupNode.transform = tr.translate(0.05, 0, 0)
    windowGroupNode.childs = [windowNode1, windowDoorNode]

    signGreenNode = csg.CustomSceneGraphNode("greenSign")
    signGreenNode.transform = tr.scale(0.1, 0.7, 1)
    signGreenNode.childs = [gpuDarkGreenQuad]

    signBlackNode = csg.CustomSceneGraphNode("blackSign")
    signBlackNode.transform = tr.scale(0.11, 0.71, 1)
    signBlackNode.childs = [gpuBlackQuad]

    signNode = csg.CustomSceneGraphNode("sign")
    signNode.transform = tr.translate(-0.2, 0, 0)
    signNode.childs = [signBlackNode, signGreenNode]

    storeNode = csg.CustomSceneGraphNode("store")
    storeNode.childs = [frontNode, windowGroupNode, signNode]

    regularNode = csg.CustomSceneGraphNode("regularStore")
    regularNode.childs = [storeNode]

    finalNode = csg.CustomSceneGraphNode("finalStore")
    finalNode.transform = tr.translate(0, 2, 0)
    finalNode.childs = [regularNode]

    return finalNode

def createText(tex_pipeline):
    # Se crean los textos de victoria y game over como texturas en un grafo de escena
    quadShape = bs.createTextureQuad(1, 1)

    gpuGameOver = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("game_over_transparent.png"))
    gpuVictory = createTextureGPUShape(quadShape, tex_pipeline, getAssetPath("win_transparent.png"))

    gameOverNode = sg.SceneGraphNode("gameOver")
    gameOverNode.childs = [gpuGameOver]

    victoryNode = sg.SceneGraphNode("victory")
    victoryNode.childs = [gpuVictory]

    finalNode = sg.SceneGraphNode("final")
    finalNode.childs = [gameOverNode, victoryNode]

    return finalNode
