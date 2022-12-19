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

        # q.put((bc, [m[j] - costs[j] for j in range(len(mats))]))
        # q = Queue()
        # q.put(([0, 0, 0, 0], new_mats))
        # while not q.empty():
        #     bots, m = q.get()
        #     # print(bots, m)
        #     yield (bots, m)  # not purchasing or saving is an option too.

        #     for i, costs in enumerate([self.ore_bot_cost, self.clay_bot_cost, self.obsidian_bot_costs, self.geode_bot_costs]):
        #         if self._afford(m,  costs):
        #             bc = bots.copy()
        #             bc[i] += 1
        #             q.put((bc, [m[j] - costs[j] for j in range(len(mats))]))

    def simplifyMats(self, mats):
        # print(mats)
        # print(self.bounds)
        return tuple(min(bound, mats[i]) for i, bound in enumerate(self.bounds))

    def simulate(self, minutes):
        print(self.bounds)
        geodes = 0

        q = PriorityQueue()
        q.put((0, 0, [1, 0, 0, 0], [0, 0, 0, 0]))
        seen = dict()
        while not q.empty():
            _, minute, bots, mats = q.get()

            # pruning by some estimate.
            timeleft = minutes - minute
            if (timeleft + bots[3]) * (timeleft) + mats[3] < geodes:
                continue

            if minute >= minutes:
                geodes = max(geodes, mats[3])
                continue

            simpler_mats = self.simplifyMats(mats)
            options = self.purchaseOptions(simpler_mats)
            # print("minute", minute+1)
            # print("bots", bots)
            # print("mats", mats)
            # print("options", len(options), options)
            # print()

            # generate new mats while bot is built.
            # mats = [m + b for m, b in zip(mats, bots)] # now in nm

            for b, cost in options:
                nb = tuple(ob + b for ob, b in zip(bots, b))
                nm = tuple(mats[j] + bots[j] - cost[j]
                           for j in range(len(mats)))
                # Pruning previously seen states (if seen before with same materials/bots available, then
                # this state is worse than the previous)
                t = (nb, nm)
                if t in seen:
                    if minute >= seen[t]:
                        # print("hit!", minute, seen[t])
                        continue
                seen[t] = minute
                nmin = minute+1
                q.put((-nmin, nmin, nb, nm))
                # print(b, m)

            # print(mats)
            # print(bots)
            # print()

        return geodes


blueprints = []
for line in sys.stdin:
    costs = [int(p) for p in re.findall("\d+", line)]
    bb = Blueprint(costs)
    blueprints.append(bb)
    # print(*bb.costs, sep="\n")
    # print()

# print(list(blueprints[0].purchaseOptions((30, 2, 40, 4))))

# print(blueprints[1].simulate(24))

s = 0
for id, bb in enumerate(blueprints):
    print(*bb.costs, sep="\n")
    v = bb.simulate(24)
    print(v, v*(id+1))
    s += v*(id+1)
    # _m = max(v, _m)
    # print()

print()
print(s)
