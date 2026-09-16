/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVideoGrafikTabel struct {
}

var micsport uint16 = 0x3c2
var crtcIndeksport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerIndeksport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikcontrollerIndeksport uint16 = 0x3ce
var grafikcontrollerdataport uint16 = 0x3cf
var egenskabcontrollerIndeksport uint16 = 0x3c0
var egenskabcontrollerLæseport uint16 = 0x3c1
var egenskabcontrollerSkriveport uint16 = 0x3c0
var egenskabcontrollerNulstilport uint16 = 0x3da

func (selv *TVideoGrafikTabel) Skriveregister(register []byte) {
	var regIndeks uint16 = 0

	PortSkrivebyte(micsport, register[regIndeks])
	regIndeks++

	var i uint8
	for i = 0; i < 5; i++ {
		PortSkrivebyte(sequencerIndeksport, i)
		PortSkrivebyte(sequencerdataport, register[regIndeks])
		regIndeks++
	}

	PortSkrivebyte(crtcIndeksport, 0x03)

	PortSkrivebyte(crtcdataport, (PortLæsebyte(crtcdataport) | 0x80))
	PortSkrivebyte(crtcIndeksport, 0x11)
	PortSkrivebyte(crtcdataport, (PortLæsebyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortSkrivebyte(crtcIndeksport, i)
		PortSkrivebyte(crtcdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 9; i++ {
		PortSkrivebyte(grafikcontrollerIndeksport, i)
		PortSkrivebyte(grafikcontrollerdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 21; i++ {
		PortLæsebyte(egenskabcontrollerNulstilport)
		PortSkrivebyte(egenskabcontrollerIndeksport, i)
		PortSkrivebyte(egenskabcontrollerSkriveport, register[regIndeks])
		regIndeks++
	}

	PortLæsebyte(egenskabcontrollerNulstilport)
	PortSkrivebyte(egenskabcontrollerIndeksport, 0x20)

}

func (selv *TVideoGrafikTabel) GetRammebuffersegment() uintptr {
	PortSkrivebyte(grafikcontrollerIndeksport, 0x06)
	var segmentTal uint8 = ((PortLæsebyte(grafikcontrollerdataport) >> 2) & 0x03)
	switch segmentTal {
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
func (selv *TVideoGrafikTabel) Putpixel(x uint32, y uint32, farveIndeks uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = selv.GetRammebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = farveIndeks

}
func (selv *TVideoGrafikTabel) GetFarveIndeks(r uint8, g uint8, b uint8) uint8 {
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
func (selv *TVideoGrafikTabel) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	selv.Putpixel(x, y, selv.GetFarveIndeks(r, g, b))
}
func (selv *TVideoGrafikTabel) FillRektangel(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			selv.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (selv *TVideoGrafikTabel) Understøttelsetilstand(bredde uint32, højde uint32, farveDybde uint32) bool {
	return bredde == 320 && højde == 200 && farveDybde == 8
}
func (selv *TVideoGrafikTabel) Sattilstand(bredde uint32, højde uint32, farveDybde uint32) bool {
	if !selv.Understøttelsetilstand(bredde, højde, farveDybde) {
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

	selv.Skriveregister(g320x200x256)

	return true
}
