package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func b() {
	// content := lib.ReadInput("example")
	content := lib.ReadInput("input")
	lines := strings.Split(content, "\n")

	var symbols []lib.Coord
	symbolMap := map[string]rune{}
	// var numbers []Number
	numberMap := map[string]Number{}

	for y, line := range lines {
		for x, char := range line {
			if char == '.' {
				continue
			}

			c := lib.Coord{x, y}
			if strings.ContainsRune("0123456789", char) {
				number := Number{c, char}
				// numbers = append(numbers, number)
				numberMap[c.String()] = number
			} else {
				symbols = append(symbols, c)
				symbolMap[c.String()] = char
			}
		}
	}

	visited := map[string]bool{}
	neighbourToSymbol := map[string][]int{}

	for _, number := range numberMap {
		if visited[number.String()] {
			continue
		}
		visited[number.String()] = true

		numS := string(number.Number)

		pieces := []Number{number}
		// Check if there is a number to the right
		right, ok := numberMap[number.Right().String()]
		for ok {
			pieces = append(pieces, right)
			visited[right.String()] = true
			numS = numS + string(right.Number)
			right, ok = numberMap[right.Right().String()]
		}
		// Check if there is a number to the left
		left, ok := numberMap[number.Left().String()]
		for ok {
			pieces = append(pieces, left)
			visited[left.String()] = true
			numS = string(left.Number) + numS
			left, ok = numberMap[left.Left().String()]
		}

		fmt.Println(numS)
		num, err := strconv.Atoi(numS)
		if err != nil {
			panic(err)
		}

		// Check if any symbols are neighbors to the number
		seen := map[string]bool{}
		for _, np := range pieces {
			for _, neigh := range np.Neighbors8() {
				if _, ok := symbolMap[neigh.String()]; ok {
					if seen[neigh.String()] {
						continue
					}
					seen[neigh.String()] = true
					if _, ok := neighbourToSymbol[neigh.String()]; !ok {
						neighbourToSymbol[neigh.String()] = []int{}
					}

					neighbourToSymbol[neigh.String()] = append(neighbourToSymbol[neigh.String()], num)
				}
			}
		}
	}

	ratios := []int{}
	for _, symbol := range symbols {
		if symbolMap[symbol.String()] != '*' {
			continue
		}

		neighbours := neighbourToSymbol[symbol.String()]
		if len(neighbours) != 2 {
			// Should not happen according to the problem description
			fmt.Println("Not 2 neighbours", symbol, neighbours)
			continue
		}

		ratio := neighbours[0] * neighbours[1]
		ratios = append(ratios, ratio)
	}

	fmt.Println(ratios)
	sum := 0
	for _, num := range ratios {
		sum += num
	}
	fmt.Println(sum)

}
