package vga

import . "unsafe"
import . "port"

type TVideoGrafikaPole struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikaRadičindexport uint16 = 0x3ce
var grafikaRadičdataport uint16 = 0x3cf
var vlastnosťRadičindexport uint16 = 0x3c0
var vlastnosťRadičČítanieport uint16 = 0x3c1
var vlastnosťRadičZápisport uint16 = 0x3c0
var vlastnosťRadičReštartovaťport uint16 = 0x3da

func (vlastný *TVideoGrafikaPole) Zápisregister(register []byte) {
	var regindex uint16 = 0

	PortZápisbyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortZápisbyte(sequencerindexport, i)
		PortZápisbyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortZápisbyte(crtcindexport, 0x03)

	PortZápisbyte(crtcdataport, (PortČítaniebyte(crtcdataport) | 0x80))
	PortZápisbyte(crtcindexport, 0x11)
	PortZápisbyte(crtcdataport, (PortČítaniebyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortZápisbyte(crtcindexport, i)
		PortZápisbyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortZápisbyte(grafikaRadičindexport, i)
		PortZápisbyte(grafikaRadičdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortČítaniebyte(vlastnosťRadičReštartovaťport)
		PortZápisbyte(vlastnosťRadičindexport, i)
		PortZápisbyte(vlastnosťRadičZápisport, register[regindex])
		regindex++
	}

	PortČítaniebyte(vlastnosťRadičReštartovaťport)
	PortZápisbyte(vlastnosťRadičindexport, 0x20)

}

func (vlastný *TVideoGrafikaPole) GetRámecbuffersegment() uintptr {
	PortZápisbyte(grafikaRadičindexport, 0x06)
	var segmentČíslo uint8 = ((PortČítaniebyte(grafikaRadičdataport) >> 2) & 0x03)
	switch segmentČíslo {
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
func (vlastný *TVideoGrafikaPole) Putpixel(x uint32, y uint32, farbaindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = vlastný.GetRámecbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = farbaindex

}
func (vlastný *TVideoGrafikaPole) GetFarbaindex(r uint8, g uint8, b uint8) uint8 {
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
func (vlastný *TVideoGrafikaPole) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	vlastný.Putpixel(x, y, vlastný.GetFarbaindex(r, g, b))
}
func (vlastný *TVideoGrafikaPole) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			vlastný.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (vlastný *TVideoGrafikaPole) Podporarežim(šírka uint32, výška uint32, farbadepth uint32) bool {
	return šírka == 320 && výška == 200 && farbadepth == 8
}
func (vlastný *TVideoGrafikaPole) Sadarežim(šírka uint32, výška uint32, farbadepth uint32) bool {
	if !vlastný.Podporarežim(šírka, výška, farbadepth) {
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

	vlastný.Zápisregister(g320x200x256)

	return true
}
