package vga

import . "unsafe"
import . "ぽーと"

type Tびでおぐらふぃっくはいれつ struct {
}

var micsぽーと uint16 = 0x3c2
var crtcもくじぽーと uint16 = 0x3d4
var crtcでーたぽーと uint16 = 0x3d5
var sequencerもくじぽーと uint16 = 0x3c4
var sequencerでーたぽーと uint16 = 0x3c5
var ぐらふぃっくせいぎょきもくじぽーと uint16 = 0x3ce
var ぐらふぃっくせいぎょきでーたぽーと uint16 = 0x3cf
var ぞくせいせいぎょきもくじぽーと uint16 = 0x3c0
var ぞくせいせいぎょきよみこみぽーと uint16 = 0x3c1
var ぞくせいせいぎょきかきこみぽーと uint16 = 0x3c0
var ぞくせいせいぎょきりせっとぽーと uint16 = 0x3da

func (self *Tびでおぐらふぃっくはいれつ) Wかきこみれじすた(れじすた []byte) {
	var regもくじ uint16 = 0

	Pぽーとかきこみばいと(micsぽーと, れじすた[regもくじ])
	regもくじ++

	var i uint8
	for i = 0; i < 5; i++ {
		Pぽーとかきこみばいと(sequencerもくじぽーと, i)
		Pぽーとかきこみばいと(sequencerでーたぽーと, れじすた[regもくじ])
		regもくじ++
	}

	Pぽーとかきこみばいと(crtcもくじぽーと, 0x03)

	Pぽーとかきこみばいと(crtcでーたぽーと, (Pぽーとよみこみばいと(crtcでーたぽーと) | 0x80))
	Pぽーとかきこみばいと(crtcもくじぽーと, 0x11)
	Pぽーとかきこみばいと(crtcでーたぽーと, (Pぽーとよみこみばいと(crtcでーたぽーと) & ^uint8(0x80)))

	れじすた[0x03] = れじすた[0x03] | 0x80
	れじすた[0x11] = れじすた[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pぽーとかきこみばいと(crtcもくじぽーと, i)
		Pぽーとかきこみばいと(crtcでーたぽーと, れじすた[regもくじ])
		regもくじ++
	}

	for i = 0; i < 9; i++ {
		Pぽーとかきこみばいと(ぐらふぃっくせいぎょきもくじぽーと, i)
		Pぽーとかきこみばいと(ぐらふぃっくせいぎょきでーたぽーと, れじすた[regもくじ])
		regもくじ++
	}

	for i = 0; i < 21; i++ {
		Pぽーとよみこみばいと(ぞくせいせいぎょきりせっとぽーと)
		Pぽーとかきこみばいと(ぞくせいせいぎょきもくじぽーと, i)
		Pぽーとかきこみばいと(ぞくせいせいぎょきかきこみぽーと, れじすた[regもくじ])
		regもくじ++
	}

	Pぽーとよみこみばいと(ぞくせいせいぎょきりせっとぽーと)
	Pぽーとかきこみばいと(ぞくせいせいぎょきもくじぽーと, 0x20)

}

func (self *Tびでおぐらふぃっくはいれつ) Getふれーむbuffersegment() uintptr {
	Pぽーとかきこみばいと(ぐらふぃっくせいぎょきもくじぽーと, 0x06)
	var segmentnumber uint8 = ((Pぽーとよみこみばいと(ぐらふぃっくせいぎょきでーたぽーと) >> 2) & 0x03)
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
func (self *Tびでおぐらふぃっくはいれつ) Putpixel(x uint32, y uint32, いろめつぎ uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getふれーむbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = いろめつぎ

}
func (self *Tびでおぐらふぃっくはいれつ) Getいろめつぎ(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tびでおぐらふぃっくはいれつ) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getいろめつぎ(r, g, b))
}
func (self *Tびでおぐらふぃっくはいれつ) Fillくけい(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tびでおぐらふぃっくはいれつ) Sさぽーともーど(はば uint32, height uint32, しょくdepth uint32) bool {
	return はば == 320 && height == 200 && しょくdepth == 8
}
func (self *Tびでおぐらふぃっくはいれつ) Sありもーど(はば uint32, height uint32, しょくdepth uint32) bool {
	if !self.Sさぽーともーど(はば, height, しょくdepth) {
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

	self.Wかきこみれじすた(g320x200x256)

	return true
}
