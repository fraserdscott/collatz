import math
import itertools as it

def collatz(number, a, b):
    if number % c == 0:
        return number // c

    return a * number + b


def denominator(lengths, a):
    love = len(lengths)
    return 2**sum(lengths) - a**love


def numerator(lengths, a):
    love = len(lengths)
    if love == 0:
        return 1

    return  a*(numerator(lengths[1:], a)) + 2**(sum(lengths))


def number_of_kinks(cycle):
    # Find places where value increases (an+b been applied)
    shifted = list(cycle[1:]) + list([cycle[0]])
    return len([x for x, y in zip(cycle, shifted) if x < y])


def constraint(t):
    # should be increasing i guess
    return all(x<y for x, y in zip(t, t[1:]))


def itery(numbers, num_variables):
    return [t for t in it.combinations_with_replacement(numbers, num_variables) if constraint(t)]


def number_of_cycles(a, b, kink):
    # why kink > 1?
    if kink > 1 and a % 3 == 0 and b in {3**i for i in range(1,10)}:
        return 0
    
    count = 0
    for t in itery(range(1, MAX_CONSECUTIVE_DIVISIONS), kink): # because x!=y
        n = b * numerator(t[1:], a) / denominator(t, a)
        if n > 0 and n.is_integer(): # Each integer solution indicates a different cycle
            count += 1
    return count


# fix me
def number_of_3_kink_cycles(a, b):
    if a % 3 == 0 and b in {3**i for i in range(1,10)}:
        return 0
    

    #make shift solution will check that solution does not match any previous found
    found_ugh = set()
    count = 0
    for x in range(1, MAX_CONSECUTIVE_DIVISIONS+1): 
        for y in range(1, MAX_CONSECUTIVE_DIVISIONS+1):
            for z in range(1, y):
                t = (x,y,z)
                n = b*numerator(t[1:],a)/denominator(t, a)
                if n > 0 and n.is_integer():
                    new_cycle = True
                    for poo in found_ugh:
                        shifted = list(poo[1:]) + list([poo[0]])
                        if t == tuple(shifted):
                            new_cycle = False
                    if new_cycle:
                        found_ugh.add(t)
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

     
def test():
    for a in range(3,100,2):
        for b in range(1,100,2):
            cycles = find_cycles(a, b)

            print("a={}, b={}, cycles={}".format(a, b, len(cycles)))
            predicted_cycles = [number_of_cycles(a, b, 1), number_of_cycles(a, b, 2), number_of_3_kink_cycles(a,b)]
            for i in range(1,4):
                divided_cycles = [cycle for cycle in cycles if number_of_kinks(cycle) == i]
                for s in sorted(divided_cycles, key=len):
                    print(s)

                if len(divided_cycles) != predicted_cycles[i-1]:
                    raise Exception("Predicted {}, found {}".format(predicted_cycles[i-1], len(divided_cycles)))

            print()

    
MAX_CONSECUTIVE_DIVISIONS = 20
MAX_CYCLE_LEN = 100

c = 2   # /2

test()
