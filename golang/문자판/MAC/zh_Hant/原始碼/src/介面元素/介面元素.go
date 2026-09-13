package 介面元素

import . "vga"

type I介面元素 interface {
	Init(parent I介面元素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Get焦點(介面元素 I介面元素)
	M設定局部座標(x int32, y int32)
	S設定色彩(r uint32, g uint32, b uint32)
	Draw(vga *T視訊圖形陣列)
	Containscoordinate(x uint32, y uint32) bool
}

type T介面元素 struct {
	parent	I介面元素
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *T介面元素) Init(parent I介面元素, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

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
func (self *T介面元素) Get焦點(介面元素 I介面元素) {
	if self.parent != nil {
		self.parent.Get焦點(介面元素)
	}
}
func (self *T介面元素) M設定局部座標(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *T介面元素) S設定色彩(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *T介面元素) Draw(vga *T視訊圖形陣列) {
	vga.Fill矩形(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *T介面元素) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type T元件滑鼠事件handler struct {
}

var 滑鼠元件 T介面元素
var 滑鼠vga T視訊圖形陣列
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self *T元件滑鼠事件handler) Init(介面元素 T介面元素, vga T視訊圖形陣列) {
	滑鼠元件 = 介面元素
	滑鼠vga = vga
}
func (self *T元件滑鼠事件handler) O時滑鼠下(按鈕 int8) {

	滑鼠元件.M設定局部座標(uint32(previousx), uint32(previousy))
	滑鼠元件.S設定色彩(0xA8, 0x00, 0x00)
	滑鼠元件.Draw(&滑鼠vga)

	滑鼠元件.Draw(&滑鼠vga)

}

func (self *T元件滑鼠事件handler) O時滑鼠上(按鈕 int8) {
}

func (self *T元件滑鼠事件handler) O時滑鼠移動(x int8, y int8) {
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

	滑鼠元件.M設定局部座標(uint32(previousx), uint32(previousy))
	滑鼠元件.S設定色彩(0x00, 0x00, 0x00)
	滑鼠元件.Draw(&滑鼠vga)

	滑鼠元件.M設定局部座標(uint32(x位置), uint32(y位置))
	滑鼠元件.S設定色彩(0x00, 0x00, 0xA8)
	滑鼠元件.Draw(&滑鼠vga)

	previousx = x位置
	previousy = y位置

}
