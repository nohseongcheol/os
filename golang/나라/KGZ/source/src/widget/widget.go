package widget

import . "vga"

type IWidget interface {
	Init(атаэне IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Setcolor(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоГрафикаМассив)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	атаэне	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TWidget) Init(атаэне IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.атаэне = атаэне

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
	if self.атаэне != nil {
		self.атаэне.Getfocus(widget)
	}
}
func (self *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if self.атаэне != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) Setcolor(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *TВидеоГрафикаМассив) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetЧычканeventhandler struct {
}

var чычканwidget TWidget
var чычканvga TВидеоГрафикаМассив
var previousx int16 = 0
var previousy int16 = 0
var xТурганжери int16 = 0
var yТурганжери int16 = 0

func (self *TWidgetЧычканeventhandler) Init(widget TWidget, vga TВидеоГрафикаМассив) {
	чычканwidget = widget
	чычканvga = vga
}
func (self *TWidgetЧычканeventhandler) OnЧычканdown(button int8) {

	чычканwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	чычканwidget.Setcolor(0xA8, 0x00, 0x00)
	чычканwidget.Draw(&чычканvga)

	чычканwidget.Draw(&чычканvga)

}

func (self *TWidgetЧычканeventhandler) OnЧычканӨйдө(button int8) {
}

func (self *TWidgetЧычканeventhandler) OnЧычканТашуу(x int8, y int8) {
	xТурганжери += int16(x)
	if xТурганжери < 0 {
		xТурганжери = 0
	}
	if xТурганжери >= 320 {
		xТурганжери = 320
	}

	yТурганжери -= int16(y)

	if yТурганжери < 0 {
		yТурганжери = 0
	}
	if yТурганжери >= 200 {
		yТурганжери = 200
	}

	чычканwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	чычканwidget.Setcolor(0x00, 0x00, 0x00)
	чычканwidget.Draw(&чычканvga)

	чычканwidget.Set_local_coordinates(uint32(xТурганжери), uint32(yТурганжери))
	чычканwidget.Setcolor(0x00, 0x00, 0xA8)
	чычканwidget.Draw(&чычканvga)

	previousx = xТурганжери
	previousy = yТурганжери

}
