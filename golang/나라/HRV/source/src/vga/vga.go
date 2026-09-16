/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVideoGrafikaNiz struct {
}

var micsport uint16 = 0x3c2
var crtcKazaloport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerKazaloport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikacontrollerKazaloport uint16 = 0x3ce
var grafikacontrollerdataport uint16 = 0x3cf
var atributcontrollerKazaloport uint16 = 0x3c0
var atributcontrollerČitajport uint16 = 0x3c1
var atributcontrollerZapišiport uint16 = 0x3c0
var atributcontrollerVratiizvornoport uint16 = 0x3da

func (sam *TVideoGrafikaNiz) Zapiširegister(register []byte) {
	var regKazalo uint16 = 0

	PortZapišibyte(micsport, register[regKazalo])
	regKazalo++

	var i uint8
	for i = 0; i < 5; i++ {
		PortZapišibyte(sequencerKazaloport, i)
		PortZapišibyte(sequencerdataport, register[regKazalo])
		regKazalo++
	}

	PortZapišibyte(crtcKazaloport, 0x03)

	PortZapišibyte(crtcdataport, (PortČitajbyte(crtcdataport) | 0x80))
	PortZapišibyte(crtcKazaloport, 0x11)
	PortZapišibyte(crtcdataport, (PortČitajbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortZapišibyte(crtcKazaloport, i)
		PortZapišibyte(crtcdataport, register[regKazalo])
		regKazalo++
	}

	for i = 0; i < 9; i++ {
		PortZapišibyte(grafikacontrollerKazaloport, i)
		PortZapišibyte(grafikacontrollerdataport, register[regKazalo])
		regKazalo++
	}

	for i = 0; i < 21; i++ {
		PortČitajbyte(atributcontrollerVratiizvornoport)
		PortZapišibyte(atributcontrollerKazaloport, i)
		PortZapišibyte(atributcontrollerZapišiport, register[regKazalo])
		regKazalo++
	}

	PortČitajbyte(atributcontrollerVratiizvornoport)
	PortZapišibyte(atributcontrollerKazaloport, 0x20)

}

func (sam *TVideoGrafikaNiz) Getframebuffersegment() uintptr {
	PortZapišibyte(grafikacontrollerKazaloport, 0x06)
	var segmentBROJ uint8 = ((PortČitajbyte(grafikacontrollerdataport) >> 2) & 0x03)
	switch segmentBROJ {
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
func (sam *TVideoGrafikaNiz) Putpixel(x uint32, y uint32, bojaKazalo uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = sam.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = bojaKazalo

}
func (sam *TVideoGrafikaNiz) GetBojaKazalo(r uint8, g uint8, b uint8) uint8 {
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
func (sam *TVideoGrafikaNiz) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	sam.Putpixel(x, y, sam.GetBojaKazalo(r, g, b))
}
func (sam *TVideoGrafikaNiz) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			sam.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (sam *TVideoGrafikaNiz) PodrškaNAČIN(širina uint32, visina uint32, bojadepth uint32) bool {
	return širina == 320 && visina == 200 && bojadepth == 8
}
func (sam *TVideoGrafikaNiz) PostaviNAČIN(širina uint32, visina uint32, bojadepth uint32) bool {
	if !sam.PodrškaNAČIN(širina, visina, bojadepth) {
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

	sam.Zapiširegister(g320x200x256)

	return true
}
