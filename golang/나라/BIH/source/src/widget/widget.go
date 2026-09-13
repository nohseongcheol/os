package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	SkupBoja(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikaarray)
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
func (self *TWidget) SkupBoja(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *TVideoGrafikaarray) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetMiševenthandler struct {
}

var mišwidget TWidget
var mišvga TVideoGrafikaarray
var previousx int16 = 0
var previousy int16 = 0
var xpoložaj int16 = 0
var ypoložaj int16 = 0

func (self *TWidgetMiševenthandler) Init(widget TWidget, vga TVideoGrafikaarray) {
	mišwidget = widget
	mišvga = vga
}
func (self *TWidgetMiševenthandler) UključenMišdown(button int8) {

	mišwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišwidget.SkupBoja(0xA8, 0x00, 0x00)
	mišwidget.Draw(&mišvga)

	mišwidget.Draw(&mišvga)

}

func (self *TWidgetMiševenthandler) UključenMišGore(button int8) {
}

func (self *TWidgetMiševenthandler) UključenMišPremjesti(x int8, y int8) {
	xpoložaj += int16(x)
	if xpoložaj < 0 {
		xpoložaj = 0
	}
	if xpoložaj >= 320 {
		xpoložaj = 320
	}

	ypoložaj -= int16(y)

	if ypoložaj < 0 {
		ypoložaj = 0
	}
	if ypoložaj >= 200 {
		ypoložaj = 200
	}

	mišwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišwidget.SkupBoja(0x00, 0x00, 0x00)
	mišwidget.Draw(&mišvga)

	mišwidget.Set_local_coordinates(uint32(xpoložaj), uint32(ypoložaj))
	mišwidget.SkupBoja(0x00, 0x00, 0xA8)
	mišwidget.Draw(&mišvga)

	previousx = xpoložaj
	previousy = ypoložaj

}
