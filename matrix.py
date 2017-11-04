import numpy
import math
from re import sub

# Set float precision
numpy.set_printoptions(precision=2)


def input_matrix(dimension=2):
    """
    Function to accept input matrix of vertices
    :param dimension : dimension of vector space used
    :type dimension: integer
    :return: vertices matrix
    :rtype: matrix
    """

    def ordinal(i):
        return "%d%s" % ((i+1), "tsnrhtdd"[(math.floor((i+1) / 10) % 10 != 1) * ((i+1) % 10 < 4) * (i+1) % 10::4])

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


def multiplication(matrix_1, matrix_2):
    """
    Function to return the result of matrix multiplication
    :param matrix_1: transformation matrix
    :type matrix_1: matrix
    :param matrix_2: vertices matrix
    :type matrix_2: matrix
    :return: transformed vertices matrix
    :rtype: matrix
    """

    # Try to do matrix multiplication
    try:
        temp = matrix_1 @ matrix_2
        return temp

    except Exception as e:
        print(">>> " + str(e) + " <<<")


def translate(dx=0, dy=0, dz=0, dim=2):
    """
    Function to return transformation matrix of translation
    :param dx: differential of the variable x
    :type dx: int / float
    :param dy: differential of the variable y
    :type dy: int / float
    :param dz: differential of the variable z
    :type dz: int / float
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    transformation = numpy.identity(dim+1, dtype=int)

    # For 2D
    if dim == 2:
        transformation = numpy.array(([1, 0, dx],
                                      [0, 1, dy],
                                      [0, 0, 1]))
    # For 3D
    elif dim == 3:
        transformation = numpy.array(([1, 0, 0, dx],
                                      [0, 1, 0, dy],
                                      [0, 0, 1, dz],
                                      [0, 0, 0, 1]))

    else:
        print(dim, "dimension matrix transformation is not available")

    return transformation


def dilate(scale=1, dim=2):
    """
    Function to return transformation matrix of dilatation by scaling factor
    :param scale: scaling factor of dilatation
    :type scale: int / float
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    transformation = numpy.identity(dim+1, dtype=int)
    k = scale

    # For 2D
    if dim == 2:
        transformation = numpy.array(([k, 0, 0],
                                      [0, k, 0],
                                      [0, 0, 1]))

    # For 3D
    elif dim == 3:
        transformation = numpy.array(([k, 0, 0, 0],
                                      [0, k, 0, 0],
                                      [0, 0, k, 0],
                                      [0, 0, 0, 1]))

    else:
        print(dim, "dimension matrix transformation is not available")

    return transformation


