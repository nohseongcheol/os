package vga

import . "unsafe"
import . "منفذ"

type Tفيديورسومياتمصفوفة struct {
}

var micsمنفذ uint16 = 0x3c2
var crtcفهرسمنفذ uint16 = 0x3d4
var crtcبياناتمنفذ uint16 = 0x3d5
var sequencerفهرسمنفذ uint16 = 0x3c4
var sequencerبياناتمنفذ uint16 = 0x3c5
var رسومياتمتحكمفهرسمنفذ uint16 = 0x3ce
var رسومياتمتحكمبياناتمنفذ uint16 = 0x3cf
var خاصيةمتحكمفهرسمنفذ uint16 = 0x3c0
var خاصيةمتحكمقراءةمنفذ uint16 = 0x3c1
var خاصيةمتحكمكتابةمنفذ uint16 = 0x3c0
var خاصيةمتحكمأعدالضبطمنفذ uint16 = 0x3da

func (نفسه *Tفيديورسومياتمصفوفة) Wكتابةسجل(سجل []byte) {
	var regفهرس uint16 = 0

	Pمنفذكتابةبايت(micsمنفذ, سجل[regفهرس])
	regفهرس++

	var i uint8
	for i = 0; i < 5; i++ {
		Pمنفذكتابةبايت(sequencerفهرسمنفذ, i)
		Pمنفذكتابةبايت(sequencerبياناتمنفذ, سجل[regفهرس])
		regفهرس++
	}

	Pمنفذكتابةبايت(crtcفهرسمنفذ, 0x03)

	Pمنفذكتابةبايت(crtcبياناتمنفذ, (Pمنفذقراءةبايت(crtcبياناتمنفذ) | 0x80))
	Pمنفذكتابةبايت(crtcفهرسمنفذ, 0x11)
	Pمنفذكتابةبايت(crtcبياناتمنفذ, (Pمنفذقراءةبايت(crtcبياناتمنفذ) & ^uint8(0x80)))

	سجل[0x03] = سجل[0x03] | 0x80
	سجل[0x11] = سجل[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pمنفذكتابةبايت(crtcفهرسمنفذ, i)
		Pمنفذكتابةبايت(crtcبياناتمنفذ, سجل[regفهرس])
		regفهرس++
	}

	for i = 0; i < 9; i++ {
		Pمنفذكتابةبايت(رسومياتمتحكمفهرسمنفذ, i)
		Pمنفذكتابةبايت(رسومياتمتحكمبياناتمنفذ, سجل[regفهرس])
		regفهرس++
	}

	for i = 0; i < 21; i++ {
		Pمنفذقراءةبايت(خاصيةمتحكمأعدالضبطمنفذ)
		Pمنفذكتابةبايت(خاصيةمتحكمفهرسمنفذ, i)
		Pمنفذكتابةبايت(خاصيةمتحكمكتابةمنفذ, سجل[regفهرس])
		regفهرس++
	}

	Pمنفذقراءةبايت(خاصيةمتحكمأعدالضبطمنفذ)
	Pمنفذكتابةبايت(خاصيةمتحكمفهرسمنفذ, 0x20)

}

func (نفسه *Tفيديورسومياتمصفوفة) Getإطارbuffersegment() uintptr {
	Pمنفذكتابةبايت(رسومياتمتحكمفهرسمنفذ, 0x06)
	var segmentالأرقام uint8 = ((Pمنفذقراءةبايت(رسومياتمتحكمبياناتمنفذ) >> 2) & 0x03)
	switch segmentالأرقام {
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
func (نفسه *Tفيديورسومياتمصفوفة) Putpixel(x uint32, y uint32, اللونفهرس uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = نفسه.Getإطارbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = اللونفهرس

}
func (نفسه *Tفيديورسومياتمصفوفة) Getاللونفهرس(r uint8, g uint8, b uint8) uint8 {
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
func (نفسه *Tفيديورسومياتمصفوفة) Putpixelحﺥﺯ(x uint32, y uint32, r uint8, g uint8, b uint8) {
	نفسه.Putpixel(x, y, نفسه.Getاللونفهرس(r, g, b))
}
func (نفسه *Tفيديورسومياتمصفوفة) Fillمستطيل(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			نفسه.Putpixelحﺥﺯ(X, Y, r, g, b)
		}
	}
}
func (نفسه *Tفيديورسومياتمصفوفة) Supportوضع(العرض uint32, الارتفاع uint32, اللونdepth uint32) bool {
	return العرض == 320 && الارتفاع == 200 && اللونdepth == 8
}
func (نفسه *Tفيديورسومياتمصفوفة) Sتحديدوضع(العرض uint32, الارتفاع uint32, اللونdepth uint32) bool {
	if !نفسه.Supportوضع(العرض, الارتفاع, اللونdepth) {
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

	نفسه.Wكتابةسجل(g320x200x256)

	return true
}
