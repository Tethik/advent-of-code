package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func match(line string) int {
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
			pow += 1
		}
	}
	return pow
}

func b() {
	// content := lib.ReadInput("example2")
	content := lib.ReadInput("input")
	lines := strings.Split(content, "\n")


	matches := map[int]int{}
	for i := len(lines) - 1; i > -1; i-- {
		card := i + 1
		m := match(lines[i])
		fmt.Println(card, m)
		matches[card] = m
	}

	counts := map[int]int{}
	
	fmt.Println()
	for card := 1; card < len(lines) + 1; card++ {			
		counts[card] += 1 // count initial copy
		m := matches[card]
		c := counts[card]
		// fmt.Println(card, m, c)
		for j := card + 1; j <= card + m; j++ { 
			// fmt.Println(j, c)
			counts[j] += c
		}
		// fmt.Println()
	}

	fmt.Println()
	sum := 0
	for i := len(lines) - 1; i > -1; i-- {
		card := i + 1
		val := counts[card]
		fmt.Println(card, val)
		sum += val
	}
	fmt.Println(sum)
}
