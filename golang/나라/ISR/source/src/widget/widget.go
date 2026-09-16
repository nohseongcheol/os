/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getמיקוד(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Sקבעצבע(r uint32, g uint32, b uint32)
	Draw(vga *Tוידאוגרפיקהמערך)
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
func (self *TWidget) Getמיקוד(widget IWidget) {
	if self.parent != nil {
		self.parent.Getמיקוד(widget)
	}
}
func (self *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) Sקבעצבע(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *Tוידאוגרפיקהמערך) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetעכברeventhandler struct {
}

var עכברwidget TWidget
var עכברvga Tוידאוגרפיקהמערך
var previousx int16 = 0
var previousy int16 = 0
var xמיקום int16 = 0
var yמיקום int16 = 0

func (self *TWidgetעכברeventhandler) Init(widget TWidget, vga Tוידאוגרפיקהמערך) {
	עכברwidget = widget
	עכברvga = vga
}
func (self *TWidgetעכברeventhandler) Oפעילעכברלמטה(לחצן int8) {

	עכברwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	עכברwidget.Sקבעצבע(0xA8, 0x00, 0x00)
	עכברwidget.Draw(&עכברvga)

	עכברwidget.Draw(&עכברvga)

}

func (self *TWidgetעכברeventhandler) Oפעילעכברמעלה(לחצן int8) {
}

func (self *TWidgetעכברeventhandler) Oפעילעכברהזז(x int8, y int8) {
	xמיקום += int16(x)
	if xמיקום < 0 {
		xמיקום = 0
	}
	if xמיקום >= 320 {
		xמיקום = 320
	}

	yמיקום -= int16(y)

	if yמיקום < 0 {
		yמיקום = 0
	}
	if yמיקום >= 200 {
		yמיקום = 200
	}

	עכברwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	עכברwidget.Sקבעצבע(0x00, 0x00, 0x00)
	עכברwidget.Draw(&עכברvga)

	עכברwidget.Set_local_coordinates(uint32(xמיקום), uint32(yמיקום))
	עכברwidget.Sקבעצבע(0x00, 0x00, 0xA8)
	עכברwidget.Draw(&עכברvga)

	previousx = xמיקום
	previousy = yמיקום

}
