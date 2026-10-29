/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TMozgóképGrafikaTömb struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikaVezérlőindexport uint16 = 0x3ce
var grafikaVezérlődataport uint16 = 0x3cf
var attribútumVezérlőindexport uint16 = 0x3c0
var attribútumVezérlőOlvasásport uint16 = 0x3c1
var attribútumVezérlőÍrásport uint16 = 0x3c0
var attribútumVezérlőVisszaállításport uint16 = 0x3da

func (self *TMozgóképGrafikaTömb) Írásregister(register []byte) {
	var regindex uint16 = 0

	PortÍrásbyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortÍrásbyte(sequencerindexport, i)
		PortÍrásbyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortÍrásbyte(crtcindexport, 0x03)

	PortÍrásbyte(crtcdataport, (PortOlvasásbyte(crtcdataport) | 0x80))
	PortÍrásbyte(crtcindexport, 0x11)
	PortÍrásbyte(crtcdataport, (PortOlvasásbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortÍrásbyte(crtcindexport, i)
		PortÍrásbyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortÍrásbyte(grafikaVezérlőindexport, i)
		PortÍrásbyte(grafikaVezérlődataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortOlvasásbyte(attribútumVezérlőVisszaállításport)
		PortÍrásbyte(attribútumVezérlőindexport, i)
		PortÍrásbyte(attribútumVezérlőÍrásport, register[regindex])
		regindex++
	}

	PortOlvasásbyte(attribútumVezérlőVisszaállításport)
	PortÍrásbyte(attribútumVezérlőindexport, 0x20)

}

func (self *TMozgóképGrafikaTömb) GetKeretbuffersegment() uintptr {
	PortÍrásbyte(grafikaVezérlőindexport, 0x06)
	var segmentSzám uint8 = ((PortOlvasásbyte(grafikaVezérlődataport) >> 2) & 0x03)
	switch segmentSzám {
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
func (self *TMozgóképGrafikaTömb) Putpixel(x uint32, y uint32, színindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.GetKeretbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = színindex

}
func (self *TMozgóképGrafikaTömb) GetSzínindex(r uint8, g uint8, b uint8) uint8 {
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
func (self *TMozgóképGrafikaTömb) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetSzínindex(r, g, b))
}
func (self *TMozgóképGrafikaTömb) FillNégyzet(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TMozgóképGrafikaTömb) Támogatásmód(szélesség uint32, magasság uint32, színMélység uint32) bool {
	return szélesség == 320 && magasság == 200 && színMélység == 8
}
func (self *TMozgóképGrafikaTömb) Halmazmód(szélesség uint32, magasság uint32, színMélység uint32) bool {
	if !self.Támogatásmód(szélesség, magasság, színMélység) {
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

	self.Írásregister(g320x200x256)

	return true
}
