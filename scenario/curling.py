from olympics_engine.core import OlympicsBase
from olympics_engine.viewer import Viewer, debug
from olympics_engine.objects import Ball, Agent

import numpy as np
import math
import pygame
import sys


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
        self.wall_restitution = 1
        self.circle_restitution = 1
        self.print_log = False
        self.tau = 0.1

        self.draw_obs = True
        self.show_traj = False

        self.start_pos = [300,150]
        self.start_init_obs = 90

        self.num_purple = 1
        self.num_green = 0
        self.max_n = 3
        self.temp_winner = -1
        self.round_max_step = 100
        self.round_step = 0

        self.stop_threshold = 1e-2

    def reset(self):
        self.init_state()
        self.step_cnt = 0
        self.done = False
        self.release = False

        self.gamma = 0.98  # for longjump env

        self.viewer = Viewer(self.view_setting)
        self.display_mode=False

        self.current_team = 0
        obs = self.get_obs()

        return [obs, np.zeros_like(obs)]

    def _reset_round(self):
        self.current_team = 1-self.current_team
        #convert last agent to ball
        if len(self.agent_list) != 0:
            last_agent = self.agent_list[-1]
            last_ball = Ball(mass = last_agent.mass, r = last_agent.r, position = self.agent_pos[-1],
                             color = last_agent.color)
            last_ball.alive = False
            self.agent_list[-1] = last_ball

        #add new agent
        if self.current_team == 0:
            #team purple
            new_agent_color = 'purple'
            self.num_purple += 1

        elif self.current_team == 1:
            new_agent_color = 'green'
            self.num_green += 1

        else:
            raise NotImplementedError

        new_agent = Agent(mass = 1, r= 15, position = self.start_pos, color = new_agent_color,
                          vis = 300, vis_clear = 12)

        self.agent_list.append(new_agent)
        self.agent_init_pos[-1] = self.start_pos
        new_boundary = self.get_obs_boundaray(self.start_pos, 15, 300)
        self.obs_boundary_init.append(new_boundary)
        self.agent_num += 1

        self.agent_pos.append(self.agent_init_pos[-1])
        self.agent_v.append([0,0])
        self.agent_accel.append([0,0])
        init_obs = self.start_init_obs
        self.agent_theta.append([init_obs])
        self.agent_record.append([self.agent_init_pos[-1]])

        self.release = False
        self.gamma = 0.98

        self.round_step = 0

        return self.get_obs()




    def cross_detect(self):
        """
        check whether the agent has reach the cross(final) line
        :return:
        """
        for agent_idx in range(self.agent_num):

            agent = self.agent_list[agent_idx]
            if agent.type != 'agent':
                continue

            for object_idx in range(len(self.map['objects'])):
                object = self.map['objects'][object_idx]

                if not object.can_pass():
                    continue
                else:
                    #print('object = ', object.type)
                    if object.color == 'red' and object.check_cross(self.agent_pos[agent_idx], agent.r):
                        # print('agent type = ', agent.type)
                        agent.alive = False
                        #agent.color = 'red'
                        self.gamma = 0.95            #this will change the gamma for the whole env, so need to change if dealing with multi-agent
                        self.release = True
                        self.round_countdown = self.round_max_step-self.round_step
                    # if the ball hasnot pass the cross, the relase will be True again in the new round
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

        actions_list = [actions_list[self.current_team]]

        #previous_pos = self.agent_pos
        action_list = self.check_action(actions_list)
        if self.release:
            input_action = [None for _ in range(len(self.agent_list))]       #if jump, stop actions
        else:
            input_action = action_list

        self.stepPhysics(input_action, self.step_cnt)

        self.cross_detect()
        self.step_cnt += 1
        self.round_step += 1

        obs_next = self.get_obs()


        done = self.is_terminal()

        if not done:
            round_end, end_info = self._round_terminal()
            if round_end:

                if end_info is not None:
                    #clean the last agent
                    del self.agent_list[-1]
                    del self.agent_pos[-1]
                    del self.agent_v[-1]
                    del self.agent_theta[-1]
                    del self.agent_accel[-1]
                    self.agent_num -= 1

                self.temp_winner, min_d = self.current_winner()
                step_reward = [1,0.] if self.temp_winner == 0 else [0., 1]          #score for each round
                obs_next = self._reset_round()

            else:
                step_reward = [0., 0.]

        else:
            self.final_winner, min_d = self.current_winner()
            step_reward = [100., 0] if self.final_winner == 0 else [0., 100]

        if self.current_team == 0:
            obs_next = [obs_next[0], np.zeros_like(obs_next[0])-1]
        else:
            obs_next = [np.zeros_like(obs_next[0])-1, obs_next[0]]


        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def get_obs_encode(self):
        obs = self.get_obs()
        if self.current_team == 0:
            return [obs, np.zeros_like(obs)]
        else:
            return [np.zeros_like(obs), obs]



    def get_reward(self):

        center = [300, 500]
        pos = self.agent_pos[0]
        distance = math.sqrt((pos[0]-center[0])**2 + (pos[1]-center[1])**2)
        return [distance]

    def is_terminal(self):

        # if self.step_cnt >= self.max_step:
        #     return True

        if (self.num_green + self.num_purple == self.max_n*2):
            if not self.release and self.round_step > self.round_max_step:
                return True

            if self.release:
                L = []
                for agent_idx in range(self.agent_num):
                    if (self.agent_v[agent_idx][0] ** 2 + self.agent_v[agent_idx][1] ** 2) < self.stop_threshold:
                        L.append(True)
                    else:
                        L.append(False)
                return all(L)
        else:
            return False

        # for agent_idx in range(self.agent_num):
        #     if self.agent_list[agent_idx].color == 'red' and (
        #             self.agent_v[agent_idx][0] ** 2 + self.agent_v[agent_idx][1] ** 2) < 1e-5:
        #         return True

    def _round_terminal(self):

        if self.round_step > self.round_max_step and not self.release:      #after maximum round step the agent has not released yet
            return True, -1

        #agent_idx = -1
        L = []
        for agent_idx in range(self.agent_num):
            if (not self.agent_list[agent_idx].alive) and (self.agent_v[agent_idx][0] ** 2 +
                                                           self.agent_v[agent_idx][1] ** 2) < self.stop_threshold:
                L.append(True)
            else:
                L.append(False)

        return all(L), None

    def current_winner(self):

        center = [300, 500]
        min_dist = 1e4
        win_team = -1
        for i, agent in enumerate(self.agent_list):
            pos = self.agent_pos[i]
            distance = math.sqrt((pos[0]-center[0])**2 + (pos[1]-center[1])**2)
            if distance < min_dist:
                win_team = 0 if agent.color == 'purple' else 1
                min_dist = distance

        return win_team, min_dist



    def render(self, info=None):

        if not self.display_mode:
            self.viewer.set_mode()
            self.display_mode=True

        self.viewer.draw_background()
        # 先画map; ball在map之上
        for w in self.map['objects']:
            self.viewer.draw_map(w)

        self.viewer.draw_ball(self.agent_pos, self.agent_list)
        if self.show_traj:
            self.get_trajectory()
            self.viewer.draw_trajectory(self.agent_record, self.agent_list)
        self.viewer.draw_direction(self.agent_pos, self.agent_accel)
        #self.viewer.draw_map()

        if self.draw_obs:
            self.viewer.draw_obs(self.obs_boundary, [self.agent_list[-1]])

            if self.current_team == 0:
                self.viewer.draw_view(self.obs_list, [self.agent_list[-1]])
            else:
                self.viewer.draw_view([None, self.obs_list[0]], [None, self.agent_list[-1]])

        debug('Agent 0', x=570, y=110)
        debug("No. throws left: ", x=470, y=140)
        debug("{}".format(self.max_n - self.num_purple), x=590, y=140)
        debug('Agent 1', x=640, y=110)
        debug("{}".format(self.max_n - self.num_green), x=660, y=140)
        debug("Current winner:", x=470, y=170)

        if self.temp_winner == 0:
            debug("*", x=590, y=170)
        elif self.temp_winner == 1:
            debug("*", x=660, y=170)
        else:
            pass

        pygame.draw.line(self.viewer.background, start_pos=[470, 130], end_pos=[690, 130], color=[0, 0, 0])
        pygame.draw.line(self.viewer.background, start_pos=[565, 100], end_pos=[565, 190], color=[0, 0, 0])
        pygame.draw.line(self.viewer.background, start_pos=[630, 100], end_pos=[630, 190], color=[0, 0, 0])
        pygame.draw.line(self.viewer.background, start_pos=[470, 160], end_pos=[690, 160], color=[0, 0, 0])




        #draw energy bar
        #debug('agent remaining energy = {}'.format([i.energy for i in self.agent_list]), x=100)
        # self.viewer.draw_energy_bar(self.agent_list)


        # debug('mouse pos = '+ str(pygame.mouse.get_pos()))
        debug('Step: ' + str(self.step_cnt), x=30)

        if not self.release:
            countdown = self.round_max_step-self.round_step
        else:
            countdown = self.round_countdown

        debug("Countdown: {}".format(countdown), x=100)
        debug("Current winner: {}".format(self.temp_winner), x = 200)


        if info is not None:
            debug(info, x=100)


        for event in pygame.event.get():
            # 如果单击关闭窗口，则退出
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        #self.viewer.background.fill((255, 255, 255))



