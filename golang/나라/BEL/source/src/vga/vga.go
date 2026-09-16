/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "poort"

type TVideoGrafischReeks struct {
}

var micsPoort uint16 = 0x3c2
var crtcindexPoort uint16 = 0x3d4
var crtcdataPoort uint16 = 0x3d5
var sequencerindexPoort uint16 = 0x3c4
var sequencerdataPoort uint16 = 0x3c5
var grafischcontrollerindexPoort uint16 = 0x3ce
var grafischcontrollerdataPoort uint16 = 0x3cf
var attribuutcontrollerindexPoort uint16 = 0x3c0
var attribuutcontrollerLezenPoort uint16 = 0x3c1
var attribuutcontrollerSchrijvenPoort uint16 = 0x3c0
var attribuutcontrollerTerugzettenPoort uint16 = 0x3da

func (zelf *TVideoGrafischReeks) Schrijvenregister(register []byte) {
	var regindex uint16 = 0

	PoortSchrijvenbyte(micsPoort, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PoortSchrijvenbyte(sequencerindexPoort, i)
		PoortSchrijvenbyte(sequencerdataPoort, register[regindex])
		regindex++
	}

	PoortSchrijvenbyte(crtcindexPoort, 0x03)

	PoortSchrijvenbyte(crtcdataPoort, (PoortLezenbyte(crtcdataPoort) | 0x80))
	PoortSchrijvenbyte(crtcindexPoort, 0x11)
	PoortSchrijvenbyte(crtcdataPoort, (PoortLezenbyte(crtcdataPoort) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PoortSchrijvenbyte(crtcindexPoort, i)
		PoortSchrijvenbyte(crtcdataPoort, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PoortSchrijvenbyte(grafischcontrollerindexPoort, i)
		PoortSchrijvenbyte(grafischcontrollerdataPoort, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PoortLezenbyte(attribuutcontrollerTerugzettenPoort)
		PoortSchrijvenbyte(attribuutcontrollerindexPoort, i)
		PoortSchrijvenbyte(attribuutcontrollerSchrijvenPoort, register[regindex])
		regindex++
	}

	PoortLezenbyte(attribuutcontrollerTerugzettenPoort)
	PoortSchrijvenbyte(attribuutcontrollerindexPoort, 0x20)

}

func (zelf *TVideoGrafischReeks) Getframebuffersegment() uintptr {
	PoortSchrijvenbyte(grafischcontrollerindexPoort, 0x06)
	var segmentGetal uint8 = ((PoortLezenbyte(grafischcontrollerdataPoort) >> 2) & 0x03)
	switch segmentGetal {
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
func (zelf *TVideoGrafischReeks) Putpixel(x uint32, y uint32, kleurindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = zelf.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = kleurindex

}
func (zelf *TVideoGrafischReeks) GetKleurindex(r uint8, g uint8, b uint8) uint8 {
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
func (zelf *TVideoGrafischReeks) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	zelf.Putpixel(x, y, zelf.GetKleurindex(r, g, b))
}
func (zelf *TVideoGrafischReeks) FillRechthoek(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			zelf.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (zelf *TVideoGrafischReeks) Ondersteuningmodus(breedte uint32, hoogte uint32, kleurDiepte uint32) bool {
	return breedte == 320 && hoogte == 200 && kleurDiepte == 8
}
func (zelf *TVideoGrafischReeks) Instellenmodus(breedte uint32, hoogte uint32, kleurDiepte uint32) bool {
	if !zelf.Ondersteuningmodus(breedte, hoogte, kleurDiepte) {
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

	zelf.Schrijvenregister(g320x200x256)

	return true
}
