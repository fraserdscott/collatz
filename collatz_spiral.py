import math
import itertools as it
import unittest
from collections import deque

MAX_CONSECUTIVE_DIVISIONS = 20
MAX_CYCLE_LEN = 100

def collatz(number, a, b):
    if number % c == 0:
        return number // c

    return a * number + b


def denominator(lengths, a):
    return 2**sum(lengths) - a**len(lengths)


def number_of_kinks(cycle):
    # Find places where value increases (an+b been applied)
    shifted = list(cycle[1:]) + list([cycle[0]])
    return len([x for x, y in zip(cycle, shifted) if x < y])


def numerator(lengths, a):
    love = len(lengths)
    if love == 0:
        return 1

    return a*(numerator(lengths[1:], a)) + 2**(sum(lengths))


def constraint(t):
    # should be increasing i guess
    return all(x<y for x, y in zip(t, t[1:]))


def itery(numbers, num_variables):
    return [t for t in it.combinations_with_replacement(numbers, num_variables) if constraint(t)]


def number_of_cycles(a, b, kink):
    if a < 1 and b < 1 and kink < 1:
        raise("Parameter validation")

    # why kink > 1?
    if kink > 1 and a % 3 == 0 and b in {3**i for i in range(1,10)}:
        return 0
    
    vectors = [t for t in it.product(range(1, MAX_CONSECUTIVE_DIVISIONS), repeat=kink)]

    #make shift solution will check that solution does not match any previous found
    found = set()
    count = 0
    for t in vectors:
        if kink > 1 and len(set(t)) == 1:
            continue
        n = b*numerator(t[1:],a)/denominator(t, a)
        if n > 0 and n.is_integer():
            new_cycle = True
            for poo in found:
                for i in range(kink):
                    items = deque(poo)
                    items.rotate(-i)
                    if t == tuple(items):
                        new_cycle = False
                        break
            if new_cycle:
                found.add(t)
                count += 1
    return count


def find_cycles(a, b):
    cycles = set()
    n_checked = set()
    for n in range(1,1000):
        res = n
        seen = []
        for count in range(MAX_CYCLE_LEN+1):
            seen.append(res)
            res = collatz(res, a, b)
            if res in n_checked:
                break
            
            if res in seen:
                # Cycle begins where current number was first seen
                cycle_index = seen.index(res)
                # Convert to tuple to make hashable and preserve order
                cycle = tuple(seen[cycle_index:])

                # Check if this cycle has same elements as found one
                cycle_already_found = set(cycle) in [set(s) for s in cycles]

                if not cycle_already_found:
                    cycles.add(cycle)
                break
        n_checked.add(n)
    return cycles


def get_cycles(cycles, k):
    return [cycle for cycle in cycles if number_of_kinks(cycle) == k]


class MyTest(unittest.TestCase):
    def test(self):
        for a in range(3,100,2):
            for b in range(1,100,2):
                cycles = find_cycles(a, b)

                print("a={}, b={}, cycles={}".format(a, b, len(cycles)))
                predicted_cycles = [number_of_cycles(a, b, 1), number_of_cycles(a, b, 2), number_of_cycles(a,b, 3)]
                for i in range(1,4):
                    divided_cycles = get_cycles(cycles, i)
                    for s in sorted(divided_cycles, key=len):
                        print(s)

                    self.assertGreaterEqual(len(divided_cycles), predicted_cycles[i-1], "Predicted more cycles than there was")
                    self.assertLessEqual(len(divided_cycles), predicted_cycles[i-1], "Found more cycles than predicted")

                print()


    def check(self):
        for a in range(3,50,6):
            for b in [3**x for x in range(10)]:
                cycles = find_cycles(a, b)

                for i in range(2,4):
                    divided_cycles = get_cycles(cycles,i)

                    self.assertEqual(len(divided_cycles), 0, "Found an a and b with more than 0")
                    

c = 2   # /2

MyTest().test()
