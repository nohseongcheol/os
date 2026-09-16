/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "連接埠"

type T視訊圖形陣列 struct {
}

var mics連接埠 uint16 = 0x3c2
var crtc索引連接埠 uint16 = 0x3d4
var crtc資料連接埠 uint16 = 0x3d5
var sequencer索引連接埠 uint16 = 0x3c4
var sequencer資料連接埠 uint16 = 0x3c5
var 圖形控制器索引連接埠 uint16 = 0x3ce
var 圖形控制器資料連接埠 uint16 = 0x3cf
var 屬性控制器索引連接埠 uint16 = 0x3c0
var 屬性控制器讀取連接埠 uint16 = 0x3c1
var 屬性控制器寫入連接埠 uint16 = 0x3c0
var 屬性控制器重設連接埠 uint16 = 0x3da

func (self *T視訊圖形陣列) W寫入暫存器(暫存器 []byte) {
	var reg索引 uint16 = 0

	P連接埠寫入位元組(mics連接埠, 暫存器[reg索引])
	reg索引++

	var i uint8
	for i = 0; i < 5; i++ {
		P連接埠寫入位元組(sequencer索引連接埠, i)
		P連接埠寫入位元組(sequencer資料連接埠, 暫存器[reg索引])
		reg索引++
	}

	P連接埠寫入位元組(crtc索引連接埠, 0x03)

	P連接埠寫入位元組(crtc資料連接埠, (P連接埠讀取位元組(crtc資料連接埠) | 0x80))
	P連接埠寫入位元組(crtc索引連接埠, 0x11)
	P連接埠寫入位元組(crtc資料連接埠, (P連接埠讀取位元組(crtc資料連接埠) & ^uint8(0x80)))

	暫存器[0x03] = 暫存器[0x03] | 0x80
	暫存器[0x11] = 暫存器[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		P連接埠寫入位元組(crtc索引連接埠, i)
		P連接埠寫入位元組(crtc資料連接埠, 暫存器[reg索引])
		reg索引++
	}

	for i = 0; i < 9; i++ {
		P連接埠寫入位元組(圖形控制器索引連接埠, i)
		P連接埠寫入位元組(圖形控制器資料連接埠, 暫存器[reg索引])
		reg索引++
	}

	for i = 0; i < 21; i++ {
		P連接埠讀取位元組(屬性控制器重設連接埠)
		P連接埠寫入位元組(屬性控制器索引連接埠, i)
		P連接埠寫入位元組(屬性控制器寫入連接埠, 暫存器[reg索引])
		reg索引++
	}

	P連接埠讀取位元組(屬性控制器重設連接埠)
	P連接埠寫入位元組(屬性控制器索引連接埠, 0x20)

}

func (self *T視訊圖形陣列) Get框架buffersegment() uintptr {
	P連接埠寫入位元組(圖形控制器索引連接埠, 0x06)
	var segment數字 uint8 = ((P連接埠讀取位元組(圖形控制器資料連接埠) >> 2) & 0x03)
	switch segment數字 {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (self *T視訊圖形陣列) Putpixel(x uint32, y uint32, 色彩索引 uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Get框架buffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = 色彩索引

}
func (self *T視訊圖形陣列) Get色彩索引(r uint8, g uint8, b uint8) uint8 {
	if r == 0x00 && g == 0x00 && b == 0x00 {
		return 0x00
	}
	if r == 0x00 && g == 0x00 && b == 0xA8 {
		return 0x01
	}
	if r == 0x00 && g == 0xA8 && b == 0x00 {
		return 0x02
	}
	if r == 0xA8 && g == 0x00 && b == 0x00 {
		return 0x04
	}
	if r == 0xFF && g == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (self *T視訊圖形陣列) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Get色彩索引(r, g, b))
}
func (self *T視訊圖形陣列) Fill矩形(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *T視訊圖形陣列) S支援模式(寬度 uint32, height uint32, 色彩深度 uint32) bool {
	return 寬度 == 320 && height == 200 && 色彩深度 == 8
}
func (self *T視訊圖形陣列) S設定模式(寬度 uint32, height uint32, 色彩深度 uint32) bool {
	if !self.S支援模式(寬度, height, 色彩深度) {
		return false
	}

	var g320x200x256 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	self.W寫入暫存器(g320x200x256)

	return true
}
