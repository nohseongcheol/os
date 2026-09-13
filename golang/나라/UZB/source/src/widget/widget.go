package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
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
func (self *TWidget) Setcolor(r uint32, g uint32, b uint32) {
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

type TWidgetSichqonchaeventhandler struct {
}

var sichqonchawidget TWidget
var sichqonchavga TVideoGrafikaarray
var previousx int16 = 0
var previousy int16 = 0
var xHolati int16 = 0
var yHolati int16 = 0

func (self *TWidgetSichqonchaeventhandler) Init(widget TWidget, vga TVideoGrafikaarray) {
	sichqonchawidget = widget
	sichqonchavga = vga
}
func (self *TWidgetSichqonchaeventhandler) YoqishSichqonchaPastga(tugma int8) {

	sichqonchawidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	sichqonchawidget.Setcolor(0xA8, 0x00, 0x00)
	sichqonchawidget.Draw(&sichqonchavga)

	sichqonchawidget.Draw(&sichqonchavga)

}

func (self *TWidgetSichqonchaeventhandler) YoqishSichqonchaYuqoriga(tugma int8) {
}

func (self *TWidgetSichqonchaeventhandler) YoqishSichqonchaKoʻchirish(x int8, y int8) {
	xHolati += int16(x)
	if xHolati < 0 {
		xHolati = 0
	}
	if xHolati >= 320 {
		xHolati = 320
	}

	yHolati -= int16(y)

	if yHolati < 0 {
		yHolati = 0
	}
	if yHolati >= 200 {
		yHolati = 200
	}

	sichqonchawidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	sichqonchawidget.Setcolor(0x00, 0x00, 0x00)
	sichqonchawidget.Draw(&sichqonchavga)

	sichqonchawidget.Set_local_coordinates(uint32(xHolati), uint32(yHolati))
	sichqonchawidget.Setcolor(0x00, 0x00, 0xA8)
	sichqonchawidget.Draw(&sichqonchavga)

	previousx = xHolati
	previousy = yHolati

}
