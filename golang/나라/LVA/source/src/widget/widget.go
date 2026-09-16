/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(vecāks IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokuss(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	KopaKrāsa(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikaMasīvs)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	vecāks	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (pats *TWidget) Init(vecāks IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	pats.vecāks = vecāks

	pats.x = x
	pats.y = y
	pats.w = w
	pats.h = h

	pats.r = r
	pats.g = g
	pats.b = b

	pats.Focussable = true

}
func (pats *TWidget) GetFokuss(widget IWidget) {
	if pats.vecāks != nil {
		pats.vecāks.GetFokuss(widget)
	}
}
func (pats *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if pats.vecāks != nil {

	}
	pats.x = x
	pats.y = y

}
func (pats *TWidget) KopaKrāsa(r uint32, g uint32, b uint32) {
	pats.r = r
	pats.g = g
	pats.b = b
}

func (pats *TWidget) Draw(vga *TVideoGrafikaMasīvs) {
	vga.FillTaisnstūris(pats.x, pats.y, pats.w, pats.h, uint8(pats.r), uint8(pats.g), uint8(pats.b))
}

func (pats *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return pats.x <= x && x < (pats.x+pats.w) && pats.y <= y && y < (pats.y+pats.h)
}

type TWidgetPeleNotikumshandler struct {
}

var pelewidget TWidget
var pelevga TVideoGrafikaMasīvs
var previousx int16 = 0
var previousy int16 = 0
var xNovietojums int16 = 0
var yNovietojums int16 = 0

func (pats *TWidgetPeleNotikumshandler) Init(widget TWidget, vga TVideoGrafikaMasīvs) {
	pelewidget = widget
	pelevga = vga
}
func (pats *TWidgetPeleNotikumshandler) IeslēgtsPeleLejup(pogas int8) {

	pelewidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	pelewidget.KopaKrāsa(0xA8, 0x00, 0x00)
	pelewidget.Draw(&pelevga)

	pelewidget.Draw(&pelevga)

}

func (pats *TWidgetPeleNotikumshandler) IeslēgtsPeleAugšup(pogas int8) {
}

func (pats *TWidgetPeleNotikumshandler) IeslēgtsPelePārvietot(x int8, y int8) {
	xNovietojums += int16(x)
	if xNovietojums < 0 {
		xNovietojums = 0
	}
	if xNovietojums >= 320 {
		xNovietojums = 320
	}

	yNovietojums -= int16(y)

	if yNovietojums < 0 {
		yNovietojums = 0
	}
	if yNovietojums >= 200 {
		yNovietojums = 200
	}

	pelewidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	pelewidget.KopaKrāsa(0x00, 0x00, 0x00)
	pelewidget.Draw(&pelevga)

	pelewidget.Set_local_coordinates(uint32(xNovietojums), uint32(yNovietojums))
	pelewidget.KopaKrāsa(0x00, 0x00, 0xA8)
	pelewidget.Draw(&pelevga)

	previousx = xNovietojums
	previousy = yNovietojums

}
