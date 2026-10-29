/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package консол

import . "unsafe"

const (
	fbӨргөн			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TКонсол struct {
	xposition	uint16
	yposition	uint16
}

var serialready bool

func Serialinit()
func SerialБичихbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialready = true
}

func seriallogbyte(data byte) {
	if !serialready {
		return
	}

	if data == '\n' {
		SerialБичихbyte('\r')
	}
	SerialБичихbyte(uint8(data))
}

func MEmergencylogБИЧВЭР(data string) {
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

func (self *TКонсол) MХэвлэх(argumentУтга ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var утга_2 interface{}

	for i, p := range argumentУтга {
		switch i {
		case 0:
			param, _ := p.(interface{})
			утга_2 = param
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

	self.MХэвлэхxy(утга_2, x, y)

}
func (self *TКонсол) MХэвлэхxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MХэвлэхБайтxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalХэвлэхxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Хэвлэхxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Хэвлэхxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Хэвлэхxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MХэвлэхБайтxy(data_2, x, y)
	}

}
func (self *TКонсол) MХэвлэхБайтxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xposition = x
	}
	if y <= 999 {
		self.yposition = y
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
			self.yposition++
			self.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribute<<8 | uint16(buffer[i])
			self.xposition++
		}

		if self.xposition >= 80 {
			self.yposition++
			self.xposition = 0
		}

		if self.yposition >= 25 {
			for self.yposition = 0; self.yposition < 25; self.yposition++ {
				for self.xposition = 0; self.xposition < 80; self.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribute<<8 | ' '
				}
			}
			self.xposition = 0
			self.yposition = 0
		}

	}

}
func (self *TКонсол) MHexadecimalХэвлэх(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.MХэвлэх(buffer)
}
func (self *TКонсол) MHexadecimalХэвлэхxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.MХэвлэхxy(buffer, x, y)
}
func (self *TКонсол) MUnsignedinteger16Хэвлэх(key uint16) {
	self.MHexadecimalХэвлэх(uint8(key >> 8))
	self.MHexadecimalХэвлэх(uint8(key))
}
func (self *TКонсол) MUnsignedinteger16Хэвлэхxy(key uint16, x uint16, y uint16) {
	self.MHexadecimalХэвлэхxy(uint8(key>>8), x, y)
	self.MHexadecimalХэвлэхxy(uint8(key), x, y)
}
func (self *TКонсол) MUnsignedinteger32Хэвлэх(data uint32) {
	self.MHexadecimalХэвлэх(uint8(data >> 24))
	self.MHexadecimalХэвлэх(uint8(data >> 16))
	self.MHexadecimalХэвлэх(uint8(data >> 8))
	self.MHexadecimalХэвлэх(uint8(data))
}
func (self *TКонсол) MUnsignedinteger32Хэвлэхxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalХэвлэхxy(uint8(data>>24), x+0, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>16), x+2, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>8), x+4, y)
	self.MHexadecimalХэвлэхxy(uint8(data), x+6, y)
}
func (self *TКонсол) MUnsignedinteger64Хэвлэх(data uint64) {
	self.MHexadecimalХэвлэх(uint8(data >> 56))
	self.MHexadecimalХэвлэх(uint8(data >> 48))
	self.MHexadecimalХэвлэх(uint8(data >> 40))
	self.MHexadecimalХэвлэх(uint8(data >> 32))
	self.MHexadecimalХэвлэх(uint8(data >> 24))
	self.MHexadecimalХэвлэх(uint8(data >> 16))
	self.MHexadecimalХэвлэх(uint8(data >> 8))
	self.MHexadecimalХэвлэх(uint8(data))
}
func (self *TКонсол) MUnsignedinteger64Хэвлэхxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalХэвлэхxy(uint8(data>>56), x+0, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>48), x+2, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>40), x+4, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>32), x+6, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>24), x+8, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>16), x+10, y)
	self.MHexadecimalХэвлэхxy(uint8(data>>8), x+12, y)
	self.MHexadecimalХэвлэхxy(uint8(data), x+14, y)
}
func MХэвлэх(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TКонсол) MХэвлэхhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MХэвлэх(uintptr(fbphysaddress), buffer[0], x, y)
	MХэвлэх(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TКонсол) MХэвлэхunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MХэвлэхhexadecimal(uint8(data>>8), x+0*2, y)
	self.MХэвлэхhexadecimal(uint8(data), x+2*2, y)
}

func (self *TКонсол) MХэвлэхunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MХэвлэхhexadecimal(uint8(data>>24), x+0*2, y)
	self.MХэвлэхhexadecimal(uint8(data>>16), x+2*2, y)
	self.MХэвлэхhexadecimal(uint8(data>>8), x+4*2, y)
	self.MХэвлэхhexadecimal(uint8(data), x+6*2, y)
}

func (self *TКонсол) M테스트() {
}
