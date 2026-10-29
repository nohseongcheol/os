/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package kontrola

import . "vga"

type IKontrola interface {
	Init(nadređeni IKontrola, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetЖижа(kontrola IKontrola)
	Set_local_coordinates(x int32, y int32)
	СкупБоја(r uint32, g uint32, b uint32)
	Draw(vga *TВидеоgrafikaНиз)
	Containscoordinate(x uint32, y uint32) bool
}

type TKontrola struct {
	nadređeni	IKontrola
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (isti *TKontrola) Init(nadređeni IKontrola, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	isti.nadređeni = nadređeni

	isti.x = x
	isti.y = y
	isti.w = w
	isti.h = h

	isti.r = r
	isti.g = g
	isti.b = b

	isti.Focussable = true

}
func (isti *TKontrola) GetЖижа(kontrola IKontrola) {
	if isti.nadređeni != nil {
		isti.nadređeni.GetЖижа(kontrola)
	}
}
func (isti *TKontrola) Set_local_coordinates(x uint32, y uint32) {
	if isti.nadređeni != nil {

	}
	isti.x = x
	isti.y = y

}
func (isti *TKontrola) СкупБоја(r uint32, g uint32, b uint32) {
	isti.r = r
	isti.g = g
	isti.b = b
}

func (isti *TKontrola) Draw(vga *TВидеоgrafikaНиз) {
	vga.FillPravougaonik(isti.x, isti.y, isti.w, isti.h, uint8(isti.r), uint8(isti.g), uint8(isti.b))
}

func (isti *TKontrola) Containscoordinate(x uint32, y uint32) bool {
	return isti.x <= x && x < (isti.x+isti.w) && isti.y <= y && y < (isti.y+isti.h)
}

type TKontrolaМишДогађајhandler struct {
}

var мишKontrola TKontrola
var мишvga TВидеоgrafikaНиз
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (isti *TKontrolaМишДогађајhandler) Init(kontrola TKontrola, vga TВидеоgrafikaНиз) {
	мишKontrola = kontrola
	мишvga = vga
}
func (isti *TKontrolaМишДогађајhandler) NaМишНиже(дугме int8) {

	мишKontrola.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишKontrola.СкупБоја(0xA8, 0x00, 0x00)
	мишKontrola.Draw(&мишvga)

	мишKontrola.Draw(&мишvga)

}

func (isti *TKontrolaМишДогађајhandler) NaМишGore(дугме int8) {
}

func (isti *TKontrolaМишДогађајhandler) NaМишПремести(x int8, y int8) {
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

	мишKontrola.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мишKontrola.СкупБоја(0x00, 0x00, 0x00)
	мишKontrola.Draw(&мишvga)

	мишKontrola.Set_local_coordinates(uint32(xПоложај), uint32(yПоложај))
	мишKontrola.СкупБоја(0x00, 0x00, 0xA8)
	мишKontrola.Draw(&мишvga)

	previousx = xПоложај
	previousy = yПоложај

}
