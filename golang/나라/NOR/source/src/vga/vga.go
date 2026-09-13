package vga

import . "unsafe"
import . "port"

type TVideoGrafikkTabell struct {
}

var micsport uint16 = 0x3c2
var crtcIndeksport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerIndeksport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikkcontrollerIndeksport uint16 = 0x3ce
var grafikkcontrollerdataport uint16 = 0x3cf
var egenskapcontrollerIndeksport uint16 = 0x3c0
var egenskapcontrollerLesport uint16 = 0x3c1
var egenskapcontrollerSkrivport uint16 = 0x3c0
var egenskapcontrollerNullstillport uint16 = 0x3da

func (selv *TVideoGrafikkTabell) Skrivregister(register []byte) {
	var regIndeks uint16 = 0

	PortSkrivbyte(micsport, register[regIndeks])
	regIndeks++

	var i uint8
	for i = 0; i < 5; i++ {
		PortSkrivbyte(sequencerIndeksport, i)
		PortSkrivbyte(sequencerdataport, register[regIndeks])
		regIndeks++
	}

	PortSkrivbyte(crtcIndeksport, 0x03)

	PortSkrivbyte(crtcdataport, (PortLesbyte(crtcdataport) | 0x80))
	PortSkrivbyte(crtcIndeksport, 0x11)
	PortSkrivbyte(crtcdataport, (PortLesbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortSkrivbyte(crtcIndeksport, i)
		PortSkrivbyte(crtcdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 9; i++ {
		PortSkrivbyte(grafikkcontrollerIndeksport, i)
		PortSkrivbyte(grafikkcontrollerdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 21; i++ {
		PortLesbyte(egenskapcontrollerNullstillport)
		PortSkrivbyte(egenskapcontrollerIndeksport, i)
		PortSkrivbyte(egenskapcontrollerSkrivport, register[regIndeks])
		regIndeks++
	}

	PortLesbyte(egenskapcontrollerNullstillport)
	PortSkrivbyte(egenskapcontrollerIndeksport, 0x20)

}

func (selv *TVideoGrafikkTabell) GetRammebuffersegment() uintptr {
	PortSkrivbyte(grafikkcontrollerIndeksport, 0x06)
	var segmentTall uint8 = ((PortLesbyte(grafikkcontrollerdataport) >> 2) & 0x03)
	switch segmentTall {
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
func (selv *TVideoGrafikkTabell) Putpixel(x uint32, y uint32, fargeIndeks uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = selv.GetRammebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = fargeIndeks

}
func (selv *TVideoGrafikkTabell) GetFargeIndeks(r uint8, g uint8, b uint8) uint8 {
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
func (selv *TVideoGrafikkTabell) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	selv.Putpixel(x, y, selv.GetFargeIndeks(r, g, b))
}
func (selv *TVideoGrafikkTabell) FillRektangel(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			selv.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (selv *TVideoGrafikkTabell) Støttemodus(bredde uint32, høyde uint32, fargeDybde uint32) bool {
	return bredde == 320 && høyde == 200 && fargeDybde == 8
}
func (selv *TVideoGrafikkTabell) Settmodus(bredde uint32, høyde uint32, fargeDybde uint32) bool {
	if !selv.Støttemodus(bredde, høyde, fargeDybde) {
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

	selv.Skrivregister(g320x200x256)

	return true
}
