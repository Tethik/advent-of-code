package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

type SeedRange struct {
	Src int
	Ran int
}

func (sr *SeedRange) Contains(num int) bool {
	return num >= sr.Src && num <= sr.Src+sr.Ran
}

func Lowest(sr SeedRange, maps []TaskMap, c chan int) {
	lowest := 99999999999999999
	lowestSeed := -1
	for i := 0; i < sr.Ran; i++ {
		s := sr.Src + i
		for _, m := range maps {			
			s = m.Translate(s)
		}
		// fmt.Println(seed)
		if s < lowest {
			lowest = s
			lowestSeed = sr.Src + i
		}
	}
	fmt.Println("seed range", sr.Src, sr.Ran, "lowest", lowest, "seed", lowestSeed)		
	c <- lowest
}


func b() {
	numberPattern := regexp.MustCompile(numberLineRe)
	headerPattern := regexp.MustCompile(headerLineRe)

	
	// content := lib.ReadInput("example")
	content := lib.ReadInput(os.Args[1])
	lines := strings.Split(content, "\n")

	seedRangeStr := strings.Split(strings.Split(lines[0], ": ")[1], " ")
	seedRanges := []SeedRange{}
	totalSeeds := 0
	for i := 0; i < len(seedRangeStr); i += 2 {
		src := lib.MustAtoi(seedRangeStr[i])
		ran := lib.MustAtoi(seedRangeStr[i+1])
		seedRanges = append(seedRanges, SeedRange{Src: src, Ran: ran})
		fmt.Println(src, ran)
		totalSeeds += ran
	}

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
	fmt.Println("seeds:", totalSeeds)	
	c := make(chan int)
	for _, rng := range seedRanges {				
		go Lowest(rng, maps, c)
	}

	lowest := 99999999999999999
	for i := 0; i < len(seedRanges); i++ {
		l := <-c		
		if l < lowest {
			lowest = l
		}
	}

	fmt.Println(lowest)
}
