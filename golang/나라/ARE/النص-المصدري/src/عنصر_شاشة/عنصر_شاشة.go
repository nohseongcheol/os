package عنصر_شاشة

import . "vga"

type Iعنصر_شاشة interface {
	Init(أب Iعنصر_شاشة, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getالتركيز(عنصر_شاشة Iعنصر_شاشة)
	Mتعيين_الإحداثيات_المحلية(x int32, y int32)
	Sتحديداللون(r uint32, g uint32, b uint32)
	Draw(vga *Tفيديورسومياتمصفوفة)
	Containscoordinate(x uint32, y uint32) bool
}

type Tعنصر_شاشة struct {
	أب	Iعنصر_شاشة
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (نفسه *Tعنصر_شاشة) Init(أب Iعنصر_شاشة, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	نفسه.أب = أب

	نفسه.x = x
	نفسه.y = y
	نفسه.w = w
	نفسه.h = h

	نفسه.r = r
	نفسه.g = g
	نفسه.b = b

	نفسه.Focussable = true

}
func (نفسه *Tعنصر_شاشة) Getالتركيز(عنصر_شاشة Iعنصر_شاشة) {
	if نفسه.أب != nil {
		نفسه.أب.Getالتركيز(عنصر_شاشة)
	}
}
func (نفسه *Tعنصر_شاشة) Mتعيين_الإحداثيات_المحلية(x uint32, y uint32) {
	if نفسه.أب != nil {

	}
	نفسه.x = x
	نفسه.y = y

}
func (نفسه *Tعنصر_شاشة) Sتحديداللون(r uint32, g uint32, b uint32) {
	نفسه.r = r
	نفسه.g = g
	نفسه.b = b
}

func (نفسه *Tعنصر_شاشة) Draw(vga *Tفيديورسومياتمصفوفة) {
	vga.Fillمستطيل(نفسه.x, نفسه.y, نفسه.w, نفسه.h, uint8(نفسه.r), uint8(نفسه.g), uint8(نفسه.b))
}

func (نفسه *Tعنصر_شاشة) Containscoordinate(x uint32, y uint32) bool {
	return نفسه.x <= x && x < (نفسه.x+نفسه.w) && نفسه.y <= y && y < (نفسه.y+نفسه.h)
}

type Tعنصرواجهةفأرةحدثhandler struct {
}

var فأرةعنصرواجهة Tعنصر_شاشة
var فأرةvga Tفيديورسومياتمصفوفة
var previousx int16 = 0
var previousy int16 = 0
var xالموضع int16 = 0
var yالموضع int16 = 0

func (نفسه *Tعنصرواجهةفأرةحدثhandler) Init(عنصر_شاشة Tعنصر_شاشة, vga Tفيديورسومياتمصفوفة) {
	فأرةعنصرواجهة = عنصر_شاشة
	فأرةvga = vga
}
func (نفسه *Tعنصرواجهةفأرةحدثhandler) Oعندفأرةأسفل(زر int8) {

	فأرةعنصرواجهة.Mتعيين_الإحداثيات_المحلية(uint32(previousx), uint32(previousy))
	فأرةعنصرواجهة.Sتحديداللون(0xA8, 0x00, 0x00)
	فأرةعنصرواجهة.Draw(&فأرةvga)

	فأرةعنصرواجهة.Draw(&فأرةvga)

}

func (نفسه *Tعنصرواجهةفأرةحدثhandler) Oعندفأرةأعلى(زر int8) {
}

func (نفسه *Tعنصرواجهةفأرةحدثhandler) Oعندفأرةانقل(x int8, y int8) {
	xالموضع += int16(x)
	if xالموضع < 0 {
		xالموضع = 0
	}
	if xالموضع >= 320 {
		xالموضع = 320
	}

	yالموضع -= int16(y)

	if yالموضع < 0 {
		yالموضع = 0
	}
	if yالموضع >= 200 {
		yالموضع = 200
	}

	فأرةعنصرواجهة.Mتعيين_الإحداثيات_المحلية(uint32(previousx), uint32(previousy))
	فأرةعنصرواجهة.Sتحديداللون(0x00, 0x00, 0x00)
	فأرةعنصرواجهة.Draw(&فأرةvga)

	فأرةعنصرواجهة.Mتعيين_الإحداثيات_المحلية(uint32(xالموضع), uint32(yالموضع))
	فأرةعنصرواجهة.Sتحديداللون(0x00, 0x00, 0xA8)
	فأرةعنصرواجهة.Draw(&فأرةvga)

	previousx = xالموضع
	previousy = yالموضع

}
