/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	ПоставиБоја(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоГрафикаПострои)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	parent	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (само *TWidget) Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	само.parent = parent

	само.x = x
	само.y = y
	само.w = w
	само.h = h

	само.r = r
	само.g = g
	само.b = b

	само.Focussable = true

}
func (само *TWidget) Getfocus(widget IWidget) {
	if само.parent != nil {
		само.parent.Getfocus(widget)
	}
}
func (само *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if само.parent != nil {

	}
	само.x = x
	само.y = y

}
func (само *TWidget) ПоставиБоја(r uint32, g uint32, b uint32) {
	само.r = r
	само.g = g
	само.b = b
}

func (само *TWidget) Draw(vga *TВидеоГрафикаПострои) {
	vga.FillПравоаголник(само.x, само.y, само.w, само.h, uint8(само.r), uint8(само.g), uint8(само.b))
}

func (само *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return само.x <= x && x < (само.x+само.w) && само.y <= y && y < (само.y+само.h)
}

type TWidgetГлушецeventhandler struct {
}

var глушецwidget TWidget
var глушецvga TВидеоГрафикаПострои
var previousx int16 = 0
var previousy int16 = 0
var xПозиција int16 = 0
var yПозиција int16 = 0

func (само *TWidgetГлушецeventhandler) Init(widget TWidget, vga TВидеоГрафикаПострои) {
	глушецwidget = widget
	глушецvga = vga
}
func (само *TWidgetГлушецeventhandler) ВклученоГлушецДолу(button int8) {

	глушецwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	глушецwidget.ПоставиБоја(0xA8, 0x00, 0x00)
	глушецwidget.Draw(&глушецvga)

	глушецwidget.Draw(&глушецvga)

}

func (само *TWidgetГлушецeventhandler) ВклученоГлушецГоре(button int8) {
}

func (само *TWidgetГлушецeventhandler) ВклученоГлушецПомести(x int8, y int8) {
	xПозиција += int16(x)
	if xПозиција < 0 {
		xПозиција = 0
	}
	if xПозиција >= 320 {
		xПозиција = 320
	}

	yПозиција -= int16(y)

	if yПозиција < 0 {
		yПозиција = 0
	}
	if yПозиција >= 200 {
		yПозиција = 200
	}

	глушецwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	глушецwidget.ПоставиБоја(0x00, 0x00, 0x00)
	глушецwidget.Draw(&глушецvga)

	глушецwidget.Set_local_coordinates(uint32(xПозиција), uint32(yПозиција))
	глушецwidget.ПоставиБоја(0x00, 0x00, 0xA8)
	глушецwidget.Draw(&глушецvga)

	previousx = xПозиција
	previousy = yПозиција

}
