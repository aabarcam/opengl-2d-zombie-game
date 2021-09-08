# Proyecto de OpenGL en 2D

Primer proyecto del curso Modelación y Computación Gráfica para Ingenieros de la Universidad de Chile, semestre otoño, 2021.

Consiste en un juego en 2D simple creado con Python y OpenGL con temática de zombies, busca mostrar el uso de transformaciones, texturas, shaders y otras funcionalidades 2D de OpenGL. Todos los elementos en la carpeta 'gráfica' fueron provistos por el profesor del curso Daniel Calderón.

Modo de ejecución: python survival.py Z H T P
Donde Z y H son enteros representando la cantidad de zombies y humanos respectivamente, a instanciar cada T segundos. T también es un entero, y P es un real que representa la probabilidad de que un humano infectado se transforme en un zombie cada T segundos. 

Los controles son W, A, S, D para moverse, barra espaciadora para activar/desactivar el detector de infectados, y escape para cerrar el juego

El juego termina cuando el jugador se transforma en zombie, o cuando se llega a la tienda luego de avanzar lo suficiente.

-----------------------------------------------------------------------------------
# OpenGL 2D project
First project for the Modeling and Computer Graphics for Engineers course at the University de Chile, autumn semester, 2021.

Consists of a simple, zombie themed 2D game made with Python and OpenGL, showcasing use of transformations, textures and shaders among other 2D functionalities offered by OpenGL. All elements inside the 'gráfica' folder were provided by the course professor Daniel Calderón.

Execution method: python survival.py Z H T P
Where Z and H are integers that represent the quantity of zombies and humans respectively, that are to be instanciated every T seconds. T is an integer, and P is a real number representing the probabilty of an intected human to transform into a zombie every T seconds.

Controls are W, A, S, D for movement, spacebar for activating/deactivating the infected detector and escape key to close the game.

The game ends when the player turns into a zombie, or when the store is reached after moving up a certain distance.
