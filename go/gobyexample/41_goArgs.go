package main

import (
  "fmt"
  "os"
  )
// print input args
func main() {
  for _, arg := range os.Args[1:] {
    fmt.Println(arg)
  }
}
