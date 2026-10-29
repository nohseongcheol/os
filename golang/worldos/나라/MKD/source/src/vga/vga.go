/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "порта"

type TВидеоГрафикаПострои struct {
}

var micsПорта uint16 = 0x3c2
var crtcИндексПорта uint16 = 0x3d4
var crtcdataПорта uint16 = 0x3d5
var sequencerИндексПорта uint16 = 0x3c4
var sequencerdataПорта uint16 = 0x3c5
var графикаcontrollerИндексПорта uint16 = 0x3ce
var графикаcontrollerdataПорта uint16 = 0x3cf
var атрибутcontrollerИндексПорта uint16 = 0x3c0
var атрибутcontrollerЧитајПорта uint16 = 0x3c1
var атрибутcontrollerЗапишиПорта uint16 = 0x3c0
var атрибутcontrollerРесетирајПорта uint16 = 0x3da

func (само *TВидеоГрафикаПострои) Запишиregister(register []byte) {
	var regИндекс uint16 = 0

	ПортаЗапишиbyte(micsПорта, register[regИндекс])
	regИндекс++

	var i uint8
	for i = 0; i < 5; i++ {
		ПортаЗапишиbyte(sequencerИндексПорта, i)
		ПортаЗапишиbyte(sequencerdataПорта, register[regИндекс])
		regИндекс++
	}

	ПортаЗапишиbyte(crtcИндексПорта, 0x03)

	ПортаЗапишиbyte(crtcdataПорта, (ПортаЧитајbyte(crtcdataПорта) | 0x80))
	ПортаЗапишиbyte(crtcИндексПорта, 0x11)
	ПортаЗапишиbyte(crtcdataПорта, (ПортаЧитајbyte(crtcdataПорта) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ПортаЗапишиbyte(crtcИндексПорта, i)
		ПортаЗапишиbyte(crtcdataПорта, register[regИндекс])
		regИндекс++
	}

	for i = 0; i < 9; i++ {
		ПортаЗапишиbyte(графикаcontrollerИндексПорта, i)
		ПортаЗапишиbyte(графикаcontrollerdataПорта, register[regИндекс])
		regИндекс++
	}

	for i = 0; i < 21; i++ {
		ПортаЧитајbyte(атрибутcontrollerРесетирајПорта)
		ПортаЗапишиbyte(атрибутcontrollerИндексПорта, i)
		ПортаЗапишиbyte(атрибутcontrollerЗапишиПорта, register[regИндекс])
		regИндекс++
	}

	ПортаЧитајbyte(атрибутcontrollerРесетирајПорта)
	ПортаЗапишиbyte(атрибутcontrollerИндексПорта, 0x20)

}

func (само *TВидеоГрафикаПострои) GetРамкаbuffersegment() uintptr {
	ПортаЗапишиbyte(графикаcontrollerИндексПорта, 0x06)
	var segmentnumber uint8 = ((ПортаЧитајbyte(графикаcontrollerdataПорта) >> 2) & 0x03)
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
func (само *TВидеоГрафикаПострои) Putpixel(x uint32, y uint32, бојаИндекс uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = само.GetРамкаbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = бојаИндекс

}
func (само *TВидеоГрафикаПострои) GetБојаИндекс(r uint8, g uint8, b uint8) uint8 {
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
func (само *TВидеоГрафикаПострои) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	само.Putpixel(x, y, само.GetБојаИндекс(r, g, b))
}
func (само *TВидеоГрафикаПострои) FillПравоаголник(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			само.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (само *TВидеоГрафикаПострои) SupportРежим(ширина uint32, висина uint32, бојаdepth uint32) bool {
	return ширина == 320 && висина == 200 && бојаdepth == 8
}
func (само *TВидеоГрафикаПострои) ПоставиРежим(ширина uint32, висина uint32, бојаdepth uint32) bool {
	if !само.SupportРежим(ширина, висина, бојаdepth) {
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

	само.Запишиregister(g320x200x256)

	return true
}
