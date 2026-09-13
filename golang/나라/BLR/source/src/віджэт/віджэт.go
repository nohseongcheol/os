package віджэт

import . "vga"

type IВіджэт interface {
	Init(parent IВіджэт, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(віджэт IВіджэт)
	Set_local_coordinates(x int32, y int32)
	ВызначанаКолер(r uint32, g uint32, b uint32)
	Draw(vga *TВідэаГрафікаМасіў)
	Containscoordinate(x uint32, y uint32) bool
}

type TВіджэт struct {
	parent	IВіджэт
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TВіджэт) Init(parent IВіджэт, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *TВіджэт) Getfocus(віджэт IВіджэт) {
	if self.parent != nil {
		self.parent.Getfocus(віджэт)
	}
}
func (self *TВіджэт) Set_local_coordinates(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TВіджэт) ВызначанаКолер(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TВіджэт) Draw(vga *TВідэаГрафікаМасіў) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TВіджэт) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TВіджэтМышПадзеяhandler struct {
}

var мышВіджэт TВіджэт
var мышvga TВідэаГрафікаМасіў
var previousx int16 = 0
var previousy int16 = 0
var xПазіцыя int16 = 0
var yПазіцыя int16 = 0

func (self *TВіджэтМышПадзеяhandler) Init(віджэт TВіджэт, vga TВідэаГрафікаМасіў) {
	мышВіджэт = віджэт
	мышvga = vga
}
func (self *TВіджэтМышПадзеяhandler) OnМышУніз(кнопка int8) {

	мышВіджэт.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мышВіджэт.ВызначанаКолер(0xA8, 0x00, 0x00)
	мышВіджэт.Draw(&мышvga)

	мышВіджэт.Draw(&мышvga)

}

func (self *TВіджэтМышПадзеяhandler) OnМышВышэй(кнопка int8) {
}

func (self *TВіджэтМышПадзеяhandler) OnМышПеранесці(x int8, y int8) {
	xПазіцыя += int16(x)
	if xПазіцыя < 0 {
		xПазіцыя = 0
	}
	if xПазіцыя >= 320 {
		xПазіцыя = 320
	}

	yПазіцыя -= int16(y)

	if yПазіцыя < 0 {
		yПазіцыя = 0
	}
	if yПазіцыя >= 200 {
		yПазіцыя = 200
	}

	мышВіджэт.Set_local_coordinates(uint32(previousx), uint32(previousy))
	мышВіджэт.ВызначанаКолер(0x00, 0x00, 0x00)
	мышВіджэт.Draw(&мышvga)

	мышВіджэт.Set_local_coordinates(uint32(xПазіцыя), uint32(yПазіцыя))
	мышВіджэт.ВызначанаКолер(0x00, 0x00, 0xA8)
	мышВіджэт.Draw(&мышvga)

	previousx = xПазіцыя
	previousy = yПазіцыя

}
