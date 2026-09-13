package がめんようそ

import . "vga"

type Iがめんようそ interface {
	Init(parent Iがめんようそ, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getふぉーかす(がめんようそ Iがめんようそ)
	Mきょくしょざひょうをせってい(x int32, y int32)
	Sありしょく(r uint32, g uint32, b uint32)
	Draw(vga *Tびでおぐらふぃっくはいれつ)
	Containscoordinate(x uint32, y uint32) bool
}

type Tがめんようそ struct {
	parent	Iがめんようそ
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *Tがめんようそ) Init(parent Iがめんようそ, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *Tがめんようそ) Getふぉーかす(がめんようそ Iがめんようそ) {
	if self.parent != nil {
		self.parent.Getふぉーかす(がめんようそ)
	}
}
func (self *Tがめんようそ) Mきょくしょざひょうをせってい(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *Tがめんようそ) Sありしょく(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *Tがめんようそ) Draw(vga *Tびでおぐらふぃっくはいれつ) {
	vga.Fillくけい(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *Tがめんようそ) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type Tがめんようそまうすじしょうhandler struct {
}

var まうすがめんようそ Tがめんようそ
var まうすvga Tびでおぐらふぃっくはいれつ
var previousx int16 = 0
var previousy int16 = 0
var xはいち int16 = 0
var yはいち int16 = 0

func (self *Tがめんようそまうすじしょうhandler) Init(がめんようそ Tがめんようそ, vga Tびでおぐらふぃっくはいれつ) {
	まうすがめんようそ = がめんようそ
	まうすvga = vga
}
func (self *Tがめんようそまうすじしょうhandler) Oときまうすした(ぼたん int8) {

	まうすがめんようそ.Mきょくしょざひょうをせってい(uint32(previousx), uint32(previousy))
	まうすがめんようそ.Sありしょく(0xA8, 0x00, 0x00)
	まうすがめんようそ.Draw(&まうすvga)

	まうすがめんようそ.Draw(&まうすvga)

}

func (self *Tがめんようそまうすじしょうhandler) Oときまうすうえへ(ぼたん int8) {
}

func (self *Tがめんようそまうすじしょうhandler) Oときまうすいどう(x int8, y int8) {
	xはいち += int16(x)
	if xはいち < 0 {
		xはいち = 0
	}
	if xはいち >= 320 {
		xはいち = 320
	}

	yはいち -= int16(y)

	if yはいち < 0 {
		yはいち = 0
	}
	if yはいち >= 200 {
		yはいち = 200
	}

	まうすがめんようそ.Mきょくしょざひょうをせってい(uint32(previousx), uint32(previousy))
	まうすがめんようそ.Sありしょく(0x00, 0x00, 0x00)
	まうすがめんようそ.Draw(&まうすvga)

	まうすがめんようそ.Mきょくしょざひょうをせってい(uint32(xはいち), uint32(yはいち))
	まうすがめんようそ.Sありしょく(0x00, 0x00, 0xA8)
	まうすがめんようそ.Draw(&まうすvga)

	previousx = xはいち
	previousy = yはいち

}
