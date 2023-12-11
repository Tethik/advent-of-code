package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func a(content string) {
	lines := strings.Split(content, "\n")

	// Expand lines for empty rows
	for i := 0; i < len(lines); i++ {
		if emptyLine(lines[i]) {
			fmt.Println("Inserting line", i)
			lines = slices.Insert(lines, i, lines[i])
			i++
		}
	}

	// Expand lines for empty columns
	for i := 0; i < len(lines[0]); i++ {
		empty := true
		for j := 0; j < len(lines); j++ {
			if lines[j][i] != '.' {
				empty = false
				break
			}
		}
		if empty {
			fmt.Println("Inserting column", i)
			for j := 0; j < len(lines); j++ {
				lines[j] = lines[j][:i] + "." + lines[j][i:]				
			}
			i++
		}
	}

	// Show the map
	for _, line := range lines {
		println(line)
	}

	fmt.Println("Cosmos has expanded")

	galaxies := []lib.Coord{}
	for y, line := range lines {
		for x, c := range line {
			if c == '#' {
				galaxies = append(galaxies, lib.Coord{X: x, Y: y})
			}
		}
	}

	fmt.Println("Galaxies identified")


	// Naive approach, just check all pairs	
	sum := 0
	for i, a := range galaxies {
		for _, b := range galaxies[i+1:] {
			dist := a.ManhattanDistance(b)
			sum += dist
		}		
	}

	fmt.Println(sum)

}
