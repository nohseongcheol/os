package widget

import . "vga"

type IWidget interface {
	Init(roditelj IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	PostaviBoja(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikaNiz)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	roditelj	IWidget
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (sam *TWidget) Init(roditelj IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	sam.roditelj = roditelj

	sam.x = x
	sam.y = y
	sam.w = w
	sam.h = h

	sam.r = r
	sam.g = g
	sam.b = b

	sam.Focussable = true

}
func (sam *TWidget) GetFokus(widget IWidget) {
	if sam.roditelj != nil {
		sam.roditelj.GetFokus(widget)
	}
}
func (sam *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if sam.roditelj != nil {

	}
	sam.x = x
	sam.y = y

}
func (sam *TWidget) PostaviBoja(r uint32, g uint32, b uint32) {
	sam.r = r
	sam.g = g
	sam.b = b
}

func (sam *TWidget) Draw(vga *TVideoGrafikaNiz) {
	vga.Fillrectangle(sam.x, sam.y, sam.w, sam.h, uint8(sam.r), uint8(sam.g), uint8(sam.b))
}

func (sam *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return sam.x <= x && x < (sam.x+sam.w) && sam.y <= y && y < (sam.y+sam.h)
}

type TWidgetMišDogađajhandler struct {
}

var mišwidget TWidget
var mišvga TVideoGrafikaNiz
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (sam *TWidgetMišDogađajhandler) Init(widget TWidget, vga TVideoGrafikaNiz) {
	mišwidget = widget
	mišvga = vga
}
func (sam *TWidgetMišDogađajhandler) UključenoMišDolje(dugme int8) {

	mišwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišwidget.PostaviBoja(0xA8, 0x00, 0x00)
	mišwidget.Draw(&mišvga)

	mišwidget.Draw(&mišvga)

}

func (sam *TWidgetMišDogađajhandler) UključenoMišGore(dugme int8) {
}

func (sam *TWidgetMišDogađajhandler) UključenoMišPremjesti(x int8, y int8) {
	xPozicija += int16(x)
	if xPozicija < 0 {
		xPozicija = 0
	}
	if xPozicija >= 320 {
		xPozicija = 320
	}

	yPozicija -= int16(y)

	if yPozicija < 0 {
		yPozicija = 0
	}
	if yPozicija >= 200 {
		yPozicija = 200
	}

	mišwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišwidget.PostaviBoja(0x00, 0x00, 0x00)
	mišwidget.Draw(&mišvga)

	mišwidget.Set_local_coordinates(uint32(xPozicija), uint32(yPozicija))
	mišwidget.PostaviBoja(0x00, 0x00, 0xA8)
	mišwidget.Draw(&mišvga)

	previousx = xPozicija
	previousy = yPozicija

}
