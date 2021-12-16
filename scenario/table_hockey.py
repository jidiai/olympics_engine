from olympics_engine.core import OlympicsBase
from olympics_engine.viewer import debug
import pygame
import sys
import random

class table_hockey(OlympicsBase):
    def __init__(self, map):
        super(table_hockey, self).__init__(map)
        self.gamma = 1  # v衰减系数
        self.wall_restitution = 0.8
        self.circle_restitution = 1
        self.tau = 0.1

        self.print_log = False

        self.draw_obs = True
        self.show_traj = False
        
        self.speed_cap = 200



    def check_overlap(self):
        pass

    # def generate_map(self, map):
    #     self.ball_init_y = [300,500]
    #     for index, item in enumerate(map['agents']):
    #         if item.type == 'ball':         #initialise ball position
    #             random_y = random.uniform(self.ball_init_y[0], self.ball_init_y[1])
    #             item.position_init[1] = random_y
    #
    #         self.agent_list.append(item)
    #
    #         position = item.position_init
    #
    #         r = item.r
    #         self.agent_init_pos.append(item.position_init)
    #         self.agent_num += 1
    #
    #         if item.type == 'agent':
    #             visibility = item.visibility
    #             boundary = self.get_obs_boundaray(position, r, visibility)
    #             # print("boundary: ", boundary)
    #             self.obs_boundary_init.append(boundary)


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

        self.stepPhysics(actions_list)
        self.speed_limit()
        self.step_cnt += 1
        self.cross_detect()



        step_reward = self.get_reward()
        obs_next = self.get_obs()              #need to add agent or ball check in get_obs

        done = self.is_terminal()
        self.change_inner_state()
        #check overlapping
        #self.check_overlap()

        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

    def cross_detect(self, **kwargs):
        """
        check whether the agent has reach the cross(final) line
        :return:
        """
        for agent_idx in range(self.agent_num):

            agent = self.agent_list[agent_idx]

            if agent.type == 'ball':
                for object_idx in range(len(self.map['objects'])):
                    object = self.map['objects'][object_idx]

                    if not object.can_pass():
                        continue
                    else:
                        if object.color == 'red' and object.check_cross(self.agent_pos[agent_idx], agent.r):
                            agent.color = 'red'
                            agent.finished = True  # when agent has crossed the finished line
                            agent.alive = False


    def get_reward(self):

        ball_end_pos = None

        for agent_idx in range(self.agent_num):
            agent = self.agent_list[agent_idx]

            if agent.type == 'ball' and agent.finished:
                ball_end_pos = self.agent_pos[agent_idx]

        if ball_end_pos is not None and ball_end_pos[0] < 400:
            if self.agent_pos[0][0] < 400:
                return [0.,100.]
            else:
                return [100., 0.]
        elif ball_end_pos is not None and ball_end_pos[0] > 400:
            if self.agent_pos[0][0] < 400:
                return [100. ,0.]
            else:
                return [0., 100.]

        else:
            return [0. ,0.]



    def is_terminal(self):

        if self.step_cnt >= self.max_step:
            return True

        for agent_idx in range(self.agent_num):
            agent = self.agent_list[agent_idx]
            if agent.type == 'ball' and agent.finished:
                return True

        return False


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
        self.viewer.draw_energy_bar(self.agent_list, height=130)
        debug('Agent 0', x=570, y=140)
        debug('Agent 1', x=640, y=140)
        if self.map_num is not None:
            debug('Map {}'.format(self.map_num), x=100)

        # debug('mouse pos = '+ str(pygame.mouse.get_pos()))
        debug('Step: ' + str(self.step_cnt), x=30)
        if info is not None:
            debug(info, x=100)


        for event in pygame.event.get():
            # 如果单击关闭窗口，则退出
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        #self.viewer.background.fill((255, 255, 255))
