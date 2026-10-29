/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVídeoGràficsMatriu struct {
}

var micsport uint16 = 0x3c2
var crtcÍndexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerÍndexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var gràficsControladorÍndexport uint16 = 0x3ce
var gràficsControladordataport uint16 = 0x3cf
var atributControladorÍndexport uint16 = 0x3c0
var atributControladorLecturaport uint16 = 0x3c1
var atributControladorEscripturaport uint16 = 0x3c0
var atributControladorRestableixport uint16 = 0x3da

func (unmateix *TVídeoGràficsMatriu) Escripturaregister(register []byte) {
	var regÍndex uint16 = 0

	PortEscripturabyte(micsport, register[regÍndex])
	regÍndex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortEscripturabyte(sequencerÍndexport, i)
		PortEscripturabyte(sequencerdataport, register[regÍndex])
		regÍndex++
	}

	PortEscripturabyte(crtcÍndexport, 0x03)

	PortEscripturabyte(crtcdataport, (PortLecturabyte(crtcdataport) | 0x80))
	PortEscripturabyte(crtcÍndexport, 0x11)
	PortEscripturabyte(crtcdataport, (PortLecturabyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortEscripturabyte(crtcÍndexport, i)
		PortEscripturabyte(crtcdataport, register[regÍndex])
		regÍndex++
	}

	for i = 0; i < 9; i++ {
		PortEscripturabyte(gràficsControladorÍndexport, i)
		PortEscripturabyte(gràficsControladordataport, register[regÍndex])
		regÍndex++
	}

	for i = 0; i < 21; i++ {
		PortLecturabyte(atributControladorRestableixport)
		PortEscripturabyte(atributControladorÍndexport, i)
		PortEscripturabyte(atributControladorEscripturaport, register[regÍndex])
		regÍndex++
	}

	PortLecturabyte(atributControladorRestableixport)
	PortEscripturabyte(atributControladorÍndexport, 0x20)

}

func (unmateix *TVídeoGràficsMatriu) GetMarcbuffersegment() uintptr {
	PortEscripturabyte(gràficsControladorÍndexport, 0x06)
	var segmentNombre uint8 = ((PortLecturabyte(gràficsControladordataport) >> 2) & 0x03)
	switch segmentNombre {
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
func (unmateix *TVídeoGràficsMatriu) Putpixel(x uint32, y uint32, colorÍndex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelAdreça uintptr = unmateix.GetMarcbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelAdreça)) = colorÍndex

}
func (unmateix *TVídeoGràficsMatriu) GetcolorÍndex(r uint8, g uint8, b uint8) uint8 {
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
func (unmateix *TVídeoGràficsMatriu) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	unmateix.Putpixel(x, y, unmateix.GetcolorÍndex(r, g, b))
}
func (unmateix *TVídeoGràficsMatriu) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			unmateix.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (unmateix *TVídeoGràficsMatriu) Suportmode(amplada uint32, alçada uint32, colordepth uint32) bool {
	return amplada == 320 && alçada == 200 && colordepth == 8
}
func (unmateix *TVídeoGràficsMatriu) Estableixmode(amplada uint32, alçada uint32, colordepth uint32) bool {
	if !unmateix.Suportmode(amplada, alçada, colordepth) {
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

	unmateix.Escripturaregister(g320x200x256)

	return true
}
