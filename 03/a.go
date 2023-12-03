package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func a() {
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
	wholeNumbers := []string{}

	for _, number := range numberMap {
		if visited[number.String()] {
			continue
		}
		visited[number.String()] = true

		num := string(number.Number)

		pieces := []Number{number}
		// Check if there is a number to the right
		right, ok := numberMap[number.Right().String()]
		for ok {
			pieces = append(pieces, right)
			visited[right.String()] = true
			num = num + string(right.Number)
			right, ok = numberMap[right.Right().String()]
		}
		// Check if there is a number to the left
		left, ok := numberMap[number.Left().String()]
		for ok {
			pieces = append(pieces, left)
			visited[left.String()] = true
			num = string(left.Number) + num
			left, ok = numberMap[left.Left().String()]
		}

		fmt.Println(num)

		// Check if any symbols are neighbors to the number
		nextToSymbol := false
	symbolCheck:
		for _, np := range pieces {
			for _, neigh := range np.Neighbors8() {
				if _, ok := symbolMap[neigh.String()]; ok {
					nextToSymbol = true
					break symbolCheck
				}
			}
		}

		if nextToSymbol {
			wholeNumbers = append(wholeNumbers, num)
		}
	}

	fmt.Println(wholeNumbers)
	sum := 0
	for _, num := range wholeNumbers {
		n, _ := strconv.Atoi(num)
		sum += n
	}
	fmt.Println(sum)

}
