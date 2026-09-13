package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	SetLitur(r uint32, g uint32, b uint32)
	Draw(vga *TVideographicsarray)
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
func (self *TWidget) SetLitur(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *TVideographicsarray) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetMúseventhandler struct {
}

var múswidget TWidget
var músvga TVideographicsarray
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TWidgetMúseventhandler) Init(widget TWidget, vga TVideographicsarray) {
	múswidget = widget
	músvga = vga
}
func (self *TWidgetMúseventhandler) OnMúsdown(knappur int8) {

	múswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	múswidget.SetLitur(0xA8, 0x00, 0x00)
	múswidget.Draw(&músvga)

	múswidget.Draw(&músvga)

}

func (self *TWidgetMúseventhandler) OnMúsup(knappur int8) {
}

func (self *TWidgetMúseventhandler) OnMúsmove(x int8, y int8) {
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

	múswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	múswidget.SetLitur(0x00, 0x00, 0x00)
	múswidget.Draw(&músvga)

	múswidget.Set_local_coordinates(uint32(xposition), uint32(yposition))
	múswidget.SetLitur(0x00, 0x00, 0xA8)
	múswidget.Draw(&músvga)

	previousx = xposition
	previousy = yposition

}
