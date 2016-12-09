package main

import "fmt"

func main() {
	messages := make(chan string)
	go func() { messages <- "ping" }()
	go func() { messages <- "hello" }()

	msg1, msg2 := <-messages, <-messages
	fmt.Println(msg1)
	fmt.Println(msg2)
}
