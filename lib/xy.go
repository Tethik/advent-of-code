package lib

import "fmt"

type Coord struct {
	X int
	Y int
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func (c Coord) Add(other Coord) Coord {
	return Coord{c.X + other.X, c.Y + other.Y}
}

func (c Coord) Sub(other Coord) Coord {
	return Coord{c.X - other.X, c.Y - other.Y}
}

// func (c Coord) Mul(other Coord) Coord {
// 	return Coord{c.X * other.X, c.Y * other.Y}
// }

// func (c Coord) Div(other Coord) Coord {
// 	return Coord{c.X / other.X, c.Y / other.Y}
// }

func (c Coord) Abs() Coord {
	return Coord{Abs(c.X), Abs(c.Y)}
}

func (c Coord) Copy() Coord {
	return Coord{c.X, c.Y}
}

type Direction int

const (
	Up Direction = iota
	Down
	Left
	Right // May need diagonals later too
)

func (c Coord) Neighbors() []Coord {
	return []Coord{
		c.Add(Coord{0, 1}),
		c.Add(Coord{0, -1}),
		c.Add(Coord{1, 0}),
		c.Add(Coord{-1, 0}),
	}
}

func (c Coord) Neighbors8() []Coord {
	return []Coord{
		c.Add(Coord{0, 1}),
		c.Add(Coord{0, -1}),
		c.Add(Coord{1, 0}),
		c.Add(Coord{-1, 0}),
		c.Add(Coord{1, 1}),
		c.Add(Coord{1, -1}),
		c.Add(Coord{-1, 1}),
		c.Add(Coord{-1, -1}),
	}
}

func (c Coord) Left() Coord {
	return c.Add(Coord{-1, 0})
}

func (c Coord) Right() Coord {
	return c.Add(Coord{1, 0})
}

func (c Coord) Up() Coord {
	return c.Add(Coord{0, -1})
}

func (c Coord) Down() Coord {
	return c.Add(Coord{0, 1})
}

func (c Coord) String() string {
	return fmt.Sprintf("(%d, %d)", c.X, c.Y)
}

func (c Coord) Equals(other Coord) bool {
	return c.X == other.X && c.Y == other.Y
}

type Bounds struct {
	Min Coord
	Max Coord
}

func (b Bounds) Contains(c Coord) bool {
	return c.X >= b.Min.X && c.X <= b.Max.X && c.Y >= b.Min.Y && c.Y <= b.Max.Y
}
