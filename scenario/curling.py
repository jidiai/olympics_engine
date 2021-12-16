from olympics_engine.core import OlympicsBase
from olympics_engine.viewer import Viewer

import math


def closest_point(l1, l2, point):
    """
    compute the coordinate of point on the line l1l2 closest to the given point, reference: https://en.wikipedia.org/wiki/Cramer%27s_rule
    :param l1: start pos
    :param l2: end pos
    :param point:
    :return:
    """
    A1 = l2[1] - l1[1]
    B1 = l1[0] - l2[0]
    C1 = (l2[1] - l1[1])*l1[0] + (l1[0] - l2[0])*l1[1]
    C2 = -B1 * point[0] + A1 * point[1]
    det = A1*A1 + B1*B1
    if det == 0:
        cx, cy = point
    else:
        cx = (A1*C1 - B1*C2)/det
        cy = (A1*C2 + B1*C1)/det

    return [cx, cy]

def distance_to_line(l1, l2, pos):
    closest_p = closest_point(l1, l2, pos)

    n = [pos[0] - closest_p[0], pos[1] - closest_p[1]]  # compute normal
    nn = n[0] ** 2 + n[1] ** 2
    nn_sqrt = math.sqrt(nn)
    cl1 = [l1[0] - pos[0], l1[1] - pos[1]]
    cl1_n = (cl1[0] * n[0] + cl1[1] * n[1]) / nn_sqrt

    return abs(cl1_n)


class curling(OlympicsBase):
    def __init__(self, map):
        super(curling, self).__init__(map)

        self.release = False
        self.gamma = 0.98
        self.restitution = 1
        self.print_log = False
        self.tau = 0.1

        self.draw_obs = True
        self.show_traj = True


    def reset(self):
        self.init_state()
        self.step_cnt = 0
        self.done = False
        self.release = False

        self.gamma = 0.98  # for longjump env

        self.viewer = Viewer(self.view_setting)
        self.display_mode=False

        return self.get_obs()


    def cross_detect(self):
        """
        check whether the agent has reach the cross(final) line
        :return:
        """
        for agent_idx in range(self.agent_num):

            agent = self.agent_list[agent_idx]
            for object_idx in range(len(self.map['objects'])):
                object = self.map['objects'][object_idx]

                if not object.can_pass():
                    continue
                else:
                    #print('object = ', object.type)
                    if object.color == 'red' and object.check_cross(self.agent_pos[agent_idx], agent.r):

                        agent.color = 'red'
                        self.gamma = 0.95            #this will change the gamma for the whole env, so need to change if dealing with multi-agent
                        self.release = True

    def check_action(self, action_list):
        action = []
        for agent_idx in range(len(self.agent_list)):
            if self.agent_list[agent_idx].type == 'agent':
                action.append(action_list[0])
                _ = action_list.pop(0)
            else:
                action.append(None)

        return action



    def step(self, actions_list):
        previous_pos = self.agent_pos
        action_list = self.check_action(actions_list)
        if self.release:
            input_action = [None for _ in range(len(self.agent_list))]       #if jump, stop actions
        else:
            input_action = action_list

        self.stepPhysics(input_action, self.step_cnt)

        self.cross_detect()
        self.step_cnt += 1

        obs_next = self.get_obs()

        done = self.is_terminal()
        if not done:
            step_reward = [0.]
        else:
            step_reward = self.get_reward()
        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def get_reward(self):

        center = [300, 500]
        pos = self.agent_pos[0]
        distance = math.sqrt((pos[0]-center[0])**2 + (pos[1]-center[1])**2)
        return [distance]

    def is_terminal(self):

        if self.step_cnt >= self.max_step:
            return True

        for agent_idx in range(self.agent_num):
            if self.agent_list[agent_idx].color == 'red' and (
                    self.agent_v[agent_idx][0] ** 2 + self.agent_v[agent_idx][1] ** 2) < 1e-5:
                return True





