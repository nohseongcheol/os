/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "端口"

type T视频图形数组 struct {
}

var mics端口 uint16 = 0x3c2
var crtc索引端口 uint16 = 0x3d4
var crtc数据端口 uint16 = 0x3d5
var sequencer索引端口 uint16 = 0x3c4
var sequencer数据端口 uint16 = 0x3c5
var 图形控制器索引端口 uint16 = 0x3ce
var 图形控制器数据端口 uint16 = 0x3cf
var 属性控制器索引端口 uint16 = 0x3c0
var 属性控制器读取端口 uint16 = 0x3c1
var 属性控制器写入端口 uint16 = 0x3c0
var 属性控制器重置端口 uint16 = 0x3da

func (self *T视频图形数组) W写入寄存器(寄存器 []byte) {
	var reg索引 uint16 = 0

	P端口写入字节(mics端口, 寄存器[reg索引])
	reg索引++

	var i uint8
	for i = 0; i < 5; i++ {
		P端口写入字节(sequencer索引端口, i)
		P端口写入字节(sequencer数据端口, 寄存器[reg索引])
		reg索引++
	}

	P端口写入字节(crtc索引端口, 0x03)

	P端口写入字节(crtc数据端口, (P端口读取字节(crtc数据端口) | 0x80))
	P端口写入字节(crtc索引端口, 0x11)
	P端口写入字节(crtc数据端口, (P端口读取字节(crtc数据端口) & ^uint8(0x80)))

	寄存器[0x03] = 寄存器[0x03] | 0x80
	寄存器[0x11] = 寄存器[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		P端口写入字节(crtc索引端口, i)
		P端口写入字节(crtc数据端口, 寄存器[reg索引])
		reg索引++
	}

	for i = 0; i < 9; i++ {
		P端口写入字节(图形控制器索引端口, i)
		P端口写入字节(图形控制器数据端口, 寄存器[reg索引])
		reg索引++
	}

	for i = 0; i < 21; i++ {
		P端口读取字节(属性控制器重置端口)
		P端口写入字节(属性控制器索引端口, i)
		P端口写入字节(属性控制器写入端口, 寄存器[reg索引])
		reg索引++
	}

	P端口读取字节(属性控制器重置端口)
	P端口写入字节(属性控制器索引端口, 0x20)

}

func (self *T视频图形数组) Get帧buffersegment() uintptr {
	P端口写入字节(图形控制器索引端口, 0x06)
	var segment数字 uint8 = ((P端口读取字节(图形控制器数据端口) >> 2) & 0x03)
	switch segment数字 {
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
func (self *T视频图形数组) Putpixel(x uint32, y uint32, 颜色索引 uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Get帧buffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = 颜色索引

}
func (self *T视频图形数组) Get颜色索引(r uint8, g uint8, b uint8) uint8 {
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
func (self *T视频图形数组) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Get颜色索引(r, g, b))
}
func (self *T视频图形数组) Fill矩形(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *T视频图形数组) S支持模式(宽度 uint32, 高度 uint32, 颜色深度 uint32) bool {
	return 宽度 == 320 && 高度 == 200 && 颜色深度 == 8
}
func (self *T视频图形数组) S集合模式(宽度 uint32, 高度 uint32, 颜色深度 uint32) bool {
	if !self.S支持模式(宽度, 高度, 颜色深度) {
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

	self.W写入寄存器(g320x200x256)

	return true
}
