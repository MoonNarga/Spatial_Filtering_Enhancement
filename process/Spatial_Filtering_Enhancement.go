package process

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"io"
	"os"
)

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

func ReadImage(filename string) (image.Image, string, error) {
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

func RGBA2Gray(im image.Image) *image.Gray {
	bounds := im.Bounds()
	imgray := image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, _ := im.At(x, y).RGBA()
			r = r >> 8
			g = g >> 8
			b = b >> 8
			Y_YUV := uint8((float32(r)*299 + float32(g)*587 + float32(b)*114) / 1000)
			imgray.Set(x, y, color.Gray{Y_YUV})
		}
	}
	return imgray
}

func SetColor(im image.Gray) *image.RGBA {
	bounds := im.Bounds()
	imRGBA := image.NewRGBA(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			Y := im.At(x, y)
			r, g, b, a := Y.RGBA()
			fmt.Println(Y, r, g, b, a)
			// Y_YUV := uint8((float32(r)*299 + float32(g)*587 + float32(b)*114) / 1000)
			imRGBA.Set(x, y, color.RGBA{uint8(r), uint8(g), uint8(b), uint8(a)})
		}
	}
	return imRGBA
}
