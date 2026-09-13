package vga

import . "unsafe"
import . "port"

type TVideoGrafikTatasusunan struct {
}

var micsport uint16 = 0x3c2
var crtcIndeksport uint16 = 0x3d4
var crtcdataport uint16 = 0x3d5
var sequencerIndeksport uint16 = 0x3c4
var sequencerdataport uint16 = 0x3c5
var grafikcontrollerIndeksport uint16 = 0x3ce
var grafikcontrollerdataport uint16 = 0x3cf
var atributcontrollerIndeksport uint16 = 0x3c0
var atributcontrollerBacaport uint16 = 0x3c1
var atributcontrollerTulisport uint16 = 0x3c0
var atributcontrollerTetapSemulaport uint16 = 0x3da

func (diri *TVideoGrafikTatasusunan) Tulisregister(register []byte) {
	var regIndeks uint16 = 0

	PortTulisbyte(micsport, register[regIndeks])
	regIndeks++

	var i uint8
	for i = 0; i < 5; i++ {
		PortTulisbyte(sequencerIndeksport, i)
		PortTulisbyte(sequencerdataport, register[regIndeks])
		regIndeks++
	}

	PortTulisbyte(crtcIndeksport, 0x03)

	PortTulisbyte(crtcdataport, (PortBacabyte(crtcdataport) | 0x80))
	PortTulisbyte(crtcIndeksport, 0x11)
	PortTulisbyte(crtcdataport, (PortBacabyte(crtcdataport) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortTulisbyte(crtcIndeksport, i)
		PortTulisbyte(crtcdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 9; i++ {
		PortTulisbyte(grafikcontrollerIndeksport, i)
		PortTulisbyte(grafikcontrollerdataport, register[regIndeks])
		regIndeks++
	}

	for i = 0; i < 21; i++ {
		PortBacabyte(atributcontrollerTetapSemulaport)
		PortTulisbyte(atributcontrollerIndeksport, i)
		PortTulisbyte(atributcontrollerTulisport, register[regIndeks])
		regIndeks++
	}

	PortBacabyte(atributcontrollerTetapSemulaport)
	PortTulisbyte(atributcontrollerIndeksport, 0x20)

}

func (diri *TVideoGrafikTatasusunan) GetBingkaibuffersegment() uintptr {
	PortTulisbyte(grafikcontrollerIndeksport, 0x06)
	var segmentNOMBOR uint8 = ((PortBacabyte(grafikcontrollerdataport) >> 2) & 0x03)
	switch segmentNOMBOR {
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
func (diri *TVideoGrafikTatasusunan) Putpixel(x uint32, y uint32, warnaIndeks uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = diri.GetBingkaibuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = warnaIndeks

}
func (diri *TVideoGrafikTatasusunan) GetWarnaIndeks(r uint8, g uint8, b uint8) uint8 {
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
func (diri *TVideoGrafikTatasusunan) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	diri.Putpixel(x, y, diri.GetWarnaIndeks(r, g, b))
}
func (diri *TVideoGrafikTatasusunan) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			diri.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (diri *TVideoGrafikTatasusunan) Sokonganmod(lebar uint32, tinggi uint32, warnadepth uint32) bool {
	return lebar == 320 && tinggi == 200 && warnadepth == 8
}
func (diri *TVideoGrafikTatasusunan) Tetapkanmod(lebar uint32, tinggi uint32, warnadepth uint32) bool {
	if !diri.Sokonganmod(lebar, tinggi, warnadepth) {
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

	diri.Tulisregister(g320x200x256)

	return true
}
