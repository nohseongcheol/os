package джаджа

import . "vga"

type IДжаджа interface {
	Init(родител IДжаджа, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetФокус(джаджа IДжаджа)
	Set_local_coordinates(x int32, y int32)
	ЗадайЦвят(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоГрафикаМасив)
	Containscoordinate(x uint32, y uint32) bool
}

type TДжаджа struct {
	родител	IДжаджа
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (себеси *TДжаджа) Init(родител IДжаджа, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	себеси.родител = родител

	себеси.x = x
	себеси.y = y
	себеси.w = w
	себеси.h = h

	себеси.r = r
	себеси.g = g
	себеси.b = b

	себеси.Focussable = true

}
func (себеси *TДжаджа) GetФокус(джаджа IДжаджа) {
	if себеси.родител != nil {
		себеси.родител.GetФокус(джаджа)
	}
}
func (себеси *TДжаджа) Set_local_coordinates(x uint32, y uint32) {
	if себеси.родител != nil {

	}
	себеси.x = x
	себеси.y = y

}
func (себеси *TДжаджа) ЗадайЦвят(r uint32, g uint32, b uint32) {
	себеси.r = r
	себеси.g = g
	себеси.b = b
}

func (себеси *TДжаджа) Draw(vga *TВидеоГрафикаМасив) {
	vga.FillПравоъгълник(себеси.x, себеси.y, себеси.w, себеси.h, uint8(себеси.r), uint8(себеси.g), uint8(себеси.b))
}

func (себеси *TДжаджа) Containscoordinate(x uint32, y uint32) bool {
	return себеси.x <= x && x < (себеси.x+себеси.w) && себеси.y <= y && y < (себеси.y+себеси.h)
}

type TДжаджаМишкаСъбитиеhandler struct {
}

var мишкаДжаджа TДжаджа
var мишкаvga TВидеоГрафикаМасив
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (себеси *TДжаджаМишкаСъбитиеhandler) Init(джаджа TДжаджа, vga TВидеоГрафикаМасив) {
	мишкаДжаджа = джаджа
	мишкаvga = vga
}
func (себеси *TДжаджаМишкаСъбитиеhandler) ВклМишкаНадолу(бутон int8) {

	мишкаДжаджа.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишкаДжаджа.ЗадайЦвят(0xA8, 0x00, 0x00)
	мишкаДжаджа.Draw(&мишкаvga)

	мишкаДжаджа.Draw(&мишкаvga)

}

func (себеси *TДжаджаМишкаСъбитиеhandler) ВклМишкаНагоре(бутон int8) {
}

func (себеси *TДжаджаМишкаСъбитиеhandler) ВклМишкаПреместване(x int8, y int8) {
	xПозиция += int16(x)
	if xПозиция < 0 {
		xПозиция = 0
	}
	if xПозиция >= 320 {
		xПозиция = 320
	}

	yПозиция -= int16(y)

	if yПозиция < 0 {
		yПозиция = 0
	}
	if yПозиция >= 200 {
		yПозиция = 200
	}

	мишкаДжаджа.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишкаДжаджа.ЗадайЦвят(0x00, 0x00, 0x00)
	мишкаДжаджа.Draw(&мишкаvga)

	мишкаДжаджа.Set_local_coordinates(uint32(xПозиция), uint32(yПозиция))
	мишкаДжаджа.ЗадайЦвят(0x00, 0x00, 0xA8)
	мишкаДжаджа.Draw(&мишкаvga)

	previousx = xПозиция
	previousy = yПозиция

}
