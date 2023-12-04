package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func a() {
	// content := lib.ReadInput("example")
	content := lib.ReadInput("input")
	lines := strings.Split(content, "\n")

	sum := 0
	for _, line := range lines {
		parts := strings.Split(line, ":")
		card := parts[1]
		parts = strings.Split(card, "|")
		
		winning := map[int]bool{}
		for _, v := range strings.Split(strings.TrimSpace(parts[0]), " ") {
			if v == "" {
				continue
			}
			num, err := strconv.Atoi(v)
			if err != nil {
				panic(err)
			}
			winning[num] = true
		}
		
		pow := 0
		for _, v := range strings.Split(strings.TrimSpace(parts[1]), " ") {
			if v == "" {
				continue
			}
			num, err := strconv.Atoi(v)
			if err != nil {
				panic(err)
			}
			if _, win := winning[num]; win {
				if pow == 0 {
					pow = 1
				} else {
					pow *= 2
				}				
			}
		}
		sum += pow
		fmt.Println(pow)
	}
	fmt.Println(sum)

}
