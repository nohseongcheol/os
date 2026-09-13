package vga

import . "unsafe"
import . "ポート"

type Tビデオグラフィックハイレツ struct {
}

var micsポート uint16 = 0x3c2
var crtcモクジポート uint16 = 0x3d4
var crtcデータポート uint16 = 0x3d5
var sequencerモクジポート uint16 = 0x3c4
var sequencerデータポート uint16 = 0x3c5
var グラフィックセイギョキモクジポート uint16 = 0x3ce
var グラフィックセイギョキデータポート uint16 = 0x3cf
var ゾクセイセイギョキモクジポート uint16 = 0x3c0
var ゾクセイセイギョキヨミコミポート uint16 = 0x3c1
var ゾクセイセイギョキカキコミポート uint16 = 0x3c0
var ゾクセイセイギョキリセットポート uint16 = 0x3da

func (self *Tビデオグラフィックハイレツ) Wカキコミレジスタ(レジスタ []byte) {
	var regモクジ uint16 = 0

	Pポートカキコミバイト(micsポート, レジスタ[regモクジ])
	regモクジ++

	var i uint8
	for i = 0; i < 5; i++ {
		Pポートカキコミバイト(sequencerモクジポート, i)
		Pポートカキコミバイト(sequencerデータポート, レジスタ[regモクジ])
		regモクジ++
	}

	Pポートカキコミバイト(crtcモクジポート, 0x03)

	Pポートカキコミバイト(crtcデータポート, (Pポートヨミコミバイト(crtcデータポート) | 0x80))
	Pポートカキコミバイト(crtcモクジポート, 0x11)
	Pポートカキコミバイト(crtcデータポート, (Pポートヨミコミバイト(crtcデータポート) & ^uint8(0x80)))

	レジスタ[0x03] = レジスタ[0x03] | 0x80
	レジスタ[0x11] = レジスタ[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pポートカキコミバイト(crtcモクジポート, i)
		Pポートカキコミバイト(crtcデータポート, レジスタ[regモクジ])
		regモクジ++
	}

	for i = 0; i < 9; i++ {
		Pポートカキコミバイト(グラフィックセイギョキモクジポート, i)
		Pポートカキコミバイト(グラフィックセイギョキデータポート, レジスタ[regモクジ])
		regモクジ++
	}

	for i = 0; i < 21; i++ {
		Pポートヨミコミバイト(ゾクセイセイギョキリセットポート)
		Pポートカキコミバイト(ゾクセイセイギョキモクジポート, i)
		Pポートカキコミバイト(ゾクセイセイギョキカキコミポート, レジスタ[regモクジ])
		regモクジ++
	}

	Pポートヨミコミバイト(ゾクセイセイギョキリセットポート)
	Pポートカキコミバイト(ゾクセイセイギョキモクジポート, 0x20)

}

func (self *Tビデオグラフィックハイレツ) Getフレームbuffersegment() uintptr {
	Pポートカキコミバイト(グラフィックセイギョキモクジポート, 0x06)
	var segmentnumber uint8 = ((Pポートヨミコミバイト(グラフィックセイギョキデータポート) >> 2) & 0x03)
	switch segmentnumber {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (self *Tビデオグラフィックハイレツ) Putpixel(x uint32, y uint32, イロメツギ uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getフレームbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = イロメツギ

}
func (self *Tビデオグラフィックハイレツ) Getイロメツギ(r uint8, g uint8, b uint8) uint8 {
	if r == 0x00 && g == 0x00 && b == 0x00 {
		return 0x00
	}
	if r == 0x00 && g == 0x00 && b == 0xA8 {
		return 0x01
	}
	if r == 0x00 && g == 0xA8 && b == 0x00 {
		return 0x02
	}
	if r == 0xA8 && g == 0x00 && b == 0x00 {
		return 0x04
	}
	if r == 0xFF && g == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (self *Tビデオグラフィックハイレツ) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getイロメツギ(r, g, b))
}
func (self *Tビデオグラフィックハイレツ) Fillクケイ(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tビデオグラフィックハイレツ) Sサポートモード(ハバ uint32, height uint32, ショクdepth uint32) bool {
	return ハバ == 320 && height == 200 && ショクdepth == 8
}
func (self *Tビデオグラフィックハイレツ) Sアリモード(ハバ uint32, height uint32, ショクdepth uint32) bool {
	if !self.Sサポートモード(ハバ, height, ショクdepth) {
		return false
	}

	var g320x200x256 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	self.Wカキコミレジスタ(g320x200x256)

	return true
}
