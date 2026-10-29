/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package element_ekranu

import . "vga"

type IElement_ekranu interface {
	Init(rodzic IElement_ekranu, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetUaktywnianie(element_ekranu IElement_ekranu)
	Ustaw_współrzędne_lokalne(x int32, y int32)
	ZbiórKolor(r uint32, g uint32, b uint32)
	Draw(vga *TWideoGrafikaTablica)
	Containscoordinate(x uint32, y uint32) bool
}

type TElement_ekranu struct {
	rodzic	IElement_ekranu
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (bieżący *TElement_ekranu) Init(rodzic IElement_ekranu, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	bieżący.rodzic = rodzic

	bieżący.x = x
	bieżący.y = y
	bieżący.w = w
	bieżący.h = h

	bieżący.r = r
	bieżący.g = g
	bieżący.b = b

	bieżący.Focussable = true

}
func (bieżący *TElement_ekranu) GetUaktywnianie(element_ekranu IElement_ekranu) {
	if bieżący.rodzic != nil {
		bieżący.rodzic.GetUaktywnianie(element_ekranu)
	}
}
func (bieżący *TElement_ekranu) Ustaw_współrzędne_lokalne(x uint32, y uint32) {
	if bieżący.rodzic != nil {

	}
	bieżący.x = x
	bieżący.y = y

}
func (bieżący *TElement_ekranu) ZbiórKolor(r uint32, g uint32, b uint32) {
	bieżący.r = r
	bieżący.g = g
	bieżący.b = b
}

func (bieżący *TElement_ekranu) Draw(vga *TWideoGrafikaTablica) {
	vga.FillProstokąt(bieżący.x, bieżący.y, bieżący.w, bieżący.h, uint8(bieżący.r), uint8(bieżący.g), uint8(bieżący.b))
}

func (bieżący *TElement_ekranu) Containscoordinate(x uint32, y uint32) bool {
	return bieżący.x <= x && x < (bieżący.x+bieżący.w) && bieżący.y <= y && y < (bieżący.y+bieżący.h)
}

type TWidżetyMyszWydarzeniehandler struct {
}

var myszWidżety TElement_ekranu
var myszvga TWideoGrafikaTablica
var previousx int16 = 0
var previousy int16 = 0
var xPozycja int16 = 0
var yPozycja int16 = 0

func (bieżący *TWidżetyMyszWydarzeniehandler) Init(element_ekranu TElement_ekranu, vga TWideoGrafikaTablica) {
	myszWidżety = element_ekranu
	myszvga = vga
}
func (bieżący *TWidżetyMyszWydarzeniehandler) WłączMyszWdół(przycisk int8) {

	myszWidżety.Ustaw_współrzędne_lokalne(uint32(previousx), uint32(previousy))
	myszWidżety.ZbiórKolor(0xA8, 0x00, 0x00)
	myszWidżety.Draw(&myszvga)

	myszWidżety.Draw(&myszvga)

}

func (bieżący *TWidżetyMyszWydarzeniehandler) WłączMyszGóra(przycisk int8) {
}

func (bieżący *TWidżetyMyszWydarzeniehandler) WłączMyszPrzenoszenie(x int8, y int8) {
	xPozycja += int16(x)
	if xPozycja < 0 {
		xPozycja = 0
	}
	if xPozycja >= 320 {
		xPozycja = 320
	}

	yPozycja -= int16(y)

	if yPozycja < 0 {
		yPozycja = 0
	}
	if yPozycja >= 200 {
		yPozycja = 200
	}

	myszWidżety.Ustaw_współrzędne_lokalne(uint32(previousx), uint32(previousy))
	myszWidżety.ZbiórKolor(0x00, 0x00, 0x00)
	myszWidżety.Draw(&myszvga)

	myszWidżety.Ustaw_współrzędne_lokalne(uint32(xPozycja), uint32(yPozycja))
	myszWidżety.ZbiórKolor(0x00, 0x00, 0xA8)
	myszWidżety.Draw(&myszvga)

	previousx = xPozycja
	previousy = yPozycja

}
