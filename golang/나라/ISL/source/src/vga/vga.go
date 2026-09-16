/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVideóMyndefniFylki struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var myndefnicontrollerindexport uint16 = 0x3ce
var myndefnicontrollerdataport uint16 = 0x3cf
var eigindicontrollerindexport uint16 = 0x3c0
var eigindicontrollerLesturport uint16 = 0x3c1
var eigindicontrollerSkriftport uint16 = 0x3c0
var eigindicontrollerFrumstillaport uint16 = 0x3da

func (sjálft *TVideóMyndefniFylki) Skriftregister(register []byte) {
	var regindex uint16 = 0

	PortSkriftbyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortSkriftbyte(sequencerindexport, i)
		PortSkriftbyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortSkriftbyte(crtcindexport, 0x03)

	PortSkriftbyte(crtcdataport, (PortLesturbyte(crtcdataport) | 0x80))
	PortSkriftbyte(crtcindexport, 0x11)
	PortSkriftbyte(crtcdataport, (PortLesturbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortSkriftbyte(crtcindexport, i)
		PortSkriftbyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortSkriftbyte(myndefnicontrollerindexport, i)
		PortSkriftbyte(myndefnicontrollerdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortLesturbyte(eigindicontrollerFrumstillaport)
		PortSkriftbyte(eigindicontrollerindexport, i)
		PortSkriftbyte(eigindicontrollerSkriftport, register[regindex])
		regindex++
	}

	PortLesturbyte(eigindicontrollerFrumstillaport)
	PortSkriftbyte(eigindicontrollerindexport, 0x20)

}

func (sjálft *TVideóMyndefniFylki) GetRammibuffersegment() uintptr {
	PortSkriftbyte(myndefnicontrollerindexport, 0x06)
	var segmentnumber uint8 = ((PortLesturbyte(myndefnicontrollerdataport) >> 2) & 0x03)
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
func (sjálft *TVideóMyndefniFylki) Putpixel(x uint32, y uint32, liturindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = sjálft.GetRammibuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = liturindex

}
func (sjálft *TVideóMyndefniFylki) GetLiturindex(r uint8, g uint8, b uint8) uint8 {
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
func (sjálft *TVideóMyndefniFylki) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	sjálft.Putpixel(x, y, sjálft.GetLiturindex(r, g, b))
}
func (sjálft *TVideóMyndefniFylki) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			sjálft.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (sjálft *TVideóMyndefniFylki) StuðningurHAMUR(breidd uint32, hæð uint32, liturdepth uint32) bool {
	return breidd == 320 && hæð == 200 && liturdepth == 8
}
func (sjálft *TVideóMyndefniFylki) SetjaHAMUR(breidd uint32, hæð uint32, liturdepth uint32) bool {
	if !sjálft.StuðningurHAMUR(breidd, hæð, liturdepth) {
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

	sjálft.Skriftregister(g320x200x256)

	return true
}