def rotate(degree=0, pivot_x=0, pivot_y=0, pivot_z=0, dim=2, axis='x'):
    """
    Function to return transformation matrix of rotation with pivot specified
    :param degree: rotating degree
    :type degree: int/float
    :param pivot_x : rotating pivot [x]
    :type pivot_x : int/float
    :param pivot_y : rotating pivot [y]
    :type pivot_y : int/float
    :param pivot_z : rotating pivot [z]
    :type pivot_z : int/float
    :param dim: dimension of space
    :type dim: integer
    :param axis: axis of rotation (for 3D only)
    :type axis: char
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    transformation = numpy.identity(dim+1, dtype=int)

    # Gather information from parameters
    cos = math.cos(math.radians(float(degree)))
    sin = math.sin(math.radians(float(degree)))
    pivot_change = False

    # Validating pivot element
    try:
        pivot_x = float(pivot_x)
        pivot_y = float(pivot_y)
        pivot_z = float(pivot_z)

    except Exception as e:
        print(">>> " + str(e) + " <<<")

    # Initializing pre and post translation
    pre_translation = transformation
    post_translation = transformation

    # If pivot is not (0,0,0) update the pre and post translation matrix
    if pivot_x != 0 or pivot_y != 0 or pivot_z != 0:

        pivot_change = True
        pre_translation = translate(-pivot_x, -pivot_y, -pivot_z, dim=dim)
        post_translation = translate(pivot_x, pivot_y, pivot_z, dim=dim)

    # For 2D
    if dim == 2:

        # Rotation to 'arbitrary' z axis
        transformation = numpy.array(([cos, -sin, 0],
                                      [sin, cos, 0],
                                      [0, 0, 1]))

    # For 3D
    elif dim == 3:

        # Get the axis
        axis = axis.strip().lower()

        # Rotate depend on axis
        if axis == "x":
            transformation = numpy.array(([1, 0, 0, 0],
                                          [0, cos, -sin, 0],
                                          [0, sin, cos, 0],
                                          [0, 0, 0, 1]))
        elif axis == "y":
            transformation = numpy.array(([cos, 0, sin, 0],
                                          [0, 1, 0, 0],
                                          [-sin, 0, cos, 0],
                                          [0, 0, 0, 1]))
        elif axis == "z":
            transformation = numpy.array(([cos, -sin, 0, 0],
                                          [sin, cos, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]))
        else:
            print("There's no such axis")

    else:
        print(dim, "dimension matrix transformation is not available")

    # Multiply rotation matrix by pre and post translation if necessary
    if pivot_change:
        transformation = multiplication(transformation, pre_translation)
        transformation = multiplication(post_translation, transformation)

    return transformation


def stretch(axis, scale=1, dim=2):
    """
    Function to return transformation matrix of stretching by scaling factor into specified axis
    :param axis: axis of stretching
    :type axis: char
    :param scale: scaling factor of stretch
    :type scale: int / float
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    axis = axis.strip().lower()
    cont = True
    transformation = numpy.identity(dim+1, dtype=int)

    x = 1
    y = 1
    z = 1

    # Try to get the axis
    if axis == "x":
        x = scale
    elif axis == "y":
        y = scale
    elif axis == "z":
        z = scale
    else:
        print("There's no such axis")
        cont = False

    # Change value of transformation matrix depend on axis
    if cont:

        # For 2D
        if dim == 2:
            transformation = numpy.array(([x, 0, 0],
                                          [0, y, 0],
                                          [0, 0, 1]))

        # For 3D
        elif dim == 3:
            transformation = numpy.array(([x, 0, 0, 0],
                                          [0, y, 0, 0],
                                          [0, 0, z, 0],
                                          [0, 0, 0, 1]))
        else:
            print(dim, "dimension matrix transformation is not available")

    return transformation


def shear(axis, scale=1, dim=2):
    """
    Function to return transformation matrix of shearing by scaling factor into specified axis
    :param axis: axis of shearing
    :type axis: char
    :param scale: scaling factor of shearing
    :type scale: int / float
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    axis = axis.strip().lower()
    cont = True
    transformation = numpy.identity(dim+1, dtype=int)

    x = 0
    y = 0
    z = 0

    # Try to get the axis
    if axis == "x":
        x = scale
    elif axis == "y":
        y = scale
    elif axis == "z":
        z = scale
    else:
        print("There's no such axis")
        cont = False

    # Change value of transformation matrix depend on axis
    if cont:

        # For 2D
        if dim == 2:
            transformation = numpy.array(([1, x, 0],
                                          [y, 1, 0],
                                          [0, 0, 1]))

        # For 3D
        if dim == 3:
            transformation = numpy.array(([1, y, z, 0],
                                          [x, 1, z, 0],
                                          [x, y, 1, 0],
                                          [0, 0, 0, 1]))

        else:
            print(dim, "dimension matrix transformation is not available")

    return transformation


def custom(value_list, dim=2):
    """
    Function to return transformation matrix consist of list element
    :param value_list: list of value of transformation matrix
    :type value_list: list of integer / float
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    transformation = numpy.identity(dim+1, dtype=int)

    # Try to check whether value list is usable
    try:
        value_list = [float(x) for x in value_list]
    except Exception as e:
        print(">>> " + str(e) + " <<<")
        return transformation

    # Complete the value list when necessary
    while len(value_list) < dim**2:
        print("transformation matrix missing some element, adding 0...")
        value_list.append(0)

    # Adding extra zero to last (complete homogeneous matrix)
    i = dim
    while i < len(value_list)+1:
        value_list.insert(i, 0)
        i += dim+1

    # Adding last dummy vector (complete homogeneous matrix)
    for i in range(0, dim):
        value_list.append(0)
    value_list.append(1)

    transformation = numpy.array(value_list).reshape((dim + 1, dim + 1))
    return transformation


