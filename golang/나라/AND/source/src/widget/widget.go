/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(pare IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetEnfocament(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	Estableixcolor(r uint32, g uint32, b uint32)
	Draw(vga *TVídeoGràficsMatriu)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	pare	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (unmateix *TWidget) Init(pare IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	unmateix.pare = pare

	unmateix.x = x
	unmateix.y = y
	unmateix.w = w
	unmateix.h = h

	unmateix.r = r
	unmateix.g = g
	unmateix.b = b

	unmateix.Focussable = true

}
func (unmateix *TWidget) GetEnfocament(widget IWidget) {
	if unmateix.pare != nil {
		unmateix.pare.GetEnfocament(widget)
	}
}
func (unmateix *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if unmateix.pare != nil {

	}
	unmateix.x = x
	unmateix.y = y

}
func (unmateix *TWidget) Estableixcolor(r uint32, g uint32, b uint32) {
	unmateix.r = r
	unmateix.g = g
	unmateix.b = b
}

func (unmateix *TWidget) Draw(vga *TVídeoGràficsMatriu) {
	vga.Fillrectangle(unmateix.x, unmateix.y, unmateix.w, unmateix.h, uint8(unmateix.r), uint8(unmateix.g), uint8(unmateix.b))
}

func (unmateix *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return unmateix.x <= x && x < (unmateix.x+unmateix.w) && unmateix.y <= y && y < (unmateix.y+unmateix.h)
}

type TWidgetRatolíEsdevenimenthandler struct {
}

var ratolíwidget TWidget
var ratolívga TVídeoGràficsMatriu
var previousx int16 = 0
var previousy int16 = 0
var xPosició int16 = 0
var yPosició int16 = 0

func (unmateix *TWidgetRatolíEsdevenimenthandler) Init(widget TWidget, vga TVídeoGràficsMatriu) {
	ratolíwidget = widget
	ratolívga = vga
}
func (unmateix *TWidgetRatolíEsdevenimenthandler) EngegatRatolíAvall(botó int8) {

	ratolíwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ratolíwidget.Estableixcolor(0xA8, 0x00, 0x00)
	ratolíwidget.Draw(&ratolívga)

	ratolíwidget.Draw(&ratolívga)

}

func (unmateix *TWidgetRatolíEsdevenimenthandler) EngegatRatolíAmunt(botó int8) {
}

func (unmateix *TWidgetRatolíEsdevenimenthandler) EngegatRatolíMou(x int8, y int8) {
	xPosició += int16(x)
	if xPosició < 0 {
		xPosició = 0
	}
	if xPosició >= 320 {
		xPosició = 320
	}

	yPosició -= int16(y)

	if yPosició < 0 {
		yPosició = 0
	}
	if yPosició >= 200 {
		yPosició = 200
	}

	ratolíwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ratolíwidget.Estableixcolor(0x00, 0x00, 0x00)
	ratolíwidget.Draw(&ratolívga)

	ratolíwidget.Set_local_coordinates(uint32(xPosició), uint32(yPosició))
	ratolíwidget.Estableixcolor(0x00, 0x00, 0xA8)
	ratolíwidget.Draw(&ratolívga)

	previousx = xPosició
	previousy = yPosició

}
