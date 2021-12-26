package process

import (
	"bufio"
	"encoding/base64"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"
	"io"
	"math/rand"
	"os"
	"time"

	"gocv.io/x/gocv"
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
			Y_YUV := uint8((float32(uint8(r))*299 + float32(uint8(g))*587 + float32(uint8(b))*114) / 1000)
			imgray.Set(x, y, color.Gray{Y_YUV})
		}
	}
	return imgray
}

func FakeColor(im image.Gray) *image.RGBA {
	bounds := im.Bounds()
	imRGBA := image.NewRGBA(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			Y := im.At(x, y)
			r, g, b, a := Y.RGBA()
			r = r >> 8
			g = g >> 8
			b = b >> 8
			imRGBA.Set(x, y, color.RGBA{uint8(r + 5990), uint8(g + 1800), uint8(b + 3250), uint8(a)})
		}
	}
	return imRGBA
}

func GenerateGaussNoise(im image.Gray, mean, sigma float64) (noise, res *image.Gray) {
	rand.Seed(time.Now().UnixNano())
	bounds := im.Bounds()
	noise = image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			Y := im.At(x, y)
			g, _, _, _ := Y.RGBA()
			g = g >> 8
			n := uint8(rand.NormFloat64()*sigma + mean)
			noise.Set(x, y, color.Gray{n})
			im.Set(x, y, color.Gray{uint8(g) + n})
		}
	}
	return noise, &im
}

func GenerateSaltAndPepperNoise(im image.Gray) (noise, res *image.Gray) {
	rand.Seed(time.Now().UnixNano())
	bounds := im.Bounds()
	noise = image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			n := uint8(rand.Intn(255))
			if n > 230 {
				noise.Set(x, y, color.Gray{255})
				im.Set(x, y, color.Gray{255})
			} else if n < 30 {
				noise.Set(x, y, color.Gray{0})
				im.Set(x, y, color.Gray{0})
			}
		}
	}
	return noise, &im
}

func GaussianFilter(src gocv.Mat, ksize int) *gocv.Mat {
	dst := gocv.NewMat()
	gocv.GaussianBlur(src, &dst, image.Point{X: ksize, Y: ksize}, 0, 0, gocv.BorderDefault)
	return &dst
}

func CustomFilter(src gocv.Mat, kernel gocv.Mat) *gocv.Mat {
	dst := gocv.NewMat()
	gocv.Filter2D(src, &dst, gocv.MatTypeCV8UC1, kernel, image.Point{-1, -1}, -1, gocv.BorderDefault)
	return &dst
}

func DFTtrans(src gocv.Mat) {
	// high := gocv.NewMat()
	gocv.DFT(src, &src, gocv.DftComplexOutput)
	// return &src
}