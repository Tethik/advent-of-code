package main

import (
	"fmt"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func parseLineB(line string) int {
	intPart := strings.Split(line, ":")[1]	
	return lib.MustAtoi(strings.ReplaceAll(intPart, " ", ""))
}

func b(content string) {
	lines := strings.Split(content, "\n")
	
	time := parseLineB(lines[0])
	distance := parseLineB(lines[1])

	fmt.Println(time, distance)

	methods := 0
	for t0 := 1; t0 < time; t0++ {
		tl := time - t0
		dc := t0 * tl		
		if dc > distance {
			methods++
		}						
	}
	fmt.Println(methods)		

}
