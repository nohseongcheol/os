/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "порт"

type TВидеоГрафикаМассив struct {
}

var micsПорт uint16 = 0x3c2
var crtcМазмунПорт uint16 = 0x3d4
var crtcdataПорт uint16 = 0x3d5
var sequencerМазмунПорт uint16 = 0x3c4
var sequencerdataПорт uint16 = 0x3c5
var графикаcontrollerМазмунПорт uint16 = 0x3ce
var графикаcontrollerdataПорт uint16 = 0x3cf
var атрибутcontrollerМазмунПорт uint16 = 0x3c0
var атрибутcontrollerОкууПорт uint16 = 0x3c1
var атрибутcontrollerЖазууПорт uint16 = 0x3c0
var атрибутcontrollerТүшүрүүПорт uint16 = 0x3da

func (self *TВидеоГрафикаМассив) Жазууregister(register []byte) {
	var regМазмун uint16 = 0

	ПортЖазууbyte(micsПорт, register[regМазмун])
	regМазмун++

	var i uint8
	for i = 0; i < 5; i++ {
		ПортЖазууbyte(sequencerМазмунПорт, i)
		ПортЖазууbyte(sequencerdataПорт, register[regМазмун])
		regМазмун++
	}

	ПортЖазууbyte(crtcМазмунПорт, 0x03)

	ПортЖазууbyte(crtcdataПорт, (ПортОкууbyte(crtcdataПорт) | 0x80))
	ПортЖазууbyte(crtcМазмунПорт, 0x11)
	ПортЖазууbyte(crtcdataПорт, (ПортОкууbyte(crtcdataПорт) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ПортЖазууbyte(crtcМазмунПорт, i)
		ПортЖазууbyte(crtcdataПорт, register[regМазмун])
		regМазмун++
	}

	for i = 0; i < 9; i++ {
		ПортЖазууbyte(графикаcontrollerМазмунПорт, i)
		ПортЖазууbyte(графикаcontrollerdataПорт, register[regМазмун])
		regМазмун++
	}

	for i = 0; i < 21; i++ {
		ПортОкууbyte(атрибутcontrollerТүшүрүүПорт)
		ПортЖазууbyte(атрибутcontrollerМазмунПорт, i)
		ПортЖазууbyte(атрибутcontrollerЖазууПорт, register[regМазмун])
		regМазмун++
	}

	ПортОкууbyte(атрибутcontrollerТүшүрүүПорт)
	ПортЖазууbyte(атрибутcontrollerМазмунПорт, 0x20)

}

func (self *TВидеоГрафикаМассив) Getframebuffersegment() uintptr {
	ПортЖазууbyte(графикаcontrollerМазмунПорт, 0x06)
	var segmentНОМЕР uint8 = ((ПортОкууbyte(графикаcontrollerdataПорт) >> 2) & 0x03)
	switch segmentНОМЕР {
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
func (self *TВидеоГрафикаМассив) Putpixel(x uint32, y uint32, colorМазмун uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = colorМазмун

}
func (self *TВидеоГрафикаМассив) GetcolorМазмун(r uint8, g uint8, b uint8) uint8 {
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
func (self *TВидеоГрафикаМассив) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetcolorМазмун(r, g, b))
}
func (self *TВидеоГрафикаМассив) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TВидеоГрафикаМассив) SupportРежим(туурасы uint32, бийиктик uint32, colordepth uint32) bool {
	return туурасы == 320 && бийиктик == 200 && colordepth == 8
}
func (self *TВидеоГрафикаМассив) SetРежим(туурасы uint32, бийиктик uint32, colordepth uint32) bool {
	if !self.SupportРежим(туурасы, бийиктик, colordepth) {
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

	self.Жазууregister(g320x200x256)

	return true
}
