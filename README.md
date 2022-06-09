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


## Installation

To install the olympics_engine, clone the repository and use `pip install .`

## Run a game

```python
python -m olympics_engine.main
```

