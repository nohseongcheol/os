package widget

import . "vga"

type IWidget interface {
	Init(prind IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	CaktoniNgjyra(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikëRreshtimi)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	prind	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (vetvetja *TWidget) Init(prind IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	vetvetja.prind = prind

	vetvetja.x = x
	vetvetja.y = y
	vetvetja.w = w
	vetvetja.h = h

	vetvetja.r = r
	vetvetja.g = g
	vetvetja.b = b

	vetvetja.Focussable = true

}
func (vetvetja *TWidget) GetFokus(widget IWidget) {
	if vetvetja.prind != nil {
		vetvetja.prind.GetFokus(widget)
	}
}
func (vetvetja *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if vetvetja.prind != nil {

	}
	vetvetja.x = x
	vetvetja.y = y

}
func (vetvetja *TWidget) CaktoniNgjyra(r uint32, g uint32, b uint32) {
	vetvetja.r = r
	vetvetja.g = g
	vetvetja.b = b
}

func (vetvetja *TWidget) Draw(vga *TVideoGrafikëRreshtimi) {
	vga.FillDrejtkëndësh(vetvetja.x, vetvetja.y, vetvetja.w, vetvetja.h, uint8(vetvetja.r), uint8(vetvetja.g), uint8(vetvetja.b))
}

func (vetvetja *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return vetvetja.x <= x && x < (vetvetja.x+vetvetja.w) && vetvetja.y <= y && y < (vetvetja.y+vetvetja.h)
}

type TWidgetMiuNgjarjehandler struct {
}

var miuwidget TWidget
var miuvga TVideoGrafikëRreshtimi
var previousx int16 = 0
var previousy int16 = 0
var xPozicion int16 = 0
var yPozicion int16 = 0

func (vetvetja *TWidgetMiuNgjarjehandler) Init(widget TWidget, vga TVideoGrafikëRreshtimi) {
	miuwidget = widget
	miuvga = vga
}
func (vetvetja *TWidgetMiuNgjarjehandler) OnMiuPoshtë(buton int8) {

	miuwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	miuwidget.CaktoniNgjyra(0xA8, 0x00, 0x00)
	miuwidget.Draw(&miuvga)

	miuwidget.Draw(&miuvga)

}

func (vetvetja *TWidgetMiuNgjarjehandler) OnMiuSipër(buton int8) {
}

func (vetvetja *TWidgetMiuNgjarjehandler) OnMiuLëviz(x int8, y int8) {
	xPozicion += int16(x)
	if xPozicion < 0 {
		xPozicion = 0
	}
	if xPozicion >= 320 {
		xPozicion = 320
	}

	yPozicion -= int16(y)

	if yPozicion < 0 {
		yPozicion = 0
	}
	if yPozicion >= 200 {
		yPozicion = 200
	}

	miuwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	miuwidget.CaktoniNgjyra(0x00, 0x00, 0x00)
	miuwidget.Draw(&miuvga)

	miuwidget.Set_local_coordinates(uint32(xPozicion), uint32(yPozicion))
	miuwidget.CaktoniNgjyra(0x00, 0x00, 0xA8)
	miuwidget.Draw(&miuvga)

	previousx = xPozicion
	previousy = yPozicion

}
