package valdiklis

import . "vga"

type IValdiklis interface {
	Init(parent IValdiklis, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokusavimas(valdiklis IValdiklis)
	Set_local_coordinates(x int32, y int32)
	NustatytaSpalva(r uint32, g uint32, b uint32)
	Draw(vga *TVaizdoįrašaiGrafikaMasyvas)
	Containscoordinate(x uint32, y uint32) bool
}

type TValdiklis struct {
	parent	IValdiklis
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TValdiklis) Init(parent IValdiklis, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *TValdiklis) GetFokusavimas(valdiklis IValdiklis) {
	if self.parent != nil {
		self.parent.GetFokusavimas(valdiklis)
	}
}
func (self *TValdiklis) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TValdiklis) NustatytaSpalva(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TValdiklis) Draw(vga *TVaizdoįrašaiGrafikaMasyvas) {
	vga.FillStačiakampis(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TValdiklis) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TValdiklisPelėĮvykishandler struct {
}

var pelėValdiklis TValdiklis
var pelėvga TVaizdoįrašaiGrafikaMasyvas
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (self *TValdiklisPelėĮvykishandler) Init(valdiklis TValdiklis, vga TVaizdoįrašaiGrafikaMasyvas) {
	pelėValdiklis = valdiklis
	pelėvga = vga
}
func (self *TValdiklisPelėĮvykishandler) ĮjungtaPelėŽemyn(mygtukas int8) {

	pelėValdiklis.Set_local_coordinates(uint32(previousx), uint32(previousy))
	pelėValdiklis.NustatytaSpalva(0xA8, 0x00, 0x00)
	pelėValdiklis.Draw(&pelėvga)

	pelėValdiklis.Draw(&pelėvga)

}

func (self *TValdiklisPelėĮvykishandler) ĮjungtaPelėAukštyn(mygtukas int8) {
}

func (self *TValdiklisPelėĮvykishandler) ĮjungtaPelėPerkelti(x int8, y int8) {
	xPozicija += int16(x)
	if xPozicija < 0 {
		xPozicija = 0
	}
	if xPozicija >= 320 {
		xPozicija = 320
	}

	yPozicija -= int16(y)

	if yPozicija < 0 {
		yPozicija = 0
	}
	if yPozicija >= 200 {
		yPozicija = 200
	}

	pelėValdiklis.Set_local_coordinates(uint32(previousx), uint32(previousy))
	pelėValdiklis.NustatytaSpalva(0x00, 0x00, 0x00)
	pelėValdiklis.Draw(&pelėvga)

	pelėValdiklis.Set_local_coordinates(uint32(xPozicija), uint32(yPozicija))
	pelėValdiklis.NustatytaSpalva(0x00, 0x00, 0xA8)
	pelėValdiklis.Draw(&pelėvga)

	previousx = xPozicija
	previousy = yPozicija

}
