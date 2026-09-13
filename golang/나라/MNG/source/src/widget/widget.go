package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоГрафикarray)
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

func (self *TWidget) Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.parent = parent

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TWidget) Getfocus(widget IWidget) {
	if self.parent != nil {
		self.parent.Getfocus(widget)
	}
}
func (self *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) Setcolor(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *TВидеоГрафикarray) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetХулганаeventhandler struct {
}

var хулганаwidget TWidget
var хулганаvga TВидеоГрафикarray
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TWidgetХулганаeventhandler) Init(widget TWidget, vga TВидеоГрафикarray) {
	хулганаwidget = widget
	хулганаvga = vga
}
func (self *TWidgetХулганаeventhandler) OnХулганаdown(button int8) {

	хулганаwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	хулганаwidget.Setcolor(0xA8, 0x00, 0x00)
	хулганаwidget.Draw(&хулганаvga)

	хулганаwidget.Draw(&хулганаvga)

}

func (self *TWidgetХулганаeventhandler) OnХулганаДээш(button int8) {
}

func (self *TWidgetХулганаeventhandler) OnХулганаЗөөх(x int8, y int8) {
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

	хулганаwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	хулганаwidget.Setcolor(0x00, 0x00, 0x00)
	хулганаwidget.Draw(&хулганаvga)

	хулганаwidget.Set_local_coordinates(uint32(xposition), uint32(yposition))
	хулганаwidget.Setcolor(0x00, 0x00, 0xA8)
	хулганаwidget.Draw(&хулганаvga)

	previousx = xposition
	previousy = yposition

}
