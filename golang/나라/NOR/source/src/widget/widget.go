/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(opphav IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	SettFarge(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikkTabell)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	opphav	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (selv *TWidget) Init(opphav IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	selv.opphav = opphav

	selv.x = x
	selv.y = y
	selv.w = w
	selv.h = h

	selv.r = r
	selv.g = g
	selv.b = b

	selv.Focussable = true

}
func (selv *TWidget) GetFokus(widget IWidget) {
	if selv.opphav != nil {
		selv.opphav.GetFokus(widget)
	}
}
func (selv *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if selv.opphav != nil {

	}
	selv.x = x
	selv.y = y

}
func (selv *TWidget) SettFarge(r uint32, g uint32, b uint32) {
	selv.r = r
	selv.g = g
	selv.b = b
}

func (selv *TWidget) Draw(vga *TVideoGrafikkTabell) {
	vga.FillRektangel(selv.x, selv.y, selv.w, selv.h, uint8(selv.r), uint8(selv.g), uint8(selv.b))
}

func (selv *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return selv.x <= x && x < (selv.x+selv.w) && selv.y <= y && y < (selv.y+selv.h)
}

type TWidgetMusHendelsehandler struct {
}

var muswidget TWidget
var musvga TVideoGrafikkTabell
var previousx int16 = 0
var previousy int16 = 0
var xPosisjon int16 = 0
var yPosisjon int16 = 0

func (selv *TWidgetMusHendelsehandler) Init(widget TWidget, vga TVideoGrafikkTabell) {
	muswidget = widget
	musvga = vga
}
func (selv *TWidgetMusHendelsehandler) PåMusNed(knapp int8) {

	muswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	muswidget.SettFarge(0xA8, 0x00, 0x00)
	muswidget.Draw(&musvga)

	muswidget.Draw(&musvga)

}

func (selv *TWidgetMusHendelsehandler) PåMusOpp(knapp int8) {
}

func (selv *TWidgetMusHendelsehandler) PåMusFlytt(x int8, y int8) {
	xPosisjon += int16(x)
	if xPosisjon < 0 {
		xPosisjon = 0
	}
	if xPosisjon >= 320 {
		xPosisjon = 320
	}

	yPosisjon -= int16(y)

	if yPosisjon < 0 {
		yPosisjon = 0
	}
	if yPosisjon >= 200 {
		yPosisjon = 200
	}

	muswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	muswidget.SettFarge(0x00, 0x00, 0x00)
	muswidget.Draw(&musvga)

	muswidget.Set_local_coordinates(uint32(xPosisjon), uint32(yPosisjon))
	muswidget.SettFarge(0x00, 0x00, 0xA8)
	muswidget.Draw(&musvga)

	previousx = xPosisjon
	previousy = yPosisjon

}
