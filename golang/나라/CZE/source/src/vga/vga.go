/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TObrazGrafikaPole struct {
}

var micsport uint16 = 0x3c2
var crtcRejstříkport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerRejstříkport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikacontrollerRejstříkport uint16 = 0x3ce
var grafikacontrollerdataport uint16 = 0x3cf
var atributcontrollerRejstříkport uint16 = 0x3c0
var atributcontrollerČteníport uint16 = 0x3c1
var atributcontrollerZápisport uint16 = 0x3c0
var atributcontrollerInicializovatport uint16 = 0x3da

func (self *TObrazGrafikaPole) Zápisregister(register []byte) {
	var regRejstřík uint16 = 0

	PortZápisbyte(micsport, register[regRejstřík])
	regRejstřík++

	var i uint8
	for i = 0; i < 5; i++ {
		PortZápisbyte(sequencerRejstříkport, i)
		PortZápisbyte(sequencerdataport, register[regRejstřík])
		regRejstřík++
	}

	PortZápisbyte(crtcRejstříkport, 0x03)

	PortZápisbyte(crtcdataport, (PortČteníbyte(crtcdataport) | 0x80))
	PortZápisbyte(crtcRejstříkport, 0x11)
	PortZápisbyte(crtcdataport, (PortČteníbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortZápisbyte(crtcRejstříkport, i)
		PortZápisbyte(crtcdataport, register[regRejstřík])
		regRejstřík++
	}

	for i = 0; i < 9; i++ {
		PortZápisbyte(grafikacontrollerRejstříkport, i)
		PortZápisbyte(grafikacontrollerdataport, register[regRejstřík])
		regRejstřík++
	}

	for i = 0; i < 21; i++ {
		PortČteníbyte(atributcontrollerInicializovatport)
		PortZápisbyte(atributcontrollerRejstříkport, i)
		PortZápisbyte(atributcontrollerZápisport, register[regRejstřík])
		regRejstřík++
	}

	PortČteníbyte(atributcontrollerInicializovatport)
	PortZápisbyte(atributcontrollerRejstříkport, 0x20)

}

func (self *TObrazGrafikaPole) GetRámbuffersegment() uintptr {
	PortZápisbyte(grafikacontrollerRejstříkport, 0x06)
	var segmentČíslo uint8 = ((PortČteníbyte(grafikacontrollerdataport) >> 2) & 0x03)
	switch segmentČíslo {
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
func (self *TObrazGrafikaPole) Putpixel(x uint32, y uint32, barvaRejstřík uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelAdresa uintptr = self.GetRámbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelAdresa)) = barvaRejstřík

}
func (self *TObrazGrafikaPole) GetBarvaRejstřík(r uint8, g uint8, b uint8) uint8 {
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
func (self *TObrazGrafikaPole) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetBarvaRejstřík(r, g, b))
}
func (self *TObrazGrafikaPole) FillObdélníkový(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TObrazGrafikaPole) PodporaMÓD(šířka uint32, výška uint32, barvadepth uint32) bool {
	return šířka == 320 && výška == 200 && barvadepth == 8
}
func (self *TObrazGrafikaPole) NastavitMÓD(šířka uint32, výška uint32, barvadepth uint32) bool {
	if !self.PodporaMÓD(šířka, výška, barvadepth) {
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

	self.Zápisregister(g320x200x256)

	return true
}
