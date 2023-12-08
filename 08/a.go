package main

import (
	"fmt"
	"regexp"
	"strings"
)

func a(content string) {
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

	n := nodes["AAA"]
	s := 0
mainloop:
	for n.value != "ZZZ" {
		for _, c := range instructions {
			s++
			if c == 'L' {
				n = n.left
			} else if c == 'R' {
				n = n.right
			}
			if n.value == "ZZZ" {
				break mainloop
			}
		}
	}

	fmt.Println(s)
}
