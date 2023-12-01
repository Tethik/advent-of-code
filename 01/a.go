package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func mainA() {
	f, err := os.ReadFile(os.Args[1])

	if err != nil {
		panic(err)
	}

	contents := string(f)

	s := 0
	for _, line := range strings.Split(contents, "\n") {
		first := -1
		second := -1
		for _, c := range line {
			if n, err := strconv.Atoi(string(c)); err == nil {
				fmt.Printf("%q looks like a number.\n", c)
				if first == -1 {
					first = n
				}
				second = n
			}
		}
		if first != -1 && second != -1 {
			fmt.Printf("%d + %d = %d\n", first, second, first+second)
			s += first*10 + second
		}
	}
	fmt.Println(s)

}
