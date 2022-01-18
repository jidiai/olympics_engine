from olympics_engine.core import OlympicsBase
from olympics_engine.viewer import Viewer, debug
import pygame
import sys
import math
import copy

def point2point(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class billiard(OlympicsBase):
    def __init__(self, map):
        super(billiard, self).__init__(map)

        self.gamma = 0.99  # v衰减系数
        self.wall_restitution = 0.8
        self.circle_restitution = 0.8
        self.print_log = False
        self.tau = 0.1

        self.draw_obs = True
        self.show_traj = False

        self.dead_agent_list = []
        self.max_step = 500
        self.original_num_ball = len(self.agent_list)
        self.white_ball_in = False

        self.total_reward = 0

    def reset(self):
        self.agent_num = 0
        self.agent_list = []
        self.agent_init_pos = []
        self.agent_pos = []
        self.agent_previous_pos = []
        self.agent_v = []
        self.agent_accel = []
        self.agent_theta = []
        self.obs_boundary_init = list()
        self.obs_boundary = self.obs_boundary_init

        self.generate_map(self.map)
        self.merge_map()

        self.set_seed()
        self.init_state()
        self.step_cnt = 0
        self.done = False

        self.viewer = Viewer(self.view_setting)
        self.display_mode=False

        self.white_ball_in = False
        self.dead_agent_list = []
        self.total_reward = 0

        return self.get_obs()

    def check_overlap(self):
        pass

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

        actions_list = self.check_action(actions_list)

        self.stepPhysics(actions_list, self.step_cnt)

        self.cross_detect(self.agent_pos)

        done = self.is_terminal()
        self.step_cnt += 1
        step_reward = self.get_reward()
        self.total_reward += step_reward[0]
        obs_next = self.get_obs()

        self.change_inner_state()

        self.clear_agent()
        #check overlapping
        #self.check_overlap()

        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def cross_detect(self, new_pos):
        finals = []
        for object_idx in range(len(self.map['objects'])):
            object = self.map['objects'][object_idx]
            if object.can_pass() and object.color == 'blue':
                #arc_pos = object.init_pos
                finals.append(object)

        for agent_idx in range(len(self.agent_list)):
            agent = self.agent_list[agent_idx]
            agent_new_pos = new_pos[agent_idx]
            for final in finals:
                center = (final.init_pos[0] + 0.5*final.init_pos[2], final.init_pos[1]+0.5*final.init_pos[3])
                arc_r = final.init_pos[2]/2

                if final.check_radian(agent_new_pos, [0,0],0):
                    l = point2point(agent_new_pos, center)
                    if abs(l - arc_r) <= agent.r:
                        agent.color = 'blue'
                        agent.finished = True
                        agent.alive = False
                        self.dead_agent_list.append(agent_idx)

    def clear_agent(self):
        if len(self.dead_agent_list) == 0:
            return
        index_add_on = 0
        for idx in self.dead_agent_list:
            del self.agent_list[idx-index_add_on]
            del self.agent_pos[idx-index_add_on]
            del self.agent_v[idx-index_add_on]
            del self.agent_theta[idx-index_add_on]
            del self.agent_accel[idx-index_add_on]
            index_add_on += 1
        self.agent_num -= len(self.dead_agent_list)
        self.dead_agent_list = []


    def is_terminal(self):

        if self.step_cnt >= self.max_step:
            return True

        for agent_idx in range(len(self.agent_list)):
            if (self.agent_list[agent_idx].type == 'agent') and (self.agent_list[agent_idx].finished):
                self.white_ball_in = True
                return True

        if len(self.agent_list) == 1:
            return True

        return False

    def get_reward(self):
        if len(self.agent_list) == 1 and not self.white_ball_in:
            return [500.]

        reward = [-0.1]
        if not self.white_ball_in:
            reward[0] += len(self.dead_agent_list)*100
        else:
            reward[0] -= 50

        return reward

        # if self.white_ball_in:
        #     self.white_ball_in = False
        #     reward[0] -= 100
        #
        #
        # elif len(self.agent_list) == 1:
        #     return [100.]
        # else:
        #     return [(self.num_ball - self.agent_num)*10]


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
            self.viewer.draw_obs(self.obs_boundary, self.agent_list)
            self.viewer.draw_view(self.obs_list, self.agent_list)

        #draw energy bar
        #debug('agent remaining energy = {}'.format([i.energy for i in self.agent_list]), x=100)
        self.viewer.draw_energy_bar(self.agent_list)
        debug('Agent 0', x=570, y=110)

        if self.map_num is not None:
            debug('Map {}'.format(self.map_num), x=100)

        # debug('mouse pos = '+ str(pygame.mouse.get_pos()))
        debug('Step: ' + str(self.step_cnt), x=30)
        if info is not None:
            debug(info, x=100)

        debug("-----------SCORE: {}".format(self.original_num_ball-self.agent_num), x = 100)


        for event in pygame.event.get():
            # 如果单击关闭窗口，则退出
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()