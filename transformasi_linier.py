
from OpenGL.GL import *
from OpenGL.GLUT import *
import matrix_transformation
import threading
import numpy
import copy
from time import sleep


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
    Procedure to keep the GLUT Window size
    :param width: width size for window
    :type width: float
    :param height: height size for window
    :type height: float
    :I.S.: a window
    :F.S.: the window is keep showing
    """

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_line():
    """
    Procedure to make Line Coordinate in GLUT Window
    :I.S. : Plain GLUT Window
    :F.S. : Line Coordinate on GLUT Window
    """

    # Small Size Line
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
    # Medium Size Line
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
    # Main Line
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
    Procedure to draw user polygon input (saved on vertices variable) in GLUT Window
    :I.S. : Plain GLUT Window, Vertices is a global matrix variable that contain the polygon info
    :F.S. : Polygon on GLUT Window
    """

    glBegin(GL_POLYGON)
    glColor3f(0.3, 0.4, 1.0)
    i = 0
    while i <= (matrix_order - 1):
        x = vertices[0][i]
        y = vertices[1][i]
        # casting
        glVertex2f((float(x) / 2) + (width / 2), (float(y) / 2) + (height / 2))
        i = i + 1
    glEnd()


def draw():
    """
    Procedure to render GLUT Window
    :I.S. : No Window
    :F.S. : GLUT Window with line coordinate and user input polygon
    """

    # Draw is called all the time
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
        This thread execute the rendering command loop for GLUT Window
        It render all over the time and change when the global variable Vertices
        are changed.
        I.S. : No Window
        F.S. : GLUT Window that rendering over and over
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
        This thread execute the user command input loop.
        I.S. : GLUT Window with Polygon defined
        F.S. : GLUT Window with transformed polygon by user command
        """

        # User input loop
        global vertices

        repeat = 1
        while repeat:
            # asking command
            command, parameters = matrix_transformation.input_command()
            result = vertices

            # calling translate function
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

                transformation = matrix_transformation.translate(dx=dx, dy=dy, dz=dz, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling dilate function
            elif "dilate" in command:

                try:
                    scale = parameters[0]
                except:
                    scale = 1

                transformation = matrix_transformation.dilate(scale=scale, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling rotate function
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

                try:
                    axis = parameters[4]
                except:
                    axis = 'x'

                transformation = matrix_transformation.rotate(degree=degree, pivot_x=pivot_x, pivot_y=pivot_y, pivot_z=pivot_z, dim=dimension, axis=axis)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling reflect function
            elif "reflect" in command:

                try:
                    cond = parameters[0]
                except:
                    cond = "(0,0)"

                transformation = matrix_transformation.reflect(cond=cond, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling shear function
            elif "shear" in command:

                try:
                    axis = parameters[0]
                except:
                    axis = 'x'
                try:
                    scale = parameters[1]
                except:
                    scale = 1

                transformation = matrix_transformation.shear(axis=axis, scale=scale, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling stretch function
            elif "stretch" in command:

                try:
                    axis = parameters[0]
                except:
                    axis = 'x'
                try:
                    scale = parameters[1]
                except:
                    scale = 1

                transformation = matrix_transformation.stretch(axis=axis, scale=scale, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling custom function
            elif "custom" in command:
                try:
                    value_list = parameters[0:]
                except:
                    value_list = []

                transformation = matrix_transformation.custom(value_list, dim=dimension)
                result = matrix_transformation.multiplication(transformation, vertices)

            # calling multiple function
            elif "multiple" in command:
                try:
                    repeat = int(parameters[0]) + repeat
                except:
                    repeat = 1 + repeat
                    print("please re input your command")
                result = vertices

            # reset the vertices value
            elif "reset" in command:
                result = vertices_ori

            # exiting command
            elif "exit" in command:
                exit(1)

            repeat -= 1

            # animation drawing new vertices
            if "multiple" not in command:
                try:
                    frame = 200
                    delta = numpy.subtract(result, vertices)
                    transformation_split = (1 / frame) * delta

                    for _ in range(0, frame):
                        vertices = vertices + transformation_split
                        sleep((1/frame))
                except:
                    pass

        print("Process successfully executed...")


"""
MAIN PROGRAM
This program will generate a window to show Linier Transformation on
2D or 3D (based on user input). User can give transform input command 
on another window.
"""

try:
    # Declaring two thread, User and Layar (GLUT Window)
    threadInput = User(2, "Thread-2", 2)
    threadLayar = Layar(1, "Thread-1", 1)

    # Getting dimension info (2D or 3D)
    dimension = get_dimension()
    vertices, matrix_order = matrix_transformation.input_matrix(dimension)
    print(vertices)

    # Saving original vertices
    vertices_ori = copy.deepcopy(vertices)

    # All Thread Start
    threadInput.start()
    threadLayar.start()
except Exception as e:
    print(">>> " + str(e) + " <<<")
