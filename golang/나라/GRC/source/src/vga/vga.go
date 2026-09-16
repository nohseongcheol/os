/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "θύρα"

type TΒίντεοΓραφικάΔιάταξη struct {
}

var micsΘύρα uint16 = 0x3c2
var crtcΚατάλογοςΘύρα uint16 = 0x3d4
var crtcdataΘύρα uint16 = 0x3d5
var sequencerΚατάλογοςΘύρα uint16 = 0x3c4
var sequencerdataΘύρα uint16 = 0x3c5
var γραφικάcontrollerΚατάλογοςΘύρα uint16 = 0x3ce
var γραφικάcontrollerdataΘύρα uint16 = 0x3cf
var γνώρισμαcontrollerΚατάλογοςΘύρα uint16 = 0x3c0
var γνώρισμαcontrollerΑνάγνωσηΘύρα uint16 = 0x3c1
var γνώρισμαcontrollerΕγγραφήΘύρα uint16 = 0x3c0
var γνώρισμαcontrollerΕπαναφοράΘύρα uint16 = 0x3da

func (self *TΒίντεοΓραφικάΔιάταξη) Εγγραφήregister(register []byte) {
	var regΚατάλογος uint16 = 0

	ΘύραΕγγραφήbyte(micsΘύρα, register[regΚατάλογος])
	regΚατάλογος++

	var i uint8
	for i = 0; i < 5; i++ {
		ΘύραΕγγραφήbyte(sequencerΚατάλογοςΘύρα, i)
		ΘύραΕγγραφήbyte(sequencerdataΘύρα, register[regΚατάλογος])
		regΚατάλογος++
	}

	ΘύραΕγγραφήbyte(crtcΚατάλογοςΘύρα, 0x03)

	ΘύραΕγγραφήbyte(crtcdataΘύρα, (ΘύραΑνάγνωσηbyte(crtcdataΘύρα) | 0x80))
	ΘύραΕγγραφήbyte(crtcΚατάλογοςΘύρα, 0x11)
	ΘύραΕγγραφήbyte(crtcdataΘύρα, (ΘύραΑνάγνωσηbyte(crtcdataΘύρα) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ΘύραΕγγραφήbyte(crtcΚατάλογοςΘύρα, i)
		ΘύραΕγγραφήbyte(crtcdataΘύρα, register[regΚατάλογος])
		regΚατάλογος++
	}

	for i = 0; i < 9; i++ {
		ΘύραΕγγραφήbyte(γραφικάcontrollerΚατάλογοςΘύρα, i)
		ΘύραΕγγραφήbyte(γραφικάcontrollerdataΘύρα, register[regΚατάλογος])
		regΚατάλογος++
	}

	for i = 0; i < 21; i++ {
		ΘύραΑνάγνωσηbyte(γνώρισμαcontrollerΕπαναφοράΘύρα)
		ΘύραΕγγραφήbyte(γνώρισμαcontrollerΚατάλογοςΘύρα, i)
		ΘύραΕγγραφήbyte(γνώρισμαcontrollerΕγγραφήΘύρα, register[regΚατάλογος])
		regΚατάλογος++
	}

	ΘύραΑνάγνωσηbyte(γνώρισμαcontrollerΕπαναφοράΘύρα)
	ΘύραΕγγραφήbyte(γνώρισμαcontrollerΚατάλογοςΘύρα, 0x20)

}

func (self *TΒίντεοΓραφικάΔιάταξη) GetΠλαίσιοbuffersegment() uintptr {
	ΘύραΕγγραφήbyte(γραφικάcontrollerΚατάλογοςΘύρα, 0x06)
	var segmentΑριθμός uint8 = ((ΘύραΑνάγνωσηbyte(γραφικάcontrollerdataΘύρα) >> 2) & 0x03)
	switch segmentΑριθμός {
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
func (self *TΒίντεοΓραφικάΔιάταξη) Putpixel(x uint32, y uint32, χρώμαΚατάλογος uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.GetΠλαίσιοbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = χρώμαΚατάλογος

}
func (self *TΒίντεοΓραφικάΔιάταξη) GetΧρώμαΚατάλογος(r uint8, g uint8, b uint8) uint8 {
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
func (self *TΒίντεοΓραφικάΔιάταξη) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetΧρώμαΚατάλογος(r, g, b))
}
func (self *TΒίντεοΓραφικάΔιάταξη) FillΟρθογώνιο(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TΒίντεοΓραφικάΔιάταξη) ΥποστήριξηΚΑΤΑΣΤΑΣΗ(πλάτος uint32, ύψος uint32, χρώμαdepth uint32) bool {
	return πλάτος == 320 && ύψος == 200 && χρώμαdepth == 8
}
func (self *TΒίντεοΓραφικάΔιάταξη) ΣύνολοΚΑΤΑΣΤΑΣΗ(πλάτος uint32, ύψος uint32, χρώμαdepth uint32) bool {
	if !self.ΥποστήριξηΚΑΤΑΣΤΑΣΗ(πλάτος, ύψος, χρώμαdepth) {
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

	self.Εγγραφήregister(g320x200x256)

	return true
}
