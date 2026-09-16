/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "ポート"

type Tビデオグラフィック配列 struct {
}

var micsポート uint16 = 0x3c2
var crtc目次ポート uint16 = 0x3d4
var crtcデータポート uint16 = 0x3d5
var sequencer目次ポート uint16 = 0x3c4
var sequencerデータポート uint16 = 0x3c5
var グラフィック制御器目次ポート uint16 = 0x3ce
var グラフィック制御器データポート uint16 = 0x3cf
var 属性制御器目次ポート uint16 = 0x3c0
var 属性制御器読込みポート uint16 = 0x3c1
var 属性制御器書込みポート uint16 = 0x3c0
var 属性制御器リセットポート uint16 = 0x3da

func (self *Tビデオグラフィック配列) W書込みレジスタ(レジスタ []byte) {
	var reg目次 uint16 = 0

	Pポート書込みバイト(micsポート, レジスタ[reg目次])
	reg目次++

	var i uint8
	for i = 0; i < 5; i++ {
		Pポート書込みバイト(sequencer目次ポート, i)
		Pポート書込みバイト(sequencerデータポート, レジスタ[reg目次])
		reg目次++
	}

	Pポート書込みバイト(crtc目次ポート, 0x03)

	Pポート書込みバイト(crtcデータポート, (Pポート読込みバイト(crtcデータポート) | 0x80))
	Pポート書込みバイト(crtc目次ポート, 0x11)
	Pポート書込みバイト(crtcデータポート, (Pポート読込みバイト(crtcデータポート) & ^uint8(0x80)))

	レジスタ[0x03] = レジスタ[0x03] | 0x80
	レジスタ[0x11] = レジスタ[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pポート書込みバイト(crtc目次ポート, i)
		Pポート書込みバイト(crtcデータポート, レジスタ[reg目次])
		reg目次++
	}

	for i = 0; i < 9; i++ {
		Pポート書込みバイト(グラフィック制御器目次ポート, i)
		Pポート書込みバイト(グラフィック制御器データポート, レジスタ[reg目次])
		reg目次++
	}

	for i = 0; i < 21; i++ {
		Pポート読込みバイト(属性制御器リセットポート)
		Pポート書込みバイト(属性制御器目次ポート, i)
		Pポート書込みバイト(属性制御器書込みポート, レジスタ[reg目次])
		reg目次++
	}

	Pポート読込みバイト(属性制御器リセットポート)
	Pポート書込みバイト(属性制御器目次ポート, 0x20)

}

func (self *Tビデオグラフィック配列) Getフレームbuffersegment() uintptr {
	Pポート書込みバイト(グラフィック制御器目次ポート, 0x06)
	var segmentnumber uint8 = ((Pポート読込みバイト(グラフィック制御器データポート) >> 2) & 0x03)
	switch segmentnumber {
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
func (self *Tビデオグラフィック配列) Putpixel(x uint32, y uint32, 色目次 uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getフレームbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = 色目次

}
func (self *Tビデオグラフィック配列) Get色目次(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tビデオグラフィック配列) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Get色目次(r, g, b))
}
func (self *Tビデオグラフィック配列) Fill矩形(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tビデオグラフィック配列) Sサポートモード(幅 uint32, height uint32, 色depth uint32) bool {
	return 幅 == 320 && height == 200 && 色depth == 8
}
func (self *Tビデオグラフィック配列) Sありモード(幅 uint32, height uint32, 色depth uint32) bool {
	if !self.Sサポートモード(幅, height, 色depth) {
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

	self.W書込みレジスタ(g320x200x256)

	return true
}
