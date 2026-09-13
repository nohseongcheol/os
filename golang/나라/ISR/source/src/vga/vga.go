package vga

import . "unsafe"
import . "שער"

type Tוידאוגרפיקהמערך struct {
}

var micsשער uint16 = 0x3c2
var crtcמפתחשער uint16 = 0x3d4
var crtcdataשער uint16 = 0x3d5
var sequencerמפתחשער uint16 = 0x3c4
var sequencerdataשער uint16 = 0x3c5
var גרפיקהcontrollerמפתחשער uint16 = 0x3ce
var גרפיקהcontrollerdataשער uint16 = 0x3cf
var תכונהcontrollerמפתחשער uint16 = 0x3c0
var תכונהcontrollerקריאהשער uint16 = 0x3c1
var תכונהcontrollerכתיבהשער uint16 = 0x3c0
var תכונהcontrollerאפסשער uint16 = 0x3da

func (self *Tוידאוגרפיקהמערך) Wכתיבהregister(register []byte) {
	var regמפתח uint16 = 0

	Pשערכתיבהbyte(micsשער, register[regמפתח])
	regמפתח++

	var i uint8
	for i = 0; i < 5; i++ {
		Pשערכתיבהbyte(sequencerמפתחשער, i)
		Pשערכתיבהbyte(sequencerdataשער, register[regמפתח])
		regמפתח++
	}

	Pשערכתיבהbyte(crtcמפתחשער, 0x03)

	Pשערכתיבהbyte(crtcdataשער, (Pשערקריאהbyte(crtcdataשער) | 0x80))
	Pשערכתיבהbyte(crtcמפתחשער, 0x11)
	Pשערכתיבהbyte(crtcdataשער, (Pשערקריאהbyte(crtcdataשער) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pשערכתיבהbyte(crtcמפתחשער, i)
		Pשערכתיבהbyte(crtcdataשער, register[regמפתח])
		regמפתח++
	}

	for i = 0; i < 9; i++ {
		Pשערכתיבהbyte(גרפיקהcontrollerמפתחשער, i)
		Pשערכתיבהbyte(גרפיקהcontrollerdataשער, register[regמפתח])
		regמפתח++
	}

	for i = 0; i < 21; i++ {
		Pשערקריאהbyte(תכונהcontrollerאפסשער)
		Pשערכתיבהbyte(תכונהcontrollerמפתחשער, i)
		Pשערכתיבהbyte(תכונהcontrollerכתיבהשער, register[regמפתח])
		regמפתח++
	}

	Pשערקריאהbyte(תכונהcontrollerאפסשער)
	Pשערכתיבהbyte(תכונהcontrollerמפתחשער, 0x20)

}

func (self *Tוידאוגרפיקהמערך) Getframebuffersegment() uintptr {
	Pשערכתיבהbyte(גרפיקהcontrollerמפתחשער, 0x06)
	var segmentמספר uint8 = ((Pשערקריאהbyte(גרפיקהcontrollerdataשער) >> 2) & 0x03)
	switch segmentמספר {
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
func (self *Tוידאוגרפיקהמערך) Putpixel(x uint32, y uint32, צבעמפתח uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = צבעמפתח

}
func (self *Tוידאוגרפיקהמערך) Getצבעמפתח(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tוידאוגרפיקהמערך) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getצבעמפתח(r, g, b))
}
func (self *Tוידאוגרפיקהמערך) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tוידאוגרפיקהמערך) Sתמיכהמצב(width uint32, height uint32, צבעdepth uint32) bool {
	return width == 320 && height == 200 && צבעdepth == 8
}
func (self *Tוידאוגרפיקהמערך) Sקבעמצב(width uint32, height uint32, צבעdepth uint32) bool {
	if !self.Sתמיכהמצב(width, height, צבעdepth) {
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

	self.Wכתיבהregister(g320x200x256)

	return true
}
