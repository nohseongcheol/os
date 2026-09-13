package elem

import . "vga"

type IElem interface {
	Init(parent IElem, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFókusz(elem IElem)
	Set_local_coordinates(x int32, y int32)
	HalmazSzín(r uint32, g uint32, b uint32)
	Draw(vga *TMozgóképGrafikaTömb)
	Containscoordinate(x uint32, y uint32) bool
}

type TElem struct {
	parent	IElem
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TElem) Init(parent IElem, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.parent = parent

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TElem) GetFókusz(elem IElem) {
	if self.parent != nil {
		self.parent.GetFókusz(elem)
	}
}
func (self *TElem) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TElem) HalmazSzín(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TElem) Draw(vga *TMozgóképGrafikaTömb) {
	vga.FillNégyzet(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TElem) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TElemEgérEseményhandler struct {
}

var egérElem TElem
var egérvga TMozgóképGrafikaTömb
var previousx int16 = 0
var previousy int16 = 0
var xPozíció int16 = 0
var yPozíció int16 = 0

func (self *TElemEgérEseményhandler) Init(elem TElem, vga TMozgóképGrafikaTömb) {
	egérElem = elem
	egérvga = vga
}
func (self *TElemEgérEseményhandler) BeEgérLe(gomb int8) {

	egérElem.Set_local_coordinates(uint32(previousx), uint32(previousy))
	egérElem.HalmazSzín(0xA8, 0x00, 0x00)
	egérElem.Draw(&egérvga)

	egérElem.Draw(&egérvga)

}

func (self *TElemEgérEseményhandler) BeEgérFel(gomb int8) {
}

func (self *TElemEgérEseményhandler) BeEgérÁthelyezés(x int8, y int8) {
	xPozíció += int16(x)
	if xPozíció < 0 {
		xPozíció = 0
	}
	if xPozíció >= 320 {
		xPozíció = 320
	}

	yPozíció -= int16(y)

	if yPozíció < 0 {
		yPozíció = 0
	}
	if yPozíció >= 200 {
		yPozíció = 200
	}

	egérElem.Set_local_coordinates(uint32(previousx), uint32(previousy))
	egérElem.HalmazSzín(0x00, 0x00, 0x00)
	egérElem.Draw(&egérvga)

	egérElem.Set_local_coordinates(uint32(xPozíció), uint32(yPozíció))
	egérElem.HalmazSzín(0x00, 0x00, 0xA8)
	egérElem.Draw(&egérvga)

	previousx = xPozíció
	previousy = yPozíció

}
