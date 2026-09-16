/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package εφαρμογίδιο

import . "vga"

type IΕφαρμογίδιο interface {
	Init(γονικό IΕφαρμογίδιο, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetΕστίαση(εφαρμογίδιο IΕφαρμογίδιο)
	Set_local_coordinates(x int32, y int32)
	ΣύνολοΧρώμα(r uint32, g uint32, b uint32)
	Draw(vga *TΒίντεοΓραφικάΔιάταξη)
	Containscoordinate(x uint32, y uint32) bool
}

type TΕφαρμογίδιο struct {
	γονικό	IΕφαρμογίδιο
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TΕφαρμογίδιο) Init(γονικό IΕφαρμογίδιο, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.γονικό = γονικό

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TΕφαρμογίδιο) GetΕστίαση(εφαρμογίδιο IΕφαρμογίδιο) {
	if self.γονικό != nil {
		self.γονικό.GetΕστίαση(εφαρμογίδιο)
	}
}
func (self *TΕφαρμογίδιο) Set_local_coordinates(x uint32, y uint32) {
	if self.γονικό != nil {

	}
	self.x = x
	self.y = y

}
func (self *TΕφαρμογίδιο) ΣύνολοΧρώμα(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TΕφαρμογίδιο) Draw(vga *TΒίντεοΓραφικάΔιάταξη) {
	vga.FillΟρθογώνιο(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TΕφαρμογίδιο) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TΕφαρμογίδιοΠοντίκιΣυμβάνhandler struct {
}

var ποντίκιΕφαρμογίδιο TΕφαρμογίδιο
var ποντίκιvga TΒίντεοΓραφικάΔιάταξη
var previousx int16 = 0
var previousy int16 = 0
var xΘέση int16 = 0
var yΘέση int16 = 0

func (self *TΕφαρμογίδιοΠοντίκιΣυμβάνhandler) Init(εφαρμογίδιο TΕφαρμογίδιο, vga TΒίντεοΓραφικάΔιάταξη) {
	ποντίκιΕφαρμογίδιο = εφαρμογίδιο
	ποντίκιvga = vga
}
func (self *TΕφαρμογίδιοΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΚάτω(κουμπί int8) {

	ποντίκιΕφαρμογίδιο.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ποντίκιΕφαρμογίδιο.ΣύνολοΧρώμα(0xA8, 0x00, 0x00)
	ποντίκιΕφαρμογίδιο.Draw(&ποντίκιvga)

	ποντίκιΕφαρμογίδιο.Draw(&ποντίκιvga)

}

func (self *TΕφαρμογίδιοΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΠάνω(κουμπί int8) {
}

func (self *TΕφαρμογίδιοΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΜετακίνηση(x int8, y int8) {
	xΘέση += int16(x)
	if xΘέση < 0 {
		xΘέση = 0
	}
	if xΘέση >= 320 {
		xΘέση = 320
	}

	yΘέση -= int16(y)

	if yΘέση < 0 {
		yΘέση = 0
	}
	if yΘέση >= 200 {
		yΘέση = 200
	}

	ποντίκιΕφαρμογίδιο.Set_local_coordinates(uint32(previousx), uint32(previousy))
	ποντίκιΕφαρμογίδιο.ΣύνολοΧρώμα(0x00, 0x00, 0x00)
	ποντίκιΕφαρμογίδιο.Draw(&ποντίκιvga)

	ποντίκιΕφαρμογίδιο.Set_local_coordinates(uint32(xΘέση), uint32(yΘέση))
	ποντίκιΕφαρμογίδιο.ΣύνολοΧρώμα(0x00, 0x00, 0xA8)
	ποντίκιΕφαρμογίδιο.Draw(&ποντίκιvga)

	previousx = xΘέση
	previousy = yΘέση

}
