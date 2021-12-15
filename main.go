package main

import (
	"log"

	. "imageProcessing/process"
)

func main() {
	im, _, err := ReadImage("./flower_gray.JPG")
	if err != nil {
		log.Fatal(err)
	}

	SaveJPEG(GenerateGaussNoise(*RGBA2Gray(im), 1, 2), "./1.jpg")
}
