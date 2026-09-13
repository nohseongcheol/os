package widget

import . "vga"

type IWidget interface {
	Init(ወላጅ IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
	Draw(vga *Tቪዲዮንድፎችማዘጋጃ)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	ወላጅ	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TWidget) Init(ወላጅ IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.ወላጅ = ወላጅ

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
	if self.ወላጅ != nil {
		self.ወላጅ.Getfocus(widget)
	}
}
func (self *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if self.ወላጅ != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) Setcolor(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *Tቪዲዮንድፎችማዘጋጃ) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetአይጥeventhandler struct {
}

var አይጥwidget TWidget
var አይጥvga Tቪዲዮንድፎችማዘጋጃ
var previousx int16 = 0
var previousy int16 = 0
var xአካባቢ int16 = 0
var yአካባቢ int16 = 0

func (self *TWidgetአይጥeventhandler) Init(widget TWidget, vga Tቪዲዮንድፎችማዘጋጃ) {
	አይጥwidget = widget
	አይጥvga = vga
}
func (self *TWidgetአይጥeventhandler) Oማብሪያአይጥወደታች(button int8) {

	አይጥwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	አይጥwidget.Setcolor(0xA8, 0x00, 0x00)
	አይጥwidget.Draw(&አይጥvga)

	አይጥwidget.Draw(&አይጥvga)

}

func (self *TWidgetአይጥeventhandler) Oማብሪያአይጥወደላይ(button int8) {
}

func (self *TWidgetአይጥeventhandler) Oማብሪያአይጥመንቀሳቅስ(x int8, y int8) {
	xአካባቢ += int16(x)
	if xአካባቢ < 0 {
		xአካባቢ = 0
	}
	if xአካባቢ >= 320 {
		xአካባቢ = 320
	}

	yአካባቢ -= int16(y)

	if yአካባቢ < 0 {
		yአካባቢ = 0
	}
	if yአካባቢ >= 200 {
		yአካባቢ = 200
	}

	አይጥwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	አይጥwidget.Setcolor(0x00, 0x00, 0x00)
	አይጥwidget.Draw(&አይጥvga)

	አይጥwidget.Set_local_coordinates(uint32(xአካባቢ), uint32(yአካባቢ))
	አይጥwidget.Setcolor(0x00, 0x00, 0xA8)
	አይጥwidget.Draw(&አይጥvga)

	previousx = xአካባቢ
	previousy = yአካባቢ

}
