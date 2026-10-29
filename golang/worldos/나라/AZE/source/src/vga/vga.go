/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "qapı"

type TVideographicsarray struct {
}

var micsQapı uint16 = 0x3c2
var crtcindexQapı uint16 = 0x3d4
var crtcdataQapı uint16 = 0x3d5
var sequencerindexQapı uint16 = 0x3c4
var sequencerdataQapı uint16 = 0x3c5
var graphicscontrollerindexQapı uint16 = 0x3ce
var graphicscontrollerdataQapı uint16 = 0x3cf
var attributecontrollerindexQapı uint16 = 0x3c0
var attributecontrollerOxumaQapı uint16 = 0x3c1
var attributecontrollerYazmaQapı uint16 = 0x3c0
var attributecontrollerSıfırlaQapı uint16 = 0x3da

func (self *TVideographicsarray) Yazmaregister(register []byte) {
	var regindex uint16 = 0

	QapıYazmabyte(micsQapı, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		QapıYazmabyte(sequencerindexQapı, i)
		QapıYazmabyte(sequencerdataQapı, register[regindex])
		regindex++
	}

	QapıYazmabyte(crtcindexQapı, 0x03)

	QapıYazmabyte(crtcdataQapı, (QapıOxumabyte(crtcdataQapı) | 0x80))
	QapıYazmabyte(crtcindexQapı, 0x11)
	QapıYazmabyte(crtcdataQapı, (QapıOxumabyte(crtcdataQapı) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		QapıYazmabyte(crtcindexQapı, i)
		QapıYazmabyte(crtcdataQapı, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		QapıYazmabyte(graphicscontrollerindexQapı, i)
		QapıYazmabyte(graphicscontrollerdataQapı, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		QapıOxumabyte(attributecontrollerSıfırlaQapı)
		QapıYazmabyte(attributecontrollerindexQapı, i)
		QapıYazmabyte(attributecontrollerYazmaQapı, register[regindex])
		regindex++
	}

	QapıOxumabyte(attributecontrollerSıfırlaQapı)
	QapıYazmabyte(attributecontrollerindexQapı, 0x20)

}

func (self *TVideographicsarray) Getframebuffersegment() uintptr {
	QapıYazmabyte(graphicscontrollerindexQapı, 0x06)
	var segmentnumber uint8 = ((QapıOxumabyte(graphicscontrollerdataQapı) >> 2) & 0x03)
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
func (self *TVideographicsarray) Putpixel(x uint32, y uint32, colorindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = colorindex

}
func (self *TVideographicsarray) Getcolorindex(r uint8, g uint8, b uint8) uint8 {
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
	self.Putpixel(x, y, self.Getcolorindex(r, g, b))
}
func (self *TVideographicsarray) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TVideographicsarray) SupportMod(en uint32, height uint32, colordepth uint32) bool {
	return en == 320 && height == 200 && colordepth == 8
}
func (self *TVideographicsarray) SetMod(en uint32, height uint32, colordepth uint32) bool {
	if !self.SupportMod(en, height, colordepth) {
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

	self.Yazmaregister(g320x200x256)

	return true
}
