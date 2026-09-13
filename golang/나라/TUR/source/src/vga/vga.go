package vga

import . "unsafe"
import . "bağlantıNoktası"

type TGörüntüGrafiklerDizi struct {
}

var micsBağlantıNoktası uint16 = 0x3c2
var crtcİçindekilerBağlantıNoktası uint16 = 0x3d4
var crtcdataBağlantıNoktası uint16 = 0x3d5
var sequencerİçindekilerBağlantıNoktası uint16 = 0x3c4
var sequencerdataBağlantıNoktası uint16 = 0x3c5
var grafiklerDenetleyiciİçindekilerBağlantıNoktası uint16 = 0x3ce
var grafiklerDenetleyicidataBağlantıNoktası uint16 = 0x3cf
var öznitelikDenetleyiciİçindekilerBağlantıNoktası uint16 = 0x3c0
var öznitelikDenetleyiciOkumaBağlantıNoktası uint16 = 0x3c1
var öznitelikDenetleyiciYazmaBağlantıNoktası uint16 = 0x3c0
var öznitelikDenetleyiciSıfırlaBağlantıNoktası uint16 = 0x3da

func (self *TGörüntüGrafiklerDizi) Yazmaregister(register []byte) {
	var regİçindekiler uint16 = 0

	BağlantıNoktasıYazmabyte(micsBağlantıNoktası, register[regİçindekiler])
	regİçindekiler++

	var i uint8
	for i = 0; i < 5; i++ {
		BağlantıNoktasıYazmabyte(sequencerİçindekilerBağlantıNoktası, i)
		BağlantıNoktasıYazmabyte(sequencerdataBağlantıNoktası, register[regİçindekiler])
		regİçindekiler++
	}

	BağlantıNoktasıYazmabyte(crtcİçindekilerBağlantıNoktası, 0x03)

	BağlantıNoktasıYazmabyte(crtcdataBağlantıNoktası, (BağlantıNoktasıOkumabyte(crtcdataBağlantıNoktası) | 0x80))
	BağlantıNoktasıYazmabyte(crtcİçindekilerBağlantıNoktası, 0x11)
	BağlantıNoktasıYazmabyte(crtcdataBağlantıNoktası, (BağlantıNoktasıOkumabyte(crtcdataBağlantıNoktası) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		BağlantıNoktasıYazmabyte(crtcİçindekilerBağlantıNoktası, i)
		BağlantıNoktasıYazmabyte(crtcdataBağlantıNoktası, register[regİçindekiler])
		regİçindekiler++
	}

	for i = 0; i < 9; i++ {
		BağlantıNoktasıYazmabyte(grafiklerDenetleyiciİçindekilerBağlantıNoktası, i)
		BağlantıNoktasıYazmabyte(grafiklerDenetleyicidataBağlantıNoktası, register[regİçindekiler])
		regİçindekiler++
	}

	for i = 0; i < 21; i++ {
		BağlantıNoktasıOkumabyte(öznitelikDenetleyiciSıfırlaBağlantıNoktası)
		BağlantıNoktasıYazmabyte(öznitelikDenetleyiciİçindekilerBağlantıNoktası, i)
		BağlantıNoktasıYazmabyte(öznitelikDenetleyiciYazmaBağlantıNoktası, register[regİçindekiler])
		regİçindekiler++
	}

	BağlantıNoktasıOkumabyte(öznitelikDenetleyiciSıfırlaBağlantıNoktası)
	BağlantıNoktasıYazmabyte(öznitelikDenetleyiciİçindekilerBağlantıNoktası, 0x20)

}

func (self *TGörüntüGrafiklerDizi) GetÇerçevebuffersegment() uintptr {
	BağlantıNoktasıYazmabyte(grafiklerDenetleyiciİçindekilerBağlantıNoktası, 0x06)
	var segmentSayı uint8 = ((BağlantıNoktasıOkumabyte(grafiklerDenetleyicidataBağlantıNoktası) >> 2) & 0x03)
	switch segmentSayı {
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
func (self *TGörüntüGrafiklerDizi) Putpixel(x uint32, y uint32, renkİçindekiler uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.GetÇerçevebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = renkİçindekiler

}
func (self *TGörüntüGrafiklerDizi) GetRenkİçindekiler(r uint8, g uint8, b uint8) uint8 {
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
func (self *TGörüntüGrafiklerDizi) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetRenkİçindekiler(r, g, b))
}
func (self *TGörüntüGrafiklerDizi) FillDikdörtgen(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TGörüntüGrafiklerDizi) DestekKİP(genişlik uint32, başlık uint32, renkdepth uint32) bool {
	return genişlik == 320 && başlık == 200 && renkdepth == 8
}
func (self *TGörüntüGrafiklerDizi) AyarlaKİP(genişlik uint32, başlık uint32, renkdepth uint32) bool {
	if !self.DestekKİP(genişlik, başlık, renkdepth) {
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

	self.Yazmaregister(g320x200x256)

	return true
}
