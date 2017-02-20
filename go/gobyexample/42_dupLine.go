package main

import (
	"bufio"
	"fmt"
	"strings"
)

func main() {
	counts := make(map[string]int)
	str :=strings.NewReader("a\nb\nc\nd\nd\nd\na\n")
        // satisfy interface from io.Reader
	input := bufio.NewScanner(str)

	for input.Scan() {
		counts[input.Text()] ++
	}

	for line, n := range counts {
		fmt.Printf("%d\t%s\n", n, line)
	}
}