# olympics_engine

AI-Olympics is a 2D physical simulator created from scratch with only basic dependencies and
Pygame for visualization. This means that AI-Olympics is easy to deploy. Using AI-Olympics,
researchers can design various gaming scenarios with shared map elements and multiple individual
agents. The characteristic of each map element is implied by its color, for example, a black line
represents a non-penetrable wall, a red line represents the awarding transferable final and a green
line represents a penalising obstacle. Assembling the elements together we can build up a specific
map that includes both rewarding and hazardous area, and potentially various objectives for agent to
explore.


<img src=https://github.com/jidiai/olympics_engine/blob/main/olympics_engine/assets/AI-Olympics.png>

## Navigation
```
|-- olympics_engine   
	|-- env_wrapper                             // wrapper for Jidi evaluation (www.jidiai.cn)
	|-- scenario		                    // detail scenario implementation
	|	|-- running_competition_maps        // multiple running maps
	|	|-- billiard_competition.py         // billiard scenario script
	|   |-- curling_competition.py              // curling scenario script
	|   |-- football.py                         // 1 vs 1 football script
	|   |-- running_competition.py              // running scenario script
	|   |-- table_hockey.py                     // table hockey scenario script
	|   |-- wrestling.py                        // wrestling scenario script
	|-- tools		                    // mathmatical toolbox
	|-- train                                   // Training examples of some of the sub-scenarios (for reference only)
	|-- utils               
	|-- AI_olympics.py		            // An integrated scenarios containing six tasks
	|-- core.py                                 // game engine script
	|-- main.py                                 // run a game
	|-- objects.py                              // objects in the game map
	|-- scenario.json                           // scenario setting
	|-- viewer.py                               // pygame render
```


## Installation

To install the olympics_engine, clone the repository and use `pip install .`

## Run a game

```python
python -m olympics_engine.main
```

