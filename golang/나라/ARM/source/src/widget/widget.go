/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(ծնող IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	SetԳույն(r uint32, g uint32, b uint32)
	Draw(vga *TՏեսանյութԳրաֆիկաԶանգված)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	ծնող	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (ինքնուրույն *TWidget) Init(ծնող IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	ինքնուրույն.ծնող = ծնող

	ինքնուրույն.x = x
	ինքնուրույն.y = y
	ինքնուրույն.w = w
	ինքնուրույն.h = h

	ինքնուրույն.r = r
	ինքնուրույն.g = g
	ինքնուրույն.b = b

	ինքնուրույն.Focussable = true

}
func (ինքնուրույն *TWidget) Getfocus(widget IWidget) {
	if ինքնուրույն.ծնող != nil {
		ինքնուրույն.ծնող.Getfocus(widget)
	}
}
func (ինքնուրույն *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if ինքնուրույն.ծնող != nil {

	}
	ինքնուրույն.x = x
	ինքնուրույն.y = y

}
func (ինքնուրույն *TWidget) SetԳույն(r uint32, g uint32, b uint32) {
	ինքնուրույն.r = r
	ինքնուրույն.g = g
	ինքնուրույն.b = b
}

func (ինքնուրույն *TWidget) Draw(vga *TՏեսանյութԳրաֆիկաԶանգված) {
	vga.Fillrectangle(ինքնուրույն.x, ինքնուրույն.y, ինքնուրույն.w, ինքնուրույն.h, uint8(ինքնուրույն.r), uint8(ինքնուրույն.g), uint8(ինքնուրույն.b))
}

func (ինքնուրույն *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return ինքնուրույն.x <= x && x < (ինքնուրույն.x+ինքնուրույն.w) && ինքնուրույն.y <= y && y < (ինքնուրույն.y+ինքնուրույն.h)
}

type TWidgetՄկնիկeventhandler struct {
}

var մկնիկwidget TWidget
var մկնիկvga TՏեսանյութԳրաֆիկաԶանգված
var previousx int16 = 0
var previousy int16 = 0
var xԴիրք int16 = 0
var yԴիրք int16 = 0

func (ինքնուրույն *TWidgetՄկնիկeventhandler) Init(widget TWidget, vga TՏեսանյութԳրաֆիկաԶանգված) {
	մկնիկwidget = widget
	մկնիկvga = vga
}
func (ինքնուրույն *TWidgetՄկնիկeventhandler) ՄիացնելՄկնիկՆերքև(button int8) {

	մկնիկwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	մկնիկwidget.SetԳույն(0xA8, 0x00, 0x00)
	մկնիկwidget.Draw(&մկնիկvga)

	մկնիկwidget.Draw(&մկնիկvga)

}

func (ինքնուրույն *TWidgetՄկնիկeventhandler) ՄիացնելՄկնիկՎերև(button int8) {
}

func (ինքնուրույն *TWidgetՄկնիկeventhandler) ՄիացնելՄկնիկՏեղաշարժել(x int8, y int8) {
	xԴիրք += int16(x)
	if xԴիրք < 0 {
		xԴիրք = 0
	}
	if xԴիրք >= 320 {
		xԴիրք = 320
	}

	yԴիրք -= int16(y)

	if yԴիրք < 0 {
		yԴիրք = 0
	}
	if yԴիրք >= 200 {
		yԴիրք = 200
	}

	մկնիկwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	մկնիկwidget.SetԳույն(0x00, 0x00, 0x00)
	մկնիկwidget.Draw(&մկնիկvga)

	մկնիկwidget.Set_local_coordinates(uint32(xԴիրք), uint32(yԴիրք))
	մկնիկwidget.SetԳույն(0x00, 0x00, 0xA8)
	մկնիկwidget.Draw(&մկնիկvga)

	previousx = xԴիրք
	previousy = yԴիրք

}
