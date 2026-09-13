package こんそーる

import . "unsafe"

const (
	fbはば			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type Tこんそーる struct {
	xはいち	uint16
	yはいち	uint16
}

var ちょくれつじゅんびOK bool

func Sちょくれつinit()
func Sちょくれつかきこみばいと(でーた uint8)

func Mちょくれつろぐinit() {
	Sちょくれつinit()
	ちょくれつじゅんびOK = true
}

func ちょくれつろぐばいと(でーた byte) {
	if !ちょくれつじゅんびOK {
		return
	}

	if でーた == '\n' {
		Sちょくれつかきこみばいと('\r')
	}
	Sちょくれつかきこみばいと(uint8(でーた))
}

func MEmergencyろぐもじれつ(でーた string) {
	for i := 0; i < len(でーた); i++ {
		ちょくれつろぐばいと(でーた[i])
	}
}

func MEmergencyろぐhexadecimal8(でーた uint8) {
	const digits = "0123456789ABCDEF"
	ちょくれつろぐばいと(digits[(でーた>>4)&0x0F])
	ちょくれつろぐばいと(digits[でーた&0x0F])
}

func MEmergencyろぐunsignedinteger32(でーた uint32) {
	MEmergencyろぐhexadecimal8(uint8(でーた >> 24))
	MEmergencyろぐhexadecimal8(uint8(でーた >> 16))
	MEmergencyろぐhexadecimal8(uint8(でーた >> 8))
	MEmergencyろぐhexadecimal8(uint8(でーた))
}

func (self *Tこんそーる) Mいんさつ(argumentあたい ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var あたい_2 interface{}

	for i, p := range argumentあたい {
		switch i {
		case 0:
			param, _ := p.(interface{})
			あたい_2 = param
		case 1:
			switch p.(type) {
			case uint16:
				param, _ := p.(uint16)
				x = param
			case int:
				param, _ := p.(int)
				x = uint16(param)
			}
		case 2:
			switch p.(type) {
			case uint16:
				param, _ := p.(uint16)
				y = param
			case int:
				param, _ := p.(int)
				y = uint16(param)
			}
		}
	}

	self.Mいんさつxy(あたい_2, x, y)

}
func (self *Tこんそーる) Mいんさつxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		でーた_2, _ := temporary_2.(string)
		self.Mいんさつばいとxy(([]byte)(でーた_2), x, y)
	case uint8:
		でーた_2, _ := temporary_2.(uint8)
		self.MHexadecimalいんさつxy(でーた_2, x, y)
	case uint16:
		でーた_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16いんさつxy(でーた_2, x, y)
	case uint32:
		でーた_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32いんさつxy(でーた_2, x, y)
	case uint64:
		でーた_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64いんさつxy(でーた_2, x, y)
	default:
		でーた_2, _ := temporary_2.([]byte)
		self.Mいんさつばいとxy(でーた_2, x, y)
	}

}
func (self *Tこんそーる) Mいんさつばいとxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xはいち = x
	}
	if y <= 999 {
		self.yはいち = y
	}

	ぞくせい := uint16(0x0F)
	せいげん := len(buffer)
	if せいげん > 4096 {
		せいげん = 4096
	}
	for i := 0; i < せいげん; i++ {
		ちょくれつろぐばいと(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yはいち++
			self.xはいち = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yはいち+self.xはいち)*2))) = ぞくせい<<8 | uint16(buffer[i])
			self.xはいち++
		}

		if self.xはいち >= 80 {
			self.yはいち++
			self.xはいち = 0
		}

		if self.yはいち >= 25 {
			for self.yはいち = 0; self.yはいち < 25; self.yはいち++ {
				for self.xはいち = 0; self.xはいち < 80; self.xはいち++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yはいち+self.xはいち)*2))) = ぞくせい<<8 | ' '
				}
			}
			self.xはいち = 0
			self.yはいち = 0
		}

	}

}
func (self *Tこんそーる) MHexadecimalいんさつ(かぎ uint8) {
	buffer := []byte{'0', '0'}
	あたい16すすむ := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = あたい16すすむ[(かぎ>>4)&0xF]
	buffer[1] = あたい16すすむ[かぎ&0xF]
	self.Mいんさつ(buffer)
}
func (self *Tこんそーる) MHexadecimalいんさつxy(かぎ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	あたい16すすむ := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = あたい16すすむ[(かぎ>>4)&0xF]
	buffer[1] = あたい16すすむ[かぎ&0xF]
	self.Mいんさつxy(buffer, x, y)
}
func (self *Tこんそーる) MUnsignedinteger16いんさつ(かぎ uint16) {
	self.MHexadecimalいんさつ(uint8(かぎ >> 8))
	self.MHexadecimalいんさつ(uint8(かぎ))
}
func (self *Tこんそーる) MUnsignedinteger16いんさつxy(かぎ uint16, x uint16, y uint16) {
	self.MHexadecimalいんさつxy(uint8(かぎ>>8), x, y)
	self.MHexadecimalいんさつxy(uint8(かぎ), x, y)
}
func (self *Tこんそーる) MUnsignedinteger32いんさつ(でーた uint32) {
	self.MHexadecimalいんさつ(uint8(でーた >> 24))
	self.MHexadecimalいんさつ(uint8(でーた >> 16))
	self.MHexadecimalいんさつ(uint8(でーた >> 8))
	self.MHexadecimalいんさつ(uint8(でーた))
}
func (self *Tこんそーる) MUnsignedinteger32いんさつxy(でーた uint32, x uint16, y uint16) {

	self.MHexadecimalいんさつxy(uint8(でーた>>24), x+0, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>16), x+2, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>8), x+4, y)
	self.MHexadecimalいんさつxy(uint8(でーた), x+6, y)
}
func (self *Tこんそーる) MUnsignedinteger64いんさつ(でーた uint64) {
	self.MHexadecimalいんさつ(uint8(でーた >> 56))
	self.MHexadecimalいんさつ(uint8(でーた >> 48))
	self.MHexadecimalいんさつ(uint8(でーた >> 40))
	self.MHexadecimalいんさつ(uint8(でーた >> 32))
	self.MHexadecimalいんさつ(uint8(でーた >> 24))
	self.MHexadecimalいんさつ(uint8(でーた >> 16))
	self.MHexadecimalいんさつ(uint8(でーた >> 8))
	self.MHexadecimalいんさつ(uint8(でーた))
}
func (self *Tこんそーる) MUnsignedinteger64いんさつxy(でーた uint64, x uint16, y uint16) {
	self.MHexadecimalいんさつxy(uint8(でーた>>56), x+0, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>48), x+2, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>40), x+4, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>32), x+6, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>24), x+8, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>16), x+10, y)
	self.MHexadecimalいんさつxy(uint8(でーた>>8), x+12, y)
	self.MHexadecimalいんさつxy(uint8(でーた), x+14, y)
}
func Mいんさつ(phyaddr uintptr, でーた uint8, x uint32, y uint32)

func (self *Tこんそーる) Mいんさつhexadecimal(でーた uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	あたい16すすむ := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = あたい16すすむ[(でーた>>4)&0xF]
	buffer[1] = あたい16すすむ[でーた&0xF]

	Mいんさつ(uintptr(fbphysaddress), buffer[0], x, y)
	Mいんさつ(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *Tこんそーる) Mいんさつunsignedinteger16(でーた uint16, x uint32, y uint32) {
	self.Mいんさつhexadecimal(uint8(でーた>>8), x+0*2, y)
	self.Mいんさつhexadecimal(uint8(でーた), x+2*2, y)
}

func (self *Tこんそーる) Mいんさつunsignedinteger32(でーた uint32, x uint32, y uint32) {
	x = x * 2
	self.Mいんさつhexadecimal(uint8(でーた>>24), x+0*2, y)
	self.Mいんさつhexadecimal(uint8(でーた>>16), x+2*2, y)
	self.Mいんさつhexadecimal(uint8(でーた>>8), x+4*2, y)
	self.Mいんさつhexadecimal(uint8(でーた), x+6*2, y)
}

func (self *Tこんそーる) M테스트() {
}
