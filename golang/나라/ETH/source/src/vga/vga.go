/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type Tቪዲዮንድፎችማዘጋጃ struct {
}

var micsport uint16 = 0x3c2
var crtcማውጫport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerማውጫport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var ንድፎችcontrollerማውጫport uint16 = 0x3ce
var ንድፎችcontrollerdataport uint16 = 0x3cf
var መለያcontrollerማውጫport uint16 = 0x3c0
var መለያcontrollerማንበቢያport uint16 = 0x3c1
var መለያcontrollerመጻፊያport uint16 = 0x3c0
var መለያcontrollerእንደነበረመመለሻport uint16 = 0x3da

func (self *Tቪዲዮንድፎችማዘጋጃ) Wመጻፊያregister(register []byte) {
	var regማውጫ uint16 = 0

	Portመጻፊያbyte(micsport, register[regማውጫ])
	regማውጫ++

	var i uint8
	for i = 0; i < 5; i++ {
		Portመጻፊያbyte(sequencerማውጫport, i)
		Portመጻፊያbyte(sequencerdataport, register[regማውጫ])
		regማውጫ++
	}

	Portመጻፊያbyte(crtcማውጫport, 0x03)

	Portመጻፊያbyte(crtcdataport, (Portማንበቢያbyte(crtcdataport) | 0x80))
	Portመጻፊያbyte(crtcማውጫport, 0x11)
	Portመጻፊያbyte(crtcdataport, (Portማንበቢያbyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Portመጻፊያbyte(crtcማውጫport, i)
		Portመጻፊያbyte(crtcdataport, register[regማውጫ])
		regማውጫ++
	}

	for i = 0; i < 9; i++ {
		Portመጻፊያbyte(ንድፎችcontrollerማውጫport, i)
		Portመጻፊያbyte(ንድፎችcontrollerdataport, register[regማውጫ])
		regማውጫ++
	}

	for i = 0; i < 21; i++ {
		Portማንበቢያbyte(መለያcontrollerእንደነበረመመለሻport)
		Portመጻፊያbyte(መለያcontrollerማውጫport, i)
		Portመጻፊያbyte(መለያcontrollerመጻፊያport, register[regማውጫ])
		regማውጫ++
	}

	Portማንበቢያbyte(መለያcontrollerእንደነበረመመለሻport)
	Portመጻፊያbyte(መለያcontrollerማውጫport, 0x20)

}

func (self *Tቪዲዮንድፎችማዘጋጃ) Getክፈፍbuffersegment() uintptr {
	Portመጻፊያbyte(ንድፎችcontrollerማውጫport, 0x06)
	var segmentቁጥር uint8 = ((Portማንበቢያbyte(ንድፎችcontrollerdataport) >> 2) & 0x03)
	switch segmentቁጥር {
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
func (self *Tቪዲዮንድፎችማዘጋጃ) Putpixel(x uint32, y uint32, colorማውጫ uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getክፈፍbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = colorማውጫ

}
func (self *Tቪዲዮንድፎችማዘጋጃ) Getcolorማውጫ(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tቪዲዮንድፎችማዘጋጃ) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getcolorማውጫ(r, g, b))
}
func (self *Tቪዲዮንድፎችማዘጋጃ) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tቪዲዮንድፎችማዘጋጃ) Supportዘዴ(ስፋት uint32, እርዝመት uint32, colordepth uint32) bool {
	return ስፋት == 320 && እርዝመት == 200 && colordepth == 8
}
func (self *Tቪዲዮንድፎችማዘጋጃ) Setዘዴ(ስፋት uint32, እርዝመት uint32, colordepth uint32) bool {
	if !self.Supportዘዴ(ስፋት, እርዝመት, colordepth) {
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

	self.Wመጻፊያregister(g320x200x256)

	return true
}
