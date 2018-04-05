import sys
import time
import queue
import heapq


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()


class State:
    def __init__(self, config, parent_node, direction,
                 depth):
        self.parentNode = parent_node
        self.depth = depth
        if direction == 'D':
            self.rel = 'Down'
            self.config = self.configDown(config)
        elif direction == 'U':
            self.rel = 'Up'
            self.config = self.configUp(config)
        elif direction == 'R':
            self.rel = 'Right'
            self.config = self.configRight(config)
        elif direction == 'L':
            self.rel = 'Left'
            self.config = self.configLeft(config)
        else:
            self.rel = direction
            self.config = config
        if alg == 'ast':
            self.cost = self.manhattan_dist() + self.depth

    def __lt__(self, other):
        return not self.cost > other.cost

    def __le__(self, other):
        return not self.cost >= other.cost

    def __gt__(self, other):
        return not self.cost < other.cost

    def __ge__(self, other):
        return not self.cost <= other.cost

    def configDown(self, config):
        config = list(config)
        idx = config.index('0')
        if idx + 3 <= 8:
            config[idx] = config[idx + 3]
            idx += 3
            config[idx] = '0'
        return ''.join(config)

    def configUp(self, config):
        config = list(config)
        idx = config.index('0')
        if idx - 3 >= 0:
            config[idx] = config[idx - 3]
            idx -= 3
            config[idx] = '0'
        return ''.join(config)

    def configRight(self, config):
        config = list(config)
        idx = config.index('0')
        if (idx + 1) % 3 != 0:
            config[idx] = config[idx + 1]
            idx += 1
            config[idx] = '0'
        return ''.join(config)

    def configLeft(self, config):
        config = list(config)
        idx = config.index('0')
        if idx % 3 != 0:
            config[idx] = config[idx - 1]
            idx -= 1
            config[idx] = '0'
        return ''.join(config)

    def goalTest(self):
        return self.config == '012345678'

    def manhattan_dist(self):
        dist = 0
        for k in range(1, 9):
            exp_i = k // 3
            exp_j = k % 3
            cur_i = self.config.find(str(k)) // 3
            cur_j = self.config.find(str(k)) % 3
            dist += abs(cur_i - exp_i) + abs(cur_j - exp_j)
        return dist


def ast(init_state):
    frontier = []
    frontier_configs = set()
    heapq.heappush(frontier, init_state)
    frontier_configs.add(init_state.config)
    explored = set()
    n_exp = 0
    max_depth = 0

    while not frontier == []:
        state = heapq.heappop(frontier)
        frontier_configs.remove(state.config)
        explored.add(state.config)

        if state.goalTest():
            moves = []
            depth = state.depth
            while state.parentNode is not None:
                moves.append(state.rel)
                state = state.parentNode
            moves.reverse()
            print('path_to_goal:', moves, file=f1)
            print('cost_of_path:', len(moves), file=f1)
            print('nodes_expanded:', n_exp, file=f1)
            print('search_depth:', depth, file=f1)
            print('max_search_depth:', max_depth, file=f1)
            return True

        n_exp += 1
        if state.depth > max_depth:
            max_depth = state.depth + 1

        neighbours = []
        for dir in ['U', 'D', 'L', 'R']:
            neighbours.append(
                State(state.config, state, dir,
                      state.depth + 1))

        for neighbour in neighbours:
            if neighbour.config not in frontier_configs \
                    and neighbour.config not in explored:
                heapq.heappush(frontier, neighbour)
                frontier_configs.add(neighbour.config)
                if neighbour.depth > max_depth:
                    max_depth = neighbour.depth
            elif neighbour.config in frontier_configs:
                for state in frontier:
                    if state.config == neighbour.config:
                        frontier.remove(state)
                        heapq.heappush(frontier, neighbour)
                        if neighbour.depth > max_depth:
                            max_depth = neighbour.depth
                        break

    return False


def bfs(init_state):
    frontier = queue.Queue()
    frontier_configs = set()
    frontier.put(init_state)
    frontier_configs.add(init_state.config)
    explored = set()
    n_exp = 0
    max_depth = 0

    while not frontier.empty():
        state = frontier.get()
        frontier_configs.remove(state.config)
        explored.add(state.config)

        if state.goalTest():
            moves = []
            depth = state.depth
            while state.parentNode is not None:
                moves.append(state.rel)
                state = state.parentNode
            moves.reverse()
            print('path_to_goal:', moves, file=f1)
            print('cost_of_path:', len(moves), file=f1)
            print('nodes_expanded:', n_exp, file=f1)
            print('search_depth:', depth, file=f1)
            print('max_search_depth:', max_depth, file=f1)
            return True

        n_exp += 1
        if state.depth > max_depth:
            max_depth = state.depth + 1

        neighbours = []
        for dir in ['U', 'D', 'L', 'R']:
            neighbours.append(State(state.config, state, dir, state.depth + 1))

        for neighbour in neighbours:
            if neighbour.config not in frontier_configs and neighbour.config not in explored:
                frontier.put(neighbour)
                frontier_configs.add(neighbour.config)
                if neighbour.depth > max_depth:
                    max_depth = neighbour.depth

    return False


def dfs(init_state):
    frontier = Stack()
    frontier.push(init_state)
    frontier_configs = set()
    frontier_configs.add(init_state.config)
    explored = set()
    n_exp = 0
    max_depth = 0

    while not frontier.isEmpty():
        state = frontier.pop()
        frontier_configs.remove(state.config)
        explored.add(state.config)

        if state.goalTest():
            moves = []
            depth = state.depth
            while state.parentNode is not None:
                moves.append(state.rel)
                state = state.parentNode
            moves.reverse()
            print('path_to_goal:', moves, file=f1)
            print('cost_of_path:', len(moves), file=f1)
            print('nodes_expanded:', n_exp, file=f1)
            print('search_depth:', depth, file=f1)
            print('max_search_depth:', max_depth, file=f1)
            return True

        n_exp += 1

        neighbours = []
        for dir in ['R', 'L', 'D', 'U']:
            neighbours.append(
                State(state.config, state, dir,
                      state.depth + 1))

        for neighbour in neighbours:
            if neighbour.config not in frontier_configs and neighbour.config not in explored:
                frontier.push(neighbour)
                frontier_configs.add(neighbour.config)
                if neighbour.depth > max_depth:
                    max_depth = neighbour.depth

    return False


alg = ''
if __name__ == '__main__':
    start_time = time.time()
    init_state = State(str(sys.argv[2]).replace(',', ''),
                       None, None, 0)
    f1 = open('output.txt', 'w')
    alg = sys.argv[1]
    if alg == 'bfs':
        bfs(init_state)
    elif alg == 'dfs':
        dfs(init_state)
    elif alg == 'ast':
        ast(init_state)
    print("running_time: ", (time.time() - start_time),
          file=f1)
    if sys.platform == "win32":
        import psutil

        print("max_ram_usage:",
              psutil.Process().memory_info().rss * 0.000001,
              file=f1)
    else:
        import resource

        print("max_ram_usage:", resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss * 0.000001,
              file=f1)
    f1.close()
