package main

import (
	"fmt"
	. "imageProcessing/process"
	"log"

	"gocv.io/x/gocv"
)

func main() {
	// im, _, err := ReadImage("./flower.JPG")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	img := gocv.IMRead("./flowerGray.jpg", gocv.IMReadGrayScale)
	defer img.Close()
	window1 := gocv.NewWindow("1")
	window2 := gocv.NewWindow("2")
	defer window1.Close()
	defer window2.Close()
	kernel, err := gocv.NewMatFromBytes(3, 3, gocv.MatTypeCV8UC1, []byte{-2, -1, 0, -1, 0, 1, 0, 1, 2})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(img)
	res := CustomFilter(img, kernel)
	gocv.IMWrite("CustomFilter.jpg", *res)
	for {
		window1.IMShow(img)
		window2.IMShow(*res)
		if window2.WaitKey(1) >= 0 {
			break
		}
	}

	// SaveJPEG(noise, "./SaltAndPepperNoise.jpg")
	// SaveJPEG(res, "./withSaltAndPepperNoise.jpg")
}
