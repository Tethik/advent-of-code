package lib

import "os"

// ReadInput reads the input from the file at the given path
// cleans up any newlines and returns the input as a string
func ReadInput(path string) string {
	bytes, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	content := string(bytes)
	if content[len(content)-1] == '\n' {
		content = content[:len(content)-1]
	}
	return content
}
