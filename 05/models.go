package main

import "fmt"

type Range struct {
	Src int
	Ran int
	Dst int
}

func (r *Range) Contains(num int) bool {
	return num >= r.Src && num < r.Src+r.Ran
}

func (r* Range) ContainsDstRange(other *Range) bool {
	return r.Contains(other.Dst) && r.Contains(other.Dst + other.Ran)
}

func (r *Range) String() string {
	return fmt.Sprintf("%d -> %d (%d)", r.Src, r.Dst, r.Ran)
}

// func (r *Range) CombineWith(other Range) []Range {
// 	// Merge with other range so that any overlapping ranges
// 	// will automatically translate through both ranges.
// 	// Example:
// 	// This range 1 -> 2 (2)
// 	// Other range 2 -> 3 (1)
// 	// Combined ranges 1 -> 3 (1), 2 -> 3 (1)

// 	// If the ranges don't overlap, return both ranges
// 	if r.Dst+r.Ran < other.Src || other.Src+other.Ran < r.Dst {
// 		return []Range{*r, other}
// 	}

// 	dstStart, dstEnd := r.Dst, r.Dst+r.Ran


// 	if other.ContainsDstRange(r) {		
// 		return []Range{other}
// 	}

// 	start := r.Dst
// }

type TaskMap struct {
	Src string
	Dst string
	Ranges []Range
}

func (t *TaskMap) Translate(num int) int {
	for _, r := range t.Ranges {
		if r.Contains(num) {
			return num + (r.Dst - r.Src)
		}
	}
	// Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.
	return num
}

func (t *TaskMap) String() string {
	s := t.Src + " -> " + t.Dst
	for _, r := range t.Ranges {
		s += fmt.Sprintf("\n\t%d -> %d (%d)", r.Src, r.Dst, r.Ran)
	}
	return s
}

var numberLineRe = `(\d+) (\d+) (\d+)`
var headerLineRe = `(.+)-to-(.+) map:`