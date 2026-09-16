/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "پورٹ"

type Tویڈیوترسیمیاتلڑی struct {
}

var micsپورٹ uint16 = 0x3c2
var crtcindexپورٹ uint16 = 0x3d4
var crtcdataپورٹ uint16 = 0x3d5
var sequencerindexپورٹ uint16 = 0x3c4
var sequencerdataپورٹ uint16 = 0x3c5
var ترسیمیاتcontrollerindexپورٹ uint16 = 0x3ce
var ترسیمیاتcontrollerdataپورٹ uint16 = 0x3cf
var وصفcontrollerindexپورٹ uint16 = 0x3c0
var وصفcontrollerپڑھیںپورٹ uint16 = 0x3c1
var وصفcontrollerلکھیںپورٹ uint16 = 0x3c0
var وصفcontrollerازسرنوتعینکریںپورٹ uint16 = 0x3da

func (self *Tویڈیوترسیمیاتلڑی) Wلکھیںregister(register []byte) {
	var regindex uint16 = 0

	Pپورٹلکھیںbyte(micsپورٹ, register[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		Pپورٹلکھیںbyte(sequencerindexپورٹ, i)
		Pپورٹلکھیںbyte(sequencerdataپورٹ, register[regindex])
		regindex++
	}

	Pپورٹلکھیںbyte(crtcindexپورٹ, 0x03)

	Pپورٹلکھیںbyte(crtcdataپورٹ, (Pپورٹپڑھیںbyte(crtcdataپورٹ) | 0x80))
	Pپورٹلکھیںbyte(crtcindexپورٹ, 0x11)
	Pپورٹلکھیںbyte(crtcdataپورٹ, (Pپورٹپڑھیںbyte(crtcdataپورٹ) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pپورٹلکھیںbyte(crtcindexپورٹ, i)
		Pپورٹلکھیںbyte(crtcdataپورٹ, register[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		Pپورٹلکھیںbyte(ترسیمیاتcontrollerindexپورٹ, i)
		Pپورٹلکھیںbyte(ترسیمیاتcontrollerdataپورٹ, register[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		Pپورٹپڑھیںbyte(وصفcontrollerازسرنوتعینکریںپورٹ)
		Pپورٹلکھیںbyte(وصفcontrollerindexپورٹ, i)
		Pپورٹلکھیںbyte(وصفcontrollerلکھیںپورٹ, register[regindex])
		regindex++
	}

	Pپورٹپڑھیںbyte(وصفcontrollerازسرنوتعینکریںپورٹ)
	Pپورٹلکھیںbyte(وصفcontrollerindexپورٹ, 0x20)

}

func (self *Tویڈیوترسیمیاتلڑی) Getframebuffersegment() uintptr {
	Pپورٹلکھیںbyte(ترسیمیاتcontrollerindexپورٹ, 0x06)
	var segmentnumber uint8 = ((Pپورٹپڑھیںbyte(ترسیمیاتcontrollerdataپورٹ) >> 2) & 0x03)
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
func (self *Tویڈیوترسیمیاتلڑی) Putpixel(x uint32, y uint32, رنگindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = رنگindex

}
func (self *Tویڈیوترسیمیاتلڑی) Getرنگindex(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tویڈیوترسیمیاتلڑی) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getرنگindex(r, g, b))
}
func (self *Tویڈیوترسیمیاتلڑی) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tویڈیوترسیمیاتلڑی) Sمعاونتmode(چوڑائی uint32, اونچائی uint32, رنگdepth uint32) bool {
	return چوڑائی == 320 && اونچائی == 200 && رنگdepth == 8
}
func (self *Tویڈیوترسیمیاتلڑی) Sسیٹmode(چوڑائی uint32, اونچائی uint32, رنگdepth uint32) bool {
	if !self.Sمعاونتmode(چوڑائی, اونچائی, رنگdepth) {
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

	self.Wلکھیںregister(g320x200x256)

	return true
}
