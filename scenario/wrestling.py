from olympics_engine.core import OlympicsBase
import pygame
import sys
import math

def point2point(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class wrestling(OlympicsBase):
    def __init__(self, map):
        super(wrestling, self).__init__(map)

        self.gamma = 1  # v衰减系数
        self.wall_restitution = 1
        self.circle_restitution = 1
        self.print_log = False
        self.tau = 0.1

        self.draw_obs = True
        self.show_traj = True


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
        previous_pos = self.agent_pos

        actions_list = self.check_action(actions_list)

        self.stepPhysics(actions_list, self.step_cnt)

        self.cross_detect(previous_pos, self.agent_pos)

        self.step_cnt += 1
        step_reward = self.get_reward()
        obs_next = self.get_obs()
        # obs_next = 1
        done = self.is_terminal()
        self.change_inner_state()
        #check overlapping
        #self.check_overlap()

        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def cross_detect(self, previous_pos, new_pos):

        #case one: arc intersect with the agent
        #check radian first
        finals = []
        for object_idx in range(len(self.map['objects'])):
            object = self.map['objects'][object_idx]
            if object.can_pass() and object.color == 'blue':
                #arc_pos = object.init_pos
                finals.append(object)

        for agent_idx in range(self.agent_num):
            agent = self.agent_list[agent_idx]
            agent_pre_pos, agent_new_pos = previous_pos[agent_idx], new_pos[agent_idx]

            for final in finals:
                center = (final.init_pos[0] + 0.5*final.init_pos[2], final.init_pos[1]+0.5*final.init_pos[3])
                arc_r = final.init_pos[2]/2

                if final.check_radian(agent_new_pos, [0,0], 0):
                    l = point2point(agent_new_pos, center)
                    if abs(l - arc_r) <= agent.r:
                        agent.color = 'blue'
                        agent.finished = True
                        agent.alive = False



        #case two: the agent cross the arc, inner  to outer or outer to inner


    def get_reward(self):

        agent1_finished = self.agent_list[0].finished
        agent2_finished = self.agent_list[1].finished
        if agent1_finished and agent2_finished:
            return [0., 0]
        elif agent1_finished and not agent2_finished:
            return [0., 100]
        elif not agent1_finished and agent2_finished:
            return [100., 0]
        else:
            return [0,0]

    def is_terminal(self):

        if self.step_cnt >= self.max_step:
            return True

        for agent_idx in range(self.agent_num):
            if self.agent_list[agent_idx].finished:
                return True

        return False

