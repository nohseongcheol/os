/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ekran_öğesi

import . "vga"

type IEkran_öğesi interface {
	Init(üst IEkran_öğesi, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetOdak(ekran_öğesi IEkran_öğesi)
	Yerel_koordinatları_ayarla(x int32, y int32)
	AyarlaRenk(r uint32, g uint32, b uint32)
	Draw(vga *TGörüntüGrafiklerDizi)
	Containscoordinate(x uint32, y uint32) bool
}

type TEkran_öğesi struct {
	üst	IEkran_öğesi
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TEkran_öğesi) Init(üst IEkran_öğesi, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.üst = üst

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TEkran_öğesi) GetOdak(ekran_öğesi IEkran_öğesi) {
	if self.üst != nil {
		self.üst.GetOdak(ekran_öğesi)
	}
}
func (self *TEkran_öğesi) Yerel_koordinatları_ayarla(x uint32, y uint32) {
	if self.üst != nil {

	}
	self.x = x
	self.y = y

}
func (self *TEkran_öğesi) AyarlaRenk(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TEkran_öğesi) Draw(vga *TGörüntüGrafiklerDizi) {
	vga.FillDikdörtgen(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TEkran_öğesi) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TGereçFareOlayhandler struct {
}

var fareGereç TEkran_öğesi
var farevga TGörüntüGrafiklerDizi
var previousx int16 = 0
var previousy int16 = 0
var xKonum int16 = 0
var yKonum int16 = 0

func (self *TGereçFareOlayhandler) Init(ekran_öğesi TEkran_öğesi, vga TGörüntüGrafiklerDizi) {
	fareGereç = ekran_öğesi
	farevga = vga
}
func (self *TGereçFareOlayhandler) AçıkFareAşağı(düğme int8) {

	fareGereç.Yerel_koordinatları_ayarla(uint32(previousx), uint32(previousy))
	fareGereç.AyarlaRenk(0xA8, 0x00, 0x00)
	fareGereç.Draw(&farevga)

	fareGereç.Draw(&farevga)

}

func (self *TGereçFareOlayhandler) AçıkFareYukarı(düğme int8) {
}

func (self *TGereçFareOlayhandler) AçıkFareTaşı(x int8, y int8) {
	xKonum += int16(x)
	if xKonum < 0 {
		xKonum = 0
	}
	if xKonum >= 320 {
		xKonum = 320
	}

	yKonum -= int16(y)

	if yKonum < 0 {
		yKonum = 0
	}
	if yKonum >= 200 {
		yKonum = 200
	}

	fareGereç.Yerel_koordinatları_ayarla(uint32(previousx), uint32(previousy))
	fareGereç.AyarlaRenk(0x00, 0x00, 0x00)
	fareGereç.Draw(&farevga)

	fareGereç.Yerel_koordinatları_ayarla(uint32(xKonum), uint32(yKonum))
	fareGereç.AyarlaRenk(0x00, 0x00, 0xA8)
	fareGereç.Draw(&farevga)

	previousx = xKonum
	previousy = yKonum

}
