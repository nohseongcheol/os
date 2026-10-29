/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package элемент_экрана

import . "vga"

type IЭлемент_экрана interface {
	Init(родитель IЭлемент_экрана, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetФокус(элемент_экрана IЭлемент_экрана)
	Задать_локальные_координаты(x int32, y int32)
	УказатьЦвет(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоГрафикамассив)
	Containscoordinate(x uint32, y uint32) bool
}

type TЭлемент_экрана struct {
	родитель	IЭлемент_экрана
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (текущий *TЭлемент_экрана) Init(родитель IЭлемент_экрана, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	текущий.родитель = родитель

	текущий.x = x
	текущий.y = y
	текущий.w = w
	текущий.h = h

	текущий.r = r
	текущий.g = g
	текущий.b = b

	текущий.Focussable = true

}
func (текущий *TЭлемент_экрана) GetФокус(элемент_экрана IЭлемент_экрана) {
	if текущий.родитель != nil {
		текущий.родитель.GetФокус(элемент_экрана)
	}
}
func (текущий *TЭлемент_экрана) Задать_локальные_координаты(x uint32, y uint32) {
	if текущий.родитель != nil {

	}
	текущий.x = x
	текущий.y = y

}
func (текущий *TЭлемент_экрана) УказатьЦвет(r uint32, g uint32, b uint32) {
	текущий.r = r
	текущий.g = g
	текущий.b = b
}

func (текущий *TЭлемент_экрана) Draw(vga *TВидеоГрафикамассив) {
	vga.FillПрямоугольник(текущий.x, текущий.y, текущий.w, текущий.h, uint8(текущий.r), uint8(текущий.g), uint8(текущий.b))
}

func (текущий *TЭлемент_экрана) Containscoordinate(x uint32, y uint32) bool {
	return текущий.x <= x && x < (текущий.x+текущий.w) && текущий.y <= y && y < (текущий.y+текущий.h)
}

type TЭлементмышьсобытиеhandler struct {
}

var мышьэлемент TЭлемент_экрана
var мышьvga TВидеоГрафикамассив
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (текущий *TЭлементмышьсобытиеhandler) Init(элемент_экрана TЭлемент_экрана, vga TВидеоГрафикамассив) {
	мышьэлемент = элемент_экрана
	мышьvga = vga
}
func (текущий *TЭлементмышьсобытиеhandler) ПримышьВниз(кнопка int8) {

	мышьэлемент.Задать_локальные_координаты(uint32(previousx), uint32(previousy))
	мышьэлемент.УказатьЦвет(0xA8, 0x00, 0x00)
	мышьэлемент.Draw(&мышьvga)

	мышьэлемент.Draw(&мышьvga)

}

func (текущий *TЭлементмышьсобытиеhandler) ПримышьВверх(кнопка int8) {
}

func (текущий *TЭлементмышьсобытиеhandler) ПримышьПереместить(x int8, y int8) {
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

	мышьэлемент.Задать_локальные_координаты(uint32(previousx), uint32(previousy))
	мышьэлемент.УказатьЦвет(0x00, 0x00, 0x00)
	мышьэлемент.Draw(&мышьvga)

	мышьэлемент.Задать_локальные_координаты(uint32(xПозиция), uint32(yПозиция))
	мышьэлемент.УказатьЦвет(0x00, 0x00, 0xA8)
	мышьэлемент.Draw(&мышьvga)

	previousx = xПозиция
	previousy = yПозиция

}
