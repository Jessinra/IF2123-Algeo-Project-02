from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import threading
import matrix
import numpy
import math
import copy
from re import sub

# Set float precision
numpy.set_printoptions(precision=2)


window = 0                                             # glut window number
width, height = 700, 700                               # window size
global matrix_order 		#number of dots
global vertices 			#matrix of dots
global vertices_ori 		#original matrix of dots
global command 				#user inputs
global dimension 			#matrix dimension

matrix_order = 0
vertices = []
vertices_ori = []
command = ""
dimension = 0

def input_matrix(dimension=2):
    """
    Function to accept input matrix of vertices
    :param dimension : dimension of vector space used
    :type dimension: integer
    :return: vertices matrix
    :rtype: matrix
    """

    print("Creating matrix for", dimension, "dimension vertices")
    # Getting input of matrix order
    while True:
        command = "Insert matrix order : "
        raw_input = input(command).strip()
        try:
            matrix_order = int(raw_input)

            # Validating input
            if matrix_order < 0:
                print("Matrix's order has to be a positive integer..")
            else:
                break
        except:
            print("Matrix's order has to be a positive integer..")

    # Getting input of vertices value
    vertices = []
    i = 0
    while i < matrix_order:

        # Message
        ordinal = lambda n: "%d%s" % ((i+1), "tsnrhtdd"[(math.floor((i+1) / 10) % 10 != 1) * ((i+1) % 10 < 4) * (i+1) % 10::4])
        command = "Insert "+ordinal(i)+" vertices value : "

        # Process input
        raw_input = input(command)
        array = raw_input.strip().split(" ")
        array = list(filter(None, array))

        append = True

        # If vertices contain more than dimension value
        if len(array) > dimension:

            # Suspend first
            append = False

            # Display error text
            error_text = ["Did you mean ["]
            for j in range(0, dimension):
                error_text.append(str(array[j]) + ",")
            error_text.append("] and " + str(array[dimension])+"... ?")
            print("".join(error_text))

            # Prompt user
            prompt = input("< yes / no >     (if 'yes' then everything after 'and' will get cut)   : ")

            # If yes then cut the rest
            if "yes" in prompt:
                array = array[0:dimension]
                append = True

            elif "no" in prompt:
                print("Please re-input this vertices value...")

            else:
                print("I assume it was a 'no', please re-input this vertices value...")

        # If vertices is incomplete in terms of 3D value
        if len(array) < dimension:
            # Suspend first
            append = False

            # Display error text
            error_text = ["Did you mean ["]
            for j in range(0, len(array)):
                error_text.append(str(array[j])+",")
            error_text.append('0, '*(dimension - len(array)) + "] ?")
            print(" ".join(error_text))

            # Prompt user
            prompt = input("< yes / no > : ")

            # If yes, append extra 0 to the array
            if "yes" in prompt:
                while len(array) < dimension:
                    array.append('0')
                append = True

            elif "no" in prompt:
                print("Please re-input this vertices value...")

            else:
                print("I assume it was a 'no', please re-input this vertices value...")

        # Fill up the last slot - for translation purpose
        array.append("1")

        # If there's no problem with vertices value
        if append:

            vertices.append(array)
            i += 1

            # Convert to float / integer
            """
            # Convert vertices value into integer
            try:
                array = [float(x) for x in array]
                vertices.append(array)
                i += 1

            except:
                try:
                    array = [int(x) for x in array]
                    vertices.append(array)
                    i += 1
                except Exception as e:
                    print(e)
                    print("Seems the vertices is not in integer.. Please re-input this vertices ")
            """

    # Set-up as numpy matrix
    vertices = numpy.array(vertices)
    vertices = numpy.transpose(vertices)
    return vertices, matrix_order

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_line () :
	glLineWidth(0.1)
	glColor3f(0.5, 1.0, 0.9)
	wid = 0
	while (wid <= width) :
		len = 0
		while (len <= height) :
			glBegin(GL_LINES)
			glVertex3f(0.0, len, 0.0)
			glVertex3f(wid, len, 0)
			glEnd()
			glBegin(GL_LINES)
			glVertex3f(len, 0, 0.0)
			glVertex3f(len, wid, 0)
			glEnd()
			len += 10
		wid += 50
	# membuat garis sedang
	glLineWidth(2.0)
	wid = 0
	while (wid <= width) :
		len = 0
		while (len <= height) :
			glBegin(GL_LINES)
			glVertex3f(0.0, len, 0.0)
			glVertex3f(wid, len, 0)
			glEnd()
			len += 50
			glBegin(GL_LINES)
			glVertex3f(len, 0, 0.0)
			glVertex3f(len, wid, 0)
			glEnd()
		wid += 50
	# membuat garis utama
	# ordinat
	glLineWidth(1.5)
	glColor3f(0.5, 0.4, 0.8)	
	glBegin(GL_LINES)
	glVertex3f(height/2, 0, 0.0)
	glVertex3f(height/2, width, 0)
	glEnd()
	#absis
	glBegin(GL_LINES)
	glVertex3f(0, width/2, 0.0)
	glVertex3f(height, width/2, 0)
	glEnd()
	
def draw_polygon () :
	glBegin(GL_POLYGON)
	glColor3f(0.3, 0.4, 1.0)
	i = 0
	while (i <= (matrix_order - 1)) :
		x = vertices[0][i]
		y = vertices[1][i]
		glVertex2f(float(x),float(y))
		i = i + 1
	glEnd()
	
	"""
	INI KOK BISA?!
	glBegin(GL_POLYGON)
	glColor3f(0.0, 0.0, 0.0)
	glVertex2f(300,300)
	glVertex2f(200,100)
	glVertex2f(100,200)
	glEnd()
	"""
	
def draw():                                            # ondraw is called all the time
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
	glLoadIdentity()                                   # reset position
	glClearColor(0.8, 1.0, 0.9, 0.0)
	draw_line()
	refresh2d(width, height)                           # set mode to 2d
	#glColor3f(0.0, 0.0, 1.0)                           # set color to blue
	#draw_rect(10, 10, 200, 100)                        # rect at (10, 10) with width 200, height 100
	# Draw Polygon
	draw_polygon()
	glutSwapBuffers()                                  # important for double buffering
	
	
class layar (threading.Thread) :
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self) :
		#GUI
		# initialization
		glutInit()                                             # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(width, height)                      # set window size
		glutInitWindowPosition(0, 0)                           # set window position
		window = glutCreateWindow(b'-- YAY --')                # create window with title
		glutDisplayFunc(draw)                                  # set draw function callback
		glutIdleFunc(draw)                                     # draw all the time
		glutMainLoop()

class user (threading.Thread) :
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self) :
		print("mancay")
	

threadInput = user(2, "Thread-2", 2)
threadLayar = layar(1, "Thread-1", 1)
	
dimension = 0
while ((dimension != '2') and (dimension != '3')) : 
	dimension = input("What dimension do you want (2/3)? ")
	if ((dimension != '2') and (dimension != '3')) :
		print ("Wrong Input! Type 2 or 3")
dimension = int(dimension)
vertices, matrix_order = input_matrix(dimension)
print(vertices)
	
#saving original vertices
vertices_ori = copy.deepcopy(vertices)
	
threadInput.start()
threadLayar.start()

	
