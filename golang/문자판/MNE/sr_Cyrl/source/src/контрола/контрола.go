/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package контрола

import . "vga"

type IКонтрола interface {
	Init(надређени IКонтрола, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetЖижа(контрола IКонтрола)
	Set_local_coordinates(x int32, y int32)
	СкупБоја(r uint32, g uint32, b uint32)
	Draw(vga *TВидеографикаНиз)
	Containscoordinate(x uint32, y uint32) bool
}

type TКонтрола struct {
	надређени	IКонтрола
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (исти *TКонтрола) Init(надређени IКонтрола, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	исти.надређени = надређени

	исти.x = x
	исти.y = y
	исти.w = w
	исти.h = h

	исти.r = r
	исти.g = g
	исти.b = b

	исти.Focussable = true

}
func (исти *TКонтрола) GetЖижа(контрола IКонтрола) {
	if исти.надређени != nil {
		исти.надређени.GetЖижа(контрола)
	}
}
func (исти *TКонтрола) Set_local_coordinates(x uint32, y uint32) {
	if исти.надређени != nil {

	}
	исти.x = x
	исти.y = y

}
func (исти *TКонтрола) СкупБоја(r uint32, g uint32, b uint32) {
	исти.r = r
	исти.g = g
	исти.b = b
}

func (исти *TКонтрола) Draw(vga *TВидеографикаНиз) {
	vga.FillПравоугаоник(исти.x, исти.y, исти.w, исти.h, uint8(исти.r), uint8(исти.g), uint8(исти.b))
}

func (исти *TКонтрола) Containscoordinate(x uint32, y uint32) bool {
	return исти.x <= x && x < (исти.x+исти.w) && исти.y <= y && y < (исти.y+исти.h)
}

type TКонтролаМишДогађајhandler struct {
}

var мишКонтрола TКонтрола
var мишvga TВидеографикаНиз
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (исти *TКонтролаМишДогађајhandler) Init(контрола TКонтрола, vga TВидеографикаНиз) {
	мишКонтрола = контрола
	мишvga = vga
}
func (исти *TКонтролаМишДогађајhandler) НаМишНиже(дугме int8) {

	мишКонтрола.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишКонтрола.СкупБоја(0xA8, 0x00, 0x00)
	мишКонтрола.Draw(&мишvga)

	мишКонтрола.Draw(&мишvga)

}

func (исти *TКонтролаМишДогађајhandler) НаМишГоре(дугме int8) {
}

func (исти *TКонтролаМишДогађајhandler) НаМишПремести(x int8, y int8) {
	xПоложај += int16(x)
	if xПоложај < 0 {
		xПоложај = 0
	}
	if xПоложај >= 320 {
		xПоложај = 320
	}

	yПоложај -= int16(y)

	if yПоложај < 0 {
		yПоложај = 0
	}
	if yПоложај >= 200 {
		yПоложај = 200
	}

	мишКонтрола.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишКонтрола.СкупБоја(0x00, 0x00, 0x00)
	мишКонтрола.Draw(&мишvga)

	мишКонтрола.Set_local_coordinates(uint32(xПоложај), uint32(yПоложај))
	мишКонтрола.СкупБоја(0x00, 0x00, 0xA8)
	мишКонтрола.Draw(&мишvga)

	previousx = xПоложај
	previousy = yПоложај

}
