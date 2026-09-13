package widget

import . "vga"

type IWidget interface {
	Init(آبائی IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getفوکس(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Sسیٹرنگ(r uint32, g uint32, b uint32)
	Draw(vga *Tویڈیوترسیمیاتلڑی)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	آبائی	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TWidget) Init(آبائی IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.آبائی = آبائی

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TWidget) Getفوکس(widget IWidget) {
	if self.آبائی != nil {
		self.آبائی.Getفوکس(widget)
	}
}
func (self *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if self.آبائی != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) Sسیٹرنگ(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *Tویڈیوترسیمیاتلڑی) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetماؤسواقعہhandler struct {
}

var ماؤسwidget TWidget
var ماؤسvga Tویڈیوترسیمیاتلڑی
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TWidgetماؤسواقعہhandler) Init(widget TWidget, vga Tویڈیوترسیمیاتلڑی) {
	ماؤسwidget = widget
	ماؤسvga = vga
}
func (self *TWidgetماؤسواقعہhandler) Oچالوماؤسنیچے(بٹن int8) {

	ماؤسwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ماؤسwidget.Sسیٹرنگ(0xA8, 0x00, 0x00)
	ماؤسwidget.Draw(&ماؤسvga)

	ماؤسwidget.Draw(&ماؤسvga)

}

func (self *TWidgetماؤسواقعہhandler) Oچالوماؤساوپر(بٹن int8) {
}

func (self *TWidgetماؤسواقعہhandler) Oچالوماؤسمنتقلکریں(x int8, y int8) {
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

	ماؤسwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ماؤسwidget.Sسیٹرنگ(0x00, 0x00, 0x00)
	ماؤسwidget.Draw(&ماؤسvga)

	ماؤسwidget.Set_local_coordinates(uint32(xposition), uint32(yposition))
	ماؤسwidget.Sسیٹرنگ(0x00, 0x00, 0xA8)
	ماؤسwidget.Draw(&ماؤسvga)

	previousx = xposition
	previousy = yposition

}
