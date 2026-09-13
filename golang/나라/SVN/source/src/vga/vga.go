package vga

import . "unsafe"
import . "vrata"

type TVideoGrafikaPolje struct {
}

var micsVrata uint16 = 0x3c2
var crtcKazaloVrata uint16 = 0x3d4
var crtcdataVrata uint16 = 0x3d5
var sequencerKazaloVrata uint16 = 0x3c4
var sequencerdataVrata uint16 = 0x3c5
var grafikacontrollerKazaloVrata uint16 = 0x3ce
var grafikacontrollerdataVrata uint16 = 0x3cf
var atributcontrollerKazaloVrata uint16 = 0x3c0
var atributcontrollerBranjeVrata uint16 = 0x3c1
var atributcontrollerPisanjeVrata uint16 = 0x3c0
var atributcontrollerPonastaviVrata uint16 = 0x3da

func (sam *TVideoGrafikaPolje) Pisanjeregister(register []byte) {
	var regKazalo uint16 = 0

	VrataPisanjebyte(micsVrata, register[regKazalo])
	regKazalo++

	var i uint8
	for i = 0; i < 5; i++ {
		VrataPisanjebyte(sequencerKazaloVrata, i)
		VrataPisanjebyte(sequencerdataVrata, register[regKazalo])
		regKazalo++
	}

	VrataPisanjebyte(crtcKazaloVrata, 0x03)

	VrataPisanjebyte(crtcdataVrata, (VrataBranjebyte(crtcdataVrata) | 0x80))
	VrataPisanjebyte(crtcKazaloVrata, 0x11)
	VrataPisanjebyte(crtcdataVrata, (VrataBranjebyte(crtcdataVrata) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		VrataPisanjebyte(crtcKazaloVrata, i)
		VrataPisanjebyte(crtcdataVrata, register[regKazalo])
		regKazalo++
	}

	for i = 0; i < 9; i++ {
		VrataPisanjebyte(grafikacontrollerKazaloVrata, i)
		VrataPisanjebyte(grafikacontrollerdataVrata, register[regKazalo])
		regKazalo++
	}

	for i = 0; i < 21; i++ {
		VrataBranjebyte(atributcontrollerPonastaviVrata)
		VrataPisanjebyte(atributcontrollerKazaloVrata, i)
		VrataPisanjebyte(atributcontrollerPisanjeVrata, register[regKazalo])
		regKazalo++
	}

	VrataBranjebyte(atributcontrollerPonastaviVrata)
	VrataPisanjebyte(atributcontrollerKazaloVrata, 0x20)

}

func (sam *TVideoGrafikaPolje) GetOkvirbuffersegment() uintptr {
	VrataPisanjebyte(grafikacontrollerKazaloVrata, 0x06)
	var segmentŠtevilka uint8 = ((VrataBranjebyte(grafikacontrollerdataVrata) >> 2) & 0x03)
	switch segmentŠtevilka {
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
func (sam *TVideoGrafikaPolje) Putpixel(x uint32, y uint32, barvaKazalo uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = sam.GetOkvirbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = barvaKazalo

}
func (sam *TVideoGrafikaPolje) GetBarvaKazalo(r uint8, g uint8, b uint8) uint8 {
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
func (sam *TVideoGrafikaPolje) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	sam.Putpixel(x, y, sam.GetBarvaKazalo(r, g, b))
}
func (sam *TVideoGrafikaPolje) FillPravokotnik(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			sam.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (sam *TVideoGrafikaPolje) PodrobnostiNAČIN(širina uint32, višina uint32, barvadepth uint32) bool {
	return širina == 320 && višina == 200 && barvadepth == 8
}
func (sam *TVideoGrafikaPolje) MnožicaNAČIN(širina uint32, višina uint32, barvadepth uint32) bool {
	if !sam.PodrobnostiNAČIN(širina, višina, barvadepth) {
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

	sam.Pisanjeregister(g320x200x256)

	return true
}
