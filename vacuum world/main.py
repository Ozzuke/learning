# 2D vacuum world, vacuum cleaner has to clean all squares
# env: fully observable, single-agent, deterministic, sequential, static, discrete, known

import random
from time import sleep
from copy import deepcopy


class EnvSettings:
    """Settings for the environment"""
    def __init__(self) -> None:
        self.map_x = 10
        self.map_y = 5
        self.max_turns = 100
        self.env_actions = \
        {Vacuum: 
            {'right': (1, 0),
             'left': (-1, 0),
             'up': (0, -1),
             'down': (0, 1),
             'clean': None}}


class Map:
    """A map in the form of a dictionary with keys as location tuples and values as a list of [x, y, dirty, entity]
    x and y are the coordinates of the location up to the max x and y
    dirty is a boolean value indicating whether the location is dirty, initially random
    entity is the entity at the location, initially None"""
    def __init__(self, settings: EnvSettings) -> None:
        self.settings = settings
        self.map = {}
        for x in range(settings.map_x):
            for y in range(settings.map_y):
                self.map[(x, y)] = [x, y, random.choice([True, False]), None]


class Vacuum:
    """A vacuum cleaner which can move around the map and clean dirty locations"""
    def __init__(self) -> None:
        self.location = [0, 0]
        self.performance = 0
    
    def choose_action(self, settings: EnvSettings, map: dict) -> str:
        """Simulate each possible action with next_state and return the best one (lowest performance measure).
        If more than one action has the same performance measure, choose a random one"""
        action_evals = {}
        shuffled_actions = [*settings.env_actions[Vacuum]]
        random.shuffle(shuffled_actions)
        for action in shuffled_actions:
            n_map, n_slef = Methods.next_state(settings, map, self, action)
            action_evals[action] = Methods.eval_perf(settings, n_map, n_slef.location)
        best_action = min(action_evals.items(), key=lambda x: x[1])
        return best_action[0]


class Methods:
    """A class for the methods used in the vacuum world"""
    
    def manhattan_distance(loc1: list, loc2: list) -> int:
        """Return the Manhattan distance between two locations"""
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
    
    def add_tuples(t1: tuple, t2: tuple) -> tuple:
        """Return the sum of two tuples"""
        return tuple(map(sum, zip(t1, t2)))

    def print_map(settings: EnvSettings, map: dict) -> None:
        """Print the map in a readable format in the form
        {entity}{dirty} for each location with the lack of dirt or entity indicated by a '.',
        'd' for dirty and 'C' for vacuum cleaner. ex:
        .d .d C. .. .d
        Cd .. .. .d .d"""
        for y in range(settings.map_y):
            for x in range(settings.map_x):
                loc = map[(x, y)]
                if loc[2]:
                    dirty = 'd'
                else:
                    dirty = '.'
                if loc[3] is None:
                    entity = '.'
                elif isinstance(loc[3], Vacuum):
                    entity = 'C'
                else:
                    entity = 'X'
                print(entity + dirty, end=' ')
            print()
        
    def eval_perf(settings: EnvSettings, map: dict, loc: list) -> int:
        """Return the performance measure of the vacuum cleaner at a location, the lower the better.
        Calculating performance: the sum of dirty locations + 
        (manhattan distance from current location to closest dirty location divided by longest possible manhattan distance)"""
        dirty_locs = [loc for loc in map.values() if loc[2]]
        if len(dirty_locs) == 0:
            return 0
        closest_loc = min(dirty_locs, key=lambda x: Methods.manhattan_distance(loc, x))
        return len(dirty_locs) + Methods.manhattan_distance(loc, closest_loc) / (settings.map_x + settings.map_y)
    
    def next_state(settings: EnvSettings, map: dict, entity, action: str) -> tuple[Map, Vacuum]:
        """Make a deepcopy of the entity and map, perform the action on the entity and update the map accordingly."""
        c_entity = deepcopy(entity)
        c_map = deepcopy(map)
        if action == 'clean':
            c_map[tuple(c_entity.location)][2] = False
        else:
            # if new location is out of bounds, do nothing
            if c_entity.location[0] + settings.env_actions[type(entity)][action][0] < 0 or \
                c_entity.location[0] + settings.env_actions[type(entity)][action][0] >= settings.map_x or \
                c_entity.location[1] + settings.env_actions[type(entity)][action][1] < 0 or \
                c_entity.location[1] + settings.env_actions[type(entity)][action][1] >= settings.map_y:
                return c_map, c_entity
            
            c_map[tuple(c_entity.location)][3] = None
            c_entity.location = Methods.add_tuples(c_entity.location, settings.env_actions[type(entity)][action])
            c_map[tuple(c_entity.location)][3] = c_entity
        return c_map, c_entity


if __name__ == "__main__":
    
    # initialize environment
    env_settings = EnvSettings()
    env_map = Map(env_settings)
    
    # initialize vacuum cleaner and set it at a random location
    vacuum = Vacuum()
    vacuum.location = random.choice(list(env_map.map.values()))[:2]
    
    # update map with vacuum cleaner
    env_map.map[tuple(vacuum.location)][3] = vacuum
    
    # print initial map and performance measure
    Methods.print_map(env_settings, env_map.map)
    performance = Methods.eval_perf(env_settings, env_map.map, vacuum.location)
    dust = len([loc for loc in env_map.map.values() if loc[2]])
    print("Dust:", dust)
    print()
    turns = env_settings.max_turns
    
    while turns and performance:
        turns -= 1
        sleep(0.01)
        
        # choose action and print it
        action = vacuum.choose_action(env_settings, env_map.map)
        
        # update map and vacuum cleaner
        env_map.map, vacuum = Methods.next_state(env_settings, env_map.map, vacuum, action)
        
        # print map and performance measure
        Methods.print_map(env_settings, env_map.map)
        performance = Methods.eval_perf(env_settings, env_map.map, vacuum.location)
        print()
    
    if not turns:
        print("Out of turns! Dust left:", len([loc for loc in env_map.map.values() if loc[2]]))
    else:
        print("Starting dust:", dust)
        print("Turns taken:", env_settings.max_turns - turns)
        print("Performance:", (env_settings.max_turns - turns)/dust)