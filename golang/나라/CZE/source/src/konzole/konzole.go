/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konzole

import . "unsafe"

const (
	fbŠířka			= 80
	fbVýška			= 25
	fbphysAdresa	uintptr	= 0xb8000
)

type TKonzole struct {
	xUmístění	uint16
	yUmístění	uint16
}

var sériovýPřipraven bool

func Sériovýinit()
func SériovýZápisbyte(data uint8)

func MSériovýProtokolinit() {
	Sériovýinit()
	sériovýPřipraven = true
}

func sériovýProtokolbyte(data byte) {
	if !sériovýPřipraven {
		return
	}

	if data == '\n' {
		SériovýZápisbyte('\r')
	}
	SériovýZápisbyte(uint8(data))
}

func MEmergencyProtokolřetězec(data string) {
	for i := 0; i < len(data); i++ {
		sériovýProtokolbyte(data[i])
	}
}

func MEmergencyProtokolhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sériovýProtokolbyte(digits[(data>>4)&0x0F])
	sériovýProtokolbyte(digits[data&0x0F])
}

func MEmergencyProtokolunsignedinteger32(data uint32) {
	MEmergencyProtokolhexadecimal8(uint8(data >> 24))
	MEmergencyProtokolhexadecimal8(uint8(data >> 16))
	MEmergencyProtokolhexadecimal8(uint8(data >> 8))
	MEmergencyProtokolhexadecimal8(uint8(data))
}

func (self *TKonzole) MTisknout(argumentHodnota ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var hodnota_2 interface{}

	for i, p := range argumentHodnota {
		switch i {
		case 0:
			param, _ := p.(interface{})
			hodnota_2 = param
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

	self.MTisknoutxy(hodnota_2, x, y)

}
func (self *TKonzole) MTisknoutxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MTisknoutBytůxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalTisknoutxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Tisknoutxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Tisknoutxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Tisknoutxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MTisknoutBytůxy(data_2, x, y)
	}

}
func (self *TKonzole) MTisknoutBytůxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xUmístění = x
	}
	if y <= 999 {
		self.yUmístění = y
	}

	atribut := uint16(0x0F)
	omezení := len(buffer)
	if omezení > 4096 {
		omezení = 4096
	}
	for i := 0; i < omezení; i++ {
		sériovýProtokolbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yUmístění++
			self.xUmístění = 0
		default:
			*(*uint16)(Pointer(fbphysAdresa + uintptr((80*self.yUmístění+self.xUmístění)*2))) = atribut<<8 | uint16(buffer[i])
			self.xUmístění++
		}

		if self.xUmístění >= 80 {
			self.yUmístění++
			self.xUmístění = 0
		}

		if self.yUmístění >= 25 {
			for self.yUmístění = 0; self.yUmístění < 25; self.yUmístění++ {
				for self.xUmístění = 0; self.xUmístění < 80; self.xUmístění++ {
					*(*uint16)(Pointer(fbphysAdresa + uintptr((80*self.yUmístění+self.xUmístění)*2))) = atribut<<8 | ' '
				}
			}
			self.xUmístění = 0
			self.yUmístění = 0
		}

	}

}
func (self *TKonzole) MHexadecimalTisknout(klíč uint8) {
	buffer := []byte{'0', '0'}
	šestnáctkově := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnáctkově[(klíč>>4)&0xF]
	buffer[1] = šestnáctkově[klíč&0xF]
	self.MTisknout(buffer)
}
func (self *TKonzole) MHexadecimalTisknoutxy(klíč uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	šestnáctkově := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnáctkově[(klíč>>4)&0xF]
	buffer[1] = šestnáctkově[klíč&0xF]
	self.MTisknoutxy(buffer, x, y)
}
func (self *TKonzole) MUnsignedinteger16Tisknout(klíč uint16) {
	self.MHexadecimalTisknout(uint8(klíč >> 8))
	self.MHexadecimalTisknout(uint8(klíč))
}
func (self *TKonzole) MUnsignedinteger16Tisknoutxy(klíč uint16, x uint16, y uint16) {
	self.MHexadecimalTisknoutxy(uint8(klíč>>8), x, y)
	self.MHexadecimalTisknoutxy(uint8(klíč), x, y)
}
func (self *TKonzole) MUnsignedinteger32Tisknout(data uint32) {
	self.MHexadecimalTisknout(uint8(data >> 24))
	self.MHexadecimalTisknout(uint8(data >> 16))
	self.MHexadecimalTisknout(uint8(data >> 8))
	self.MHexadecimalTisknout(uint8(data))
}
func (self *TKonzole) MUnsignedinteger32Tisknoutxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalTisknoutxy(uint8(data>>24), x+0, y)
	self.MHexadecimalTisknoutxy(uint8(data>>16), x+2, y)
	self.MHexadecimalTisknoutxy(uint8(data>>8), x+4, y)
	self.MHexadecimalTisknoutxy(uint8(data), x+6, y)
}
func (self *TKonzole) MUnsignedinteger64Tisknout(data uint64) {
	self.MHexadecimalTisknout(uint8(data >> 56))
	self.MHexadecimalTisknout(uint8(data >> 48))
	self.MHexadecimalTisknout(uint8(data >> 40))
	self.MHexadecimalTisknout(uint8(data >> 32))
	self.MHexadecimalTisknout(uint8(data >> 24))
	self.MHexadecimalTisknout(uint8(data >> 16))
	self.MHexadecimalTisknout(uint8(data >> 8))
	self.MHexadecimalTisknout(uint8(data))
}
func (self *TKonzole) MUnsignedinteger64Tisknoutxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalTisknoutxy(uint8(data>>56), x+0, y)
	self.MHexadecimalTisknoutxy(uint8(data>>48), x+2, y)
	self.MHexadecimalTisknoutxy(uint8(data>>40), x+4, y)
	self.MHexadecimalTisknoutxy(uint8(data>>32), x+6, y)
	self.MHexadecimalTisknoutxy(uint8(data>>24), x+8, y)
	self.MHexadecimalTisknoutxy(uint8(data>>16), x+10, y)
	self.MHexadecimalTisknoutxy(uint8(data>>8), x+12, y)
	self.MHexadecimalTisknoutxy(uint8(data), x+14, y)
}
func MTisknout(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TKonzole) MTisknouthexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	šestnáctkově := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnáctkově[(data>>4)&0xF]
	buffer[1] = šestnáctkově[data&0xF]

	MTisknout(uintptr(fbphysAdresa), buffer[0], x, y)
	MTisknout(uintptr(fbphysAdresa), buffer[1], x+2, y)
}

func (self *TKonzole) MTisknoutunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MTisknouthexadecimal(uint8(data>>8), x+0*2, y)
	self.MTisknouthexadecimal(uint8(data), x+2*2, y)
}

func (self *TKonzole) MTisknoutunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MTisknouthexadecimal(uint8(data>>24), x+0*2, y)
	self.MTisknouthexadecimal(uint8(data>>16), x+2*2, y)
	self.MTisknouthexadecimal(uint8(data>>8), x+4*2, y)
	self.MTisknouthexadecimal(uint8(data), x+6*2, y)
}

func (self *TKonzole) M테스트() {
}
