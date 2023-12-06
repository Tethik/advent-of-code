package main

import (
	"fmt"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func parseLine(line string) []int {
	intParts := strings.Split(line, ":")[1]
	var nums []int
	for _, part := range strings.Split(intParts, " ") {
		if part == "" {
			continue
		}
		nums = append(nums, lib.MustAtoi(part))
	}
	return nums
}

func a(content string) {
	lines := strings.Split(content, "\n")
	
	times := parseLine(lines[0])
	distances := parseLine(lines[1])

	fmt.Println(times, distances)
	
	p := 1
	for i := 0; i < len(times); i++ {
		d := distances[i]
		mt := times[i]
		methods := 0
		for t0 := 1; t0 < mt; t0++ {
			tl := mt - t0
			dc := t0 * tl
			if dc > d {
				methods++
			}						
		}
		fmt.Println(methods)		
		p *= methods
	}
	fmt.Println(p)
}
