package widget

import . "vga"

type IWidget interface {
	Vआरंभ_करना(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFocus(widget IWidget)
	Vस्थानीय_निर्देशांक_रखना(x int32, y int32)
	SetColor(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGraphicsArray)
	ContainsCoordinate(x uint32, y uint32) bool
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

func (self *TWidget) Vआरंभ_करना(parent IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *TWidget) GetFocus(widget IWidget) {
	if self.parent != nil {
		self.parent.GetFocus(widget)
	}
}
func (self *TWidget) Vस्थानीय_निर्देशांक_रखना(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TWidget) SetColor(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TWidget) Draw(vga *TVideoGraphicsArray) {
	vga.FillRectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TWidget) ContainsCoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetMouseEventHandler struct {
}

var mouseWidget TWidget
var mouseVGA TVideoGraphicsArray
var prevX int16 = 0
var prevY int16 = 0
var xPos int16 = 0
var yPos int16 = 0

func (self *TWidgetMouseEventHandler) Vआरंभ_करना(widget TWidget, vga TVideoGraphicsArray) {
	mouseWidget = widget
	mouseVGA = vga
}
func (self *TWidgetMouseEventHandler) OnMouseDown(button int8) {

	mouseWidget.Vस्थानीय_निर्देशांक_रखना(uint32(prevX), uint32(prevY))
	mouseWidget.SetColor(0xA8, 0x00, 0x00)
	mouseWidget.Draw(&mouseVGA)

	mouseWidget.Draw(&mouseVGA)

}

func (self *TWidgetMouseEventHandler) OnMouseUp(button int8) {
}

func (self *TWidgetMouseEventHandler) OnMouseMove(x int8, y int8) {
	xPos += int16(x)
	if xPos < 0 {
		xPos = 0
	}
	if xPos >= 320 {
		xPos = 320
	}

	yPos -= int16(y)

	if yPos < 0 {
		yPos = 0
	}
	if yPos >= 200 {
		yPos = 200
	}

	mouseWidget.Vस्थानीय_निर्देशांक_रखना(uint32(prevX), uint32(prevY))
	mouseWidget.SetColor(0x00, 0x00, 0x00)
	mouseWidget.Draw(&mouseVGA)

	mouseWidget.Vस्थानीय_निर्देशांक_रखना(uint32(xPos), uint32(yPos))
	mouseWidget.SetColor(0x00, 0x00, 0xA8)
	mouseWidget.Draw(&mouseVGA)

	prevX = xPos
	prevY = yPos

}
