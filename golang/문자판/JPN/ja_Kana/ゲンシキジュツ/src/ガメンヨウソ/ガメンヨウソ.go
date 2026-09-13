package ガメンヨウソ

import . "vga"

type Iガメンヨウソ interface {
	Init(parent Iガメンヨウソ, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getフォーカス(ガメンヨウソ Iガメンヨウソ)
	Mキョクショザヒョウヲセッテイ(x int32, y int32)
	Sアリショク(r uint32, g uint32, b uint32)
	Draw(vga *Tビデオグラフィックハイレツ)
	Containscoordinate(x uint32, y uint32) bool
}

type Tガメンヨウソ struct {
	parent	Iガメンヨウソ
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *Tガメンヨウソ) Init(parent Iガメンヨウソ, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *Tガメンヨウソ) Getフォーカス(ガメンヨウソ Iガメンヨウソ) {
	if self.parent != nil {
		self.parent.Getフォーカス(ガメンヨウソ)
	}
}
func (self *Tガメンヨウソ) Mキョクショザヒョウヲセッテイ(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *Tガメンヨウソ) Sアリショク(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *Tガメンヨウソ) Draw(vga *Tビデオグラフィックハイレツ) {
	vga.Fillクケイ(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *Tガメンヨウソ) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type Tガメンヨウソマウスジショウhandler struct {
}

var マウスガメンヨウソ Tガメンヨウソ
var マウスvga Tビデオグラフィックハイレツ
var previousx int16 = 0
var previousy int16 = 0
var xハイチ int16 = 0
var yハイチ int16 = 0

func (self *Tガメンヨウソマウスジショウhandler) Init(ガメンヨウソ Tガメンヨウソ, vga Tビデオグラフィックハイレツ) {
	マウスガメンヨウソ = ガメンヨウソ
	マウスvga = vga
}
func (self *Tガメンヨウソマウスジショウhandler) Oトキマウスシタ(ボタン int8) {

	マウスガメンヨウソ.Mキョクショザヒョウヲセッテイ(uint32(previousx), uint32(previousy))
	マウスガメンヨウソ.Sアリショク(0xA8, 0x00, 0x00)
	マウスガメンヨウソ.Draw(&マウスvga)

	マウスガメンヨウソ.Draw(&マウスvga)

}

func (self *Tガメンヨウソマウスジショウhandler) Oトキマウスウエヘ(ボタン int8) {
}

func (self *Tガメンヨウソマウスジショウhandler) Oトキマウスイドウ(x int8, y int8) {
	xハイチ += int16(x)
	if xハイチ < 0 {
		xハイチ = 0
	}
	if xハイチ >= 320 {
		xハイチ = 320
	}

	yハイチ -= int16(y)

	if yハイチ < 0 {
		yハイチ = 0
	}
	if yハイチ >= 200 {
		yハイチ = 200
	}

	マウスガメンヨウソ.Mキョクショザヒョウヲセッテイ(uint32(previousx), uint32(previousy))
	マウスガメンヨウソ.Sアリショク(0x00, 0x00, 0x00)
	マウスガメンヨウソ.Draw(&マウスvga)

	マウスガメンヨウソ.Mキョクショザヒョウヲセッテイ(uint32(xハイチ), uint32(yハイチ))
	マウスガメンヨウソ.Sアリショク(0x00, 0x00, 0xA8)
	マウスガメンヨウソ.Draw(&マウスvga)

	previousx = xハイチ
	previousy = yハイチ

}
