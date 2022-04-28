import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
print(base_path)


from core import OlympicsBase
from objects import *
from tools.func import *
import time
import numpy as np
import matplotlib.pyplot as plt

gamemap = {'objects':[], 'agents':[]}

gamemap['objects'].append(Wall(init_pos = [[250, 500], [300, 0]], color = 'black'))
gamemap['objects'].append(Wall(init_pos = [[150, 100], [500, 60]], color = 'black'))

# gamemap['objects'].append(Wall(init_pos = [[200, 10], [100, 200]], color = 'black'))
# gamemap['objects'].append(Wall(init_pos = [[400, 10], [500, 200]], color = 'black'))
# gamemap['objects'].append(Wall(init_pos = [[500, 200], [100, 200]], color = 'black'))

gamemap['agents'].append(Agent(position = [300,26], mass=1, r=15, color='purple', vis=200, vis_clear=5))



gamemap['view'] = {'width': 600, 'height':600, 'edge': 50, "init_obs": [90]}


def point_rotate(center, point, theta):
    px = point[0] - center[0]
    py = point[1] - center[1]

    nx = [math.cos(theta * math.pi / 180), math.sin(theta * math.pi / 180)]
    ny = [-math.sin(theta * math.pi / 180), math.cos(theta * math.pi / 180)]
    new_x = px * nx[0] + py * nx[1]
    new_y = px * ny[0] + py * ny[1]
    return [new_x, new_y]

def DDA_line(matrix, draw_line, vis, vis_clear):
    size = int(vis/vis_clear)
    assert matrix.shape[0] == size
    if len(draw_line) == 1:
        point1 = draw_line[0]
        x1, y1 = point1
        y1 += vis/2
        x1 /= vis_clear
        y1 /= vis_clear

        x = x1+0.5
        y = y1+0.5
        matrix[size-int(x)][int(y)] = 1
        return matrix

    elif len(draw_line) == 2:
        point1, point2 = draw_line
    else:
        raise NotImplementedError

    x1,y1 = point1
    y1 += vis/2
    x1 /= vis_clear
    y1 /= vis_clear
    x2, y2 = point2
    y2 += vis/2
    x2 /= vis_clear
    y2 /= vis_clear

    dx = x2-x1
    dy = y2-y1

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    delta_x = float(dx/steps)
    delta_y = float(dy/steps)

    x = x1-0.5
    y = y1-0.5

    assert  0<=int(x)<=size-1
    assert 0<=int(y)<=size-1

    for i in range(0, int(steps + 1)):
        matrix[size-1-int(x)][int(y)] = 1
        x += delta_x
        y += delta_y

    return matrix








