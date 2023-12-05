package main

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

func a() {
	numberPattern := regexp.MustCompile(numberLineRe)
	headerPattern := regexp.MustCompile(headerLineRe)

	// content := lib.ReadInput("example")
	content := lib.ReadInput("input")
	lines := strings.Split(content, "\n")

	seeds := strings.Split(strings.Split(lines[0], ": ")[1], " ")
	fmt.Println(seeds)

	maps := []TaskMap{}
	currMap := &TaskMap{}	
	
	for i, line := range lines[1:] {
		fmt.Println(i, line)
		trimmed := strings.TrimSpace(line)

		if trimmed == "" {
			if i > 0 {
				maps = append(maps, *currMap)
				currMap = &TaskMap{}				
			}
			continue
		}

		if matched := numberPattern.FindStringSubmatch(line); len(matched) > 0 {
			dst := lib.MustAtoi(matched[1])
			src := lib.MustAtoi(matched[2])
			ran := lib.MustAtoi(matched[3])							
			currMap.Ranges = append(currMap.Ranges, Range{Src: src, Dst: dst, Ran: ran})						
		}

		if matched := headerPattern.FindStringSubmatch(line); len(matched) > 0 {
			src := matched[1]
			dst := matched[2]			

			currMap.Src = src
			currMap.Dst = dst
		}
	}
	maps = append(maps, *currMap)

	// Show all maps
	for _, m := range maps {
		println(m.String())
		fmt.Println()
	}

	// Translate all seeds
	lowest := 99999999999999999
	for _, seed := range seeds {
		seedNum := lib.MustAtoi(seed)
		for _, m := range maps {			
			after := m.Translate(seedNum)
			fmt.Println(m.Src, m.Dst, seedNum, after)
			seedNum = after
		}
		fmt.Println(seedNum)
		if seedNum < lowest {
			lowest = seedNum
		}
	}
	
	fmt.Println(lowest)

}
