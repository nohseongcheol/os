/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbТуурасы		= 80
	fbБийиктик		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xТурганжери	uint16
	yТурганжери	uint16
}

var serialДаяр bool

func Serialinit()
func SerialЖазууbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialДаяр = true
}

func seriallogbyte(data byte) {
	if !serialДаяр {
		return
	}

	if data == '\n' {
		SerialЖазууbyte('\r')
	}
	SerialЖазууbyte(uint8(data))
}

func MEmergencylogСАП(data string) {
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

func (self *TConsole) MБасма(argumentМааниси ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var мааниси_2 interface{}

	for i, p := range argumentМааниси {
		switch i {
		case 0:
			param, _ := p.(interface{})
			мааниси_2 = param
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

	self.MБасмаxy(мааниси_2, x, y)

}
func (self *TConsole) MБасмаxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MБасмаБайтxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalБасмаxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Басмаxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Басмаxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Басмаxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MБасмаБайтxy(data_2, x, y)
	}

}
func (self *TConsole) MБасмаБайтxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xТурганжери = x
	}
	if y <= 999 {
		self.yТурганжери = y
	}

	атрибут := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yТурганжери++
			self.xТурганжери = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yТурганжери+self.xТурганжери)*2))) = атрибут<<8 | uint16(buffer[i])
			self.xТурганжери++
		}

		if self.xТурганжери >= 80 {
			self.yТурганжери++
			self.xТурганжери = 0
		}

		if self.yТурганжери >= 25 {
			for self.yТурганжери = 0; self.yТурганжери < 25; self.yТурганжери++ {
				for self.xТурганжери = 0; self.xТурганжери < 80; self.xТурганжери++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yТурганжери+self.xТурганжери)*2))) = атрибут<<8 | ' '
				}
			}
			self.xТурганжери = 0
			self.yТурганжери = 0
		}

	}

}
func (self *TConsole) MHexadecimalБасма(ачкыч uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ачкыч>>4)&0xF]
	buffer[1] = hex[ачкыч&0xF]
	self.MБасма(buffer)
}
func (self *TConsole) MHexadecimalБасмаxy(ачкыч uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ачкыч>>4)&0xF]
	buffer[1] = hex[ачкыч&0xF]
	self.MБасмаxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Басма(ачкыч uint16) {
	self.MHexadecimalБасма(uint8(ачкыч >> 8))
	self.MHexadecimalБасма(uint8(ачкыч))
}
func (self *TConsole) MUnsignedinteger16Басмаxy(ачкыч uint16, x uint16, y uint16) {
	self.MHexadecimalБасмаxy(uint8(ачкыч>>8), x, y)
	self.MHexadecimalБасмаxy(uint8(ачкыч), x, y)
}
func (self *TConsole) MUnsignedinteger32Басма(data uint32) {
	self.MHexadecimalБасма(uint8(data >> 24))
	self.MHexadecimalБасма(uint8(data >> 16))
	self.MHexadecimalБасма(uint8(data >> 8))
	self.MHexadecimalБасма(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Басмаxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalБасмаxy(uint8(data>>24), x+0, y)
	self.MHexadecimalБасмаxy(uint8(data>>16), x+2, y)
	self.MHexadecimalБасмаxy(uint8(data>>8), x+4, y)
	self.MHexadecimalБасмаxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Басма(data uint64) {
	self.MHexadecimalБасма(uint8(data >> 56))
	self.MHexadecimalБасма(uint8(data >> 48))
	self.MHexadecimalБасма(uint8(data >> 40))
	self.MHexadecimalБасма(uint8(data >> 32))
	self.MHexadecimalБасма(uint8(data >> 24))
	self.MHexadecimalБасма(uint8(data >> 16))
	self.MHexadecimalБасма(uint8(data >> 8))
	self.MHexadecimalБасма(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Басмаxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalБасмаxy(uint8(data>>56), x+0, y)
	self.MHexadecimalБасмаxy(uint8(data>>48), x+2, y)
	self.MHexadecimalБасмаxy(uint8(data>>40), x+4, y)
	self.MHexadecimalБасмаxy(uint8(data>>32), x+6, y)
	self.MHexadecimalБасмаxy(uint8(data>>24), x+8, y)
	self.MHexadecimalБасмаxy(uint8(data>>16), x+10, y)
	self.MHexadecimalБасмаxy(uint8(data>>8), x+12, y)
	self.MHexadecimalБасмаxy(uint8(data), x+14, y)
}
func MБасма(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MБасмаhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MБасма(uintptr(fbphysaddress), buffer[0], x, y)
	MБасма(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MБасмаunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MБасмаhexadecimal(uint8(data>>8), x+0*2, y)
	self.MБасмаhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MБасмаunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MБасмаhexadecimal(uint8(data>>24), x+0*2, y)
	self.MБасмаhexadecimal(uint8(data>>16), x+2*2, y)
	self.MБасмаhexadecimal(uint8(data>>8), x+4*2, y)
	self.MБасмаhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
