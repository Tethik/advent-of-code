import sys
from itertools import chain


class Cell:
    def __init__(self, value) -> None:
        self.value = int(value)
        self.marked = False
        self.subscribed = []

    def mark(self):
        self.marked = True

    def __str__(self) -> str:
        if self.marked:
            return f"*{self.value}*"
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


cellRefs = dict([(val, Cell(val)) for val in range(100)])


def tokenize(line: str):
    tok = ""
    for c in line:
        if c.strip() == "":
            if len(tok) > 0:
                yield cellRefs.get(int(tok))
                tok = ""
        else:
            tok += c


CARD_WIDTH = 5


class Card:
    def __init__(self, id, lines) -> None:
        self.id = id
        self.rows = []
        self.cols = []
        # Oops, did not need diagonal :)
        # self.left_diagonal = []
        # self.right_diagonal = []

        self.rows = [list(tokenize(line)) for line in lines]
        for cell in chain.from_iterable(self.rows):
            cell.subscribed.append(self)

        for x in range(CARD_WIDTH):
            self.cols.append([])
            for y in range(CARD_WIDTH):
                self.cols[x].append(self.rows[y][x])

        print(len(lines))
        print(self.rows)
        print(self.cols)
        print()

        # for d in range(CARD_WIDTH):
        #     self.left_diagonal.append(self.rows[d][d])
        #     self.right_diagonal.append(
        #         self.rows[CARD_WIDTH - 1 - d][CARD_WIDTH - 1 - d])

    def check(self):
        # , [self.right_diagonal, self.left_diagonal]]):
        for l in chain.from_iterable([self.rows, self.cols]):
            # print(l)
            if all(c.marked for c in l):
                print(l)
                return True
            # print()
        return False

    def sum(self) -> int:
        return sum(cell.value for cell in chain.from_iterable(self.rows) if not cell.marked)

    def __str__(self) -> str:
        s = ""
        for row in self.rows:
            for cell in row:
                s += f"{str(cell):<5}"
            s += "\n"
        return s


call_outs = input().split(",")

lines = []
cards = []
i = 1
for line in sys.stdin:
    if line.strip() == "":
        continue

    lines.append(line)

    if len(lines) == 5:
        card = Card(i, lines)
        cards.append(card)
        lines = []
        i += 1
        continue

print("Boards:")
for card in cards:
    print(card)
    print()
print()


won = dict()
print("Simlating callouts:")
for t, call in enumerate([int(c) for c in call_outs]):
    print(f"Callout: {call} (t: {t})")
    cell = cellRefs[call]
    cell.marked = True

    for card in cell.subscribed:
        if card.id in won.keys():
            continue

        if card.check():
            print(f"Bingo on card {card.id}!")
            print(card)
            print(f"Sum: {call} * {card.sum()} = {call * card.sum()}")
            print(f"Callouts: {call_outs[:t+1]}")
            won[card.id] = (t, call, card.sum(), call * card.sum())
            print()

    print()
    if len(won) == len(cards):
        break

print()
print("Winning Table:")
for key, val in sorted(won.items(), key=lambda dict_item: dict_item[1][0]):
    print(key, val)

print(len(won), len(cards))
