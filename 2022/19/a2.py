import re
import sys
from functools import lru_cache
from queue import PriorityQueue, Queue
from typing import List


class Blueprint:
    def __init__(self, costs) -> None:
        self.ore_bot_cost = (costs[1], 0, 0, 0)
        self.clay_bot_cost = (costs[2], 0, 0, 0)
        self.obsidian_bot_costs = (costs[3], costs[4], 0, 0)
        self.geode_bot_costs = (costs[5], 0, costs[6], 0)
        self.costs = [self.ore_bot_cost, self.clay_bot_cost,
                      self.obsidian_bot_costs, self.geode_bot_costs]
        self.bounds = [max(cost[i] for cost in self.costs) for i in range(4)]
        # print(self.bounds)

    def _afford(self, mats, costs):
        for i in range(len(mats)):
            if costs[i] > mats[i]:
                return False
        return True

    # Could memoize this entire function
    @lru_cache(None)
    def purchaseOptions(self, mats):
        # Not building is always an option.
        options = [((0, 0, 0, 0), (0, 0, 0, 0))]
        for i, cost in enumerate(self.costs):
            if self._afford(mats,  cost):
                bots = [0, 0, 0, 0]
                bots[i] += 1
                # nm = tuple([mats[j] - cost[j] for j in range(len(mats))])
                options.append((tuple(bots), cost))
                # options |= self.purchaseOptions(nm)

        return options

    def simulate(self, minutes):
        bots = (1, 0, 0, 0)
        mats = (0, 0, 0, 0)
        return self._simulate(minutes, bots, mats)

    @lru_cache
    def _simulate(self, minutes, bots, mats):
        # print(minutes, bots, mats)
        if minutes == 0:
            return mats[3]

        options = self.purchaseOptions(mats)

        geodes = 0
        for b, cost in options:
            nb = tuple(ob + b for ob, b in zip(bots, b))
            nm = tuple(mats[j] + bots[j] - cost[j]
                       for j in range(len(mats)))

            g = self._simulate(minutes - 1, nb, nm)
            geodes = max(g, geodes)

        return geodes


blueprints = []
for line in sys.stdin:
    costs = [int(p) for p in re.findall("\d+", line)]
    bb = Blueprint(costs)
    blueprints.append(bb)


s = 0
for id, bb in enumerate(blueprints):
    print(*bb.costs, sep="\n")
    v = bb.simulate(17)
    print(v, v*(id+1))
    s += v*(id+1)
    # _m = max(v, _m)
    # print()

print()
print(s)
