/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 画面要素

import . "vga"

type I画面要素 interface {
	Init(parent I画面要素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getフォーカス(画面要素 I画面要素)
	M局所座標を設定(x int32, y int32)
	Sあり色(r uint32, g uint32, b uint32)
	Draw(vga *Tビデオグラフィック配列)
	Containscoordinate(x uint32, y uint32) bool
}

type T画面要素 struct {
	parent	I画面要素
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *T画面要素) Init(parent I画面要素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *T画面要素) Getフォーカス(画面要素 I画面要素) {
	if self.parent != nil {
		self.parent.Getフォーカス(画面要素)
	}
}
func (self *T画面要素) M局所座標を設定(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *T画面要素) Sあり色(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *T画面要素) Draw(vga *Tビデオグラフィック配列) {
	vga.Fill矩形(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *T画面要素) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type T画面要素マウス事象handler struct {
}

var マウス画面要素 T画面要素
var マウスvga Tビデオグラフィック配列
var previousx int16 = 0
var previousy int16 = 0
var x配置 int16 = 0
var y配置 int16 = 0

func (self *T画面要素マウス事象handler) Init(画面要素 T画面要素, vga Tビデオグラフィック配列) {
	マウス画面要素 = 画面要素
	マウスvga = vga
}
func (self *T画面要素マウス事象handler) O時マウス下(ボタン int8) {

	マウス画面要素.M局所座標を設定(uint32(previousx), uint32(previousy))
	マウス画面要素.Sあり色(0xA8, 0x00, 0x00)
	マウス画面要素.Draw(&マウスvga)

	マウス画面要素.Draw(&マウスvga)

}

func (self *T画面要素マウス事象handler) O時マウス上へ(ボタン int8) {
}

func (self *T画面要素マウス事象handler) O時マウス移動(x int8, y int8) {
	x配置 += int16(x)
	if x配置 < 0 {
		x配置 = 0
	}
	if x配置 >= 320 {
		x配置 = 320
	}

	y配置 -= int16(y)

	if y配置 < 0 {
		y配置 = 0
	}
	if y配置 >= 200 {
		y配置 = 200
	}

	マウス画面要素.M局所座標を設定(uint32(previousx), uint32(previousy))
	マウス画面要素.Sあり色(0x00, 0x00, 0x00)
	マウス画面要素.Draw(&マウスvga)

	マウス画面要素.M局所座標を設定(uint32(x配置), uint32(y配置))
	マウス画面要素.Sあり色(0x00, 0x00, 0xA8)
	マウス画面要素.Draw(&マウスvga)

	previousx = x配置
	previousy = y配置

}
