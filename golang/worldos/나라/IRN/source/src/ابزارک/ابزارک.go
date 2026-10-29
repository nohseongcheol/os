/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ابزارک

import . "vga"

type Iابزارک interface {
	Init(والد Iابزارک, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(ابزارک Iابزارک)
	Set_local_coordinates(x int32, y int32)
	Setرنگ(r uint32, g uint32, b uint32)
	Draw(vga *Tویدیوگرافیکآرایه)
	Containscoordinate(x uint32, y uint32) bool
}

type Tابزارک struct {
	والد	Iابزارک
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (خود *Tابزارک) Init(والد Iابزارک, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	خود.والد = والد

	خود.x = x
	خود.y = y
	خود.w = w
	خود.h = h

	خود.r = r
	خود.g = g
	خود.b = b

	خود.Focussable = true

}
func (خود *Tابزارک) Getfocus(ابزارک Iابزارک) {
	if خود.والد != nil {
		خود.والد.Getfocus(ابزارک)
	}
}
func (خود *Tابزارک) Set_local_coordinates(x uint32, y uint32) {
	if خود.والد != nil {

	}
	خود.x = x
	خود.y = y

}
func (خود *Tابزارک) Setرنگ(r uint32, g uint32, b uint32) {
	خود.r = r
	خود.g = g
	خود.b = b
}

func (خود *Tابزارک) Draw(vga *Tویدیوگرافیکآرایه) {
	vga.Fillrectangle(خود.x, خود.y, خود.w, خود.h, uint8(خود.r), uint8(خود.g), uint8(خود.b))
}

func (خود *Tابزارک) Containscoordinate(x uint32, y uint32) bool {
	return خود.x <= x && x < (خود.x+خود.w) && خود.y <= y && y < (خود.y+خود.h)
}

type Tابزارکموشیeventhandler struct {
}

var موشیابزارک Tابزارک
var موشیvga Tویدیوگرافیکآرایه
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (خود *Tابزارکموشیeventhandler) Init(ابزارک Tابزارک, vga Tویدیوگرافیکآرایه) {
	موشیابزارک = ابزارک
	موشیvga = vga
}
func (خود *Tابزارکموشیeventhandler) Oروشنموشیپایین(دکمه int8) {

	موشیابزارک.Set_local_coordinates(uint32(previousx), uint32(previousy))
	موشیابزارک.Setرنگ(0xA8, 0x00, 0x00)
	موشیابزارک.Draw(&موشیvga)

	موشیابزارک.Draw(&موشیvga)

}

func (خود *Tابزارکموشیeventhandler) Oروشنموشیبالا(دکمه int8) {
}

func (خود *Tابزارکموشیeventhandler) Oروشنموشیانتقال(x int8, y int8) {
	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 320 {
		xposition = 320
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 200 {
		yposition = 200
	}

	موشیابزارک.Set_local_coordinates(uint32(previousx), uint32(previousy))
	موشیابزارک.Setرنگ(0x00, 0x00, 0x00)
	موشیابزارک.Draw(&موشیvga)

	موشیابزارک.Set_local_coordinates(uint32(xposition), uint32(yposition))
	موشیابزارک.Setرنگ(0x00, 0x00, 0xA8)
	موشیابزارک.Draw(&موشیvga)

	previousx = xposition
	previousy = yposition

}
