/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "irika"

type TVidéoSaryarray struct {
}

var micsIrika uint16 = 0x3c2
var crtcFizahantakilaIrika uint16 = 0x3d4
var crtcdataIrika uint16 = 0x3d5
var sequencerFizahantakilaIrika uint16 = 0x3c4
var sequencerdataIrika uint16 = 0x3c5
var sarycontrollerFizahantakilaIrika uint16 = 0x3ce
var sarycontrollerdataIrika uint16 = 0x3cf
var marikamanokanacontrollerFizahantakilaIrika uint16 = 0x3c0
var marikamanokanacontrollerMamakyIrika uint16 = 0x3c1
var marikamanokanacontrollerManoratraIrika uint16 = 0x3c0
var marikamanokanacontrollerAverenoIrika uint16 = 0x3da

func (nytena *TVidéoSaryarray) Manoratraregister(register []byte) {
	var regFizahantakila uint16 = 0

	IrikaManoratrabyte(micsIrika, register[regFizahantakila])
	regFizahantakila++

	var i uint8
	for i = 0; i < 5; i++ {
		IrikaManoratrabyte(sequencerFizahantakilaIrika, i)
		IrikaManoratrabyte(sequencerdataIrika, register[regFizahantakila])
		regFizahantakila++
	}

	IrikaManoratrabyte(crtcFizahantakilaIrika, 0x03)

	IrikaManoratrabyte(crtcdataIrika, (IrikaMamakybyte(crtcdataIrika) | 0x80))
	IrikaManoratrabyte(crtcFizahantakilaIrika, 0x11)
	IrikaManoratrabyte(crtcdataIrika, (IrikaMamakybyte(crtcdataIrika) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		IrikaManoratrabyte(crtcFizahantakilaIrika, i)
		IrikaManoratrabyte(crtcdataIrika, register[regFizahantakila])
		regFizahantakila++
	}

	for i = 0; i < 9; i++ {
		IrikaManoratrabyte(sarycontrollerFizahantakilaIrika, i)
		IrikaManoratrabyte(sarycontrollerdataIrika, register[regFizahantakila])
		regFizahantakila++
	}

	for i = 0; i < 21; i++ {
		IrikaMamakybyte(marikamanokanacontrollerAverenoIrika)
		IrikaManoratrabyte(marikamanokanacontrollerFizahantakilaIrika, i)
		IrikaManoratrabyte(marikamanokanacontrollerManoratraIrika, register[regFizahantakila])
		regFizahantakila++
	}

	IrikaMamakybyte(marikamanokanacontrollerAverenoIrika)
	IrikaManoratrabyte(marikamanokanacontrollerFizahantakilaIrika, 0x20)

}

func (nytena *TVidéoSaryarray) Getframebuffersegment() uintptr {
	IrikaManoratrabyte(sarycontrollerFizahantakilaIrika, 0x06)
	var segmentnumber uint8 = ((IrikaMamakybyte(sarycontrollerdataIrika) >> 2) & 0x03)
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
func (nytena *TVidéoSaryarray) Putpixel(x uint32, y uint32, colorFizahantakila uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = nytena.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = colorFizahantakila

}
func (nytena *TVidéoSaryarray) GetcolorFizahantakila(r uint8, g uint8, b uint8) uint8 {
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
func (nytena *TVidéoSaryarray) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	nytena.Putpixel(x, y, nytena.GetcolorFizahantakila(r, g, b))
}
func (nytena *TVidéoSaryarray) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			nytena.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (nytena *TVidéoSaryarray) SupportFomba(indra uint32, haavo uint32, colordepth uint32) bool {
	return indra == 320 && haavo == 200 && colordepth == 8
}
func (nytena *TVidéoSaryarray) SetFomba(indra uint32, haavo uint32, colordepth uint32) bool {
	if !nytena.SupportFomba(indra, haavo, colordepth) {
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

	nytena.Manoratraregister(g320x200x256)

	return true
}
