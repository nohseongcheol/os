package vga

import . "unsafe"
import . "درگاه"

type Tویدیوگرافیکآرایه struct {
}

var micsدرگاه uint16 = 0x3c2
var crtcنمایهدرگاه uint16 = 0x3d4
var crtcdataدرگاه uint16 = 0x3d5
var sequencerنمایهدرگاه uint16 = 0x3c4
var sequencerdataدرگاه uint16 = 0x3c5
var گرافیکcontrollerنمایهدرگاه uint16 = 0x3ce
var گرافیکcontrollerdataدرگاه uint16 = 0x3cf
var مشخصهcontrollerنمایهدرگاه uint16 = 0x3c0
var مشخصهcontrollerخواندندرگاه uint16 = 0x3c1
var مشخصهcontrollerنوشتندرگاه uint16 = 0x3c0
var مشخصهcontrollerبرگرداندنبهمقادیراولیهدرگاه uint16 = 0x3da

func (خود *Tویدیوگرافیکآرایه) Wنوشتنregister(register []byte) {
	var regنمایه uint16 = 0

	Pدرگاهنوشتنbyte(micsدرگاه, register[regنمایه])
	regنمایه++

	var i uint8
	for i = 0; i < 5; i++ {
		Pدرگاهنوشتنbyte(sequencerنمایهدرگاه, i)
		Pدرگاهنوشتنbyte(sequencerdataدرگاه, register[regنمایه])
		regنمایه++
	}

	Pدرگاهنوشتنbyte(crtcنمایهدرگاه, 0x03)

	Pدرگاهنوشتنbyte(crtcdataدرگاه, (Pدرگاهخواندنbyte(crtcdataدرگاه) | 0x80))
	Pدرگاهنوشتنbyte(crtcنمایهدرگاه, 0x11)
	Pدرگاهنوشتنbyte(crtcdataدرگاه, (Pدرگاهخواندنbyte(crtcdataدرگاه) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pدرگاهنوشتنbyte(crtcنمایهدرگاه, i)
		Pدرگاهنوشتنbyte(crtcdataدرگاه, register[regنمایه])
		regنمایه++
	}

	for i = 0; i < 9; i++ {
		Pدرگاهنوشتنbyte(گرافیکcontrollerنمایهدرگاه, i)
		Pدرگاهنوشتنbyte(گرافیکcontrollerdataدرگاه, register[regنمایه])
		regنمایه++
	}

	for i = 0; i < 21; i++ {
		Pدرگاهخواندنbyte(مشخصهcontrollerبرگرداندنبهمقادیراولیهدرگاه)
		Pدرگاهنوشتنbyte(مشخصهcontrollerنمایهدرگاه, i)
		Pدرگاهنوشتنbyte(مشخصهcontrollerنوشتندرگاه, register[regنمایه])
		regنمایه++
	}

	Pدرگاهخواندنbyte(مشخصهcontrollerبرگرداندنبهمقادیراولیهدرگاه)
	Pدرگاهنوشتنbyte(مشخصهcontrollerنمایهدرگاه, 0x20)

}

func (خود *Tویدیوگرافیکآرایه) Getچارچوبbuffersegment() uintptr {
	Pدرگاهنوشتنbyte(گرافیکcontrollerنمایهدرگاه, 0x06)
	var segmentnumber uint8 = ((Pدرگاهخواندنbyte(گرافیکcontrollerdataدرگاه) >> 2) & 0x03)
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
func (خود *Tویدیوگرافیکآرایه) Putpixel(x uint32, y uint32, رنگنمایه uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = خود.Getچارچوبbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = رنگنمایه

}
func (خود *Tویدیوگرافیکآرایه) Getرنگنمایه(r uint8, g uint8, b uint8) uint8 {
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
func (خود *Tویدیوگرافیکآرایه) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	خود.Putpixel(x, y, خود.Getرنگنمایه(r, g, b))
}
func (خود *Tویدیوگرافیکآرایه) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			خود.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (خود *Tویدیوگرافیکآرایه) Sپشتیبانیحالت(عرض uint32, ارتفاع uint32, رنگdepth uint32) bool {
	return عرض == 320 && ارتفاع == 200 && رنگdepth == 8
}
func (خود *Tویدیوگرافیکآرایه) Setحالت(عرض uint32, ارتفاع uint32, رنگdepth uint32) bool {
	if !خود.Sپشتیبانیحالت(عرض, ارتفاع, رنگdepth) {
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

	خود.Wنوشتنregister(g320x200x256)

	return true
}
