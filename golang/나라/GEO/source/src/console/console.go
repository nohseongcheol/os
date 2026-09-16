/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbსიგანე		= 80
	fbსიმაღლე		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xposition	uint16
	yposition	uint16
}

var serialready bool

func Serialinit()
func Serialჩაწერაbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialready = true
}

func seriallogbyte(data byte) {
	if !serialready {
		return
	}

	if data == '\n' {
		Serialჩაწერაbyte('\r')
	}
	Serialჩაწერაbyte(uint8(data))
}

func MEmergencylogstring(data string) {
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

func (self *TConsole) Mბეჭდვა(argumentმნიშვნელობა ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var მნიშვნელობა_2 interface{}

	for i, p := range argumentმნიშვნელობა {
		switch i {
		case 0:
			param, _ := p.(interface{})
			მნიშვნელობა_2 = param
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

	self.Mბეჭდვაxy(მნიშვნელობა_2, x, y)

}
func (self *TConsole) Mბეჭდვაxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.Mბეჭდვაბაიტიxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalბეჭდვაxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16ბეჭდვაxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32ბეჭდვაxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64ბეჭდვაxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.Mბეჭდვაბაიტიxy(data_2, x, y)
	}

}
func (self *TConsole) Mბეჭდვაბაიტიxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xposition = x
	}
	if y <= 999 {
		self.yposition = y
	}

	ატრიბუტი := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yposition++
			self.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = ატრიბუტი<<8 | uint16(buffer[i])
			self.xposition++
		}

		if self.xposition >= 80 {
			self.yposition++
			self.xposition = 0
		}

		if self.yposition >= 25 {
			for self.yposition = 0; self.yposition < 25; self.yposition++ {
				for self.xposition = 0; self.xposition < 80; self.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = ატრიბუტი<<8 | ' '
				}
			}
			self.xposition = 0
			self.yposition = 0
		}

	}

}
func (self *TConsole) MHexadecimalბეჭდვა(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.Mბეჭდვა(buffer)
}
func (self *TConsole) MHexadecimalბეჭდვაxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.Mბეჭდვაxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16ბეჭდვა(key uint16) {
	self.MHexadecimalბეჭდვა(uint8(key >> 8))
	self.MHexadecimalბეჭდვა(uint8(key))
}
func (self *TConsole) MUnsignedinteger16ბეჭდვაxy(key uint16, x uint16, y uint16) {
	self.MHexadecimalბეჭდვაxy(uint8(key>>8), x, y)
	self.MHexadecimalბეჭდვაxy(uint8(key), x, y)
}
func (self *TConsole) MUnsignedinteger32ბეჭდვა(data uint32) {
	self.MHexadecimalბეჭდვა(uint8(data >> 24))
	self.MHexadecimalბეჭდვა(uint8(data >> 16))
	self.MHexadecimalბეჭდვა(uint8(data >> 8))
	self.MHexadecimalბეჭდვა(uint8(data))
}
func (self *TConsole) MUnsignedinteger32ბეჭდვაxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalბეჭდვაxy(uint8(data>>24), x+0, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>16), x+2, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>8), x+4, y)
	self.MHexadecimalბეჭდვაxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64ბეჭდვა(data uint64) {
	self.MHexadecimalბეჭდვა(uint8(data >> 56))
	self.MHexadecimalბეჭდვა(uint8(data >> 48))
	self.MHexadecimalბეჭდვა(uint8(data >> 40))
	self.MHexadecimalბეჭდვა(uint8(data >> 32))
	self.MHexadecimalბეჭდვა(uint8(data >> 24))
	self.MHexadecimalბეჭდვა(uint8(data >> 16))
	self.MHexadecimalბეჭდვა(uint8(data >> 8))
	self.MHexadecimalბეჭდვა(uint8(data))
}
func (self *TConsole) MUnsignedinteger64ბეჭდვაxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalბეჭდვაxy(uint8(data>>56), x+0, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>48), x+2, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>40), x+4, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>32), x+6, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>24), x+8, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>16), x+10, y)
	self.MHexadecimalბეჭდვაxy(uint8(data>>8), x+12, y)
	self.MHexadecimalბეჭდვაxy(uint8(data), x+14, y)
}
func Mბეჭდვა(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) Mბეჭდვაhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	Mბეჭდვა(uintptr(fbphysaddress), buffer[0], x, y)
	Mბეჭდვა(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) Mბეჭდვაunsignedinteger16(data uint16, x uint32, y uint32) {
	self.Mბეჭდვაhexadecimal(uint8(data>>8), x+0*2, y)
	self.Mბეჭდვაhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) Mბეჭდვაunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.Mბეჭდვაhexadecimal(uint8(data>>24), x+0*2, y)
	self.Mბეჭდვაhexadecimal(uint8(data>>16), x+2*2, y)
	self.Mბეჭდვაhexadecimal(uint8(data>>8), x+4*2, y)
	self.Mბეჭდვაhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
