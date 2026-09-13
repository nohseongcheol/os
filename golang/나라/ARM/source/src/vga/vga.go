package vga

import . "unsafe"
import . "պորտ"

type TՏեսանյութԳրաֆիկաԶանգված struct {
}

var micsՊորտ uint16 = 0x3c2
var crtcԻնդեքսՊորտ uint16 = 0x3d4
var crtcdataՊորտ uint16 = 0x3d5
var sequencerԻնդեքսՊորտ uint16 = 0x3c4
var sequencerdataՊորտ uint16 = 0x3c5
var գրաֆիկաcontrollerԻնդեքսՊորտ uint16 = 0x3ce
var գրաֆիկաcontrollerdataՊորտ uint16 = 0x3cf
var ատրիբուտcontrollerԻնդեքսՊորտ uint16 = 0x3c0
var ատրիբուտcontrollerԸնթերցումՊորտ uint16 = 0x3c1
var ատրիբուտcontrollerԳրելՊորտ uint16 = 0x3c0
var ատրիբուտcontrollerԴադարեցնելՊորտ uint16 = 0x3da

func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) Գրելregister(register []byte) {
	var regԻնդեքս uint16 = 0

	ՊորտԳրելbyte(micsՊորտ, register[regԻնդեքս])
	regԻնդեքս++

	var i uint8
	for i = 0; i < 5; i++ {
		ՊորտԳրելbyte(sequencerԻնդեքսՊորտ, i)
		ՊորտԳրելbyte(sequencerdataՊորտ, register[regԻնդեքս])
		regԻնդեքս++
	}

	ՊորտԳրելbyte(crtcԻնդեքսՊորտ, 0x03)

	ՊորտԳրելbyte(crtcdataՊորտ, (ՊորտԸնթերցումbyte(crtcdataՊորտ) | 0x80))
	ՊորտԳրելbyte(crtcԻնդեքսՊորտ, 0x11)
	ՊորտԳրելbyte(crtcdataՊորտ, (ՊորտԸնթերցումbyte(crtcdataՊորտ) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ՊորտԳրելbyte(crtcԻնդեքսՊորտ, i)
		ՊորտԳրելbyte(crtcdataՊորտ, register[regԻնդեքս])
		regԻնդեքս++
	}

	for i = 0; i < 9; i++ {
		ՊորտԳրելbyte(գրաֆիկաcontrollerԻնդեքսՊորտ, i)
		ՊորտԳրելbyte(գրաֆիկաcontrollerdataՊորտ, register[regԻնդեքս])
		regԻնդեքս++
	}

	for i = 0; i < 21; i++ {
		ՊորտԸնթերցումbyte(ատրիբուտcontrollerԴադարեցնելՊորտ)
		ՊորտԳրելbyte(ատրիբուտcontrollerԻնդեքսՊորտ, i)
		ՊորտԳրելbyte(ատրիբուտcontrollerԳրելՊորտ, register[regԻնդեքս])
		regԻնդեքս++
	}

	ՊորտԸնթերցումbyte(ատրիբուտcontrollerԴադարեցնելՊորտ)
	ՊորտԳրելbyte(ատրիբուտcontrollerԻնդեքսՊորտ, 0x20)

}

func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) GetՇրջանակbuffersegment() uintptr {
	ՊորտԳրելbyte(գրաֆիկաcontrollerԻնդեքսՊորտ, 0x06)
	var segmentՀԱՄԱՐ uint8 = ((ՊորտԸնթերցումbyte(գրաֆիկաcontrollerdataՊորտ) >> 2) & 0x03)
	switch segmentՀԱՄԱՐ {
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
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) Putpixel(x uint32, y uint32, գույնԻնդեքս uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = ինքնուրույն.GetՇրջանակbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = գույնԻնդեքս

}
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) GetԳույնԻնդեքս(r uint8, g uint8, b uint8) uint8 {
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
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	ինքնուրույն.Putpixel(x, y, ինքնուրույն.GetԳույնԻնդեքս(r, g, b))
}
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			ինքնուրույն.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) SupportՌեժիմ(լայնություն uint32, բարձրություն uint32, գույնdepth uint32) bool {
	return լայնություն == 320 && բարձրություն == 200 && գույնdepth == 8
}
func (ինքնուրույն *TՏեսանյութԳրաֆիկաԶանգված) SetՌեժիմ(լայնություն uint32, բարձրություն uint32, գույնdepth uint32) bool {
	if !ինքնուրույն.SupportՌեժիմ(լայնություն, բարձրություն, գույնdepth) {
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

	ինքնուրույն.Գրելregister(g320x200x256)

	return true
}
