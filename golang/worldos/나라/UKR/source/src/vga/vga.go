/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "порт"

type TВідеоГрафікаМасив struct {
}

var micsПорт uint16 = 0x3c2
var crtcІндексПорт uint16 = 0x3d4
var crtcdataПорт uint16 = 0x3d5
var sequencerІндексПорт uint16 = 0x3c4
var sequencerdataПорт uint16 = 0x3c5
var графікаКонтролерІндексПорт uint16 = 0x3ce
var графікаКонтролерdataПорт uint16 = 0x3cf
var ознакаКонтролерІндексПорт uint16 = 0x3c0
var ознакаКонтролерЧитанняПорт uint16 = 0x3c1
var ознакаКонтролерЗаписПорт uint16 = 0x3c0
var ознакаКонтролерСкинутиПорт uint16 = 0x3da

func (поточний *TВідеоГрафікаМасив) Записregister(register []byte) {
	var regІндекс uint16 = 0

	ПортЗаписbyte(micsПорт, register[regІндекс])
	regІндекс++

	var i uint8
	for i = 0; i < 5; i++ {
		ПортЗаписbyte(sequencerІндексПорт, i)
		ПортЗаписbyte(sequencerdataПорт, register[regІндекс])
		regІндекс++
	}

	ПортЗаписbyte(crtcІндексПорт, 0x03)

	ПортЗаписbyte(crtcdataПорт, (ПортЧитанняbyte(crtcdataПорт) | 0x80))
	ПортЗаписbyte(crtcІндексПорт, 0x11)
	ПортЗаписbyte(crtcdataПорт, (ПортЧитанняbyte(crtcdataПорт) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		ПортЗаписbyte(crtcІндексПорт, i)
		ПортЗаписbyte(crtcdataПорт, register[regІндекс])
		regІндекс++
	}

	for i = 0; i < 9; i++ {
		ПортЗаписbyte(графікаКонтролерІндексПорт, i)
		ПортЗаписbyte(графікаКонтролерdataПорт, register[regІндекс])
		regІндекс++
	}

	for i = 0; i < 21; i++ {
		ПортЧитанняbyte(ознакаКонтролерСкинутиПорт)
		ПортЗаписbyte(ознакаКонтролерІндексПорт, i)
		ПортЗаписbyte(ознакаКонтролерЗаписПорт, register[regІндекс])
		regІндекс++
	}

	ПортЧитанняbyte(ознакаКонтролерСкинутиПорт)
	ПортЗаписbyte(ознакаКонтролерІндексПорт, 0x20)

}

func (поточний *TВідеоГрафікаМасив) GetБлокbuffersegment() uintptr {
	ПортЗаписbyte(графікаКонтролерІндексПорт, 0x06)
	var segmentЧисло uint8 = ((ПортЧитанняbyte(графікаКонтролерdataПорт) >> 2) & 0x03)
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
func (поточний *TВідеоГрафікаМасив) Putpixel(x uint32, y uint32, колірІндекс uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelАдреса uintptr = поточний.GetБлокbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelАдреса)) = колірІндекс

}
func (поточний *TВідеоГрафікаМасив) GetКолірІндекс(r uint8, g uint8, b uint8) uint8 {
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
func (поточний *TВідеоГрафікаМасив) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	поточний.Putpixel(x, y, поточний.GetКолірІндекс(r, g, b))
}
func (поточний *TВідеоГрафікаМасив) FillПрямокутник(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			поточний.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (поточний *TВідеоГрафікаМасив) ПідтримкаРЕЖИМ(ширина uint32, висота uint32, колірdepth uint32) bool {
	return ширина == 320 && висота == 200 && колірdepth == 8
}
func (поточний *TВідеоГрафікаМасив) МножинаРЕЖИМ(ширина uint32, висота uint32, колірdepth uint32) bool {
	if !поточний.ПідтримкаРЕЖИМ(ширина, висота, колірdepth) {
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

	поточний.Записregister(g320x200x256)

	return true
}
