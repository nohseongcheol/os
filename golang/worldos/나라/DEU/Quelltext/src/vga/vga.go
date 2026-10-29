/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "anschluss"

type TVideoGrafikFeld struct {
}

var micsAnschluss uint16 = 0x3c2
var crtcInhaltAnschluss uint16 = 0x3d4
var crtcDatenAnschluss uint16 = 0x3d5
var sequencerInhaltAnschluss uint16 = 0x3c4
var sequencerDatenAnschluss uint16 = 0x3c5
var grafikSteuerungInhaltAnschluss uint16 = 0x3ce
var grafikSteuerungDatenAnschluss uint16 = 0x3cf
var attributSteuerungInhaltAnschluss uint16 = 0x3c0
var attributSteuerungLesenAnschluss uint16 = 0x3c1
var attributSteuerungSchreibenAnschluss uint16 = 0x3c0
var attributSteuerungZurücksetzenAnschluss uint16 = 0x3da

func (selbst *TVideoGrafikFeld) SchreibenRegister(register []byte) {
	var regInhalt uint16 = 0

	AnschlussSchreibenByte(micsAnschluss, register[regInhalt])
	regInhalt++

	var i uint8
	for i = 0; i < 5; i++ {
		AnschlussSchreibenByte(sequencerInhaltAnschluss, i)
		AnschlussSchreibenByte(sequencerDatenAnschluss, register[regInhalt])
		regInhalt++
	}

	AnschlussSchreibenByte(crtcInhaltAnschluss, 0x03)

	AnschlussSchreibenByte(crtcDatenAnschluss, (AnschlussLesenByte(crtcDatenAnschluss) | 0x80))
	AnschlussSchreibenByte(crtcInhaltAnschluss, 0x11)
	AnschlussSchreibenByte(crtcDatenAnschluss, (AnschlussLesenByte(crtcDatenAnschluss) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		AnschlussSchreibenByte(crtcInhaltAnschluss, i)
		AnschlussSchreibenByte(crtcDatenAnschluss, register[regInhalt])
		regInhalt++
	}

	for i = 0; i < 9; i++ {
		AnschlussSchreibenByte(grafikSteuerungInhaltAnschluss, i)
		AnschlussSchreibenByte(grafikSteuerungDatenAnschluss, register[regInhalt])
		regInhalt++
	}

	for i = 0; i < 21; i++ {
		AnschlussLesenByte(attributSteuerungZurücksetzenAnschluss)
		AnschlussSchreibenByte(attributSteuerungInhaltAnschluss, i)
		AnschlussSchreibenByte(attributSteuerungSchreibenAnschluss, register[regInhalt])
		regInhalt++
	}

	AnschlussLesenByte(attributSteuerungZurücksetzenAnschluss)
	AnschlussSchreibenByte(attributSteuerungInhaltAnschluss, 0x20)

}

func (selbst *TVideoGrafikFeld) GetRahmenbuffersegment() uintptr {
	AnschlussSchreibenByte(grafikSteuerungInhaltAnschluss, 0x06)
	var segmentNummer uint8 = ((AnschlussLesenByte(grafikSteuerungDatenAnschluss) >> 2) & 0x03)
	switch segmentNummer {
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
func (selbst *TVideoGrafikFeld) Putpixel(x uint32, y uint32, farbeInhalt uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = selbst.GetRahmenbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = farbeInhalt

}
func (selbst *TVideoGrafikFeld) GetFarbeInhalt(r uint8, g uint8, b uint8) uint8 {
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
func (selbst *TVideoGrafikFeld) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	selbst.Putpixel(x, y, selbst.GetFarbeInhalt(r, g, b))
}
func (selbst *TVideoGrafikFeld) FillRechteck(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			selbst.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (selbst *TVideoGrafikFeld) UnterstützungModus(breite uint32, höhe uint32, farbeTiefe uint32) bool {
	return breite == 320 && höhe == 200 && farbeTiefe == 8
}
func (selbst *TVideoGrafikFeld) SetzenModus(breite uint32, höhe uint32, farbeTiefe uint32) bool {
	if !selbst.UnterstützungModus(breite, höhe, farbeTiefe) {
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

	selbst.SchreibenRegister(g320x200x256)

	return true
}