class env_test(OlympicsBase):
    def __init__(self, map=gamemap):
        super(env_test, self).__init__(map)

        self.gamma = 1  # v衰减系数
        self.restitution = 1
        self.print_log = False
        self.tau = 0.1
        self.draw_obs = True
        self.show_traj = False

    def check_overlap(self):
        pass

    def check_action(self, action_list):
        action = []
        for agent_idx in range(self.agent_num):
            if self.agent_list[agent_idx].type == 'agent':
                action.append(action_list[0])
                _ = action_list.pop(0)
            else:
                action.append(None)

        return action

    def step(self, actions_list):

        actions_list = self.check_action(actions_list)

        self.stepPhysics(actions_list, self.step_cnt)
        self.step_cnt += 1
        step_reward = 1 #self.get_reward()
        obs_next = self.get_obs()
        # obs_next = 1
        done = False #self.is_terminal()
        #check overlapping
        #self.check_overlap()
        self.get_obs2()

        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def get_obs2(self):
        self.obs_boundary = list()

        obs_list = list()

        for agent_idx, agent in enumerate(self.agent_list):
            if self.agent_list[agent_idx].type == 'ball':
                self.obs_boundary.append(None)
                obs_list.append(None)
                continue

            time_s = time.time()
            theta_copy = self.agent_theta[agent_idx][0]
            agent_pos = self.agent_pos
            agent_x, agent_y = agent_pos[agent_idx][0], agent_pos[agent_idx][1]
            theta = theta_copy
            position_init = agent.position_init

            visibility = self.agent_list[agent_idx].visibility
            v_clear = self.agent_list[agent_idx].visibility_clear
            # obs_map = np.zeros((visibility[0], visibility[1]))
            # obs_weight,obs_height = int(visibility[0]/v_clear[0]),int(visibility[1]/v_clear[1])
            obs_size = int(visibility / v_clear)

            # update_obs_boundary()
            agent_current_boundary = list()
            for b in self.obs_boundary_init[agent_idx]:
                m = b[0]
                n = b[1]
                # print("check b orig: ", b_x, b_y)
                vec_oo_ = (-agent_x, agent_y)
                vec = (-position_init[0], position_init[1])
                vec_o_a = (m, -n)
                # vec_oa = (vec_oo_[0]+vec_o_a[0], vec_oo_[1]+vec_o_a[1])
                vec_oa = (vec[0] + vec_o_a[0], vec[1] + vec_o_a[1])
                b_x_ = vec_oa[0]
                b_y_ = vec_oa[1]
                # print("check b: ", b_x_, b_y_)
                x_new, y_new = rotate2(b_x_, b_y_, theta)
                # print("check x_new: ", x_new, y_new)
                # x_new_ = x_new + agent_x
                # y_new_ = -y_new + agent_y
                x_new_ = x_new - vec_oo_[0]
                y_new_ = y_new - vec_oo_[1]
                agent_current_boundary.append([x_new_, -y_new_])
            self.obs_boundary.append(agent_current_boundary)

            #compute center of view
            view_center_x = agent_x + visibility/2*math.cos(theta*math.pi/180)      #start from agent x,y
            view_center_y = agent_y + visibility/2*math.sin(theta*math.pi/180)
            view_center = [view_center_x, view_center_y]
            #compute closest distance from view center to the line
            object_consider = []
            for c in self.map['objects']:
                if (c.type == "wall") or (c.type == "cross"):
                    closest_dist = distance_to_line(c.init_pos[0], c.init_pos[1], view_center)
                    if closest_dist <= visibility*math.sqrt(2)/2:
                        object_consider.append(c)
                else:
                    raise NotImplementedError

            obs_map = np.zeros((obs_size,obs_size))
            #rotating the object
            for obj in object_consider:
                if obj.type == 'wall' or obj.type == 'cross':
                    current_pos = obj.init_pos
                    obj.rotate_pos = []
                    for end_point in current_pos:
                        # px = end_point[0]-agent_x
                        # py = end_point[1]-agent_y
                        #
                        # nx = [math.cos(theta*math.pi/180), math.sin(theta*math.pi/180)]
                        # ny = [-math.sin(theta*math.pi/180), math.cos(theta*math.pi/180)]
                        # new_x = px*nx[0] + py*nx[1]
                        # new_y = px*ny[0] + py*ny[1]
                        # obj.rotate_pos.append([new_x, new_y])
                        obj.rotate_pos.append(point_rotate([agent_x, agent_y], end_point, theta))
                        # obj.rotate_pos.append(coordinate_rotate([agent_x, agent_y], -theta, end_point))
                else:
                    raise NotImplementedError

                #compute the intersection point
                intersect_p = []
                rotate_boundary = [[[0, -visibility/2],[0, visibility/2]],
                                   [[0,visibility/2],[visibility, visibility/2]],
                                   [[visibility, visibility/2], [visibility, -visibility/2]],
                                   [[visibility, -visibility/2],[0, -visibility/2]]]

                # obs_rotate_boundary = []              #debug rotate boundard
                # for line in self.obs_boundary:
                #     rotate_bound = [point_rotate([agent_x, agent_y], i, theta) for i in line]
                #     obs_rotate_boundary.append(rotate_bound)


                # for line in self.obs_boundary:
                for line in rotate_boundary:
                    _intersect_p = line_intersect(line1 = line, line2 = obj.rotate_pos, return_p=True)
                    if _intersect_p:
                        # intersect_p.append({"bound": line, "intersect point": intersect_p})
                        intersect_p.append(_intersect_p)

                draw_line = []
                if len(intersect_p) == 0:
                    #no intersection
                    continue
                elif len(intersect_p) == 1:
                    #one intersectoin, rotate it first
                    # intersect_p1 = intersect_p[0]
                    # c_p1 = [intersect_p1[0]-agent_x, intersect_p1[1]-agent_y]
                    # rotate_intersect_p1 = [c_p1[0]*nx[0]+c_p1[1]*nx[1], c_p1[0]*ny[0]+c_p1[1]*ny[1]]
                    # draw_line.append(rotate_intersect_p1)

                    draw_line.append(intersect_p[0])

                    if obj.rotate_pos[0][0]<visibility and abs(obj.rotate_pos[0][1]) < visibility/2:
                        draw_line.append(obj.rotate_pos[0])
                    elif obj.rotate_pos[1][0]<visibility and abs(obj.rotate_pos[1][1]) < visibility/2:
                        draw_line.append(obj.rotate_pos[1])
                    else:
                        #only one point in the view
                        pass
                        # raise NotImplementedError

                elif len(intersect_p) == 2:

                    draw_line.append(intersect_p[0])
                    draw_line.append(intersect_p[1])



                #start drawing the object
                obs_map = DDA_line(obs_map, draw_line, visibility, v_clear)


            print('a')






import random

env = env_test()


for _ in range(100):

    env.reset()
    env.render()
    # env.agent_theta[0][0] = 180
    done = False
    step = 0
    while not done:
        print('\n step = ', step)
        #if step < 10:
        #    action = [[random.randint(-100,200),random.randint(-30, 30)]]#, [2,1]]#, [2,2]]#, [2,1]]#[[2,1], [2,1]] + [ None for _ in range(4)]
        #else:
        #    action = [[random.randint(-100,200),random.randint(-30, 30)]]#, [2,1]]#, [2,1]]#, [2,random.randint(0,2)]] #[[2,1], [2,1]] + [None for _ in range(4)]
        #action1 = [random.randint(-100, 200), random.randint(-30, 30)]
        #action2 = [random.randint(-100, 200), random.randint(-30, 30)]
        action1 = [100+random.uniform(0,1)*10, 0]
        action2 = [100+random.uniform(0,1)*15, 0]
        action = [[200, 0] for _ in range(1)]
        action = [[0,0]]
        _,_,done, _ = env.step(action)

        print('agent v = ', env.agent_v)
        env.render()
        step += 1

        if step < 60:
            time.sleep(0.05)
        else:
            time.sleep(0.05)


