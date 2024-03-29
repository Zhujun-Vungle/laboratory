package main

import "fmt"

func f(from string) {
	for i := 0; i < 30; i++ {
		fmt.Println(from, ":", i)
	}
}

func main() {
	f("direct")

	go f("goroutine")
	go f("yes it is")
	go func(msg string) {
		fmt.Println(msg)
	}("going")

	var input string

	fmt.Scanln(&input)

	fmt.Println("done")
}
