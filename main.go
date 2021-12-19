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

	SaveJPEG(GenerateGaussNoise(*RGBA2Gray(im), 0, 1), "./1.jpg")
}
