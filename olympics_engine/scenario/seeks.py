from olympics_engine.core import OlympicsBase
from olympics_engine.objects import Arc, Agent
from olympics_engine.viewer import debug
import time
import random
import pygame
import sys

class Seeks(OlympicsBase):
    def __init__(self, map, seed = None):
        super(Seeks, self).__init__(map, seed)

        self.gamma = 1  # v衰减系数
        self.wall_restitution = 0.8
        self.circle_restitution = 1
        self.print_log = False
        self.print_log2 = False
        self.tau = 0.1

        self.speed_cap =  50
        self.max_step=500

        self.draw_obs = True
        self.show_traj = False

        self.num_treats = 5
        self.num_pois = 3
        self.treats_r = 5
        self.pois_r = 5

        self.map = map

        self.treats_list_pos = []
        self.score = [0, 0]
        self.x_lim = [50, 500]
        self.y_lim = [50, 500]

        self.add_a_treat(self.num_treats, good=True)
        self.add_a_treat(self.num_pois, good=False)


    def generate_a_treat(self, good):


        while True:

            new_treats_x = random.uniform(self.x_lim[0]+self.treats_r, self.x_lim[1]-self.treats_r)
            new_treats_y = random.uniform(self.y_lim[0]+self.treats_r, self.y_lim[1]-self.treats_r)
            overlap = False

            dis_agent1 = (new_treats_x - self.agent_pos[0][0]) ** 2 + (new_treats_y - self.agent_pos[0][1]) ** 2
            dis_agent2 = (new_treats_x - self.agent_pos[1][0]) ** 2 + (new_treats_y - self.agent_pos[1][1]) ** 2
            if (dis_agent1 < (self.agent_list[0].r + self.treats_r) ** 2) or (
                    dis_agent2 < (self.agent_list[1].r + self.treats_r) ** 2):
                overlap = True
                continue


            for i in self.treats_list_pos:
                dis = (i[0]-new_treats_x)**2 + (i[1]-new_treats_y)**2
                if dis < (2*self.treats_r)**2:      #treats overlapping
                    overlap = True
                    break

            if overlap:
                continue
            else:
                self.treats_list_pos.append([new_treats_x, new_treats_y, good])
                return new_treats_x, new_treats_y

    def add_a_treat(self, n, good):
        for _ in range(n):
            x,y = self.generate_a_treat(good=good)
            init_pos = [x-self.treats_r, y-self.treats_r, 2*self.treats_r, 2*self.treats_r]
            self.map["objects"].append(Arc(init_pos=init_pos, start_radian=0, end_radian=-1,color='red' if good else 'blue',
                                           passable=True, collision_mode=3, width=10))
        pass


    def eat_a_treat(self):

        for idx, treat in enumerate(self.treats_list_pos):
            treat_agent1_dis2 = (treat[0]-self.agent_pos[0][0])**2 + (treat[1]-self.agent_pos[0][1])**2
            treat_agent2_dis2 = (treat[0]-self.agent_pos[1][0])**2 + (treat[1]-self.agent_pos[1][1])**2

            agent1_eat = treat_agent1_dis2 < (self.agent_list[0].r + self.treats_r)**2
            agent2_eat = treat_agent2_dis2 < (self.agent_list[1].r + self.treats_r)**2
            #check collision

            if not agent1_eat and not agent2_eat:
                continue

            if agent1_eat and not agent2_eat:
                self.score[0] += 1 if treat[2] else -1
            elif not agent1_eat and agent2_eat:
                self.score[1] += 1 if treat[2] else -1
            elif agent1_eat and agent2_eat:
                if treat_agent1_dis2<treat_agent2_dis2:
                    self.score[0] += 1 if treat[2] else -1
                else:
                    self.score[1] += 1 if treat[2] else -1
            else:
                raise NotImplementedError

            self.treats_list_pos.remove(treat)
            del self.map["objects"][4 + idx]  # plus 4 walls

            self.add_a_treat(1, treat[2])




    def check_overlap(self):
        #todo
        pass

    def get_reward(self, previous_score):
        return [self.score[0]-previous_score[0], self.score[1]-previous_score[1]]


    def is_terminal(self):

        if self.step_cnt >= self.max_step:
                return True

        return False



    def step(self, actions_list):

        previous_score = [self.score[0], self.score[1]]

        self.stepPhysics(actions_list, self.step_cnt)

        self.speed_limit()

        self.eat_a_treat()

        self.step_cnt += 1
        step_reward = self.get_reward(previous_score)
        done = self.is_terminal()
        if done:
            if self.score[0] > self.score[1]:
                step_reward = [100., 0]
            elif self.score[0] < self.score[1]:
                step_reward = [0., 100.]
            else:
                step_reward = [0., 0]


        obs_next = self.get_obs()

        self.change_inner_state()

        return obs_next, step_reward, done, ''


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
            temp_agent_list = [Agent(r=8, color='purple'), Agent(r=8, color='green')]
            self.viewer.draw_view(self.obs_list, temp_agent_list, leftmost_x=100, upmost_y=550)

            pygame.draw.line(self.viewer.background, start_pos=[520, 130], end_pos=[690, 130], color=[0,0,0])
            pygame.draw.line(self.viewer.background, start_pos=[565, 100], end_pos=[565,160], color=[0,0,0])
            pygame.draw.line(self.viewer.background, start_pos=[630, 100], end_pos=[630,160], color=[0,0,0])
            pygame.draw.line(self.viewer.background, start_pos=[520, 160], end_pos=[690, 160], color=[0,0,0])

            debug("Scores", x=520, y=140)
            debug("{}".format(self.score[0]), x= 600, y=140)
            debug("{}".format(self.score[1]), x= 660, y=140)


            # self.viewer.draw_energy_bar(self.agent_list)
            debug('Agent 0', x=570, y=110)
            debug('Agent 1', x=640, y=110)


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
