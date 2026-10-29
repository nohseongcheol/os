/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konzol

import . "unsafe"

const (
	fbSzélesség		= 80
	fbMagasság		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonzol struct {
	xPozíció	uint16
	yPozíció	uint16
}

var sorosKész bool

func Sorosinit()
func SorosÍrásbyte(data uint8)

func MSorosloginit() {
	Sorosinit()
	sorosKész = true
}

func soroslogbyte(data byte) {
	if !sorosKész {
		return
	}

	if data == '\n' {
		SorosÍrásbyte('\r')
	}
	SorosÍrásbyte(uint8(data))
}

func MEmergencylogKarakterlánc(data string) {
	for i := 0; i < len(data); i++ {
		soroslogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	soroslogbyte(digits[(data>>4)&0x0F])
	soroslogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (self *TKonzol) MNyomtatás(argumentÉrték ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var érték_2 interface{}

	for i, p := range argumentÉrték {
		switch i {
		case 0:
			param, _ := p.(interface{})
			érték_2 = param
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

	self.MNyomtatásxy(érték_2, x, y)

}
func (self *TKonzol) MNyomtatásxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MNyomtatásBájtxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalNyomtatásxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Nyomtatásxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Nyomtatásxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Nyomtatásxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MNyomtatásBájtxy(data_2, x, y)
	}

}
func (self *TKonzol) MNyomtatásBájtxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xPozíció = x
	}
	if y <= 999 {
		self.yPozíció = y
	}

	attribútum := uint16(0x0F)
	korlátozás := len(buffer)
	if korlátozás > 4096 {
		korlátozás = 4096
	}
	for i := 0; i < korlátozás; i++ {
		soroslogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yPozíció++
			self.xPozíció = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yPozíció+self.xPozíció)*2))) = attribútum<<8 | uint16(buffer[i])
			self.xPozíció++
		}

		if self.xPozíció >= 80 {
			self.yPozíció++
			self.xPozíció = 0
		}

		if self.yPozíció >= 25 {
			for self.yPozíció = 0; self.yPozíció < 25; self.yPozíció++ {
				for self.xPozíció = 0; self.xPozíció < 80; self.xPozíció++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yPozíció+self.xPozíció)*2))) = attribútum<<8 | ' '
				}
			}
			self.xPozíció = 0
			self.yPozíció = 0
		}

	}

}
func (self *TKonzol) MHexadecimalNyomtatás(billentyű uint8) {
	buffer := []byte{'0', '0'}
	hexadecimális := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimális[(billentyű>>4)&0xF]
	buffer[1] = hexadecimális[billentyű&0xF]
	self.MNyomtatás(buffer)
}
func (self *TKonzol) MHexadecimalNyomtatásxy(billentyű uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hexadecimális := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimális[(billentyű>>4)&0xF]
	buffer[1] = hexadecimális[billentyű&0xF]
	self.MNyomtatásxy(buffer, x, y)
}
func (self *TKonzol) MUnsignedinteger16Nyomtatás(billentyű uint16) {
	self.MHexadecimalNyomtatás(uint8(billentyű >> 8))
	self.MHexadecimalNyomtatás(uint8(billentyű))
}
func (self *TKonzol) MUnsignedinteger16Nyomtatásxy(billentyű uint16, x uint16, y uint16) {
	self.MHexadecimalNyomtatásxy(uint8(billentyű>>8), x, y)
	self.MHexadecimalNyomtatásxy(uint8(billentyű), x, y)
}
func (self *TKonzol) MUnsignedinteger32Nyomtatás(data uint32) {
	self.MHexadecimalNyomtatás(uint8(data >> 24))
	self.MHexadecimalNyomtatás(uint8(data >> 16))
	self.MHexadecimalNyomtatás(uint8(data >> 8))
	self.MHexadecimalNyomtatás(uint8(data))
}
func (self *TKonzol) MUnsignedinteger32Nyomtatásxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalNyomtatásxy(uint8(data>>24), x+0, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>16), x+2, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>8), x+4, y)
	self.MHexadecimalNyomtatásxy(uint8(data), x+6, y)
}
func (self *TKonzol) MUnsignedinteger64Nyomtatás(data uint64) {
	self.MHexadecimalNyomtatás(uint8(data >> 56))
	self.MHexadecimalNyomtatás(uint8(data >> 48))
	self.MHexadecimalNyomtatás(uint8(data >> 40))
	self.MHexadecimalNyomtatás(uint8(data >> 32))
	self.MHexadecimalNyomtatás(uint8(data >> 24))
	self.MHexadecimalNyomtatás(uint8(data >> 16))
	self.MHexadecimalNyomtatás(uint8(data >> 8))
	self.MHexadecimalNyomtatás(uint8(data))
}
func (self *TKonzol) MUnsignedinteger64Nyomtatásxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalNyomtatásxy(uint8(data>>56), x+0, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>48), x+2, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>40), x+4, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>32), x+6, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>24), x+8, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>16), x+10, y)
	self.MHexadecimalNyomtatásxy(uint8(data>>8), x+12, y)
	self.MHexadecimalNyomtatásxy(uint8(data), x+14, y)
}
func MNyomtatás(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TKonzol) MNyomtatáshexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hexadecimális := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimális[(data>>4)&0xF]
	buffer[1] = hexadecimális[data&0xF]

	MNyomtatás(uintptr(fbphysaddress), buffer[0], x, y)
	MNyomtatás(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TKonzol) MNyomtatásunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MNyomtatáshexadecimal(uint8(data>>8), x+0*2, y)
	self.MNyomtatáshexadecimal(uint8(data), x+2*2, y)
}

func (self *TKonzol) MNyomtatásunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MNyomtatáshexadecimal(uint8(data>>24), x+0*2, y)
	self.MNyomtatáshexadecimal(uint8(data>>16), x+2*2, y)
	self.MNyomtatáshexadecimal(uint8(data>>8), x+4*2, y)
	self.MNyomtatáshexadecimal(uint8(data), x+6*2, y)
}

func (self *TKonzol) M테스트() {
}
