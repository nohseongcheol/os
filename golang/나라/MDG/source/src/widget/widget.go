package widget

import . "vga"

type IWidget interface {
	Init(reny IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
	Draw(vga *TVidéoSaryarray)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	reny	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (nytena *TWidget) Init(reny IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	nytena.reny = reny

	nytena.x = x
	nytena.y = y
	nytena.w = w
	nytena.h = h

	nytena.r = r
	nytena.g = g
	nytena.b = b

	nytena.Focussable = true

}
func (nytena *TWidget) Getfocus(widget IWidget) {
	if nytena.reny != nil {
		nytena.reny.Getfocus(widget)
	}
}
func (nytena *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if nytena.reny != nil {

	}
	nytena.x = x
	nytena.y = y

}
func (nytena *TWidget) Setcolor(r uint32, g uint32, b uint32) {
	nytena.r = r
	nytena.g = g
	nytena.b = b
}

func (nytena *TWidget) Draw(vga *TVidéoSaryarray) {
	vga.Fillrectangle(nytena.x, nytena.y, nytena.w, nytena.h, uint8(nytena.r), uint8(nytena.g), uint8(nytena.b))
}

func (nytena *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return nytena.x <= x && x < (nytena.x+nytena.w) && nytena.y <= y && y < (nytena.y+nytena.h)
}

type TWidgetTotozyeventhandler struct {
}

var totozywidget TWidget
var totozyvga TVidéoSaryarray
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (nytena *TWidgetTotozyeventhandler) Init(widget TWidget, vga TVidéoSaryarray) {
	totozywidget = widget
	totozyvga = vga
}
func (nytena *TWidgetTotozyeventhandler) OnTotozydown(button int8) {

	totozywidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	totozywidget.Setcolor(0xA8, 0x00, 0x00)
	totozywidget.Draw(&totozyvga)

	totozywidget.Draw(&totozyvga)

}

func (nytena *TWidgetTotozyeventhandler) OnTotozyAmbony(button int8) {
}

func (nytena *TWidgetTotozyeventhandler) OnTotozyAfindrao(x int8, y int8) {
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

	totozywidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	totozywidget.Setcolor(0x00, 0x00, 0x00)
	totozywidget.Draw(&totozyvga)

	totozywidget.Set_local_coordinates(uint32(xposition), uint32(yposition))
	totozywidget.Setcolor(0x00, 0x00, 0xA8)
	totozywidget.Draw(&totozyvga)

	previousx = xposition
	previousy = yposition

}
