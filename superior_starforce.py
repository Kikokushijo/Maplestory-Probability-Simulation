from __future__ import division, print_function
from random import uniform
import numpy as np
import matplotlib.pyplot as plt

FORCE_COST = 0.55832200
PROTECT_COST = 1.2
SCROLL_COST = 0.23
SIMULATE_TIMES = 10000000

force_probs = {0: (0.50, 0.50, 0.00), 
               1: (0.50, 0.50, 0.00),
               2: (0.45, 0.55, 0.00),
               3: (0.40, 0.60, 0.00),
               4: (0.40, 0.60, 0.00),
               5: (0.40, 0.57, 0.03),
               6: (0.40, 0.55, 0.05),
               7: (0.40, 0.53, 0.07), 
               8: (0.40, 0.50, 0.10),
               9: (0.37, 0.48, 0.15),
               10:(0.35, 0.45, 0.20)}

scroll_probs = {0: 1.00, 1:0.90, 2:0.80, 3:0.70, 
                4: 0.60, 5:0.50, 6:0.40, 7:0.30,
                8: 0.20, 9:0.10}

def enhance(change=6):
    equip, force, level, scroll, protect, succ = 0, 0, 0, 0, 0, [True] * 2
    while level != 10:
        if level == 0:
            level += 1
            scroll += 1
            succ = [True] * 2
        elif level <= change:
            if not any(succ):
                force += 1
                level += 1
                succ = [True] * 2
            else:
                dice = uniform(0, 1)
                protect += 1
                scroll += 1
                succ = [True] * 2
                if dice <= scroll_probs[level]:
                    level += 1
        else:
            if not any(succ):
                force += 1
                level += 1
                succ = [True] * 2
            else:
                dice = uniform(0, 1)
                force += 1
                if dice < force_probs[level][0]:
                    level += 1
                    succ = (succ + [True])[1:]
                elif dice < sum(force_probs[level][:2]):
                    level = max(0, level - 1)
                    succ = (succ + [False])[1:]
                else:
                    equip += 1
                    level = 0
                    succ = [True] * 2
    return equip, force, scroll, protect

if __name__ == '__main__':

    costs, equips, scrolls, protects= [], [], [], []
    for i in range(SIMULATE_TIMES):
        equip, force, scroll, protect = enhance()
        equips.append(equip)
        costs.append(force * FORCE_COST + scroll * SCROLL_COST + protect * PROTECT_COST)
        scrolls.append(scroll)
        protects.append(protect)
        if i % 100000 == 0:
            print('Has Simulated %d times...' % i)

    print('Equip Avg: ', str(round(np.mean(equips), 2)).ljust(8),   'Equip Std: ', round(np.std(equips), 2))
    print('Costs Avg: ', str(round(np.mean(costs), 2)).ljust(8),    'Costs Std: ', round(np.std(costs), 2))
    print('Scrls Avg: ', str(round(np.mean(scrolls), 2)).ljust(8),  'Scrls Std: ', round(np.std(scrolls), 2))
    print('Prots Avg: ', str(round(np.mean(protects), 2)).ljust(8), 'Prots Std: ', round(np.std(protects), 2))

    costs.sort()
    equips.sort()
    scrolls.sort()
    protects.sort()

    plt.xlabel('Luckness among 100 people')
    plt.ylabel('Costs (1e8)')
    plt.plot(np.arange(0, 100, 100 / SIMULATE_TIMES), costs, '--o', markersize=1)
    plt.show()

    plt.xlabel('Luckness among 100 people')
    plt.ylabel('Equipment Number')
    plt.plot(np.arange(0, 100, 100 / SIMULATE_TIMES), equips, '--o', markersize = 1)
    plt.show()

    for i in range(0, 100, 5):
        print('The Luckiest %d%%: ' % i)
        pos = int(i / 100 * SIMULATE_TIMES)
        print('Equip: ', equips[pos])
        print('Costs: ', costs[pos])
        print('Scrls: ', scrolls[pos])
        print('Prots: ', protects[pos])

    for i in range(100):
        try:
            print(i, equips.index(i) / SIMULATE_TIMES)