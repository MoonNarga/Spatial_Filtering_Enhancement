package main

import (
	"bufio"
	"encoding/base64"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"io"
	"log"
	"os"
)

func Show(f func(dx, dy int) [][]uint8) {
	const (
		dx = 256
		dy = 256
	)
	data := f(dx, dy)
	m := image.NewNRGBA(image.Rect(0, 0, dx, dy))
	for y := 0; y < dy; y++ {
		for x := 0; x < dx; x++ {
			v := data[y][x]
			i := y*m.Stride + x*4
			m.Pix[i] = v
			m.Pix[i+1] = v
			m.Pix[i+2] = 255
			m.Pix[i+3] = 255
		}
	}
	ShowImage(m)
}

// ShowImage displays the image m
// when executed on the Go Playground.
func ShowImage(m image.Image) {
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	io.WriteString(w, "IMAGE:")
	b64 := base64.NewEncoder(base64.StdEncoding, w)
	err := (&png.Encoder{CompressionLevel: png.BestCompression}).Encode(b64, m)
	if err != nil {
		panic(err)
	}
	b64.Close()
	io.WriteString(w, "\n")
}

func readImage(filename string) (image.Image, string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, "", err
	}
	defer file.Close()
	return image.Decode(file)
}

func SaveJPEG(im image.Image, name string) error {
	file, err := os.Create(name)
	if err != nil {
		return err
	}
	defer file.Close()
	return jpeg.Encode(file, im, &jpeg.Options{100})
}

func main() {
	im, _, err := readImage("./flower.JPG")
	if err != nil {
		log.Fatal(err)
	}
	bounds := im.Bounds()
	imgray := image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, _ := im.At(x, y).RGBA()
			r = r >> 8
			g = g >> 8
			b = b >> 8
			v := uint8((float32(r)*299 + float32(g)*587 + float32(b)*114) / 1000)
			imgray.Set(x, y, color.Gray{v})
		}
	}

	SaveJPEG(imgray, "./1.jpg")
}
