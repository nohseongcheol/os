package vga

import . "unsafe"
import . "porta"

type TVideoGrafikëRreshtimi struct {
}

var micsPorta uint16 = 0x3c2
var crtcTreguesiPorta uint16 = 0x3d4
var crtcdataPorta uint16 = 0x3d5
var sequencerTreguesiPorta uint16 = 0x3c4
var sequencerdataPorta uint16 = 0x3c5
var grafikëcontrollerTreguesiPorta uint16 = 0x3ce
var grafikëcontrollerdataPorta uint16 = 0x3cf
var karakteristikacontrollerTreguesiPorta uint16 = 0x3c0
var karakteristikacontrollerLeximiPorta uint16 = 0x3c1
var karakteristikacontrollerShkrimiPorta uint16 = 0x3c0
var karakteristikacontrollerNgafillimiPorta uint16 = 0x3da

func (vetvetja *TVideoGrafikëRreshtimi) Shkrimiregister(register []byte) {
	var regTreguesi uint16 = 0

	PortaShkrimibyte(micsPorta, register[regTreguesi])
	regTreguesi++

	var i uint8
	for i = 0; i < 5; i++ {
		PortaShkrimibyte(sequencerTreguesiPorta, i)
		PortaShkrimibyte(sequencerdataPorta, register[regTreguesi])
		regTreguesi++
	}

	PortaShkrimibyte(crtcTreguesiPorta, 0x03)

	PortaShkrimibyte(crtcdataPorta, (PortaLeximibyte(crtcdataPorta) | 0x80))
	PortaShkrimibyte(crtcTreguesiPorta, 0x11)
	PortaShkrimibyte(crtcdataPorta, (PortaLeximibyte(crtcdataPorta) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortaShkrimibyte(crtcTreguesiPorta, i)
		PortaShkrimibyte(crtcdataPorta, register[regTreguesi])
		regTreguesi++
	}

	for i = 0; i < 9; i++ {
		PortaShkrimibyte(grafikëcontrollerTreguesiPorta, i)
		PortaShkrimibyte(grafikëcontrollerdataPorta, register[regTreguesi])
		regTreguesi++
	}

	for i = 0; i < 21; i++ {
		PortaLeximibyte(karakteristikacontrollerNgafillimiPorta)
		PortaShkrimibyte(karakteristikacontrollerTreguesiPorta, i)
		PortaShkrimibyte(karakteristikacontrollerShkrimiPorta, register[regTreguesi])
		regTreguesi++
	}

	PortaLeximibyte(karakteristikacontrollerNgafillimiPorta)
	PortaShkrimibyte(karakteristikacontrollerTreguesiPorta, 0x20)

}

func (vetvetja *TVideoGrafikëRreshtimi) GetKornizëbuffersegment() uintptr {
	PortaShkrimibyte(grafikëcontrollerTreguesiPorta, 0x06)
	var segmentnumber uint8 = ((PortaLeximibyte(grafikëcontrollerdataPorta) >> 2) & 0x03)
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
func (vetvetja *TVideoGrafikëRreshtimi) Putpixel(x uint32, y uint32, ngjyraTreguesi uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = vetvetja.GetKornizëbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = ngjyraTreguesi

}
func (vetvetja *TVideoGrafikëRreshtimi) GetNgjyraTreguesi(r uint8, g uint8, b uint8) uint8 {
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
func (vetvetja *TVideoGrafikëRreshtimi) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	vetvetja.Putpixel(x, y, vetvetja.GetNgjyraTreguesi(r, g, b))
}
func (vetvetja *TVideoGrafikëRreshtimi) FillDrejtkëndësh(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			vetvetja.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (vetvetja *TVideoGrafikëRreshtimi) Supportmënyrë(gjerësia uint32, lartësia uint32, ngjyradepth uint32) bool {
	return gjerësia == 320 && lartësia == 200 && ngjyradepth == 8
}
func (vetvetja *TVideoGrafikëRreshtimi) Caktonimënyrë(gjerësia uint32, lartësia uint32, ngjyradepth uint32) bool {
	if !vetvetja.Supportmënyrë(gjerësia, lartësia, ngjyradepth) {
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

	vetvetja.Shkrimiregister(g320x200x256)

	return true
}
