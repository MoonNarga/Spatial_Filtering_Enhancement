package main

import (
	"fmt"
	"log"

	. "imageProcessing/process"
)

func main() {
	im, _, err := ReadImage("./flower.JPG")
	if err != nil {
		log.Fatal(err)
	}

	// SaveJPEG(SetColor(*RGBA2Gray(im)), "./1.jpg")
	bounds := im.Bounds()
	// imgray := image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, a := im.At(x, y).RGBA()
			fmt.Printf("%b, %b, %b, %b\n", r, g, b, a)
			// r = r >> 8
			// g = g >> 8
			// b = b >> 8
			// Y_YUV := uint8((float32(r)*299 + float32(g)*587 + float32(b)*114) / 1000)
			// imgray.Set(x, y, color.Gray{Y_YUV})
		}
	}
}
