/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVideoGraficăVector struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var graficăcontrollerindexport uint16 = 0x3ce
var graficăcontrollerdataport uint16 = 0x3cf
var atributcontrollerindexport uint16 = 0x3c0
var atributcontrollerCitireport uint16 = 0x3c1
var atributcontrollerScriereport uint16 = 0x3c0
var atributcontrollerRestabileșteport uint16 = 0x3da

func (sine *TVideoGraficăVector) Scriereregister(register []byte) {
	var regindex uint16 = 0

	PortScrierebyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortScrierebyte(sequencerindexport, i)
		PortScrierebyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortScrierebyte(crtcindexport, 0x03)

	PortScrierebyte(crtcdataport, (PortCitirebyte(crtcdataport) | 0x80))
	PortScrierebyte(crtcindexport, 0x11)
	PortScrierebyte(crtcdataport, (PortCitirebyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortScrierebyte(crtcindexport, i)
		PortScrierebyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortScrierebyte(graficăcontrollerindexport, i)
		PortScrierebyte(graficăcontrollerdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortCitirebyte(atributcontrollerRestabileșteport)
		PortScrierebyte(atributcontrollerindexport, i)
		PortScrierebyte(atributcontrollerScriereport, register[regindex])
		regindex++
	}

	PortCitirebyte(atributcontrollerRestabileșteport)
	PortScrierebyte(atributcontrollerindexport, 0x20)

}

func (sine *TVideoGraficăVector) GetCadrubuffersegment() uintptr {
	PortScrierebyte(graficăcontrollerindexport, 0x06)
	var segmentNumăr uint8 = ((PortCitirebyte(graficăcontrollerdataport) >> 2) & 0x03)
	switch segmentNumăr {
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
func (sine *TVideoGraficăVector) Putpixel(x uint32, y uint32, culoareindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = sine.GetCadrubuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = culoareindex

}
func (sine *TVideoGraficăVector) GetCuloareindex(r uint8, g uint8, b uint8) uint8 {
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
func (sine *TVideoGraficăVector) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	sine.Putpixel(x, y, sine.GetCuloareindex(r, g, b))
}
func (sine *TVideoGraficăVector) FillDreptunghi(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			sine.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (sine *TVideoGraficăVector) SuportMOD(lățime uint32, înălțime uint32, culoaredepth uint32) bool {
	return lățime == 320 && înălțime == 200 && culoaredepth == 8
}
func (sine *TVideoGraficăVector) DefinitMOD(lățime uint32, înălțime uint32, culoaredepth uint32) bool {
	if !sine.SuportMOD(lățime, înălțime, culoaredepth) {
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

	sine.Scriereregister(g320x200x256)

	return true
}
