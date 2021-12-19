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
	SaveJPEG(FakeColor(*RGBA2Gray(im)), "./FakeColor.jpg")
	noise, res := GenerateGaussNoise(*RGBA2Gray(im), 5, 10)
	SaveJPEG(noise, "./noise.jpg")
	SaveJPEG(res, "./res.jpg")
}
