/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package skärmelement

import . "vga"

type ISkärmelement interface {
	Init(förälder ISkärmelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(skärmelement ISkärmelement)
	Ange_lokala_koordinater(x int32, y int32)
	MängdFärg(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikVektor)
	Containscoordinate(x uint32, y uint32) bool
}

type TSkärmelement struct {
	förälder	ISkärmelement
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (själv *TSkärmelement) Init(förälder ISkärmelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	själv.förälder = förälder

	själv.x = x
	själv.y = y
	själv.w = w
	själv.h = h

	själv.r = r
	själv.g = g
	själv.b = b

	själv.Focussable = true

}
func (själv *TSkärmelement) GetFokus(skärmelement ISkärmelement) {
	if själv.förälder != nil {
		själv.förälder.GetFokus(skärmelement)
	}
}
func (själv *TSkärmelement) Ange_lokala_koordinater(x uint32, y uint32) {
	if själv.förälder != nil {

	}
	själv.x = x
	själv.y = y

}
func (själv *TSkärmelement) MängdFärg(r uint32, g uint32, b uint32) {
	själv.r = r
	själv.g = g
	själv.b = b
}

func (själv *TSkärmelement) Draw(vga *TVideoGrafikVektor) {
	vga.FillRektangel(själv.x, själv.y, själv.w, själv.h, uint8(själv.r), uint8(själv.g), uint8(själv.b))
}

func (själv *TSkärmelement) Containscoordinate(x uint32, y uint32) bool {
	return själv.x <= x && x < (själv.x+själv.w) && själv.y <= y && y < (själv.y+själv.h)
}

type TWidgetMusHändelsehandler struct {
}

var muswidget TSkärmelement
var musvga TVideoGrafikVektor
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (själv *TWidgetMusHändelsehandler) Init(skärmelement TSkärmelement, vga TVideoGrafikVektor) {
	muswidget = skärmelement
	musvga = vga
}
func (själv *TWidgetMusHändelsehandler) PåMusNer(knapp int8) {

	muswidget.Ange_lokala_koordinater(uint32(previousx), uint32(previousy))
	muswidget.MängdFärg(0xA8, 0x00, 0x00)
	muswidget.Draw(&musvga)

	muswidget.Draw(&musvga)

}

func (själv *TWidgetMusHändelsehandler) PåMusUpp(knapp int8) {
}

func (själv *TWidgetMusHändelsehandler) PåMusFlytta(x int8, y int8) {
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

	muswidget.Ange_lokala_koordinater(uint32(previousx), uint32(previousy))
	muswidget.MängdFärg(0x00, 0x00, 0x00)
	muswidget.Draw(&musvga)

	muswidget.Ange_lokala_koordinater(uint32(xposition), uint32(yposition))
	muswidget.MängdFärg(0x00, 0x00, 0xA8)
	muswidget.Draw(&musvga)

	previousx = xposition
	previousy = yposition

}
