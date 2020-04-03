import math
import itertools as it
import unittest
from functools import reduce
import math

MAX_CYCLE_LEN = 100


def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


no_factors = {n:factors(n) for n in range(1,10)}



def collatz(number, a, b):
    if number % c == 0:
        return number // c

    return a * number + b


def number_of_kinks(cycle):
    # Find places where value increases (an+b been applied)
    shifted = list(cycle[1:]) + list([cycle[0]])
    return len([x for x, y in zip(cycle, shifted) if x < y])


def numerator(lengths, a):
    if len(lengths) == 0:
        return 1

    return a*(numerator(lengths[:-1], a)) + 2**(lengths[-1])


def denominator(total, a, k):
    return 2**total - a**k


def x_values_repeat(t):
    facs = no_factors[len(t)]
    for f in facs:
        if len(t) > f and all(t[i]==t[i+f] for i in range(0, len(t)//f)):
            return False
    return True


def lol(t):
    individual_values = [t[0]] + [j-i for (i,j) in zip(t, t[1:])]
    return not (len(t) > 1 and len(set(individual_values)) == 1) and x_values_repeat(individual_values)


def number_of_1_cycles(a, b, kink=1):
    if kink != 1:
        raise("Not implemented")

    return len([fac for fac in factors(b) if math.log2(fac + a).is_integer()])
            


def number_of_cycles(a, b, kink, mins=1, maxs=9999999):
    if a < 1 and b < 1 and kink < 1:
        raise("Parameter validation")

    if kink > 1 and a % 3 == 0 and b in {3**i for i in range(1,10)}:
        return 0

    #if kink==1:
        #return number_of_1_cycles(a, b)
    
    no_fs = no_factors[kink]

    # If the users bound is greater than the rigourous bound, use the rigourous bound
    mins = max(mins, int(math.log2(a))) # There is also a better lower limit on the total but it doesnt work rn - bounf on total is at least kink
    maxs = min(maxs, kink*(math.ceil(math.log2(a+b))))
    
    denoms = {i:denominator(i, a, kink) for i in range(mins,maxs+1)}

    vectors = [t for t in it.product(range(mins,maxs+1), repeat=kink) if all(i < j for i, j in zip(t, t[1:])) and lol(t)]

    found = set()
    count = 0
    #why not have total as it's own loop? might make more sense idk
    #i guess you could precompute every loop tho
    for t in vectors:

        #ts left to check *kink
        n = b*numerator(t[:-1],a)/denoms[t[-1]]
        if b/denoms[t[-1]] > 0 and (b/denoms[t[-1]]).is_integer():
            print(t, b/denoms[t[-1]], n)
        # b/numen * denom is an integer. What does this take? what can numen tell us? basically denom can remove facs from b and bring it into deficit. if numen can take it out of deficit, youre good
        # this can tell us when we're done!
        # if its an integer just kill it then!s
        if n > 0 and n.is_integer():
                # Convert to tuple to make hashable and preserve order
                cycle = tuple(find_cycle(a,b,n))

                # Check if this cycle has same elements as found one
                cycle_already_found = any(c in found for c in cycle)

                if not cycle_already_found:
                    found.add(n)
                    count += 1
                    if kink == 1 and count == no_fs:
                        return count

    return count


def find_cycle(a, b, n):
    res = n
    seen = []
    for count in range(MAX_CYCLE_LEN+1):
        seen.append(res)
        res = collatz(res, a, b)

        if res == n:
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
        MAX_B = 200
        MAX_KINKS = 2

        for a in range(3,MAX_A,2):
            for b in range(1,MAX_B,2):
                cycles = find_cycles(a, b)

                print("a={}, b={}, cycles={}".format(a, b, len(cycles)))
                for kink in range(1, MAX_KINKS+1):
                    predicted_cycles = number_of_cycles(a, b, kink, maxs=1500)
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

