
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
width, height = 1000, 1000                # window size
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
        glVertex2f(float(x), float(y))
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
