/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbwidth			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xמיקום	uint16
	yמיקום	uint16
}

var סידורימוכן bool

func Sסידוריinit()
func Sסידוריכתיבהbyte(data uint8)

func Mסידורייומןinit() {
	Sסידוריinit()
	סידורימוכן = true
}

func סידורייומןbyte(data byte) {
	if !סידורימוכן {
		return
	}

	if data == '\n' {
		Sסידוריכתיבהbyte('\r')
	}
	Sסידוריכתיבהbyte(uint8(data))
}

func MEmergencyיומןמחרוזת(data string) {
	for i := 0; i < len(data); i++ {
		סידורייומןbyte(data[i])
	}
}

func MEmergencyיומןhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	סידורייומןbyte(digits[(data>>4)&0x0F])
	סידורייומןbyte(digits[data&0x0F])
}

func MEmergencyיומןunsignedinteger32(data uint32) {
	MEmergencyיומןhexadecimal8(uint8(data >> 24))
	MEmergencyיומןhexadecimal8(uint8(data >> 16))
	MEmergencyיומןhexadecimal8(uint8(data >> 8))
	MEmergencyיומןhexadecimal8(uint8(data))
}

func (self *TConsole) Mהדפסה(argumentערך ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var ערך_2 interface{}

	for i, p := range argumentערך {
		switch i {
		case 0:
			param, _ := p.(interface{})
			ערך_2 = param
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

	self.Mהדפסהxy(ערך_2, x, y)

}
func (self *TConsole) Mהדפסהxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.Mהדפסהבתיםxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalהדפסהxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16הדפסהxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32הדפסהxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64הדפסהxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.Mהדפסהבתיםxy(data_2, x, y)
	}

}
func (self *TConsole) Mהדפסהבתיםxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xמיקום = x
	}
	if y <= 999 {
		self.yמיקום = y
	}

	תכונה := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		סידורייומןbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yמיקום++
			self.xמיקום = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yמיקום+self.xמיקום)*2))) = תכונה<<8 | uint16(buffer[i])
			self.xמיקום++
		}

		if self.xמיקום >= 80 {
			self.yמיקום++
			self.xמיקום = 0
		}

		if self.yמיקום >= 25 {
			for self.yמיקום = 0; self.yמיקום < 25; self.yמיקום++ {
				for self.xמיקום = 0; self.xמיקום < 80; self.xמיקום++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yמיקום+self.xמיקום)*2))) = תכונה<<8 | ' '
				}
			}
			self.xמיקום = 0
			self.yמיקום = 0
		}

	}

}
func (self *TConsole) MHexadecimalהדפסה(מפתח_2 uint8) {
	buffer := []byte{'0', '0'}
	הקסדצימלי := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = הקסדצימלי[(מפתח_2>>4)&0xF]
	buffer[1] = הקסדצימלי[מפתח_2&0xF]
	self.Mהדפסה(buffer)
}
func (self *TConsole) MHexadecimalהדפסהxy(מפתח_2 uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	הקסדצימלי := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = הקסדצימלי[(מפתח_2>>4)&0xF]
	buffer[1] = הקסדצימלי[מפתח_2&0xF]
	self.Mהדפסהxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16הדפסה(מפתח_2 uint16) {
	self.MHexadecimalהדפסה(uint8(מפתח_2 >> 8))
	self.MHexadecimalהדפסה(uint8(מפתח_2))
}
func (self *TConsole) MUnsignedinteger16הדפסהxy(מפתח_2 uint16, x uint16, y uint16) {
	self.MHexadecimalהדפסהxy(uint8(מפתח_2>>8), x, y)
	self.MHexadecimalהדפסהxy(uint8(מפתח_2), x, y)
}
func (self *TConsole) MUnsignedinteger32הדפסה(data uint32) {
	self.MHexadecimalהדפסה(uint8(data >> 24))
	self.MHexadecimalהדפסה(uint8(data >> 16))
	self.MHexadecimalהדפסה(uint8(data >> 8))
	self.MHexadecimalהדפסה(uint8(data))
}
func (self *TConsole) MUnsignedinteger32הדפסהxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalהדפסהxy(uint8(data>>24), x+0, y)
	self.MHexadecimalהדפסהxy(uint8(data>>16), x+2, y)
	self.MHexadecimalהדפסהxy(uint8(data>>8), x+4, y)
	self.MHexadecimalהדפסהxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64הדפסה(data uint64) {
	self.MHexadecimalהדפסה(uint8(data >> 56))
	self.MHexadecimalהדפסה(uint8(data >> 48))
	self.MHexadecimalהדפסה(uint8(data >> 40))
	self.MHexadecimalהדפסה(uint8(data >> 32))
	self.MHexadecimalהדפסה(uint8(data >> 24))
	self.MHexadecimalהדפסה(uint8(data >> 16))
	self.MHexadecimalהדפסה(uint8(data >> 8))
	self.MHexadecimalהדפסה(uint8(data))
}
func (self *TConsole) MUnsignedinteger64הדפסהxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalהדפסהxy(uint8(data>>56), x+0, y)
	self.MHexadecimalהדפסהxy(uint8(data>>48), x+2, y)
	self.MHexadecimalהדפסהxy(uint8(data>>40), x+4, y)
	self.MHexadecimalהדפסהxy(uint8(data>>32), x+6, y)
	self.MHexadecimalהדפסהxy(uint8(data>>24), x+8, y)
	self.MHexadecimalהדפסהxy(uint8(data>>16), x+10, y)
	self.MHexadecimalהדפסהxy(uint8(data>>8), x+12, y)
	self.MHexadecimalהדפסהxy(uint8(data), x+14, y)
}
func Mהדפסה(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) Mהדפסהhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	הקסדצימלי := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = הקסדצימלי[(data>>4)&0xF]
	buffer[1] = הקסדצימלי[data&0xF]

	Mהדפסה(uintptr(fbphysaddress), buffer[0], x, y)
	Mהדפסה(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) Mהדפסהunsignedinteger16(data uint16, x uint32, y uint32) {
	self.Mהדפסהhexadecimal(uint8(data>>8), x+0*2, y)
	self.Mהדפסהhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) Mהדפסהunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.Mהדפסהhexadecimal(uint8(data>>24), x+0*2, y)
	self.Mהדפסהhexadecimal(uint8(data>>16), x+2*2, y)
	self.Mהדפסהhexadecimal(uint8(data>>8), x+4*2, y)
	self.Mהדפסהhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
