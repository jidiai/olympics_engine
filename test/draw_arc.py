# def circle_arc(matrix, start, end, clockwise=True):
#     """Python implementation of the modified Bresenham algorithm
#     for complete circles, arcs and pies
#     radius: radius of the circle in pixels
#     start and end are angles in radians
#     function will return a list of points (tuple coordinates)
#     and the coordinates of the start and end point in a list xy
#     """
#     # round it to avoid rounding errors and wrong drawn pie slices
#     radius = matrix.shape[0]-1
#
#     start = math.radians(round(math.degrees(start)))
#     end = math.radians(round(math.degrees(end)))
#     if start>=math.pi*2:
#         start = math.radians(math.degrees(start)%360)
#     if end>=math.pi*2:
#         end = math.radians(math.degrees(end)%360)
#     # always clockwise drawing, if anti-clockwise drawing desired
#     # exchange start and end
#     if not clockwise:
#         s = start
#         start = end
#         end = s
#     # determination which quarters and octants are necessary
#     # init vars
#     xy = [[0,0], [0,0]] # to locate actual start and end point for pies
#     # the x/y border value for drawing the points
#     q_x = []
#     q_y = []
#     # first q element in list q is quarter of start angle
#     # second q element is quarter of end angle
#     # now determine the quarters to compute
#     q = []
#     # 0 - 90 degrees = 12 o clock to 3 o clock = 0.0 - math.pi/2 --> q==1
#     # 90 - 180 degrees = math.pi/2 - math.pi --> q==2
#     # 180 - 270 degrees = math.pi - math.pi/2*3 --> q==3
#     # 270 - 360 degrees = math.pi/2*3 - math.pi*2 --> q==4
#     j = 0
#     for i in [start, end]:
#         angle = i
#         if angle<math.pi/2:
#             q.append(1)
#             # compute the minimum x and y-axis value for plotting
#             q_x.append(int(round(math.sin(angle)*radius)))
#             q_y.append(int(round(math.cos(angle)*radius)))
#             if j==1 and angle==0:
#                 xy[1] = [0,-radius] # 90 degrees
#         elif angle>=math.pi/2 and angle<math.pi:
#             q.append(2)
#             # compute the minimum x and y-axis value for plotting
#             q_x.append(int(round(math.cos(angle-math.pi/2)*radius)))
#             q_y.append(int(round(math.sin(angle-math.pi/2)*radius)))
#             if j==1 and angle==math.pi/2:
#                 xy[1] = [radius,0] # 90 degrees
#         elif angle>=math.pi and angle<math.pi/2*3:
#             q.append(3)
#             # compute the minimum x and y-axis value for plotting
#             q_x.append(int(round(math.sin(angle-math.pi)*radius)))
#             q_y.append(int(round(math.cos(angle-math.pi)*radius)))
#             if j==1 and angle==math.pi:
#                 xy[1] = [0, radius]
#         else:
#             q.append(4)
#             # compute the minimum x and y-axis value for plotting
#             q_x.append(int(round(math.cos(angle-math.pi/2*3)*radius)))
#             q_y.append(int(round(math.sin(angle-math.pi/2*3)*radius)))
#             if j==1 and angle==math.pi/2*3:
#                 xy[1] = [-radius, 0]
#         j = j + 1
#     # print "q", q, "q_x", q_x, "q_y", q_y
#     quarters = []
#     sq = q[0]
#     while 1:
#         quarters.append(sq)
#         if q[1] == sq and start<end or q[1] == sq and start>end and q[0]!=q[1]:
#             break # we reach the final end quarter
#         elif q[1] == sq and start>end:
#             quarters.extend([(sq+1)%5, (sq+2)%5, (sq+3)%5, (sq+4)%5])
#             break
#         else:
#             sq = sq + 1
#             if sq>4:
#                 sq = 1
#     # print "quarters", quarters
#     switch = 3 - (2 * radius)
#     points = []
#     points1 = set()
#     points2 = set()
#     points3 = set()
#     points4 = set()
#     #
#     x = 0
#     y = int(round(radius))
#     # first quarter/octant starts clockwise at 12 o'clock
#     while x <= y:
#         if 1 in quarters:
#             if not (1 in q):
#                 # add all points of the quarter completely
#                 # first quarter first octant
#                 points1.add((x,-y))
#                 # first quarter 2nd octant
#                 points1.add((y,-x))
#             else:
#                 # start or end point in this quarter?
#                 if q[0] == 1:
#                     # start point
#                     if q_x[0]<=x and q_y[0]>=abs(-y) and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
#                         # first quarter first octant
#                         points1.add((x,-y))
#                         if -y<xy[0][1]:
#                             xy[0] = [x,-y]
#                         elif -y==xy[0][1]:
#                             if x<xy[0][0]:
#                                 xy[0] = [x,-y]
#                     if q_x[0]<=y and q_y[0]>=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=abs(-x) and q_y[1]<=abs(-x):
#                         # first quarter 2nd octant
#                         points1.add((y,-x))
#                         if -x<xy[0][1]:
#                             xy[0] = [y,-x]
#                         elif -x==xy[0][1]:
#                             if y<xy[0][0]:
#                                 xy[0] = [y,-x]
#                 if q[1] == 1:
#                     # end point
#                     if q_x[1]>=x and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
#                         # first quarter first octant
#                         points1.add((x,-y))
#                         if x>xy[1][0]:
#                             xy[1] = [x,-y]
#                         elif x==xy[1][0]:
#                             if -y>xy[1][1]:
#                                 xy[1] = [x,-y]
#                     if q_x[1]>=y and q_y[1]<=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=abs(-x) and q_y[1]<=abs(-x):
#                         # first quarter 2nd octant
#                         points1.add((y,-x))
#                         if y>xy[1][0]:
#                             xy[1] = [y,-x]
#                         elif y==xy[1][0]:
#                             if -x>xy[1][1]:
#                                 xy[1] = [y,-x]
#         if 2 in quarters:
#             if not (2 in q):
#                 # add all points of the quarter completely
#                 # second quarter 3rd octant
#                 points2.add((y,x))
#                 # second quarter 4.octant
#                 points2.add((x,y))
#             else:
#                 # start or end point in this quarter?
#                 if q[0] == 2:
#                     # start point
#                     if q_x[0]>=y and q_y[0]<=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
#                         # second quarter 3rd octant
#                         points2.add((y,x))
#                         if y>xy[0][0]:
#                             xy[0] = [y,x]
#                         elif y==xy[0][0]:
#                             if x<xy[0][1]:
#                                 xy[0] = [y,x]
#                     if q_x[0]>=x and q_y[0]<=y and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
#                         # second quarter 4.octant
#                         points2.add((x,y))
#                         if x>xy[0][0]:
#                             xy[0] = [x,y]
#                         elif x==xy[0][0]:
#                             if y<xy[0][1]:
#                                 xy[0] = [x,y]
#                 if q[1] == 2:
#                     # end point
#                     if q_x[1]<=y and q_y[1]>=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
#                         # second quarter 3rd octant
#                         points2.add((y,x))
#                         if x>xy[1][1]:
#                             xy[1] = [y,x]
#                         elif x==xy[1][1]:
#                             if y<xy[1][0]:
#                                 xy[1] = [y,x]
#                     if q_x[1]<=x and q_y[1]>=y and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
#                         # second quarter 4.octant
#                         points2.add((x,y))
#                         if y>xy[1][1]:
#                             xy[1] = [x,y]
#                         elif x==xy[1][1]:
#                             if x<xy[1][0]:
#                                 xy[1] = [x,y]
#         if 3 in quarters:
#             if not (3 in q):
#                 # add all points of the quarter completely
#                 # third quarter 5.octant
#                 points3.add((-x,y))
#                 # third quarter 6.octant
#                 points3.add((-y,x))
#             else:
#                 # start or end point in this quarter?
#                 if q[0] == 3:
#                     # start point
#                     if q_x[0]<=x and q_y[0]>=abs(y) and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
#                         # third quarter 5.octant
#                         points3.add((-x,y))
#                         if y>xy[0][1]:
#                             xy[0] = [-x,y]
#                         elif y==xy[0][1]:
#                             if -x>xy[0][0]:
#                                 xy[0] = [-x,y]
#                     if q_x[0]<=y and q_y[0]>=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=x and q_y[1]<=x:
#                         # third quarter 6.octant
#                         points3.add((-y,x))
#                         if x>xy[0][1]:
#                             xy[0] = [-y,x]
#                         elif x==xy[0][1]:
#                             if -y>xy[0][0]:
#                                 xy[0] = [-y,x]
#                 if q[1] == 3:
#                     # end point
#                     if q_x[1]>=x and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
#                         # third quarter 5.octant
#                         points3.add((-x,y))
#                         if -x<xy[1][0]:
#                             xy[1] = [-x,y]
#                         elif -x==xy[1][0]:
#                             if y<xy[1][1]:
#                                 xy[1] = [-x,y]
#                     if q_x[1]>=y and q_y[1]<=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=x and q_y[1]<=x:
#                         # third quarter 6.octant
#                         points3.add((-y,x))
#                         if -y<xy[1][0]:
#                             xy[1] = [-y,x]
#                         elif -y==xy[1][0]:
#                             if x<xy[1][1]:
#                                 xy[1] = [-y,x]
#         if 4 in quarters:
#             if not (4 in q):
#                 # add all points of the quarter completely
#                 # fourth quarter 7.octant
#                 points4.add((-y,-x))
#                 # fourth quarter 8.octant
#                 points4.add((-x,-y))
#             else:
#                 # start or end point in this quarter?
#                 if q[0] == 4:
#                     # start point
#                     if q_x[0]>=y and q_y[0]<=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
#                         # fourth quarter 7.octant
#                         points4.add((-y,-x))
#                         if -y<xy[0][0]:
#                             xy[0] = [-y,-x]
#                         elif -y==xy[0][0]:
#                             if -x>xy[0][1]:
#                                 xy[0] = [-y,-x]
#                     if q_x[0]>=x and q_y[0]<=abs(-y) and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
#                         # fourth quarter 8.octant
#                         points4.add((-x,-y))
#                         if -x<xy[0][0]:
#                             xy[0] = [-x,-y]
#                         elif -x==xy[0][0]:
#                             if -y>xy[0][1]:
#                                 xy[0] = [-x,-y]
#                 if q[1] == 4:
#                     # end point
#                     if q_x[1]<=y and q_y[1]>=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y  and q_y[0]<=x and q_y[1]>=x:
#                         # fourth quarter 7.octant
#                         points4.add((-y,-x))
#                         if -x<xy[1][1]:
#                             xy[1] = [-y,-x]
#                         elif -x==xy[1][1]:
#                             if -y>xy[1][0]:
#                                 xy[1] = [-y,-x]
#                     if q_x[1]<=x and q_y[1]>=abs(-y) and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
#                         # fourth quarter 8.octant
#                         points4.add((-x,-y))
#                         if -y<xy[1][1]:
#                             xy[1] = [-x,-y]
#                         elif -y==xy[1][1]:
#                             if -x>xy[1][0]:
#                                 xy[1] = [-x,-y]
#         if switch < 0:
#             switch = switch + (4 * x) + 6
#         else:
#             switch = switch + (4 * (x - y)) + 10
#             y = y - 1
#         x = x + 1
#
#     if 1 in quarters:
#         points1_s = list(points1)
#         # points1_s.sort() # if for some reason you need them sorted
#         points.extend(points1_s)
#     if 2 in quarters:
#         points2_s = list(points2)
#         # points2_s.sort() # if for some reason you need them sorted
#         # points2_s.reverse() # # if for some reason you need in right order
#         points.extend(points2_s)
#     if 3 in quarters:
#         points3_s = list(points3)
#         # points3_s.sort()
#         # points3_s.reverse()
#         points.extend(points3_s)
#     if 4 in quarters:
#         points4_s = list(points4)
#         # points4_s.sort()
#         points.extend(points4_s)
#
#
#     for i in points:
#         matrix[i[1]-1][i[0]] = 1
#     return matrix
#
#
#     # return points, xy
#
# import math
# import matplotlib.pyplot as plt
# import numpy as np
# size = 100
# matrix = np.zeros((size, size))
# matrix = circle_arc(matrix, start=-math.pi/2, end = 0)
#
# # for i in plot_list[0]:
# #     matrix[i[1]-1][i[0]] = 1
# #     # plt.scatter(i[0], i[1])
# plt.imshow(matrix)
# plt.show()

