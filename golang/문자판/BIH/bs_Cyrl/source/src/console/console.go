/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbŠirina		= 80
	fbVisina		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xpoložaj	uint16
	ypoložaj	uint16
}

var serialready bool

func Serialinit()
func SerialPišibyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialready = true
}

func seriallogbyte(data byte) {
	if !serialready {
		return
	}

	if data == '\n' {
		SerialPišibyte('\r')
	}
	SerialPišibyte(uint8(data))
}

func MEmergencylogNIZ(data string) {
	for i := 0; i < len(data); i++ {
		seriallogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	seriallogbyte(digits[(data>>4)&0x0F])
	seriallogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (self *TConsole) MŠtampaj(argumentVrijednost ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var vrijednost_2 interface{}

	for i, p := range argumentVrijednost {
		switch i {
		case 0:
			param, _ := p.(interface{})
			vrijednost_2 = param
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

	self.MŠtampajxy(vrijednost_2, x, y)

}
func (self *TConsole) MŠtampajxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MŠtampajBajtovaxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalŠtampajxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Štampajxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Štampajxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Štampajxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MŠtampajBajtovaxy(data_2, x, y)
	}

}
func (self *TConsole) MŠtampajBajtovaxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xpoložaj = x
	}
	if y <= 999 {
		self.ypoložaj = y
	}

	attribute := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.ypoložaj++
			self.xpoložaj = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.ypoložaj+self.xpoložaj)*2))) = attribute<<8 | uint16(buffer[i])
			self.xpoložaj++
		}

		if self.xpoložaj >= 80 {
			self.ypoložaj++
			self.xpoložaj = 0
		}

		if self.ypoložaj >= 25 {
			for self.ypoložaj = 0; self.ypoložaj < 25; self.ypoložaj++ {
				for self.xpoložaj = 0; self.xpoložaj < 80; self.xpoložaj++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.ypoložaj+self.xpoložaj)*2))) = attribute<<8 | ' '
				}
			}
			self.xpoložaj = 0
			self.ypoložaj = 0
		}

	}

}
func (self *TConsole) MHexadecimalŠtampaj(ključ uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ključ>>4)&0xF]
	buffer[1] = hex[ključ&0xF]
	self.MŠtampaj(buffer)
}
func (self *TConsole) MHexadecimalŠtampajxy(ključ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ključ>>4)&0xF]
	buffer[1] = hex[ključ&0xF]
	self.MŠtampajxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Štampaj(ključ uint16) {
	self.MHexadecimalŠtampaj(uint8(ključ >> 8))
	self.MHexadecimalŠtampaj(uint8(ključ))
}
func (self *TConsole) MUnsignedinteger16Štampajxy(ključ uint16, x uint16, y uint16) {
	self.MHexadecimalŠtampajxy(uint8(ključ>>8), x, y)
	self.MHexadecimalŠtampajxy(uint8(ključ), x, y)
}
func (self *TConsole) MUnsignedinteger32Štampaj(data uint32) {
	self.MHexadecimalŠtampaj(uint8(data >> 24))
	self.MHexadecimalŠtampaj(uint8(data >> 16))
	self.MHexadecimalŠtampaj(uint8(data >> 8))
	self.MHexadecimalŠtampaj(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Štampajxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalŠtampajxy(uint8(data>>24), x+0, y)
	self.MHexadecimalŠtampajxy(uint8(data>>16), x+2, y)
	self.MHexadecimalŠtampajxy(uint8(data>>8), x+4, y)
	self.MHexadecimalŠtampajxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Štampaj(data uint64) {
	self.MHexadecimalŠtampaj(uint8(data >> 56))
	self.MHexadecimalŠtampaj(uint8(data >> 48))
	self.MHexadecimalŠtampaj(uint8(data >> 40))
	self.MHexadecimalŠtampaj(uint8(data >> 32))
	self.MHexadecimalŠtampaj(uint8(data >> 24))
	self.MHexadecimalŠtampaj(uint8(data >> 16))
	self.MHexadecimalŠtampaj(uint8(data >> 8))
	self.MHexadecimalŠtampaj(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Štampajxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalŠtampajxy(uint8(data>>56), x+0, y)
	self.MHexadecimalŠtampajxy(uint8(data>>48), x+2, y)
	self.MHexadecimalŠtampajxy(uint8(data>>40), x+4, y)
	self.MHexadecimalŠtampajxy(uint8(data>>32), x+6, y)
	self.MHexadecimalŠtampajxy(uint8(data>>24), x+8, y)
	self.MHexadecimalŠtampajxy(uint8(data>>16), x+10, y)
	self.MHexadecimalŠtampajxy(uint8(data>>8), x+12, y)
	self.MHexadecimalŠtampajxy(uint8(data), x+14, y)
}
func MŠtampaj(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MŠtampajhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MŠtampaj(uintptr(fbphysaddress), buffer[0], x, y)
	MŠtampaj(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MŠtampajunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MŠtampajhexadecimal(uint8(data>>8), x+0*2, y)
	self.MŠtampajhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MŠtampajunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MŠtampajhexadecimal(uint8(data>>24), x+0*2, y)
	self.MŠtampajhexadecimal(uint8(data>>16), x+2*2, y)
	self.MŠtampajhexadecimal(uint8(data>>8), x+4*2, y)
	self.MŠtampajhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
