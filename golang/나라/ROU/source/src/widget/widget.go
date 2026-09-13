package widget

import . "vga"

type IWidget interface {
	Init(părinte IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(widget IWidget)
	Set_local_coordinates(x int32, y int32)
	DefinitCuloare(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGraficăVector)
	Containscoordinate(x uint32, y uint32) bool
}

type TWidget struct {
	părinte	IWidget
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (sine *TWidget) Init(părinte IWidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	sine.părinte = părinte

	sine.x = x
	sine.y = y
	sine.w = w
	sine.h = h

	sine.r = r
	sine.g = g
	sine.b = b

	sine.Focussable = true

}
func (sine *TWidget) Getfocus(widget IWidget) {
	if sine.părinte != nil {
		sine.părinte.Getfocus(widget)
	}
}
func (sine *TWidget) Set_local_coordinates(x uint32, y uint32) {
	if sine.părinte != nil {

	}
	sine.x = x
	sine.y = y

}
func (sine *TWidget) DefinitCuloare(r uint32, g uint32, b uint32) {
	sine.r = r
	sine.g = g
	sine.b = b
}

func (sine *TWidget) Draw(vga *TVideoGraficăVector) {
	vga.FillDreptunghi(sine.x, sine.y, sine.w, sine.h, uint8(sine.r), uint8(sine.g), uint8(sine.b))
}

func (sine *TWidget) Containscoordinate(x uint32, y uint32) bool {
	return sine.x <= x && x < (sine.x+sine.w) && sine.y <= y && y < (sine.y+sine.h)
}

type TWidgetMausEvenimenthandler struct {
}

var mauswidget TWidget
var mausvga TVideoGraficăVector
var previousx int16 = 0
var previousy int16 = 0
var xPoziție int16 = 0
var yPoziție int16 = 0

func (sine *TWidgetMausEvenimenthandler) Init(widget TWidget, vga TVideoGraficăVector) {
	mauswidget = widget
	mausvga = vga
}
func (sine *TWidgetMausEvenimenthandler) PornitMausÎnjos(buton int8) {

	mauswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mauswidget.DefinitCuloare(0xA8, 0x00, 0x00)
	mauswidget.Draw(&mausvga)

	mauswidget.Draw(&mausvga)

}

func (sine *TWidgetMausEvenimenthandler) PornitMausSus(buton int8) {
}

func (sine *TWidgetMausEvenimenthandler) PornitMausMutare(x int8, y int8) {
	xPoziție += int16(x)
	if xPoziție < 0 {
		xPoziție = 0
	}
	if xPoziție >= 320 {
		xPoziție = 320
	}

	yPoziție -= int16(y)

	if yPoziție < 0 {
		yPoziție = 0
	}
	if yPoziție >= 200 {
		yPoziție = 200
	}

	mauswidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mauswidget.DefinitCuloare(0x00, 0x00, 0x00)
	mauswidget.Draw(&mausvga)

	mauswidget.Set_local_coordinates(uint32(xPoziție), uint32(yPoziție))
	mauswidget.DefinitCuloare(0x00, 0x00, 0xA8)
	mauswidget.Draw(&mausvga)

	previousx = xPoziție
	previousy = yPoziție

}