def reflect(cond, dim=2):
    """
    Function to return transformation matrix of reflection
    :param cond: reflect target
    :type cond: string
    :param dim: dimension of space
    :type dim: integer
    :return: transformation matrix
    :rtype: matrix
    """

    # Initializing
    transformation = numpy.identity(dim + 1, dtype=int)

    # Get the reflection style
    cond = "".join(cond.split())
    cond = cond.strip().lower()

    def get_reflection_pivot(cond):
        """ Function to return search keyword """

        # Find the index of double bracket
        index_start = cond.find("(") + 1
        index_stop = cond.rfind(")")

        # Determine whether bracket are exist and the text exist
        text_available = (index_stop - index_start) >= 1
        if text_available:
            keyword = cond[index_start:index_stop]
            keyword = keyword.split(",")
            return keyword
        else:
            return []

    # For 2D
    if dim == 2:

        # Return transformation matrix based on reflection pivot (line)
        if cond == "x":
            transformation = numpy.array(([1, 0, 0],
                                          [0, -1, 0],
                                          [0, 0, 1]))
        elif cond == "y":
            transformation = numpy.array(([-1, 0, 0],
                                          [0, 1, 0],
                                          [0, 0, 1]))
        elif cond == "y=x":
            transformation = numpy.array(([0, 1, 0],
                                          [1, 0, 0],
                                          [0, 0, 1]))
        elif cond == "y=-x":
            transformation = numpy.array(([0, -1, 0],
                                          [-1, 0, 0],
                                          [0, 0, 1]))

        # Special case : reflection toward a point
        else:

            # Get the pivot point
            reflection_point = get_reflection_pivot(cond)
            if len(reflection_point) >= 2:

                # Try to check whether pivot point is usable
                try:
                    reflection_point = [float(x) for x in reflection_point]
                    a = float(reflection_point[0])
                    b = float(reflection_point[1])

                except Exception as e:
                    print(">>> " + str(e) + " <<<")
                    return transformation

                # Basic idea is to translate every point,, Ref(x) = 2pivot_x - x ,, same as -1 x (x- 2pivot_x)
                # Translate -2pivot_x and times -1
                transformation = numpy.array(([-1, 0, 2*a],
                                              [0, -1, 2*b],
                                              [0, 0, 1]))

            else:
                print("reflection point is incomplete or this kind of reflection ("+cond+") is not available for "+str(dim)+"D\nPlease try it again...")
                print("\nreturning identity matrix...")
                return transformation

    # For 3D
    elif dim == 3:

        # Return transformation matrix based on reflection pivot (plane)
        if cond == "xy":
            transformation = numpy.array(([1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, -1, 0],
                                          [0, 0, 0, 1]))
        elif cond == "yz":
            transformation = numpy.array(([-1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]))
        elif cond == "xz":
            transformation = numpy.array(([1, 0, 0, 0],
                                          [0, -1, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]))

    else:
        print(dim, "dimension matrix transformation is not available")

    return transformation


def multiple(command):
    """
    Function to get how many times a transformation occur from text
    :param command: input string
    :type command: string
    :return: times
    :rtype: int
    """

    # Initialization
    repeat = 1
    found = False

    # Crop and filter text
    split_text = sub('\W\s+', '', command).strip().split(" ")
    for x in split_text:

        # Try to find the number part
        try:
            repeat = int(x)
            found = True
        except:
            pass

    # If command doesn't contain any number, assume it's one times only
    if not found:
        print("Seems you didn't specify how many times the repetition should be done,")
        print("I assume it's one then...")

    return repeat

dimension = 2

# Input part
# vertices = input_matrix(dimension=dimension)
# print(vertices)

# testing vertices
if dimension == 3:
    vertices = [[6, 3, 0, 2],
                [1, 1, 2, 2],
                [2, 0, 2, 0],
                [1, 1, 1, 1]
                ]
else:
    vertices = [[5, 3, 2.5],
                [1, 1, 2.5],
                [1, 1, 1]
                ]

# Testing part
"""

transformation = translate(dx=2,dy=2,dz=0,dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : translate")
print(result)

transformation = dilate(scale = 3, dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : dilate")
print(result)

transformation = stretch('x',scale = 1.5, dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : stretch x axis")
print(result)

transformation = shear('x',scale = 1, dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : shear x axis")
print(result)

transformation = rotate(degree=22, pivot_x=2, pivot_y='2',pivot_z=0,dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : rotation ")
print(result)

value_list = [1,3.22,'4',4]
transformation = custom(value_list, dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : custom")
print(result)

transformation = reflect("( 4  , -2)", dim=dimension)
result = multiplication(transformation,vertices)
print("\ntransform : reflect")
print(result)

"""

# To do list :
# reset
# exit
