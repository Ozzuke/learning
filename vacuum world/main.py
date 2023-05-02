# 2D vacuum world, vacuum cleaner has to clean all squares
# env: fully observable, single-agent, deterministic, sequential, static, discrete, known

from random import shuffle, choice
from time import sleep


y_max = 5
x_max = 5
map = [[x, y, choice([True, False]), None] for x in range(x_max) for y in range(y_max)]


class Vacuum:
    def __init__(self) -> None:
        self.location = [0, 0]
        self.actions = ['right', 'left', 'up', 'down', 'clean']
    
    def choose_action(self, map):
        shuffle(self.actions)
        current_eval = eval_perf(map, self.location)
        action_evals = {}
        for action in self.actions:
            trans_map = next_state(map, self, action)
            for loc in trans_map:
                if loc[3] is self:
                    new_loc = loc[:2]
                    break
            action_evals[action] = eval_perf(trans_map, new_loc)
        best_action = min(action_evals.items(), key=lambda x: x[1])
        if best_action[1] > current_eval:
            action = None
        else:
            action = best_action[0]
        print(best_action, action_evals)
        return action


def find_loc_index(map: list, loc: list) -> int:
    # find the index of the specified location in the map list
    enum_map = [*enumerate(map)]
    for i, map_loc in enum_map:
        if map_loc[0] == loc[0] and map_loc[1] == loc[1]:
            return i
    return -1


def next_state(map: list, entity: Vacuum, action: str) -> list:
    # return the map in the state it would be if entity took an action
    if action == None:
        return map
    entity_loc = entity.location
    entity_index = find_loc_index(map, entity_loc)
    
    if action == 'clean':
        map[entity_index][2] = False
        return map
    
    actions = {'right': (1, 0),
               'left': (-1, 0),
               'up': (0, -1),
               'down': (0, 1)}
    
    if action in actions.keys():
        new_entity_loc = [entity_loc[0] + actions[action][0], entity_loc[1] + actions[action][1]]
        new_entity_index = find_loc_index(map, new_entity_loc)
        
        if new_entity_index == -1:
            return map
        map[entity_index][3] = None
        map[new_entity_index][3] = entity
        entity.location = new_entity_loc  #TODO: changes global entity location, meaning 'left' is correct, 'right' is the original location (same with up/down) etc
        
        return map
    
    raise Exception(f"Invalid action '{action}'")


def manhattan_distance(loc1, loc2) -> int:
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def eval_perf(map, vac_loc) -> float:
    perf = sum(square[2] for square in map)
    distances_to_dirt = []
    for loc in map:
        if loc[2]:
            distances_to_dirt.append(manhattan_distance(vac_loc, loc[:2]))
    perf += min(distances_to_dirt) / (y_max + x_max)
    return perf


def print_map(map):
    for y in range(y_max):
        for x in range(x_max):
            loc = map[find_loc_index(map, [x, y])]
            if loc[3] == None:
                print('.', end='')
            else:
                print('C', end='')
            if loc[2]:
                print('d', end=' ')
            else:
                print('.', end=' ')
        print()


if __name__ == "__main__":
    vac = Vacuum()
    start_loc = choice(map)[:2]
    vac.location = start_loc
    map[find_loc_index(map, vac.location)][3] = vac
    print_map(map)
    i = 5
    while i:
        i -= 1
        sleep(2)
        action = vac.choose_action(map)
        print(action, vac.location, eval_perf(map, vac.location))
        map = next_state(map, vac, action)
        print_map(map)
        