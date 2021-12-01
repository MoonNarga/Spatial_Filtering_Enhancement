package main

import (
	"image"
	"log"
	"os"
)

func readImage(filename string) (image.Image, string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, "", err
	}
	defer file.Close()
	return image.Decode(file)
}

func main() {
	im, _, err := readImage("./flower.JPG")
	if err != nil {
		log.Fatal(err)
	}
	bounds := im.Bounds()
	imgray := image.NewGray(bounds)
	imgray
}