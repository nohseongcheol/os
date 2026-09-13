package vga

import . "unsafe"
import . "port"

type TVideoGraafikaMassiiv struct {
}

var micsport uint16 = 0x3c2
var crtcSisukordport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerSisukordport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var graafikacontrollerSisukordport uint16 = 0x3ce
var graafikacontrollerdataport uint16 = 0x3cf
var atribuutcontrollerSisukordport uint16 = 0x3c0
var atribuutcontrollerLugemineport uint16 = 0x3c1
var atribuutcontrollerKirjutamineport uint16 = 0x3c0
var atribuutcontrollerLähtestaport uint16 = 0x3da

func (ise *TVideoGraafikaMassiiv) Kirjutamineregister(register []byte) {
	var regSisukord uint16 = 0

	PortKirjutaminebyte(micsport, register[regSisukord])
	regSisukord++

	var i uint8
	for i = 0; i < 5; i++ {
		PortKirjutaminebyte(sequencerSisukordport, i)
		PortKirjutaminebyte(sequencerdataport, register[regSisukord])
		regSisukord++
	}

	PortKirjutaminebyte(crtcSisukordport, 0x03)

	PortKirjutaminebyte(crtcdataport, (PortLugeminebyte(crtcdataport) | 0x80))
	PortKirjutaminebyte(crtcSisukordport, 0x11)
	PortKirjutaminebyte(crtcdataport, (PortLugeminebyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortKirjutaminebyte(crtcSisukordport, i)
		PortKirjutaminebyte(crtcdataport, register[regSisukord])
		regSisukord++
	}

	for i = 0; i < 9; i++ {
		PortKirjutaminebyte(graafikacontrollerSisukordport, i)
		PortKirjutaminebyte(graafikacontrollerdataport, register[regSisukord])
		regSisukord++
	}

	for i = 0; i < 21; i++ {
		PortLugeminebyte(atribuutcontrollerLähtestaport)
		PortKirjutaminebyte(atribuutcontrollerSisukordport, i)
		PortKirjutaminebyte(atribuutcontrollerKirjutamineport, register[regSisukord])
		regSisukord++
	}

	PortLugeminebyte(atribuutcontrollerLähtestaport)
	PortKirjutaminebyte(atribuutcontrollerSisukordport, 0x20)

}

func (ise *TVideoGraafikaMassiiv) GetRaambuffersegment() uintptr {
	PortKirjutaminebyte(graafikacontrollerSisukordport, 0x06)
	var segmentArv uint8 = ((PortLugeminebyte(graafikacontrollerdataport) >> 2) & 0x03)
	switch segmentArv {
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
func (ise *TVideoGraafikaMassiiv) Putpixel(x uint32, y uint32, värvSisukord uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = ise.GetRaambuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = värvSisukord

}
func (ise *TVideoGraafikaMassiiv) GetVärvSisukord(r uint8, g uint8, b uint8) uint8 {
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
func (ise *TVideoGraafikaMassiiv) PutpixelPRS(x uint32, y uint32, r uint8, g uint8, b uint8) {
	ise.Putpixel(x, y, ise.GetVärvSisukord(r, g, b))
}
func (ise *TVideoGraafikaMassiiv) FillRistkülik(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			ise.PutpixelPRS(X, Y, r, g, b)
		}
	}
}
func (ise *TVideoGraafikaMassiiv) TugiREŽIIM(kõrgus uint32, laius uint32, värvdepth uint32) bool {
	return kõrgus == 320 && laius == 200 && värvdepth == 8
}
func (ise *TVideoGraafikaMassiiv) MääraREŽIIM(kõrgus uint32, laius uint32, värvdepth uint32) bool {
	if !ise.TugiREŽIIM(kõrgus, laius, värvdepth) {
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

	ise.Kirjutamineregister(g320x200x256)

	return true
}
