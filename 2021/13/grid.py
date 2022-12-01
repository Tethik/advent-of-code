class Grid:
    def __init__(self) -> None:
        self.rows = []

    def width(self):
        return len(self.rows[0])

    def height(self):
        return len(self.rows)

    def set(self, x, y, val):
        self.rows[y][x] = val
