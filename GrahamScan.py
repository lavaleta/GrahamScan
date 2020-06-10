# # # # # # # # # # # # # # # # #
#                               #
# Made by Aleksandar Minic 2020 #
# https://github.com/lavaleta   #
#                               #
# # # # # # # # # # # # # # # # #
import matplotlib.pyplot as plt
import numpy as np
import math, copy

print('#\n'
      '#\n'
      '#')

# Here we input the number of points to generate
print('Enter the number of points:')
pintCount = int(input())

# Points are randomly generated
points = np.random.rand(pintCount, 2)

plt.plot(points[:,0], points[:,1], 'o')
plt.show()
# We sort points by their X coordinate
points = points[points[:, 0].argsort()]

i = 0
# We need a new array X*2 array, were in the y=0 we store the index
# of the corresponding number in the array points, and in the y=1 we
# store the the angle in radians.
arrayToSort = np.empty([pintCount,2])
firstPoint = copy.copy(points[0])
while i < points.size/2:
    # Before we calculate the angle we translate the points so center
    # of the coordinate system corresponds first point in our sorted
    # array.
    # We do this by subtracting the first point from all points
    points[i] = points[i]-firstPoint
    # Here we remember the index of the point so we know to what point
    # what angle corresponds to
    arrayToSort[i,0] = i
    # We calculate the angle between the point and the X axis, and atan2
    # precisely gives us that. That is the reason we translated all points
    # so the first one in in the center. That way the angle we get will be
    # the angle between the first point and the current point
    arrayToSort[i,1] = math.atan2(points[i, 0], points[i, 1])
    i+=1

plt.plot(points[:,0], points[:,1], 'o')
i=0
# Here we annotate the points with their corresponding angles
while i < points.size/2:
    plt.annotate(str(round(arrayToSort[i,1], 2))+' rad', (points[i,0], points[i,1]))
    i+=1

# Now we sort the angles in ascending order
sortedByAngle = arrayToSort[arrayToSort[:,1].argsort()]
# Since we need the array in descending order, and that is not
# something that numpy offers, we just flip the sorted array
sortedByAngleDescending = sortedByAngle[::-1]

# Graham scan uses Stack, and we will simulate in with a list
stack = []

# NOTE! Stack uses PUSH but int equivalent in Python is APPEND

# We append the first two points to stack
# We will just keep the indexes in the stack since that is
# all we really need
stack.append(0)
stack.append(sortedByAngleDescending[0,0])

# Graham scan checks  if the next point makes a left turn with
# the current line. If it does it pushes the point on the stack,
# if not it backtracks through the stack until it finds a line
# that does make a left turn with the current point
i = 1
while i < points.size/2:

    # We get the top two indexes from the stack to construct the
    # current line segment
    topOfStackIndex = stack.pop()
    beforeTopIndex = stack.pop()
    # We return the indexes to the stack
    stack.append(beforeTopIndex)
    stack.append(topOfStackIndex)

    # We use the indexes to get the points
    beforeTopPoint = points[int(beforeTopIndex)]
    topOfStackPoint = points[int(topOfStackIndex)]

    # We get the point we will consider
    nextPoint = points[int(sortedByAngleDescending[i,0])]

    # Now we check if the next point makes a left turn with the
    # current line segment
    turn = ((beforeTopPoint[0]-topOfStackPoint[0])*(nextPoint[1]-topOfStackPoint[1])
            - (beforeTopPoint[1]-topOfStackPoint[1])*(nextPoint[0]-topOfStackPoint[0]))

    if(turn<0):
        # If the current point makes a left turn we just append
        # the point to stack
        stack.append(sortedByAngleDescending[i,0])
    else:
        # if it does not make a left turn we have to backtrack
        while 1:
            # We pop two points from stack since we dont need them
            # anymore
            stack.pop()
            stack.pop()
            # We store beforeTopIndex in tmpIndex temporarily
            tmpIndex = beforeTopIndex
            # Now out new topOfStackPoint is beforeTopPoint since
            # we are going back through the stack
            topOfStackPoint = beforeTopPoint
            # We pop a value to get the new beforeTopIndex
            beforeTopIndex = stack.pop()
            # We just return the two values that we took from the
            # stack
            stack.append(beforeTopIndex)
            stack.append(tmpIndex)
            # From the index we get the point... you should get it
            # by now
            beforeTopPoint = points[int(beforeTopIndex)]

            # Again we check the turn for the new values
            turn = ((beforeTopPoint[0]-topOfStackPoint[0])*(nextPoint[1]-topOfStackPoint[1])
                    - (beforeTopPoint[1]-topOfStackPoint[1])*(nextPoint[0]-topOfStackPoint[0]))

            # We break the while loop once we find a line segment
            # that makes a left turn with the current point
            if(turn<0):
                stack.append(sortedByAngleDescending[i, 0])
                break
    i+=1

# This loop is only for matplotlib to draw the boundary of the Convex-Hull
# NOTE! At the end of this loop the stack will be empty
i=0
while i < len(stack) -1:

    point1 = stack.pop()
    point2 = stack.pop()
    stack.append(point2)

    plt.plot((points[int(point1),0],points[int(point2),0]),
             (points[int(point1),1], points[int(point2),1]),'-k')

plt.show()

