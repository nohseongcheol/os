package screen_element

import . "vga"

type IScreen_element interface {
	Init(parent IScreen_element, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(screen_element IScreen_element)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
	Draw(vga *TVideographicsarray)
	Containscoordinate(x uint32, y uint32) bool
}

type TScreen_element struct {
	parent	IScreen_element
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TScreen_element) Init(parent IScreen_element, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *TScreen_element) Getfocus(screen_element IScreen_element) {
	if self.parent != nil {
		self.parent.Getfocus(screen_element)
	}
}
func (self *TScreen_element) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TScreen_element) Setcolor(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TScreen_element) Draw(vga *TVideographicsarray) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TScreen_element) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetmouseeventhandler struct {
}

var mousewidget TScreen_element
var mousevga TVideographicsarray
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TWidgetmouseeventhandler) Init(screen_element TScreen_element, vga TVideographicsarray) {
	mousewidget = screen_element
	mousevga = vga
}
func (self *TWidgetmouseeventhandler) Onmousedown(button int8) {

	mousewidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mousewidget.Setcolor(0xA8, 0x00, 0x00)
	mousewidget.Draw(&mousevga)

	mousewidget.Draw(&mousevga)

}

func (self *TWidgetmouseeventhandler) Onmouseup(button int8) {
}

func (self *TWidgetmouseeventhandler) Onmousemove(x int8, y int8) {
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

	mousewidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mousewidget.Setcolor(0x00, 0x00, 0x00)
	mousewidget.Draw(&mousevga)

	mousewidget.Set_local_coordinates(uint32(xposition), uint32(yposition))
	mousewidget.Setcolor(0x00, 0x00, 0xA8)
	mousewidget.Draw(&mousevga)

	previousx = xposition
	previousy = yposition

}
