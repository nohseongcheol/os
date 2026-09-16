/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "porta"

type TVideoGraficaSerie struct {
}

var micsPorta uint16 = 0x3c2
var crtcIndicePorta uint16 = 0x3d4
var crtcdataPorta uint16 = 0x3d5
var sequencerIndicePorta uint16 = 0x3c4
var sequencerdataPorta uint16 = 0x3c5
var graficacontrollerIndicePorta uint16 = 0x3ce
var graficacontrollerdataPorta uint16 = 0x3cf
var attributocontrollerIndicePorta uint16 = 0x3c0
var attributocontrollerLetturaPorta uint16 = 0x3c1
var attributocontrollerScritturaPorta uint16 = 0x3c0
var attributocontrollerRipristinaPorta uint16 = 0x3da

func (séstesso *TVideoGraficaSerie) Scritturaregister(register []byte) {
	var regIndice uint16 = 0

	PortaScritturabyte(micsPorta, register[regIndice])
	regIndice++

	var i uint8
	for i = 0; i < 5; i++ {
		PortaScritturabyte(sequencerIndicePorta, i)
		PortaScritturabyte(sequencerdataPorta, register[regIndice])
		regIndice++
	}

	PortaScritturabyte(crtcIndicePorta, 0x03)

	PortaScritturabyte(crtcdataPorta, (PortaLetturabyte(crtcdataPorta) | 0x80))
	PortaScritturabyte(crtcIndicePorta, 0x11)
	PortaScritturabyte(crtcdataPorta, (PortaLetturabyte(crtcdataPorta) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortaScritturabyte(crtcIndicePorta, i)
		PortaScritturabyte(crtcdataPorta, register[regIndice])
		regIndice++
	}

	for i = 0; i < 9; i++ {
		PortaScritturabyte(graficacontrollerIndicePorta, i)
		PortaScritturabyte(graficacontrollerdataPorta, register[regIndice])
		regIndice++
	}

	for i = 0; i < 21; i++ {
		PortaLetturabyte(attributocontrollerRipristinaPorta)
		PortaScritturabyte(attributocontrollerIndicePorta, i)
		PortaScritturabyte(attributocontrollerScritturaPorta, register[regIndice])
		regIndice++
	}

	PortaLetturabyte(attributocontrollerRipristinaPorta)
	PortaScritturabyte(attributocontrollerIndicePorta, 0x20)

}

func (séstesso *TVideoGraficaSerie) GetRiquadrobuffersegment() uintptr {
	PortaScritturabyte(graficacontrollerIndicePorta, 0x06)
	var segmentNumero uint8 = ((PortaLetturabyte(graficacontrollerdataPorta) >> 2) & 0x03)
	switch segmentNumero {
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
func (séstesso *TVideoGraficaSerie) Putpixel(x uint32, y uint32, coloreIndice uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = séstesso.GetRiquadrobuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = coloreIndice

}
func (séstesso *TVideoGraficaSerie) GetColoreIndice(r uint8, g uint8, b uint8) uint8 {
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
func (séstesso *TVideoGraficaSerie) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	séstesso.Putpixel(x, y, séstesso.GetColoreIndice(r, g, b))
}
func (séstesso *TVideoGraficaSerie) FillRettangolo(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			séstesso.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (séstesso *TVideoGraficaSerie) SupportoMODO(larghezza uint32, altezza uint32, coloredepth uint32) bool {
	return larghezza == 320 && altezza == 200 && coloredepth == 8
}
func (séstesso *TVideoGraficaSerie) ImpostaMODO(larghezza uint32, altezza uint32, coloredepth uint32) bool {
	if !séstesso.SupportoMODO(larghezza, altezza, coloredepth) {
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

	séstesso.Scritturaregister(g320x200x256)

	return true
}
