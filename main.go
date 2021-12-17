package main

import (
	"log"

	. "imageProcessing/process"
)

func main() {
	im, _, err := ReadImage("./flower.JPG")
	if err != nil {
		log.Fatal(err)
	}

	SaveJPEG(RGBA2Gray(im), "./1.jpg")
}
