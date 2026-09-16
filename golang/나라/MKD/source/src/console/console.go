/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbШирина		= 80
	fbВисина		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xПозиција	uint16
	yПозиција	uint16
}

var serialПодготвено bool

func Serialinit()
func SerialЗапишиbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialПодготвено = true
}

func seriallogbyte(data byte) {
	if !serialПодготвено {
		return
	}

	if data == '\n' {
		SerialЗапишиbyte('\r')
	}
	SerialЗапишиbyte(uint8(data))
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

func (само *TConsole) MПечати(argumentВредност ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var вредност_2 interface{}

	for i, p := range argumentВредност {
		switch i {
		case 0:
			param, _ := p.(interface{})
			вредност_2 = param
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

	само.MПечатиxy(вредност_2, x, y)

}
func (само *TConsole) MПечатиxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		само.MПечатибајтиxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		само.MHexadecimalПечатиxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		само.MUnsignedinteger16Печатиxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		само.MUnsignedinteger32Печатиxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		само.MUnsignedinteger64Печатиxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		само.MПечатибајтиxy(data_2, x, y)
	}

}
func (само *TConsole) MПечатибајтиxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		само.xПозиција = x
	}
	if y <= 999 {
		само.yПозиција = y
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
			само.yПозиција++
			само.xПозиција = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*само.yПозиција+само.xПозиција)*2))) = атрибут<<8 | uint16(buffer[i])
			само.xПозиција++
		}

		if само.xПозиција >= 80 {
			само.yПозиција++
			само.xПозиција = 0
		}

		if само.yПозиција >= 25 {
			for само.yПозиција = 0; само.yПозиција < 25; само.yПозиција++ {
				for само.xПозиција = 0; само.xПозиција < 80; само.xПозиција++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*само.yПозиција+само.xПозиција)*2))) = атрибут<<8 | ' '
				}
			}
			само.xПозиција = 0
			само.yПозиција = 0
		}

	}

}
func (само *TConsole) MHexadecimalПечати(key uint8) {
	buffer := []byte{'0', '0'}
	хекса := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хекса[(key>>4)&0xF]
	buffer[1] = хекса[key&0xF]
	само.MПечати(buffer)
}
func (само *TConsole) MHexadecimalПечатиxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	хекса := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хекса[(key>>4)&0xF]
	buffer[1] = хекса[key&0xF]
	само.MПечатиxy(buffer, x, y)
}
func (само *TConsole) MUnsignedinteger16Печати(key uint16) {
	само.MHexadecimalПечати(uint8(key >> 8))
	само.MHexadecimalПечати(uint8(key))
}
func (само *TConsole) MUnsignedinteger16Печатиxy(key uint16, x uint16, y uint16) {
	само.MHexadecimalПечатиxy(uint8(key>>8), x, y)
	само.MHexadecimalПечатиxy(uint8(key), x, y)
}
func (само *TConsole) MUnsignedinteger32Печати(data uint32) {
	само.MHexadecimalПечати(uint8(data >> 24))
	само.MHexadecimalПечати(uint8(data >> 16))
	само.MHexadecimalПечати(uint8(data >> 8))
	само.MHexadecimalПечати(uint8(data))
}
func (само *TConsole) MUnsignedinteger32Печатиxy(data uint32, x uint16, y uint16) {

	само.MHexadecimalПечатиxy(uint8(data>>24), x+0, y)
	само.MHexadecimalПечатиxy(uint8(data>>16), x+2, y)
	само.MHexadecimalПечатиxy(uint8(data>>8), x+4, y)
	само.MHexadecimalПечатиxy(uint8(data), x+6, y)
}
func (само *TConsole) MUnsignedinteger64Печати(data uint64) {
	само.MHexadecimalПечати(uint8(data >> 56))
	само.MHexadecimalПечати(uint8(data >> 48))
	само.MHexadecimalПечати(uint8(data >> 40))
	само.MHexadecimalПечати(uint8(data >> 32))
	само.MHexadecimalПечати(uint8(data >> 24))
	само.MHexadecimalПечати(uint8(data >> 16))
	само.MHexadecimalПечати(uint8(data >> 8))
	само.MHexadecimalПечати(uint8(data))
}
func (само *TConsole) MUnsignedinteger64Печатиxy(data uint64, x uint16, y uint16) {
	само.MHexadecimalПечатиxy(uint8(data>>56), x+0, y)
	само.MHexadecimalПечатиxy(uint8(data>>48), x+2, y)
	само.MHexadecimalПечатиxy(uint8(data>>40), x+4, y)
	само.MHexadecimalПечатиxy(uint8(data>>32), x+6, y)
	само.MHexadecimalПечатиxy(uint8(data>>24), x+8, y)
	само.MHexadecimalПечатиxy(uint8(data>>16), x+10, y)
	само.MHexadecimalПечатиxy(uint8(data>>8), x+12, y)
	само.MHexadecimalПечатиxy(uint8(data), x+14, y)
}
func MПечати(phyaddr uintptr, data uint8, x uint32, y uint32)

func (само *TConsole) MПечатиhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	хекса := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хекса[(data>>4)&0xF]
	buffer[1] = хекса[data&0xF]

	MПечати(uintptr(fbphysaddress), buffer[0], x, y)
	MПечати(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (само *TConsole) MПечатиunsignedinteger16(data uint16, x uint32, y uint32) {
	само.MПечатиhexadecimal(uint8(data>>8), x+0*2, y)
	само.MПечатиhexadecimal(uint8(data), x+2*2, y)
}

func (само *TConsole) MПечатиunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	само.MПечатиhexadecimal(uint8(data>>24), x+0*2, y)
	само.MПечатиhexadecimal(uint8(data>>16), x+2*2, y)
	само.MПечатиhexadecimal(uint8(data>>8), x+4*2, y)
	само.MПечатиhexadecimal(uint8(data), x+6*2, y)
}

func (само *TConsole) M테스트() {
}
