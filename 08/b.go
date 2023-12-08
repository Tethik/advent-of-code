package main

import (
	"fmt"
	"regexp"
	"strings"
)

func b(content string) {
	lines := strings.Split(content, "\n")

	// XGS = (FDM, XCS)
	pattern := regexp.MustCompile(`(\w+) = \((\w+), (\w+)\)`)

	nodes := map[string]*Node{}
	instructions := lines[0]
	
	for _, line := range lines[2:] {
		m := pattern.FindStringSubmatch(line);
		fmt.Println(line, m)
		
		n, ok := nodes[m[1]]; 
		if !ok {
			n = &Node{}
			n.value = m[1]
			nodes[m[1]] = n
		} 
		l, ok := nodes[m[2]];
		if !ok {
			l = &Node{}
			l.value = m[2]
			nodes[m[2]] = l
		}
		n.left = l
		r, ok := nodes[m[3]];
		if !ok {
			r = &Node{}
			r.value = m[3]
			nodes[m[3]] = r
		}
		n.right = r
	}


	startNodes := []*Node{}
	for _, n := range nodes {
		if n.value[2] == 'A' {
			startNodes = append(startNodes, n)
		}
	}
	ends := map[string]*Node{}
	for _, n := range nodes {
		if n.value[2] == 'Z' {
			ends[n.value] = n
		}
	}

	fmt.Println(startNodes)
	fmt.Println(ends)


	// WIP detect cycles here for each start node
	// then find commmon multiple of all cycles
	s := 0
	allZ := false
	
	for !allZ {
		allZ = true
		for i, n := range startNodes {
			s++

			for _, c := range instructions {				
				if c == 'L' {
					startNodes[i] = n.left
				} else if c == 'R' {
					startNodes[i] = n.right
				}

				_, ok := ends[startNodes[i].value];				
				allZ = allZ && ok			
			}


		}
	}

	fmt.Println(s)
}
