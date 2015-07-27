import time
import math

W = int(input("Enter the width: "))
H = int(input("Enter the height: "))

middle_x = math.floor(W/2)
middle_y = math.floor(H/2)

sides = [ # each side is in the format [length, [x0, y0], [x1, y1]]
    [3,[middle_x,middle_y],[middle_x+3,middle_y]],
    [4,[middle_x,middle_y],[middle_x,middle_y+4]],
    [5,[middle_x+3,middle_y],[middle_x,middle_y+4]]
    ]

triangles = [[0,1,2]] # each triangle is in the format [a, b, c] where a, b and c are the indexes of sides

used_triangles = [[3,4,5]] # a list of used Pythagorean triples, where lengths are ordered (a < b < c)

max_bounds_length = math.sqrt(W**2 + H**2)

def check_if_pyth_triple(a,b): # accepts two lists of the form [l, [x0,y0], [x1,y1]] defining two line segments
    # returns 0 if there are no triples, 1 if there is a triple with a right angle on a,
    # and 2 if there is a triple with the right angle opposite a
    c = math.sqrt(a[0]**2 + b[0]**2)
    if c.is_integer():
        if not sorted([a[0], b[0], c]) in used_triangles:
            return 1
        return 0
    else:
        if a[0] > b[0]:
            c = math.sqrt(a[0]**2 - b[0]**2)
            if c.is_integer() and not sorted([a[0], b[0], c]) in used_triangles:
                return 2
        return 0

def check_if_out_of_bounds(p):
    out = False
    if p[0] < 0 or p[0] > W:
        out = True
    if p[1] < 0 or p[1] > H:
        out = True
    return out

def in_between(a,b,c):
    maxi = max(a,c)
    mini = min(a,c)
    return mini < b < maxi

def sides_intersect(AB,CD): # accepts two lists of the form [l, [x0,y0], [x1,y1]] defining two line segments
    # doesn't count overlapping lines
    A = AB[1]
    B = AB[2]
    C = CD[1]
    D = CD[2]

    if A[0] == B[0]: # AB is vertical
        if C[0] == D[0]: # CD is vertical
            return False
        else:
            m1 = (C[1] - D[1])/(C[0] - D[0]) # slope of CD
            y = m1*(A[0] - C[0]) + C[1] # the y value of CD at AB's x value
            return in_between(A[1], y, B[1]) and in_between(C[0], A[0], D[0])
    else:
        m0 = (A[1] - B[1])/(A[0] - B[0]) # slope of AB
        if C[0] == D[0]: # CD is vertical
            y = m0*(C[0] - A[0]) + A[1] # the y value of CD at AB's x value
            return in_between(C[1], y, D[1]) and in_between(A[0],C[0],B[0])
        else:
            m1 = (C[1] - D[1])/(C[0] - D[0]) # slope of CD
            if m0 == m1:
                return False
            else:
                x = (m0*A[0] - m1*C[0] - A[1] + C[1])/(m0 - m1)
                return in_between(A[0], x, B[0]) and in_between(C[0], x, D[0])

def check_all_sides(b,triangle):
    no_intersections = True
    for side in sides:
        if sides_intersect(side, b):
            no_intersections = False
            break
                
    return no_intersections

def check_point_still_has_room(A): # This function is needed for the weird case when all 2pi degrees
    # around a point are filled by triangles, but you could fit in a small triangle into another one
    # already built around the point. Doing this won't cause sides_intersect() to detect it because
    # the sides will all be parallel. Crazy stuff.
    connecting_sides = []
    for side in sides:
        if A in side:
            connecting_sides.append(side)

    match_count = 0
    slopes = []
    for side in connecting_sides:
        B = side[1]
        if A == B:
            B = side[2]
        if not A[0] == B[0]:
            slope = round((A[1]-B[1])/(A[0]-B[0]),4)
        else:
            if A[1] < B[1]:
                slope = "infinity"
            else:
                slope = "neg_infinity"
        if slope in slopes:
            match_count -= 1
        else:
            slopes.append(slope)
            match_count += 1

    return match_count != 0

def construct_b(a,b,pyth_triple_info,straight_b_direction,bent_b_direction):
    # this function finds the correct third point of the triangle given a and the length of b
    # pyth_triple_info determines if a is a leg or the hypotenuse
    # the b_directions determine on which side of a the triangle should be formed
    a_p = 2 # this is the index of the point in a that is not the shared point with b
    if a[1] != b[1]:
        a_p = 1

    vx = a[a_p][0] - b[1][0] # v is our vector, and these are the coordinates, adjusted so that
    vy = a[a_p][1] - b[1][1] # the shared point is the origin

    if pyth_triple_info == 1:
        # because the dot product of orthogonal vectors is zero, we can use that and the Pythagorean formula
        # to get this simple formula for generating the coordinates of b's second point
        if vy == 0:
            x = 0
            y = b[0]
        else:
            x = b[0]/math.sqrt(1+((-vx/vy)**2)) # b[0] is the desired length
            y = -vx*x/vy

        x = x*straight_b_direction # since the vector is orthagonal, if we want to reverse the direction,
        y = y*straight_b_direction # it just means finding the mirror point

    elif pyth_triple_info == 2: # this finds the intersection of the two circles of radii b[0] and c 
        # around a's endpoints, which is the third point of the triangle if a is the hypotenuse
        c = math.sqrt(a[0]**2 - b[0]**2)
        D = a[0]
        A = (b[0]**2 - c**2 + D**2 ) / (2*D)
        h = math.sqrt(b[0]**2 - A**2)
        x2 = vx*(A/D)
        y2 = vy*(A/D)        
        x = x2 + h*vy/D
        y = y2 - h*vx/D
        
        if bent_b_direction == -1: # this constitutes reflection of the vector (-x,-y) around the normal vector n,
            # which accounts for finding the triangle on the opposite side of a
            dx = -x
            dy = -y
            v_length = math.sqrt(vx**2 + vy**2)
            nx = vx/v_length
            ny = vy/v_length

            d_dot_n = dx*nx + dy*ny

            x = dx - 2*d_dot_n*nx
            y = dy - 2*d_dot_n*ny

    x = x + b[1][0] # adjust back to the original frame
    y = y + b[1][1]

    return [x,y]

