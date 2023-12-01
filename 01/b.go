package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	f, err := os.ReadFile(os.Args[1])

	vals := []string{
		"zero",
		"one",
		"two",
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
		"0",
		"1",
		"2",
		"3",
		"4",
		"5",
		"6",
		"7",
		"8",
		"9",
	}

	m := map[string]int{}

	for i, v := range vals {
		m[v] = i % 10
	}

	if err != nil {
		panic(err)
	}

	contents := string(f)

	s := 0
	for _, line := range strings.Split(contents, "\n") {
		fmt.Println(line)

		first := -1
		best := len(line)
		for _, v := range vals {
			i := strings.Index(line, v)
			if i < 0 {
				continue
			}

			if i < best {
				best = i
				first = m[v]
			}
		}
		fmt.Println(best, first)

		second := -1
		best = -1
		for _, v := range vals {
			i := strings.LastIndex(line, v)
			if i < 0 {
				continue
			}

			if i > best {
				best = i
				second = m[v]
			}
		}
		fmt.Println(best, second)
		fmt.Println(first, second)
		fmt.Println()
		if first != -1 && second != -1 {
			s += first*10 + second
		}
	}
	fmt.Println(s)

}
