/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package widget

import . "vga"

type IWidget interface {
	Init(rodič IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetZameranie(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	SadaFarba(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikaPole)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	rodič	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (vlastný *TWidget) Init(rodič IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	vlastný.rodič = rodič

	vlastný.x = x
	vlastný.y = y
	vlastný.w = w
	vlastný.h = h

	vlastný.r = r
	vlastný.g = g
	vlastný.b = b

	vlastný.Focussable = true

}
func (vlastný *TWidget) GetZameranie(widget IWidget) {
	if vlastný.rodič != nil {
		vlastný.rodič.GetZameranie(widget)
	}
}
func (vlastný *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if vlastný.rodič != nil {

	}
	vlastný.x = x
	vlastný.y = y

}
func (vlastný *TWidget) SadaFarba(r uint32, g uint32, b uint32) {
	vlastný.r = r
	vlastný.g = g
	vlastný.b = b
}

func (vlastný *TWidget) Draw(vga *TVideoGrafikaPole) {
	vga.Fillrectangle(vlastný.x, vlastný.y, vlastný.w, vlastný.h, uint8(vlastný.r), uint8(vlastný.g), uint8(vlastný.b))
}

func (vlastný *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return vlastný.x <= x && x < (vlastný.x+vlastný.w) && vlastný.y <= y && y < (vlastný.y+vlastný.h)
}

type TWidgetMyšUdalosťhandler struct {
}

var myšwidget TWidget
var myšvga TVideoGrafikaPole
var previousx int16 = 0
var previousy int16 = 0
var xPozícia int16 = 0
var yPozícia int16 = 0

func (vlastný *TWidgetMyšUdalosťhandler) Init(widget TWidget, vga TVideoGrafikaPole) {
	myšwidget = widget
	myšvga = vga
}
func (vlastný *TWidgetMyšUdalosťhandler) ZapnutéMyšDole(tlačidlo int8) {

	myšwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	myšwidget.SadaFarba(0xA8, 0x00, 0x00)
	myšwidget.Draw(&myšvga)

	myšwidget.Draw(&myšvga)

}

func (vlastný *TWidgetMyšUdalosťhandler) ZapnutéMyšHore(tlačidlo int8) {
}

func (vlastný *TWidgetMyšUdalosťhandler) ZapnutéMyšPresunúť(x int8, y int8) {
	xPozícia += int16(x)
	if xPozícia < 0 {
		xPozícia = 0
	}
	if xPozícia >= 320 {
		xPozícia = 320
	}

	yPozícia -= int16(y)

	if yPozícia < 0 {
		yPozícia = 0
	}
	if yPozícia >= 200 {
		yPozícia = 200
	}

	myšwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	myšwidget.SadaFarba(0x00, 0x00, 0x00)
	myšwidget.Draw(&myšvga)

	myšwidget.Set_local_coordinates(uint32(xPozícia), uint32(yPozícia))
	myšwidget.SadaFarba(0x00, 0x00, 0xA8)
	myšwidget.Draw(&myšvga)

	previousx = xPozícia
	previousy = yPozícia

}
