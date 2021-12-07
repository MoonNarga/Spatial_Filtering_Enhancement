package main

import (
	"log"

	"imageProcessing/process"
)

func main() {
	im, _, err := process.ReadImage("./flower_gray.JPG")
	if err != nil {
		log.Fatal(err)
	}

	process.SaveJPEG(process.SetColor(im), "./1.jpg")
}
