package vga

import . "unsafe"
import . "prievadas"

type TVaizdoįrašaiGrafikaMasyvas struct {
}

var micsPrievadas uint16 = 0x3c2
var crtcRodyklėPrievadas uint16 = 0x3d4
var crtcdataPrievadas uint16 = 0x3d5
var sequencerRodyklėPrievadas uint16 = 0x3c4
var sequencerdataPrievadas uint16 = 0x3c5
var grafikacontrollerRodyklėPrievadas uint16 = 0x3ce
var grafikacontrollerdataPrievadas uint16 = 0x3cf
var atributascontrollerRodyklėPrievadas uint16 = 0x3c0
var atributascontrollerSkaitymasPrievadas uint16 = 0x3c1
var atributascontrollerRašymasPrievadas uint16 = 0x3c0
var atributascontrollerAtstatytiPrievadas uint16 = 0x3da

func (self *TVaizdoįrašaiGrafikaMasyvas) Rašymasregister(register []byte) {
	var regRodyklė uint16 = 0

	PrievadasRašymasbyte(micsPrievadas, register[regRodyklė])
	regRodyklė++

	var i uint8
	for i = 0; i < 5; i++ {
		PrievadasRašymasbyte(sequencerRodyklėPrievadas, i)
		PrievadasRašymasbyte(sequencerdataPrievadas, register[regRodyklė])
		regRodyklė++
	}

	PrievadasRašymasbyte(crtcRodyklėPrievadas, 0x03)

	PrievadasRašymasbyte(crtcdataPrievadas, (PrievadasSkaitymasbyte(crtcdataPrievadas) | 0x80))
	PrievadasRašymasbyte(crtcRodyklėPrievadas, 0x11)
	PrievadasRašymasbyte(crtcdataPrievadas, (PrievadasSkaitymasbyte(crtcdataPrievadas) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PrievadasRašymasbyte(crtcRodyklėPrievadas, i)
		PrievadasRašymasbyte(crtcdataPrievadas, register[regRodyklė])
		regRodyklė++
	}

	for i = 0; i < 9; i++ {
		PrievadasRašymasbyte(grafikacontrollerRodyklėPrievadas, i)
		PrievadasRašymasbyte(grafikacontrollerdataPrievadas, register[regRodyklė])
		regRodyklė++
	}

	for i = 0; i < 21; i++ {
		PrievadasSkaitymasbyte(atributascontrollerAtstatytiPrievadas)
		PrievadasRašymasbyte(atributascontrollerRodyklėPrievadas, i)
		PrievadasRašymasbyte(atributascontrollerRašymasPrievadas, register[regRodyklė])
		regRodyklė++
	}

	PrievadasSkaitymasbyte(atributascontrollerAtstatytiPrievadas)
	PrievadasRašymasbyte(atributascontrollerRodyklėPrievadas, 0x20)

}

func (self *TVaizdoįrašaiGrafikaMasyvas) GetKadrasbuffersegment() uintptr {
	PrievadasRašymasbyte(grafikacontrollerRodyklėPrievadas, 0x06)
	var segmentSkaičius uint8 = ((PrievadasSkaitymasbyte(grafikacontrollerdataPrievadas) >> 2) & 0x03)
	switch segmentSkaičius {
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
func (self *TVaizdoįrašaiGrafikaMasyvas) Putpixel(x uint32, y uint32, spalvaRodyklė uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.GetKadrasbuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = spalvaRodyklė

}
func (self *TVaizdoįrašaiGrafikaMasyvas) GetSpalvaRodyklė(r uint8, g uint8, b uint8) uint8 {
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
func (self *TVaizdoįrašaiGrafikaMasyvas) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetSpalvaRodyklė(r, g, b))
}
func (self *TVaizdoįrašaiGrafikaMasyvas) FillStačiakampis(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *TVaizdoįrašaiGrafikaMasyvas) PalaikymasREŽIMAS(plotis uint32, aukštis uint32, spalvadepth uint32) bool {
	return plotis == 320 && aukštis == 200 && spalvadepth == 8
}
func (self *TVaizdoįrašaiGrafikaMasyvas) NustatytaREŽIMAS(plotis uint32, aukštis uint32, spalvadepth uint32) bool {
	if !self.PalaikymasREŽIMAS(plotis, aukštis, spalvadepth) {
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

	self.Rašymasregister(g320x200x256)

	return true
}
