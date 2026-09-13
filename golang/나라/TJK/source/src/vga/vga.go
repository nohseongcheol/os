package vga

import . "unsafe"
import . "port"

type TVideographicsarray struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var graphicscontrollerindexport uint16 = 0x3ce
var graphicscontrollerdataport uint16 = 0x3cf
var attributecontrollerindexport uint16 = 0x3c0
var attributecontrollerХонданport uint16 = 0x3c1
var attributecontrollerНавиштанport uint16 = 0x3c0
var attributecontrollerБозсозӣport uint16 = 0x3da

func (self *TVideographicsarray) Навиштанregister(register []byte) {
	var regindex uint16 = 0

	PortНавиштанbyte(micsport, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortНавиштанbyte(sequencerindexport, i)
		PortНавиштанbyte(sequencerdataport, register[regindex])
		regindex++
	}

	PortНавиштанbyte(crtcindexport, 0x03)

	PortНавиштанbyte(crtcdataport, (PortХонданbyte(crtcdataport) | 0x80))
	PortНавиштанbyte(crtcindexport, 0x11)
	PortНавиштанbyte(crtcdataport, (PortХонданbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortНавиштанbyte(crtcindexport, i)
		PortНавиштанbyte(crtcdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		PortНавиштанbyte(graphicscontrollerindexport, i)
		PortНавиштанbyte(graphicscontrollerdataport, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		PortХонданbyte(attributecontrollerБозсозӣport)
		PortНавиштанbyte(attributecontrollerindexport, i)
		PortНавиштанbyte(attributecontrollerНавиштанport, register[regindex])
		regindex++
	}

	PortХонданbyte(attributecontrollerБозсозӣport)
	PortНавиштанbyte(attributecontrollerindexport, 0x20)

}

func (self *TVideographicsarray) Getframebuffersegment() uintptr {
	PortНавиштанbyte(graphicscontrollerindexport, 0x06)
	var segmentnumber uint8 = ((PortХонданbyte(graphicscontrollerdataport) >> 2) & 0x03)
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
func (self *TVideographicsarray) Putpixel(x uint32, y uint32, рангindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = рангindex

}
func (self *TVideographicsarray) GetРангindex(r uint8, g uint8, b uint8) uint8 {
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
func (self *TVideographicsarray) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetРангindex(r, g, b))
}
func (self *TVideographicsarray) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TVideographicsarray) Supportmode(width uint32, height uint32, рангdepth uint32) bool {
	return width == 320 && height == 200 && рангdepth == 8
}
func (self *TVideographicsarray) Setmode(width uint32, height uint32, рангdepth uint32) bool {
	if !self.Supportmode(width, height, рангdepth) {
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

	self.Навиштанregister(g320x200x256)

	return true
}
