/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 界面元素

import . "vga"

type I界面元素 interface {
	Init(parent I界面元素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Get焦点(界面元素 I界面元素)
	M设置局部坐标(x int32, y int32)
	S集合颜色(r uint32, g uint32, b uint32)
	Draw(vga *T视频图形数组)
	Containscoordinate(x uint32, y uint32) bool
}

type T界面元素 struct {
	parent	I界面元素
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *T界面元素) Init(parent I界面元素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *T界面元素) Get焦点(界面元素 I界面元素) {
	if self.parent != nil {
		self.parent.Get焦点(界面元素)
	}
}
func (self *T界面元素) M设置局部坐标(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *T界面元素) S集合颜色(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *T界面元素) Draw(vga *T视频图形数组) {
	vga.Fill矩形(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *T界面元素) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type T控件鼠标事件handler struct {
}

var 鼠标控件 T界面元素
var 鼠标vga T视频图形数组
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self *T控件鼠标事件handler) Init(界面元素 T界面元素, vga T视频图形数组) {
	鼠标控件 = 界面元素
	鼠标vga = vga
}
func (self *T控件鼠标事件handler) O时鼠标下(按钮 int8) {

	鼠标控件.M设置局部坐标(uint32(previousx), uint32(previousy))
	鼠标控件.S集合颜色(0xA8, 0x00, 0x00)
	鼠标控件.Draw(&鼠标vga)

	鼠标控件.Draw(&鼠标vga)

}

func (self *T控件鼠标事件handler) O时鼠标向上(按钮 int8) {
}

func (self *T控件鼠标事件handler) O时鼠标移动(x int8, y int8) {
	x位置 += int16(x)
	if x位置 < 0 {
		x位置 = 0
	}
	if x位置 >= 320 {
		x位置 = 320
	}

	y位置 -= int16(y)

	if y位置 < 0 {
		y位置 = 0
	}
	if y位置 >= 200 {
		y位置 = 200
	}

	鼠标控件.M设置局部坐标(uint32(previousx), uint32(previousy))
	鼠标控件.S集合颜色(0x00, 0x00, 0x00)
	鼠标控件.Draw(&鼠标vga)

	鼠标控件.M设置局部坐标(uint32(x位置), uint32(y位置))
	鼠标控件.S集合颜色(0x00, 0x00, 0xA8)
	鼠标控件.Draw(&鼠标vga)

	previousx = x位置
	previousy = y位置

}
