import sys

patterns = {
    2: "cf", #1
    4: "bcdf", #4
    3: "acf", #7,
    7: "abcdefg" #8
}

o = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "abcdefg": 8, 
    
    "acdeg": 2,
    "acdfg": 3, #cf    
    "abdfg": 5,
    
    
    

    "abdefg": 6, 
    "abcefg": 0, #cf, acf
    "abcdfg": 9 #cf, acf, bcdf
}

            
def gen_filter(_len, contains, words):
    print(contains)
    letters = "".join(contains)
    print(letters)
    li = list(filter(lambda w: len(w) == _len and all(c in w for c in letters), words))
    print(_len, contains, words, "=", li)
    assert len(li) == 1
    words.remove(li[0])
    return "".join(li[0])


big_sum = 0
for line in sys.stdin:
    p1, p2 = line.split("|")
    
    words = ["".join(sorted(w)) for w in p1.split()]

    # generate mapping    
    m = dict()
    m["1"] = cf = gen_filter(2, [], words)
    m["7"] = acf = gen_filter(3, [], words)
    m["4"] = bcdf = gen_filter(4, [], words)
    bd = "".join([c for c in bcdf if c not in cf])
    m["8"] = abcdefg = gen_filter(7, [], words)
    
    # 5s
    m["5"] = gen_filter(5, [bd], words)
    m["3"] = gen_filter(5, [cf], words)
    m["2"] = gen_filter(5, [], words)
    # 6s
    m["9"] = abcdfg = gen_filter(6, [bcdf], words)
    m["6"] = abdfg = gen_filter(6, [bd], words)
    m["0"] = words.pop()

    f = dict()
    for k, v in m.items():
        f[v] = k

    assert len(words) == 0
    print(f)

    num = ""
    for word in p2.split():
        # num = ""
        # for w in words.split():
        s = "".join(sorted(word))
        num += f[s]
    
    print(num)
    big_sum += int(num)

    

print(big_sum)
