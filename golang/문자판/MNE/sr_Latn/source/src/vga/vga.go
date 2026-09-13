package vga

import . "unsafe"
import . "port"

type TVideografikaNiz struct {
}

var micsPort uint16 = 0x3c2
var crtcPopisPort uint16 = 0x3d4
var crtcdataPort uint16 = 0x3d5
var sequencerPopisPort uint16 = 0x3c4
var sequencerdataPort uint16 = 0x3c5
var grafikacontrollerPopisPort uint16 = 0x3ce
var grafikacontrollerdataPort uint16 = 0x3cf
var atributcontrollerPopisPort uint16 = 0x3c0
var atributcontrollerčitanjePort uint16 = 0x3c1
var atributcontrollerPišePort uint16 = 0x3c0
var atributcontrollerPonovopostaviPort uint16 = 0x3da

func (isti *TVideografikaNiz) Pišeregister(register []byte) {
	var regPopis uint16 = 0

	PortPišebyte(micsPort, register[regPopis])
	regPopis++

	var i uint8
	for i = 0; i < 5; i++ {
		PortPišebyte(sequencerPopisPort, i)
		PortPišebyte(sequencerdataPort, register[regPopis])
		regPopis++
	}

	PortPišebyte(crtcPopisPort, 0x03)

	PortPišebyte(crtcdataPort, (Portčitanjebyte(crtcdataPort) | 0x80))
	PortPišebyte(crtcPopisPort, 0x11)
	PortPišebyte(crtcdataPort, (Portčitanjebyte(crtcdataPort) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortPišebyte(crtcPopisPort, i)
		PortPišebyte(crtcdataPort, register[regPopis])
		regPopis++
	}

	for i = 0; i < 9; i++ {
		PortPišebyte(grafikacontrollerPopisPort, i)
		PortPišebyte(grafikacontrollerdataPort, register[regPopis])
		regPopis++
	}

	for i = 0; i < 21; i++ {
		Portčitanjebyte(atributcontrollerPonovopostaviPort)
		PortPišebyte(atributcontrollerPopisPort, i)
		PortPišebyte(atributcontrollerPišePort, register[regPopis])
		regPopis++
	}

	Portčitanjebyte(atributcontrollerPonovopostaviPort)
	PortPišebyte(atributcontrollerPopisPort, 0x20)

}

func (isti *TVideografikaNiz) GetOkvirbuffersegment() uintptr {
	PortPišebyte(grafikacontrollerPopisPort, 0x06)
	var segmentbroj uint8 = ((Portčitanjebyte(grafikacontrollerdataPort) >> 2) & 0x03)
	switch segmentbroj {
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
func (isti *TVideografikaNiz) Putpixel(x uint32, y uint32, bojaPopis uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = isti.GetOkvirbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = bojaPopis

}
func (isti *TVideografikaNiz) GetBojaPopis(r uint8, g uint8, b uint8) uint8 {
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
func (isti *TVideografikaNiz) PutpixelCZP(x uint32, y uint32, r uint8, g uint8, b uint8) {
	isti.Putpixel(x, y, isti.GetBojaPopis(r, g, b))
}
func (isti *TVideografikaNiz) FillPravougaonik(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			isti.PutpixelCZP(X, Y, r, g, b)
		}
	}
}
func (isti *TVideografikaNiz) PodrškaREŽIM(širina uint32, visina uint32, bojadepth uint32) bool {
	return širina == 320 && visina == 200 && bojadepth == 8
}
func (isti *TVideografikaNiz) SkupREŽIM(širina uint32, visina uint32, bojadepth uint32) bool {
	if !isti.PodrškaREŽIM(širina, visina, bojadepth) {
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

	isti.Pišeregister(g320x200x256)

	return true
}
