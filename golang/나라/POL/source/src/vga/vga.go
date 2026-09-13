package vga

import . "unsafe"
import . "port"

type TWideoGrafikaTablica struct {
}

var micsport uint16 = 0x3c2
var crtcIndeksport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerIndeksport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikaKontrolerIndeksport uint16 = 0x3ce
var grafikaKontrolerdataport uint16 = 0x3cf
var atrybutKontrolerIndeksport uint16 = 0x3c0
var atrybutKontrolerOdczytport uint16 = 0x3c1
var atrybutKontrolerZapisport uint16 = 0x3c0
var atrybutKontrolerWyzerujport uint16 = 0x3da

func (bieżący *TWideoGrafikaTablica) Zapisregister(register []byte) {
	var regIndeks uint16 = 0

	PortZapisbyte(micsport, register[regIndeks])
	regIndeks++

	var i uint8
	for i = 0; i < 5; i++ {
		PortZapisbyte(sequencerIndeksport, i)
		PortZapisbyte(sequencerdataport, register[regIndeks])
		regIndeks++
	}

	PortZapisbyte(crtcIndeksport, 0x03)

	PortZapisbyte(crtcdataport, (PortOdczytbyte(crtcdataport) | 0x80))
	PortZapisbyte(crtcIndeksport, 0x11)
	PortZapisbyte(crtcdataport, (PortOdczytbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortZapisbyte(crtcIndeksport, i)
		PortZapisbyte(crtcdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 9; i++ {
		PortZapisbyte(grafikaKontrolerIndeksport, i)
		PortZapisbyte(grafikaKontrolerdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 21; i++ {
		PortOdczytbyte(atrybutKontrolerWyzerujport)
		PortZapisbyte(atrybutKontrolerIndeksport, i)
		PortZapisbyte(atrybutKontrolerZapisport, register[regIndeks])
		regIndeks++
	}

	PortOdczytbyte(atrybutKontrolerWyzerujport)
	PortZapisbyte(atrybutKontrolerIndeksport, 0x20)

}

func (bieżący *TWideoGrafikaTablica) GetRamkabuffersegment() uintptr {
	PortZapisbyte(grafikaKontrolerIndeksport, 0x06)
	var segmentLiczba uint8 = ((PortOdczytbyte(grafikaKontrolerdataport) >> 2) & 0x03)
	switch segmentLiczba {
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
func (bieżący *TWideoGrafikaTablica) Putpixel(x uint32, y uint32, kolorIndeks uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelAdres uintptr = bieżący.GetRamkabuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelAdres)) = kolorIndeks

}
func (bieżący *TWideoGrafikaTablica) GetKolorIndeks(r uint8, g uint8, b uint8) uint8 {
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
func (bieżący *TWideoGrafikaTablica) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	bieżący.Putpixel(x, y, bieżący.GetKolorIndeks(r, g, b))
}
func (bieżący *TWideoGrafikaTablica) FillProstokąt(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			bieżący.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (bieżący *TWideoGrafikaTablica) ObsługaTRYB(szerokość uint32, wysokość uint32, kolordepth uint32) bool {
	return szerokość == 320 && wysokość == 200 && kolordepth == 8
}
func (bieżący *TWideoGrafikaTablica) ZbiórTRYB(szerokość uint32, wysokość uint32, kolordepth uint32) bool {
	if !bieżący.ObsługaTRYB(szerokość, wysokość, kolordepth) {
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

	bieżący.Zapisregister(g320x200x256)

	return true
}
