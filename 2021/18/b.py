import sys
from a2 import magnitude, add

if __name__ == "__main__":
    print("""
    ##################################
            main
    ##################################
    """)

    fishies = [line.strip() for line in sys.stdin if line.strip() != ""]

    _max = 0
    for f1 in fishies:
        for f2 in fishies:
            if f1 == f2:  # unsure if dupes are allowed
                continue
            fish = add(f1, f2)
            _max = max(_max, magnitude(fish))

    print(_max)
