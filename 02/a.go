package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Count = map[string]int

func main() {
	f, err := os.ReadFile(os.Args[1])

	if err != nil {
		panic(err)
	}

	contents := string(f)

	s := 0
	bSum := 0
	for _, line := range strings.Split(contents, "\n") {
		if len(strings.TrimSpace(line)) == 0 {
			continue
		}

		var counts []Count
		fmt.Println(line)

		parts := strings.Split(line, ":")
		idx, err := strconv.Atoi(strings.Split(parts[0], " ")[1])
		if err != nil {
			panic(err)
		}

		gamePart := parts[1]
		fmt.Println(gamePart)
		for _, round := range strings.Split(gamePart, ";") {
			fmt.Println(round)
			count := Count{}
			for _, part := range strings.Split(round, ",") {
				p := strings.TrimSpace(part)
				a := strings.Split(p, " ")
				// Format is color = count, e.g red 12
				count[a[1]], err = strconv.Atoi(a[0])
				if err != nil {
					panic(err)
				}
			}
			counts = append(counts, count)
		}

		// only 12 red cubes, 13 green cubes, and 14 blue cubes
		fail := false
		for _, count := range counts {
			if count["red"] > 12 || count["green"] > 13 || count["blue"] > 14 {
				fail = true
				break
			}
		}

		if !fail {
			s += idx
		}

		// Part B - multiply highest count of each color
		highest := map[string]int{}
		for _, count := range counts {
			for color, val := range count {
				if val > highest[color] {
					highest[color] = val
				}
			}
		}
		m := 1
		for _, val := range highest {
			m *= val
		}
		fmt.Println(m)
		bSum += m
		fmt.Println()
	}
	fmt.Println(s)
	fmt.Println(bSum)

}
