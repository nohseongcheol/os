/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "cổng"

type TẢnhđộngĐồhoạMảng struct {
}

var micsCổng uint16 = 0x3c2
var crtcChỉmụcCổng uint16 = 0x3d4
var crtcdataCổng uint16 = 0x3d5
var sequencerChỉmụcCổng uint16 = 0x3c4
var sequencerdataCổng uint16 = 0x3c5
var đồhoạcontrollerChỉmụcCổng uint16 = 0x3ce
var đồhoạcontrollerdataCổng uint16 = 0x3cf
var thuộctínhcontrollerChỉmụcCổng uint16 = 0x3c0
var thuộctínhcontrollerĐọcCổng uint16 = 0x3c1
var thuộctínhcontrollerGhiCổng uint16 = 0x3c0
var thuộctínhcontrollerĐặtlạiCổng uint16 = 0x3da

func (mình *TẢnhđộngĐồhoạMảng) Ghiregister(register []byte) {
	var regChỉmục uint16 = 0

	CổngGhibyte(micsCổng, register[regChỉmục])
	regChỉmục++

	var i uint8
	for i = 0; i < 5; i++ {
		CổngGhibyte(sequencerChỉmụcCổng, i)
		CổngGhibyte(sequencerdataCổng, register[regChỉmục])
		regChỉmục++
	}

	CổngGhibyte(crtcChỉmụcCổng, 0x03)

	CổngGhibyte(crtcdataCổng, (CổngĐọcbyte(crtcdataCổng) | 0x80))
	CổngGhibyte(crtcChỉmụcCổng, 0x11)
	CổngGhibyte(crtcdataCổng, (CổngĐọcbyte(crtcdataCổng) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		CổngGhibyte(crtcChỉmụcCổng, i)
		CổngGhibyte(crtcdataCổng, register[regChỉmục])
		regChỉmục++
	}

	for i = 0; i < 9; i++ {
		CổngGhibyte(đồhoạcontrollerChỉmụcCổng, i)
		CổngGhibyte(đồhoạcontrollerdataCổng, register[regChỉmục])
		regChỉmục++
	}

	for i = 0; i < 21; i++ {
		CổngĐọcbyte(thuộctínhcontrollerĐặtlạiCổng)
		CổngGhibyte(thuộctínhcontrollerChỉmụcCổng, i)
		CổngGhibyte(thuộctínhcontrollerGhiCổng, register[regChỉmục])
		regChỉmục++
	}

	CổngĐọcbyte(thuộctínhcontrollerĐặtlạiCổng)
	CổngGhibyte(thuộctínhcontrollerChỉmụcCổng, 0x20)

}

func (mình *TẢnhđộngĐồhoạMảng) Getframebuffersegment() uintptr {
	CổngGhibyte(đồhoạcontrollerChỉmụcCổng, 0x06)
	var segmentSỐ uint8 = ((CổngĐọcbyte(đồhoạcontrollerdataCổng) >> 2) & 0x03)
	switch segmentSỐ {
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
func (mình *TẢnhđộngĐồhoạMảng) Putpixel(x uint32, y uint32, màuChỉmục uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = mình.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = màuChỉmục

}
func (mình *TẢnhđộngĐồhoạMảng) GetMàuChỉmục(r uint8, g uint8, b uint8) uint8 {
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
func (mình *TẢnhđộngĐồhoạMảng) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	mình.Putpixel(x, y, mình.GetMàuChỉmục(r, g, b))
}
func (mình *TẢnhđộngĐồhoạMảng) FillChữnhật(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			mình.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (mình *TẢnhđộngĐồhoạMảng) HỗtrợChếđộ(độrộng uint32, độcao uint32, màuChiềusâu uint32) bool {
	return độrộng == 320 && độcao == 200 && màuChiềusâu == 8
}
func (mình *TẢnhđộngĐồhoạMảng) ĐặtChếđộ(độrộng uint32, độcao uint32, màuChiềusâu uint32) bool {
	if !mình.HỗtrợChếđộ(độrộng, độcao, màuChiềusâu) {
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

	mình.Ghiregister(g320x200x256)

	return true
}