def circle_arc(radius, start, end, clockwise=True):
    """Python implementation of the modified Bresenham algorithm
    for complete circles, arcs and pies
    radius: radius of the circle in pixels
    start and end are angles in radians
    function will return a list of points (tuple coordinates)
    and the coordinates of the start and end point in a list xy
    """
    # round it to avoid rounding errors and wrong drawn pie slices
    start = math.radians(round(math.degrees(start)))
    end = math.radians(round(math.degrees(end)))
    if start>=math.pi*2:
        start = math.radians(math.degrees(start)%360)
    if end>=math.pi*2:
        end = math.radians(math.degrees(end)%360)
    # always clockwise drawing, if anti-clockwise drawing desired
    # exchange start and end
    if not clockwise:
        s = start
        start = end
        end = s
    # determination which quarters and octants are necessary
    # init vars
    xy = [[0,0], [0,0]] # to locate actual start and end point for pies
    # the x/y border value for drawing the points
    q_x = []
    q_y = []
    # first q element in list q is quarter of start angle
    # second q element is quarter of end angle
    # now determine the quarters to compute
    q = []
    # 0 - 90 degrees = 12 o clock to 3 o clock = 0.0 - math.pi/2 --> q==1
    # 90 - 180 degrees = math.pi/2 - math.pi --> q==2
    # 180 - 270 degrees = math.pi - math.pi/2*3 --> q==3
    # 270 - 360 degrees = math.pi/2*3 - math.pi*2 --> q==4
    j = 0
    for i in [start, end]:
        angle = i
        if angle<math.pi/2:
            q.append(1)
            # compute the minimum x and y-axis value for plotting
            q_x.append(int(round(math.sin(angle)*radius)))
            q_y.append(int(round(math.cos(angle)*radius)))
            if j==1 and angle==0:
                xy[1] = [0,-radius] # 90 degrees
        elif angle>=math.pi/2 and angle<math.pi:
            q.append(2)
            # compute the minimum x and y-axis value for plotting
            q_x.append(int(round(math.cos(angle-math.pi/2)*radius)))
            q_y.append(int(round(math.sin(angle-math.pi/2)*radius)))
            if j==1 and angle==math.pi/2:
                xy[1] = [radius,0] # 90 degrees
        elif angle>=math.pi and angle<math.pi/2*3:
            q.append(3)
            # compute the minimum x and y-axis value for plotting
            q_x.append(int(round(math.sin(angle-math.pi)*radius)))
            q_y.append(int(round(math.cos(angle-math.pi)*radius)))
            if j==1 and angle==math.pi:
                xy[1] = [0, radius]
        else:
            q.append(4)
            # compute the minimum x and y-axis value for plotting
            q_x.append(int(round(math.cos(angle-math.pi/2*3)*radius)))
            q_y.append(int(round(math.sin(angle-math.pi/2*3)*radius)))
            if j==1 and angle==math.pi/2*3:
                xy[1] = [-radius, 0]
        j = j + 1
    # print "q", q, "q_x", q_x, "q_y", q_y
    quarters = []
    sq = q[0]
    while 1:
        quarters.append(sq)
        if q[1] == sq and start<end or q[1] == sq and start>end and q[0]!=q[1]:
            break # we reach the final end quarter
        elif q[1] == sq and start>end:
            quarters.extend([(sq+1)%5, (sq+2)%5, (sq+3)%5, (sq+4)%5])
            break
        else:
            sq = sq + 1
            if sq>4:
                sq = 1
    # print "quarters", quarters
    switch = 3 - (2 * radius)
    points = []
    points1 = set()
    points2 = set()
    points3 = set()
    points4 = set()
    #
    x = 0
    y = int(round(radius))
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        if 1 in quarters:
            if not (1 in q):
                # add all points of the quarter completely
                # first quarter first octant
                points1.add((x,-y))
                # first quarter 2nd octant
                points1.add((y,-x))
            else:
                # start or end point in this quarter?
                if q[0] == 1:
                    # start point
                    if q_x[0]<=x and q_y[0]>=abs(-y) and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
                        # first quarter first octant
                        points1.add((x,-y))
                        if -y<xy[0][1]:
                            xy[0] = [x,-y]
                        elif -y==xy[0][1]:
                            if x<xy[0][0]:
                                xy[0] = [x,-y]
                    if q_x[0]<=y and q_y[0]>=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=abs(-x) and q_y[1]<=abs(-x):
                        # first quarter 2nd octant
                        points1.add((y,-x))
                        if -x<xy[0][1]:
                            xy[0] = [y,-x]
                        elif -x==xy[0][1]:
                            if y<xy[0][0]:
                                xy[0] = [y,-x]
                if q[1] == 1:
                    # end point
                    if q_x[1]>=x and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
                        # first quarter first octant
                        points1.add((x,-y))
                        if x>xy[1][0]:
                            xy[1] = [x,-y]
                        elif x==xy[1][0]:
                            if -y>xy[1][1]:
                                xy[1] = [x,-y]
                    if q_x[1]>=y and q_y[1]<=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=abs(-x) and q_y[1]<=abs(-x):
                        # first quarter 2nd octant
                        points1.add((y,-x))
                        if y>xy[1][0]:
                            xy[1] = [y,-x]
                        elif y==xy[1][0]:
                            if -x>xy[1][1]:
                                xy[1] = [y,-x]
        if 2 in quarters:
            if not (2 in q):
                # add all points of the quarter completely
                # second quarter 3rd octant
                points2.add((y,x))
                # second quarter 4.octant
                points2.add((x,y))
            else:
                # start or end point in this quarter?
                if q[0] == 2:
                    # start point
                    if q_x[0]>=y and q_y[0]<=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
                        # second quarter 3rd octant
                        points2.add((y,x))
                        if y>xy[0][0]:
                            xy[0] = [y,x]
                        elif y==xy[0][0]:
                            if x<xy[0][1]:
                                xy[0] = [y,x]
                    if q_x[0]>=x and q_y[0]<=y and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
                        # second quarter 4.octant
                        points2.add((x,y))
                        if x>xy[0][0]:
                            xy[0] = [x,y]
                        elif x==xy[0][0]:
                            if y<xy[0][1]:
                                xy[0] = [x,y]
                if q[1] == 2:
                    # end point
                    if q_x[1]<=y and q_y[1]>=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
                        # second quarter 3rd octant
                        points2.add((y,x))
                        if x>xy[1][1]:
                            xy[1] = [y,x]
                        elif x==xy[1][1]:
                            if y<xy[1][0]:
                                xy[1] = [y,x]
                    if q_x[1]<=x and q_y[1]>=y and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
                        # second quarter 4.octant
                        points2.add((x,y))
                        if y>xy[1][1]:
                            xy[1] = [x,y]
                        elif x==xy[1][1]:
                            if x<xy[1][0]:
                                xy[1] = [x,y]
        if 3 in quarters:
            if not (3 in q):
                # add all points of the quarter completely
                # third quarter 5.octant
                points3.add((-x,y))
                # third quarter 6.octant
                points3.add((-y,x))
            else:
                # start or end point in this quarter?
                if q[0] == 3:
                    # start point
                    if q_x[0]<=x and q_y[0]>=abs(y) and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
                        # third quarter 5.octant
                        points3.add((-x,y))
                        if y>xy[0][1]:
                            xy[0] = [-x,y]
                        elif y==xy[0][1]:
                            if -x>xy[0][0]:
                                xy[0] = [-x,y]
                    if q_x[0]<=y and q_y[0]>=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=x and q_y[1]<=x:
                        # third quarter 6.octant
                        points3.add((-y,x))
                        if x>xy[0][1]:
                            xy[0] = [-y,x]
                        elif x==xy[0][1]:
                            if -y>xy[0][0]:
                                xy[0] = [-y,x]
                if q[1] == 3:
                    # end point
                    if q_x[1]>=x and len(quarters)>1 or q_x[0]<=x and q_x[1]>=x:
                        # third quarter 5.octant
                        points3.add((-x,y))
                        if -x<xy[1][0]:
                            xy[1] = [-x,y]
                        elif -x==xy[1][0]:
                            if y<xy[1][1]:
                                xy[1] = [-x,y]
                    if q_x[1]>=y and q_y[1]<=x and len(quarters)>1 or q_x[0]<=y and q_x[1]>=y and q_y[0]>=x and q_y[1]<=x:
                        # third quarter 6.octant
                        points3.add((-y,x))
                        if -y<xy[1][0]:
                            xy[1] = [-y,x]
                        elif -y==xy[1][0]:
                            if x<xy[1][1]:
                                xy[1] = [-y,x]
        if 4 in quarters:
            if not (4 in q):
                # add all points of the quarter completely
                # fourth quarter 7.octant
                points4.add((-y,-x))
                # fourth quarter 8.octant
                points4.add((-x,-y))
            else:
                # start or end point in this quarter?
                if q[0] == 4:
                    # start point
                    if q_x[0]>=y and q_y[0]<=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y and q_y[0]<=x and q_y[1]>=x:
                        # fourth quarter 7.octant
                        points4.add((-y,-x))
                        if -y<xy[0][0]:
                            xy[0] = [-y,-x]
                        elif -y==xy[0][0]:
                            if -x>xy[0][1]:
                                xy[0] = [-y,-x]
                    if q_x[0]>=x and q_y[0]<=abs(-y) and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
                        # fourth quarter 8.octant
                        points4.add((-x,-y))
                        if -x<xy[0][0]:
                            xy[0] = [-x,-y]
                        elif -x==xy[0][0]:
                            if -y>xy[0][1]:
                                xy[0] = [-x,-y]
                if q[1] == 4:
                    # end point
                    if q_x[1]<=y and q_y[1]>=x and len(quarters)>1 or q_x[0]>=y and q_x[1]<=y  and q_y[0]<=x and q_y[1]>=x:
                        # fourth quarter 7.octant
                        points4.add((-y,-x))
                        if -x<xy[1][1]:
                            xy[1] = [-y,-x]
                        elif -x==xy[1][1]:
                            if -y>xy[1][0]:
                                xy[1] = [-y,-x]
                    if q_x[1]<=x and q_y[1]>=abs(-y) and len(quarters)>1 or q_x[0]>=x and q_x[1]<=x and q_y[0]<=y and q_y[1]>=y:
                        # fourth quarter 8.octant
                        points4.add((-x,-y))
                        if -y<xy[1][1]:
                            xy[1] = [-x,-y]
                        elif -y==xy[1][1]:
                            if -x>xy[1][0]:
                                xy[1] = [-x,-y]
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1

    if 1 in quarters:
        points1_s = list(points1)
        # points1_s.sort() # if for some reason you need them sorted
        points.extend(points1_s)
    if 2 in quarters:
        points2_s = list(points2)
        # points2_s.sort() # if for some reason you need them sorted
        # points2_s.reverse() # # if for some reason you need in right order
        points.extend(points2_s)
    if 3 in quarters:
        points3_s = list(points3)
        # points3_s.sort()
        # points3_s.reverse()
        points.extend(points3_s)
    if 4 in quarters:
        points4_s = list(points4)
        # points4_s.sort()
        points.extend(points4_s)
    return points, xy


import math
import matplotlib.pyplot as plt
import numpy as np
size = 40
# matrix = np.zeros((size, size))
matrix = circle_arc(size, start=math.pi, end = 2*math.pi-0.1)

for i in matrix[0]:
    # matrix[i[1]-1][i[0]] = 1
    plt.scatter(i[0], i[1])
# plt.imshow(matrix)
plt.show()
