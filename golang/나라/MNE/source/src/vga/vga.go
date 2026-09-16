/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "порт"

type TВидеоgrafikaНиз struct {
}

var micsПорт uint16 = 0x3c2
var crtcPopisПорт uint16 = 0x3d4
var crtcdataПорт uint16 = 0x3d5
var sequencerPopisПорт uint16 = 0x3c4
var sequencerdataПорт uint16 = 0x3c5
var grafikacontrollerPopisПорт uint16 = 0x3ce
var grafikacontrollerdataПорт uint16 = 0x3cf
var atributcontrollerPopisПорт uint16 = 0x3c0
var atributcontrollerчитањеПорт uint16 = 0x3c1
var atributcontrollerupisПорт uint16 = 0x3c0
var atributcontrollerPonovopostaviПорт uint16 = 0x3da

func (isti *TВидеоgrafikaНиз) Upisregister(register []byte) {
	var regPopis uint16 = 0

	Портupisbyte(micsПорт, register[regPopis])
	regPopis++

	var i uint8
	for i = 0; i < 5; i++ {
		Портupisbyte(sequencerPopisПорт, i)
		Портupisbyte(sequencerdataПорт, register[regPopis])
		regPopis++
	}

	Портupisbyte(crtcPopisПорт, 0x03)

	Портupisbyte(crtcdataПорт, (Портчитањеbyte(crtcdataПорт) | 0x80))
	Портupisbyte(crtcPopisПорт, 0x11)
	Портupisbyte(crtcdataПорт, (Портчитањеbyte(crtcdataПорт) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Портupisbyte(crtcPopisПорт, i)
		Портupisbyte(crtcdataПорт, register[regPopis])
		regPopis++
	}

	for i = 0; i < 9; i++ {
		Портupisbyte(grafikacontrollerPopisПорт, i)
		Портupisbyte(grafikacontrollerdataПорт, register[regPopis])
		regPopis++
	}

	for i = 0; i < 21; i++ {
		Портчитањеbyte(atributcontrollerPonovopostaviПорт)
		Портupisbyte(atributcontrollerPopisПорт, i)
		Портupisbyte(atributcontrollerupisПорт, register[regPopis])
		regPopis++
	}

	Портчитањеbyte(atributcontrollerPonovopostaviПорт)
	Портupisbyte(atributcontrollerPopisПорт, 0x20)

}

func (isti *TВидеоgrafikaНиз) GetOkvirbuffersegment() uintptr {
	Портupisbyte(grafikacontrollerPopisПорт, 0x06)
	var segmentброј uint8 = ((Портчитањеbyte(grafikacontrollerdataПорт) >> 2) & 0x03)
	switch segmentброј {
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
func (isti *TВидеоgrafikaНиз) Putpixel(x uint32, y uint32, бојаPopis uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = isti.GetOkvirbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = бојаPopis

}
func (isti *TВидеоgrafikaНиз) GetБојаPopis(r uint8, g uint8, b uint8) uint8 {
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
func (isti *TВидеоgrafikaНиз) PutpixelЦЗП(x uint32, y uint32, r uint8, g uint8, b uint8) {
	isti.Putpixel(x, y, isti.GetБојаPopis(r, g, b))
}
func (isti *TВидеоgrafikaНиз) FillPravougaonik(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			isti.PutpixelЦЗП(X, Y, r, g, b)
		}
	}
}
func (isti *TВидеоgrafikaНиз) PodrškaREŽIM(širina uint32, visina uint32, бојаdepth uint32) bool {
	return širina == 320 && visina == 200 && бојаdepth == 8
}
func (isti *TВидеоgrafikaНиз) СкупREŽIM(širina uint32, visina uint32, бојаdepth uint32) bool {
	if !isti.PodrškaREŽIM(širina, visina, бојаdepth) {
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

	isti.Upisregister(g320x200x256)

	return true
}
