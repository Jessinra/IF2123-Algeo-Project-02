
from OpenGL.GL import *
from OpenGL.GLUT import *
# from OpenGL.GLU import *
from os import system
import matrix
import threading
import numpy
import copy
# from re import sub

# Initializing
numpy.set_printoptions(precision=2)     # Set float precision
window = 0                              # glut window number
width, height = 700, 700                # window size
command = ""                            # user inputs


def get_dimension():
    """
    Function to receive dimension data from user
    :return: dimension
    :rtype: integer
    """

    dimension = 0
    while (dimension != '2') and (dimension != '3'):
        dimension = input("Which dimension do you want (2/3)? ")
        if (dimension != '2') and (dimension != '3'):
            print("This program doesn't support that dimension, please input again")
    dimension = int(dimension)
    return dimension


def refresh2d(width, height):
    """
    Deskripsi
    :param width:
    :type width:
    :param height:
    :type height:
    :return:
    :rtype:
    """

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_line():
    """
    Deskripsi
    :return:
    :rtype:
    """

    glLineWidth(0.1)
    glColor3f(0.5, 1.0, 0.9)
    wid = 0
    while wid <= width:
        length = 0
        while length <= height:
            glBegin(GL_LINES)
            glVertex3f(0.0, length, 0.0)
            glVertex3f(wid, length, 0)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(length, 0, 0.0)
            glVertex3f(length, wid, 0)
            glEnd()
            length += 10
        wid += 50
    # membuat garis sedang
    glLineWidth(2.0)
    wid = 0
    while wid <= width:
        length = 0
        while length <= height:
            glBegin(GL_LINES)
            glVertex3f(0.0, length, 0.0)
            glVertex3f(wid, length, 0)
            glEnd()
            length += 50
            glBegin(GL_LINES)
            glVertex3f(length, 0, 0.0)
            glVertex3f(length, wid, 0)
            glEnd()
        wid += 50
    # membuat garis utama
    # ordinat
    glLineWidth(1.5)
    glColor3f(0.5, 0.4, 0.8)
    glBegin(GL_LINES)
    glVertex3f(height / 2, 0, 0.0)
    glVertex3f(height / 2, width, 0)
    glEnd()
    # absis
    glBegin(GL_LINES)
    glVertex3f(0, width / 2, 0.0)
    glVertex3f(height, width / 2, 0)
    glEnd()


def draw_polygon():
    """
    Deskripsi
    :return:
    :rtype:
    """

    glBegin(GL_POLYGON)
    glColor3f(0.3, 0.4, 1.0)
    i = 0
    while i <= (matrix_order - 1):
        x = vertices[0][i] 
        y = vertices[1][i]
        glVertex2f((float(x)/2) + (width/2), (float(y)/2) + (height/2))
        i = i + 1
    glEnd()

    """
    INI KOK BISA?!   apaan gai ?  
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(300,300)
    glVertex2f(200,100)
    glVertex2f(100,200)
    glEnd()
    """


def draw():
    """

    :return:
    :rtype:
    """

    # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    glClearColor(0.8, 1.0, 0.9, 0.0)
    draw_line()
    refresh2d(width, height)  # set mode to 2d
    # glColor3f(0.0, 0.0, 1.0)                           # set color to blue
    # draw_rect(10, 10, 200, 100)                        # rect at (10, 10) with width 200, height 100
    # Draw Polygon
    draw_polygon()
    glutSwapBuffers()  # important for double buffering


def animate_transformation(vertices, result, frame=200):
    """
    Function to animate transformation
    :param vertices: original vertices
    :type vertices: list
    :param result: transformed vertices
    :type result: list
    :param frame: frame rate ( divided by how much )
    :type frame: int
    :return: None
    :rtype: None
    """

    delta = numpy.subtract(result, vertices)
    transformation_split = (1/frame) * delta
    animation_vertices_frame = vertices

    for _ in range(0, frame):
        animation_vertices_frame = animation_vertices_frame + transformation_split
        # < DRAW ANIMATION VERTICES HERE >
        # < add delay if necessary >


class Layar(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        """
        Deskripsi
        """

        # GUI
        # initialization
        glutInit()  # initialize glut
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(width, height)  # set window size
        glutInitWindowPosition(0, 0)  # set window position
        window = glutCreateWindow(b'-- YAY ALGEO --')  # create window with title
        glutDisplayFunc(draw)  # set draw function callback
        glutIdleFunc(draw)  # draw all the time
        glutMainLoop()


class User(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        """
        Deskripsi
        """
        # User input loop
        repeat = 1
        while repeat:
            command, parameters = matrix.input_command()

            if "translate" in command:
                try:
                    dx = parameters[0]
                except:
                    dx = 0
                try:
                    dy = parameters[1]
                except:
                    dy = 0
                try:
                    dz = parameters[2]
                except:
                    dz = 0

                transformation = matrix.translate(dx=dx, dy=dy, dz=dz, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "dilate" in command:

                try:
                    scale = parameters[0]
                except:
                    scale = 1

                transformation = matrix.dilate(scale=scale, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "rotate" in command:

                try:
                    degree = parameters[0]
                except:
                    degree = 0
                try:
                    pivot_x = parameters[1]
                except:
                    pivot_x = 0
                try:
                    pivot_y = parameters[2]
                except:
                    pivot_y = 0
                try:
                    pivot_z = parameters[3]
                except:
                    pivot_z = 0

                transformation = matrix.rotate(degree=degree, pivot_x=pivot_x, pivot_y=pivot_y, pivot_z=pivot_z, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "reflect" in command:

                try:
                    cond = parameters[0]
                except:
                    cond = "(0,0)"

                transformation = matrix.reflect(cond=cond, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "shear" in command:

                try:
                    axis = parameters[0]
                except:
                    axis = 'x'
                try:
                    scale = parameters[1]
                except:
                    scale = 1

                transformation = matrix.shear(axis=axis, scale=scale, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "stretch" in command:

                try:
                    axis = parameters[0]
                except:
                    axis = 'x'
                try:
                    scale = parameters[1]
                except:
                    scale = 1

                transformation = matrix.stretch(axis=axis, scale=scale, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "custom" in command:
                try:
                    value_list = parameters[0:]
                except:
                    value_list = []

                transformation = matrix.custom(value_list, dim=dimension)
                result = matrix.multiplication(transformation, vertices)

            elif "multiple" in command:
                try:
                    repeat = int(parameters[0]) + repeat
                except:
                    repeat = 1 + repeat
                    print("please re input your command")

            elif "reset" in command:
                result = vertices_ori

            elif "exit" in command:
                exit(1)

            repeat -= 1

            try:
                animate_transformation(vertices=vertices_ori, result=result, frame=200)
            except:
                pass


try:
    threadInput = User(2, "Thread-2", 2)
    threadLayar = Layar(1, "Thread-1", 1)

    # Getting dimension info (2D or 3D)
    dimension = get_dimension()
    vertices, matrix_order = matrix.input_matrix(dimension)
    print(vertices)

    # Saving original vertices
    vertices_ori = copy.deepcopy(vertices)

    threadInput.start()
    threadLayar.start()
except Exception as e:
    print(e)
    system("pause")
