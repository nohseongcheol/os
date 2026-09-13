package vga

import . "unsafe"
import . "port"

type TVideoGrafikVektor struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikStyrenhetindexport uint16 = 0x3ce
var grafikStyrenhetdataport uint16 = 0x3cf
var attributStyrenhetindexport uint16 = 0x3c0
var attributStyrenhetLäsport uint16 = 0x3c1
var attributStyrenhetSkrivport uint16 = 0x3c0
var attributStyrenhetÅterställport uint16 = 0x3da

func (själv *TVideoGrafikVektor) Skrivregister(register []byte) {
	var regindex uint16 = 0

	PortSkrivbyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortSkrivbyte(sequencerindexport, i)
		PortSkrivbyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortSkrivbyte(crtcindexport, 0x03)

	PortSkrivbyte(crtcdataport, (PortLäsbyte(crtcdataport) | 0x80))
	PortSkrivbyte(crtcindexport, 0x11)
	PortSkrivbyte(crtcdataport, (PortLäsbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortSkrivbyte(crtcindexport, i)
		PortSkrivbyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortSkrivbyte(grafikStyrenhetindexport, i)
		PortSkrivbyte(grafikStyrenhetdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortLäsbyte(attributStyrenhetÅterställport)
		PortSkrivbyte(attributStyrenhetindexport, i)
		PortSkrivbyte(attributStyrenhetSkrivport, register[regindex])
		regindex++
	}

	PortLäsbyte(attributStyrenhetÅterställport)
	PortSkrivbyte(attributStyrenhetindexport, 0x20)

}

func (själv *TVideoGrafikVektor) GetRambuffersegment() uintptr {
	PortSkrivbyte(grafikStyrenhetindexport, 0x06)
	var segmentNummer uint8 = ((PortLäsbyte(grafikStyrenhetdataport) >> 2) & 0x03)
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
func (själv *TVideoGrafikVektor) Putpixel(x uint32, y uint32, färgindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelAdress uintptr = själv.GetRambuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelAdress)) = färgindex

}
func (själv *TVideoGrafikVektor) GetFärgindex(r uint8, g uint8, b uint8) uint8 {
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
func (själv *TVideoGrafikVektor) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	själv.Putpixel(x, y, själv.GetFärgindex(r, g, b))
}
func (själv *TVideoGrafikVektor) FillRektangel(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			själv.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (själv *TVideoGrafikVektor) SupportLÄGE(bredd uint32, höjd uint32, färgDjupt uint32) bool {
	return bredd == 320 && höjd == 200 && färgDjupt == 8
}
func (själv *TVideoGrafikVektor) MängdLÄGE(bredd uint32, höjd uint32, färgDjupt uint32) bool {
	if !själv.SupportLÄGE(bredd, höjd, färgDjupt) {
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

	själv.Skrivregister(g320x200x256)

	return true
}
