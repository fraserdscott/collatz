import math
import itertools as it
import unittest
from collections import deque
from functools import reduce

MAX_CONSECUTIVE_DIVISIONS = 10
MAX_CYCLE_LEN = 100

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def collatz(number, a, b):
    if number % c == 0:
        return number // c

    return a * number + b


def number_of_kinks(cycle):
    # Find places where value increases (an+b been applied)
    shifted = list(cycle[1:]) + list([cycle[0]])
    return len([x for x, y in zip(cycle, shifted) if x < y])


def numerator(lengths, a):
    love = len(lengths)
    if love == 0:
        return 1

    return a*(numerator(lengths[1:], a)) + 2**(sum(lengths))


def denominator(lengths, a):
    return 2**sum(lengths) - a**len(lengths)


def x_values_repeat(t):
    facs = factors(len(t))
    facs.remove(1)
    for f in facs:
        if len(t) > f and all(t[i]==t[i+f] for i in range(0, len(t)//f)):
            return True
    return False


def number_of_cycles(a, b, kink):
    if a < 1 and b < 1 and kink < 1:
        raise("Parameter validation")

    if kink > 1 and a % 3 == 0 and b in {3**i for i in range(1,10)}:
        return 0
    
    no_fs = len(factors(b))
    
    vectors = [t for t in it.product(range(1, MAX_CONSECUTIVE_DIVISIONS), repeat=kink)]
    # the last one can be just the this thing
    
    found = set()
    count = 0
    for t in vectors:
        if x_values_repeat(t) or kink > 1 and len(set(t)) == 1:
            continue
        
        n = b*numerator(t[1:],a)/denominator(t, a)
        if n > 0:
            # Is there an upper bound on n?
            if kink==1 and n < 1:
                # n is only going to get smaller, t[i] will only increase
                # if you had nested loops you could break here for any k
                break
            if n.is_integer():
                # Convert to tuple to make hashable and preserve order
                cycle = tuple(find_cycle(a,b,n))

                # Check if this cycle has same elements as found one
                cycle_already_found = set(cycle) in [set(s) for s in found]

                if not cycle_already_found:
                    found.add(cycle)
                    count += 1
                    if kink == 1 and count == no_fs:
                        return count
                    
    return count


def find_cycle(a, b, n, n_checked = []):
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
            
            cycle = seen[cycle_index:]
            return cycle

    
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
        MAX_A = 200
        MAX_B = 500
        MAX_KINKS = 3
        
        for a in range(5,MAX_A,2):
            for b in range(1,MAX_B,2):
                cycles = find_cycles(a, b)

                print("a={}, b={}, cycles={}".format(a, b, len(cycles)))
                for kink in range(2, MAX_KINKS+1):
                    predicted_cycles = number_of_cycles(a, b, kink)
                    divided_cycles = get_cycles(cycles, kink)
                    
                    print("{} cycles with {} kinks".format(predicted_cycles, kink))
                    for s in sorted(divided_cycles, key=len):
                        print(s)

                    self.assertGreaterEqual(len(divided_cycles), predicted_cycles, "Predicted more cycles than there was")
                    self.assertLessEqual(len(divided_cycles), predicted_cycles, "Found more cycles than predicted")

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
