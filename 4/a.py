import sys
from itertools import chain


def tokenize(line: str):
    tok = ""
    for c in line:
        if c.strip() == "":
            if len(tok) > 0:
                yield Cell(tok)
                tok = ""
            continue
        tok += c


class Cell:
    def __init__(self, value) -> None:
        self.value = int(value)
        self.marked = False

    def mark(self, number):
        self.marked = self.marked or number == self.value

    def __str__(self) -> str:
        if self.marked:
            return f"*{self.value}*"
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


CARD_WIDTH = 5


class Card:
    def __init__(self, lines) -> None:
        self.rows = []
        self.cols = []
        self.left_diagonal = []
        self.right_diagonal = []

        self.rows = [list(tokenize(line)) for line in lines]

        for x in range(CARD_WIDTH):
            self.cols.append([])
            for y in range(CARD_WIDTH):
                self.cols[x].append(self.rows[y][x])

        print(len(lines))
        print(self.rows)
        print(self.cols)
        print()

        for d in range(CARD_WIDTH):
            self.left_diagonal.append(self.rows[d][d])
            self.right_diagonal.append(
                self.rows[CARD_WIDTH - 1 - d][CARD_WIDTH - 1 - d])

    def mark(self, number) -> bool:
        for cell in chain.from_iterable(self.rows):
            cell.mark(number)
        return self.check()

    def check(self):
        for l in chain.from_iterable([self.rows, self.cols, [self.right_diagonal, self.left_diagonal]]):
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
                s += f"{str(cell):<6} "
            s += "\n"
        return s


call_outs = input().split(",")

lines = []
cards = []
for line in sys.stdin.readlines():
    if line.strip() == "":
        continue

    lines.append(line)

    if len(lines) == 5:
        card = Card(lines)
        cards.append(card)
        lines = []
        continue


won = dict()
for t, call in enumerate([int(c) for c in call_outs]):
    print(f"Callout: {call} (t: {t})")
    for i, card in enumerate(cards):
        if i in won.keys():
            continue

        # print(f"Checking card {i}")
        if card.mark(call):
            print(f"Bingo on card {i}!")
            print(card)
            # print(call, card.sum(), call * card.sum())
            won[i] = (t, call, card.sum(), call * card.sum())
            print()

    print()
    if len(won) == len(cards):
        break

for key, val in sorted(won.items(), key=lambda dict_item: dict_item[1][0]):
    print(key, val)

print(len(won), len(cards))
