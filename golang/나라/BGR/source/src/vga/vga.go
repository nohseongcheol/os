package vga

import . "unsafe"
import . "порт"

type TВидеоГрафикаМасив struct {
}

var micsПорт uint16 = 0x3c2
var crtcСъдържаниеПорт uint16 = 0x3d4
var crtcdataПорт uint16 = 0x3d5
var sequencerСъдържаниеПорт uint16 = 0x3c4
var sequencerdataПорт uint16 = 0x3c5
var графикаcontrollerСъдържаниеПорт uint16 = 0x3ce
var графикаcontrollerdataПорт uint16 = 0x3cf
var атрибутcontrollerСъдържаниеПорт uint16 = 0x3c0
var атрибутcontrollerЧетенеПорт uint16 = 0x3c1
var атрибутcontrollerПисанеПорт uint16 = 0x3c0
var атрибутcontrollerВъзстановяванеПорт uint16 = 0x3da

func (себеси *TВидеоГрафикаМасив) Писанеregister(register []byte) {
	var regСъдържание uint16 = 0

	ПортПисанеbyte(micsПорт, register[regСъдържание])
	regСъдържание++

	var i uint8
	for i = 0; i < 5; i++ {
		ПортПисанеbyte(sequencerСъдържаниеПорт, i)
		ПортПисанеbyte(sequencerdataПорт, register[regСъдържание])
		regСъдържание++
	}

	ПортПисанеbyte(crtcСъдържаниеПорт, 0x03)

	ПортПисанеbyte(crtcdataПорт, (ПортЧетенеbyte(crtcdataПорт) | 0x80))
	ПортПисанеbyte(crtcСъдържаниеПорт, 0x11)
	ПортПисанеbyte(crtcdataПорт, (ПортЧетенеbyte(crtcdataПорт) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ПортПисанеbyte(crtcСъдържаниеПорт, i)
		ПортПисанеbyte(crtcdataПорт, register[regСъдържание])
		regСъдържание++
	}

	for i = 0; i < 9; i++ {
		ПортПисанеbyte(графикаcontrollerСъдържаниеПорт, i)
		ПортПисанеbyte(графикаcontrollerdataПорт, register[regСъдържание])
		regСъдържание++
	}

	for i = 0; i < 21; i++ {
		ПортЧетенеbyte(атрибутcontrollerВъзстановяванеПорт)
		ПортПисанеbyte(атрибутcontrollerСъдържаниеПорт, i)
		ПортПисанеbyte(атрибутcontrollerПисанеПорт, register[regСъдържание])
		regСъдържание++
	}

	ПортЧетенеbyte(атрибутcontrollerВъзстановяванеПорт)
	ПортПисанеbyte(атрибутcontrollerСъдържаниеПорт, 0x20)

}

func (себеси *TВидеоГрафикаМасив) GetРамкаbuffersegment() uintptr {
	ПортПисанеbyte(графикаcontrollerСъдържаниеПорт, 0x06)
	var segmentЧисло uint8 = ((ПортЧетенеbyte(графикаcontrollerdataПорт) >> 2) & 0x03)
	switch segmentЧисло {
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
func (себеси *TВидеоГрафикаМасив) Putpixel(x uint32, y uint32, цвятСъдържание uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = себеси.GetРамкаbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = цвятСъдържание

}
func (себеси *TВидеоГрафикаМасив) GetЦвятСъдържание(r uint8, g uint8, b uint8) uint8 {
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
func (себеси *TВидеоГрафикаМасив) PutpixelОсновницветове(x uint32, y uint32, r uint8, g uint8, b uint8) {
	себеси.Putpixel(x, y, себеси.GetЦвятСъдържание(r, g, b))
}
func (себеси *TВидеоГрафикаМасив) FillПравоъгълник(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			себеси.PutpixelОсновницветове(X, Y, r, g, b)
		}
	}
}
func (себеси *TВидеоГрафикаМасив) ПоддръжкаРЕЖИМ(широчина uint32, височина uint32, цвятdepth uint32) bool {
	return широчина == 320 && височина == 200 && цвятdepth == 8
}
func (себеси *TВидеоГрафикаМасив) ЗадайРЕЖИМ(широчина uint32, височина uint32, цвятdepth uint32) bool {
	if !себеси.ПоддръжкаРЕЖИМ(широчина, височина, цвятdepth) {
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

	себеси.Писанеregister(g320x200x256)

	return true
}
