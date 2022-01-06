package main

import (
	. "imageProcessing/process"

	"gocv.io/x/gocv"
)

func main() {
	src := gocv.IMRead("./flowerGray.jpg", gocv.IMReadGrayScale)
	defer src.Close()
	window1 := gocv.NewWindow("1")
	window2 := gocv.NewWindow("2")
	window3 := gocv.NewWindow("3")
	defer window1.Close()
	defer window2.Close()
	defer window3.Close()
	// high := DFTtrans(src)
	res := DFTtrans(src)
	// gocv.IMWrite("DFT_High.jpg", *high)
	// gocv.IMWrite("DFT_Low.jpg", *low)
	for {
		window1.IMShow(*res)
		// window2.IMShow(*high)
		// window3.IMShow(*low)
		if window3.WaitKey(1) >= 0 {
			break
		}
	}
}
