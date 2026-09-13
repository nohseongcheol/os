package vga

import . "unsafe"
import . "ports"

type TVideoGrafikaMasīvs struct {
}

var micsPorts uint16 = 0x3c2
var crtcSatursPorts uint16 = 0x3d4
var crtcdataPorts uint16 = 0x3d5
var sequencerSatursPorts uint16 = 0x3c4
var sequencerdataPorts uint16 = 0x3c5
var grafikacontrollerSatursPorts uint16 = 0x3ce
var grafikacontrollerdataPorts uint16 = 0x3cf
var atribūtscontrollerSatursPorts uint16 = 0x3c0
var atribūtscontrollerLasītPorts uint16 = 0x3c1
var atribūtscontrollerRakstītPorts uint16 = 0x3c0
var atribūtscontrollerPārstatītPorts uint16 = 0x3da

func (pats *TVideoGrafikaMasīvs) Rakstītregister(register []byte) {
	var regSaturs uint16 = 0

	PortsRakstītbyte(micsPorts, register[regSaturs])
	regSaturs++

	var i uint8
	for i = 0; i < 5; i++ {
		PortsRakstītbyte(sequencerSatursPorts, i)
		PortsRakstītbyte(sequencerdataPorts, register[regSaturs])
		regSaturs++
	}

	PortsRakstītbyte(crtcSatursPorts, 0x03)

	PortsRakstītbyte(crtcdataPorts, (PortsLasītbyte(crtcdataPorts) | 0x80))
	PortsRakstītbyte(crtcSatursPorts, 0x11)
	PortsRakstītbyte(crtcdataPorts, (PortsLasītbyte(crtcdataPorts) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortsRakstītbyte(crtcSatursPorts, i)
		PortsRakstītbyte(crtcdataPorts, register[regSaturs])
		regSaturs++
	}

	for i = 0; i < 9; i++ {
		PortsRakstītbyte(grafikacontrollerSatursPorts, i)
		PortsRakstītbyte(grafikacontrollerdataPorts, register[regSaturs])
		regSaturs++
	}

	for i = 0; i < 21; i++ {
		PortsLasītbyte(atribūtscontrollerPārstatītPorts)
		PortsRakstītbyte(atribūtscontrollerSatursPorts, i)
		PortsRakstītbyte(atribūtscontrollerRakstītPorts, register[regSaturs])
		regSaturs++
	}

	PortsLasītbyte(atribūtscontrollerPārstatītPorts)
	PortsRakstītbyte(atribūtscontrollerSatursPorts, 0x20)

}

func (pats *TVideoGrafikaMasīvs) GetIetvarsbuffersegment() uintptr {
	PortsRakstītbyte(grafikacontrollerSatursPorts, 0x06)
	var segmentSkaitlis uint8 = ((PortsLasītbyte(grafikacontrollerdataPorts) >> 2) & 0x03)
	switch segmentSkaitlis {
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
func (pats *TVideoGrafikaMasīvs) Putpixel(x uint32, y uint32, krāsaSaturs uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = pats.GetIetvarsbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = krāsaSaturs

}
func (pats *TVideoGrafikaMasīvs) GetKrāsaSaturs(r uint8, g uint8, b uint8) uint8 {
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
func (pats *TVideoGrafikaMasīvs) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	pats.Putpixel(x, y, pats.GetKrāsaSaturs(r, g, b))
}
func (pats *TVideoGrafikaMasīvs) FillTaisnstūris(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			pats.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (pats *TVideoGrafikaMasīvs) SupportRežīms(platums uint32, augstums uint32, krāsadepth uint32) bool {
	return platums == 320 && augstums == 200 && krāsadepth == 8
}
func (pats *TVideoGrafikaMasīvs) KopaRežīms(platums uint32, augstums uint32, krāsadepth uint32) bool {
	if !pats.SupportRežīms(platums, augstums, krāsadepth) {
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

	pats.Rakstītregister(g320x200x256)

	return true
}
