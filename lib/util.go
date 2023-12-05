package lib

import "strconv"

func MustAtoi(s string) int {
	v, e := strconv.Atoi(s)
	if e != nil {
		panic(e)
	}
	return v
}