/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package prvek_obrazovky

import . "vga"

type IPrvek_obrazovky interface {
	Init(rodič IPrvek_obrazovky, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetZaměřit(prvek_obrazovky IPrvek_obrazovky)
	Nastavit_místní_souřadnice(x int32, y int32)
	NastavitBarva(r uint32, g uint32, b uint32)
	Draw(vga *TObrazGrafikaPole)
	Containscoordinate(x uint32, y uint32) bool
}

type TPrvek_obrazovky struct {
	rodič	IPrvek_obrazovky
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TPrvek_obrazovky) Init(rodič IPrvek_obrazovky, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.rodič = rodič

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TPrvek_obrazovky) GetZaměřit(prvek_obrazovky IPrvek_obrazovky) {
	if self.rodič != nil {
		self.rodič.GetZaměřit(prvek_obrazovky)
	}
}
func (self *TPrvek_obrazovky) Nastavit_místní_souřadnice(x uint32, y uint32) {
	if self.rodič != nil {

	}
	self.x = x
	self.y = y

}
func (self *TPrvek_obrazovky) NastavitBarva(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TPrvek_obrazovky) Draw(vga *TObrazGrafikaPole) {
	vga.FillObdélníkový(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TPrvek_obrazovky) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TWidgetMyšUdálostihandler struct {
}

var myšwidget TPrvek_obrazovky
var myšvga TObrazGrafikaPole
var previousx int16 = 0
var previousy int16 = 0
var xUmístění int16 = 0
var yUmístění int16 = 0

func (self *TWidgetMyšUdálostihandler) Init(prvek_obrazovky TPrvek_obrazovky, vga TObrazGrafikaPole) {
	myšwidget = prvek_obrazovky
	myšvga = vga
}
func (self *TWidgetMyšUdálostihandler) ZapnutoMyšDolů(tlačítko int8) {

	myšwidget.Nastavit_místní_souřadnice(uint32(previousx), uint32(previousy))
	myšwidget.NastavitBarva(0xA8, 0x00, 0x00)
	myšwidget.Draw(&myšvga)

	myšwidget.Draw(&myšvga)

}

func (self *TWidgetMyšUdálostihandler) ZapnutoMyšNahoru(tlačítko int8) {
}

func (self *TWidgetMyšUdálostihandler) ZapnutoMyšPřesunout(x int8, y int8) {
	xUmístění += int16(x)
	if xUmístění < 0 {
		xUmístění = 0
	}
	if xUmístění >= 320 {
		xUmístění = 320
	}

	yUmístění -= int16(y)

	if yUmístění < 0 {
		yUmístění = 0
	}
	if yUmístění >= 200 {
		yUmístění = 200
	}

	myšwidget.Nastavit_místní_souřadnice(uint32(previousx), uint32(previousy))
	myšwidget.NastavitBarva(0x00, 0x00, 0x00)
	myšwidget.Draw(&myšvga)

	myšwidget.Nastavit_místní_souřadnice(uint32(xUmístění), uint32(yUmístění))
	myšwidget.NastavitBarva(0x00, 0x00, 0xA8)
	myšwidget.Draw(&myšvga)

	previousx = xUmístění
	previousy = yUmístění

}
