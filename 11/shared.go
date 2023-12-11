package main

func emptyLine(line string) bool {
	for _, c := range line {
		if c != '.' {
			return false
		}
	}
	return true
}