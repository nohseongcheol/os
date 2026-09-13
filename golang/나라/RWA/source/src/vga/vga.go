package vga

import . "unsafe"
import . "umuyoboro"

type TInyerekanamashushoIbishushanyoImbonerahamwe struct {
}

var micsUmuyoboro uint16 = 0x3c2
var crtcUmubarendangaUmuyoboro uint16 = 0x3d4
var crtcdataUmuyoboro uint16 = 0x3d5
var sequencerUmubarendangaUmuyoboro uint16 = 0x3c4
var sequencerdataUmuyoboro uint16 = 0x3c5
var ibishushanyocontrollerUmubarendangaUmuyoboro uint16 = 0x3ce
var ibishushanyocontrollerdataUmuyoboro uint16 = 0x3cf
var attributecontrollerUmubarendangaUmuyoboro uint16 = 0x3c0
var attributecontrollergusomaUmuyoboro uint16 = 0x3c1
var attributecontrollerkwandikaUmuyoboro uint16 = 0x3c0
var attributecontrollerKugaruraUmuyoboro uint16 = 0x3da

func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) Kwandikaregister(register []byte) {
	var regUmubarendanga uint16 = 0

	Umuyoborokwandikabyte(micsUmuyoboro, register[regUmubarendanga])
	regUmubarendanga++

	var i uint8
	for i = 0; i < 5; i++ {
		Umuyoborokwandikabyte(sequencerUmubarendangaUmuyoboro, i)
		Umuyoborokwandikabyte(sequencerdataUmuyoboro, register[regUmubarendanga])
		regUmubarendanga++
	}

	Umuyoborokwandikabyte(crtcUmubarendangaUmuyoboro, 0x03)

	Umuyoborokwandikabyte(crtcdataUmuyoboro, (Umuyoborogusomabyte(crtcdataUmuyoboro) | 0x80))
	Umuyoborokwandikabyte(crtcUmubarendangaUmuyoboro, 0x11)
	Umuyoborokwandikabyte(crtcdataUmuyoboro, (Umuyoborogusomabyte(crtcdataUmuyoboro) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Umuyoborokwandikabyte(crtcUmubarendangaUmuyoboro, i)
		Umuyoborokwandikabyte(crtcdataUmuyoboro, register[regUmubarendanga])
		regUmubarendanga++
	}

	for i = 0; i < 9; i++ {
		Umuyoborokwandikabyte(ibishushanyocontrollerUmubarendangaUmuyoboro, i)
		Umuyoborokwandikabyte(ibishushanyocontrollerdataUmuyoboro, register[regUmubarendanga])
		regUmubarendanga++
	}

	for i = 0; i < 21; i++ {
		Umuyoborogusomabyte(attributecontrollerKugaruraUmuyoboro)
		Umuyoborokwandikabyte(attributecontrollerUmubarendangaUmuyoboro, i)
		Umuyoborokwandikabyte(attributecontrollerkwandikaUmuyoboro, register[regUmubarendanga])
		regUmubarendanga++
	}

	Umuyoborogusomabyte(attributecontrollerKugaruraUmuyoboro)
	Umuyoborokwandikabyte(attributecontrollerUmubarendangaUmuyoboro, 0x20)

}

func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) GetIkadiribuffersegment() uintptr {
	Umuyoborokwandikabyte(ibishushanyocontrollerUmubarendangaUmuyoboro, 0x06)
	var segmentnumber uint8 = ((Umuyoborogusomabyte(ibishushanyocontrollerdataUmuyoboro) >> 2) & 0x03)
	switch segmentnumber {
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
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) Putpixel(x uint32, y uint32, colorUmubarendanga uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.GetIkadiribuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = colorUmubarendanga

}
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) GetcolorUmubarendanga(r uint8, g uint8, b uint8) uint8 {
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
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetcolorUmubarendanga(r, g, b))
}
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) SupportUbwoko(ubugari uint32, ubuhagarike uint32, colordepth uint32) bool {
	return ubugari == 320 && ubuhagarike == 200 && colordepth == 8
}
func (self *TInyerekanamashushoIbishushanyoImbonerahamwe) SetUbwoko(ubugari uint32, ubuhagarike uint32, colordepth uint32) bool {
	if !self.SupportUbwoko(ubugari, ubuhagarike, colordepth) {
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

	self.Kwandikaregister(g320x200x256)

	return true
}
