/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "portti"

type TVideoGrafiikkaTaulukko struct {
}

var micsPortti uint16 = 0x3c2
var crtcHakemistoPortti uint16 = 0x3d4
var crtcdataPortti uint16 = 0x3d5
var sequencerHakemistoPortti uint16 = 0x3c4
var sequencerdataPortti uint16 = 0x3c5
var grafiikkaOhjainHakemistoPortti uint16 = 0x3ce
var grafiikkaOhjaindataPortti uint16 = 0x3cf
var määreOhjainHakemistoPortti uint16 = 0x3c0
var määreOhjainLukuPortti uint16 = 0x3c1
var määreOhjainKirjoitusPortti uint16 = 0x3c0
var määreOhjainPalautaPortti uint16 = 0x3da

func (itse *TVideoGrafiikkaTaulukko) Kirjoitusregister(register []byte) {
	var regHakemisto uint16 = 0

	PorttiKirjoitusbyte(micsPortti, register[regHakemisto])
	regHakemisto++

	var i uint8
	for i = 0; i < 5; i++ {
		PorttiKirjoitusbyte(sequencerHakemistoPortti, i)
		PorttiKirjoitusbyte(sequencerdataPortti, register[regHakemisto])
		regHakemisto++
	}

	PorttiKirjoitusbyte(crtcHakemistoPortti, 0x03)

	PorttiKirjoitusbyte(crtcdataPortti, (PorttiLukubyte(crtcdataPortti) | 0x80))
	PorttiKirjoitusbyte(crtcHakemistoPortti, 0x11)
	PorttiKirjoitusbyte(crtcdataPortti, (PorttiLukubyte(crtcdataPortti) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PorttiKirjoitusbyte(crtcHakemistoPortti, i)
		PorttiKirjoitusbyte(crtcdataPortti, register[regHakemisto])
		regHakemisto++
	}

	for i = 0; i < 9; i++ {
		PorttiKirjoitusbyte(grafiikkaOhjainHakemistoPortti, i)
		PorttiKirjoitusbyte(grafiikkaOhjaindataPortti, register[regHakemisto])
		regHakemisto++
	}

	for i = 0; i < 21; i++ {
		PorttiLukubyte(määreOhjainPalautaPortti)
		PorttiKirjoitusbyte(määreOhjainHakemistoPortti, i)
		PorttiKirjoitusbyte(määreOhjainKirjoitusPortti, register[regHakemisto])
		regHakemisto++
	}

	PorttiLukubyte(määreOhjainPalautaPortti)
	PorttiKirjoitusbyte(määreOhjainHakemistoPortti, 0x20)

}

func (itse *TVideoGrafiikkaTaulukko) GetKehysbuffersegment() uintptr {
	PorttiKirjoitusbyte(grafiikkaOhjainHakemistoPortti, 0x06)
	var segmentNumero uint8 = ((PorttiLukubyte(grafiikkaOhjaindataPortti) >> 2) & 0x03)
	switch segmentNumero {
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
func (itse *TVideoGrafiikkaTaulukko) Putpixel(x uint32, y uint32, väriHakemisto uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = itse.GetKehysbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = väriHakemisto

}
func (itse *TVideoGrafiikkaTaulukko) GetVäriHakemisto(r uint8, g uint8, b uint8) uint8 {
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
func (itse *TVideoGrafiikkaTaulukko) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	itse.Putpixel(x, y, itse.GetVäriHakemisto(r, g, b))
}
func (itse *TVideoGrafiikkaTaulukko) FillNeliö(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			itse.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (itse *TVideoGrafiikkaTaulukko) TukiTILA(leveys uint32, korkeus uint32, väridepth uint32) bool {
	return leveys == 320 && korkeus == 200 && väridepth == 8
}
func (itse *TVideoGrafiikkaTaulukko) AsetaTILA(leveys uint32, korkeus uint32, väridepth uint32) bool {
	if !itse.TukiTILA(leveys, korkeus, väridepth) {
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

	itse.Kirjoitusregister(g320x200x256)

	return true
}
