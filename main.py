import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
print(sys.path)
from olympics_engine.generator import create_scenario
import argparse
from olympics_engine.agent import *
import time
from scenario.running import *
from scenario.table_hockey import *
from scenario.football import *
from scenario.wrestling import *
from scenario.volleyball import *
from scenario.billiard import *
from scenario.curling import *

import random
import numpy as np
import matplotlib.pyplot as plt
import json


def store(record, name):

    with open('logs/'+name+'.json', 'w') as f:
        f.write(json.dumps(record))

def load_record(path):
    file = open(path, "rb")
    filejson = json.load(file)
    return filejson

RENDER = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', default="curling", type= str,
                        help = 'running/table-hockey/football/wrestling/billiard/curling')
    parser.add_argument("--seed", default=1, type=int)
    args = parser.parse_args()

    for i in range(20):
        Gamemap = create_scenario(args.map)
        #game = table_hockey(Gamemap)
        if args.map == 'table-hockey':
            game = table_hockey(Gamemap)
            agent_num = 2
        elif args.map == 'football':
            game = football(Gamemap)
            agent_num = 2
        elif args.map == 'wrestling':
            game = wrestling(Gamemap)
            agent_num = 2
        # elif args.map == 'volleyball':
        #     game = volleyball(Gamemap)
        #     agent_num = 2
        elif args.map == 'billiard':
            game = billiard(Gamemap)
            agent_num = 1
        elif args.map == 'curling':
            game = curling(Gamemap)
            agent_num = 2

        agent = random_agent()
        rand_agent = random_agent()

        obs = game.reset()
        done = False
        step = 0
        if RENDER:
            game.render()

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        time_epi_s = time.time()
        while not done:
            step += 1

            # print('\n Step ', step)

            #action1 = [100,0]#agent.act(obs)
            #action2 = [100,0] #rand_agent.act(obs)
            action1, action2 = agent.act(obs), rand_agent.act(obs)
            action = [action1, action2] if (agent_num == 2) else [action1]

            obs, reward, done, _ = game.step(action)
            # plt.imshow(obs[0])
            # plt.show()
            if RENDER:
                game.render()


        print("episode duration: ", time.time() - time_epi_s, "step: ", step, (time.time() - time_epi_s)/step)
        if args.map == 'billiard':
            print('reward =', game.total_reward)
        else:
            print('reward = ', reward)
        # if R:
        #     store(record,'bug1')