def construct_triangle(side_index):
    a = sides[side_index] # a is the base of the triangle
    a_p = 1
    b = [1, a[a_p], []] # side b, c is hypotenuse
    
    for index, triangle in enumerate(triangles):
        if side_index in triangle:
            triangle_index = index
            break

    triangle = list(triangles[triangle_index])
    triangle.remove(side_index)

    add_tri = False

    straight_b = construct_b(a,b,1,1,1)

    bent_b = construct_b(a,b,2,1,1)

    A = sides[triangle[0]][1]
    if A in a:
        A = sides[triangle[0]][2]

    Ax = A[0] - b[1][0] # adjusting A so that it's a vector
    Ay = A[1] - b[1][1]

    # these are for determining if construct_b() is going to the correct side
    triangle_on_side = (a[2][0]-a[1][0])*(A[1]-a[1][1]) - (a[2][1]-a[1][1])*(A[0]-a[1][0])
    straight_b_on_side = (a[2][0]-a[1][0])*(straight_b[1]-a[1][1]) - (a[2][1]-a[1][1])*(straight_b[0]-a[1][0])
    bent_b_on_side = (a[2][0]-a[1][0])*(bent_b[1]-a[1][1]) - (a[2][1]-a[1][1])*(bent_b[0]-a[1][0])

    straight_b_direction = 1
    if (triangle_on_side > 0 and straight_b_on_side > 0) or (triangle_on_side < 0 and straight_b_on_side < 0):
        straight_b_direction = -1

    bent_b_direction = 1
    if (triangle_on_side > 0 and bent_b_on_side > 0) or (triangle_on_side < 0 and bent_b_on_side < 0):
        bent_b_direction = -1


    a_ps = []
    for x in [1,2]:
        if check_point_still_has_room(a[x]): # here we check for that weird exception
            a_ps.append(x)

    while True:
        out_of_bounds = False
        if b[0] > max_bounds_length:
            break

        pyth_triple_info = check_if_pyth_triple(a,b)
        
        for a_p in a_ps:
            if a_p == 1: # this accounts for the change in direction when switching a's points
                new_bent_b_direction = bent_b_direction
            else:
                new_bent_b_direction = -bent_b_direction

            b[1] = a[a_p]
            if pyth_triple_info > 0:
                b[2] = construct_b(a,b,pyth_triple_info,straight_b_direction,new_bent_b_direction)

                if check_if_out_of_bounds(b[2]): # here is the check to make sure we don't go out of bounds
                    out_of_bounds = True
                    break

                if check_all_sides(b,triangle):
                    if pyth_triple_info == 1:
                        c = [math.sqrt(a[0]**2 + b[0]**2), a[3-a_p], b[2]]
                    else:
                        c = [math.sqrt(a[0]**2 - b[0]**2), a[3-a_p], b[2]]

                    if check_all_sides(c,triangle):
                        add_tri = True
                        break

        if out_of_bounds or add_tri:
            break

        b[0] += 1 # increment the length of b every time the loop goes through

    if add_tri: # this adds a new triangle
        sides.append(b)
        sides.append(c)
        sides_len = len(sides)
        triangles.append([side_index, sides_len - 2, sides_len - 1])
        used_triangles.append(sorted([a[0], b[0], c[0]])) # so we don't use the same triangle again

def build_all_triangles(): # this iterates through every side to see if a new triangle can be constructed
    # this is probably where real optimization would take place so more optimal triangles are placed first
    t0 = time.clock()

    index = 0
    while index < len(sides):
        construct_triangle(index)
        index += 1

    t1 = time.clock()

    triangles_points = [] # this is all for printing points
    for triangle in triangles:
        point_list = []
        for x in [1,2]:
            for side_index in triangle:
                point = sides[side_index][x]
                if not point in point_list:
                    point_list.append(point)
        triangles_points.append(point_list)

    for triangle in triangles_points:
        print(triangle)

    print(len(triangles), "triangles placed in", round(t1-t0,3), "seconds.")

def matplotlib_graph(): # this displays the triangles with matplotlib
    import pylab as pl
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc

    lines = []
    for side in sides:
        lines.append([side[1],side[2]])

    lc = mc.LineCollection(lines)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.show()

build_all_triangles()
matplotlib_graph()