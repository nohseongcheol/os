/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsoly

import . "unsafe"

const (
	fbIndra			= 80
	fbHaavo			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonsoly struct {
	xposition	uint16
	yposition	uint16
}

var serialVonona bool

func Serialinit()
func SerialManoratrabyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialVonona = true
}

func seriallogbyte(data byte) {
	if !serialVonona {
		return
	}

	if data == '\n' {
		SerialManoratrabyte('\r')
	}
	SerialManoratrabyte(uint8(data))
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

func (nytena *TKonsoly) MAtontay(argumentSanda ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var sanda_2 interface{}

	for i, p := range argumentSanda {
		switch i {
		case 0:
			param, _ := p.(interface{})
			sanda_2 = param
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

	nytena.MAtontayxy(sanda_2, x, y)

}
func (nytena *TKonsoly) MAtontayxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		nytena.MAtontayOctetxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		nytena.MHexadecimalAtontayxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		nytena.MUnsignedinteger16Atontayxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		nytena.MUnsignedinteger32Atontayxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		nytena.MUnsignedinteger64Atontayxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		nytena.MAtontayOctetxy(data_2, x, y)
	}

}
func (nytena *TKonsoly) MAtontayOctetxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		nytena.xposition = x
	}
	if y <= 999 {
		nytena.yposition = y
	}

	marikamanokana := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			nytena.yposition++
			nytena.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*nytena.yposition+nytena.xposition)*2))) = marikamanokana<<8 | uint16(buffer[i])
			nytena.xposition++
		}

		if nytena.xposition >= 80 {
			nytena.yposition++
			nytena.xposition = 0
		}

		if nytena.yposition >= 25 {
			for nytena.yposition = 0; nytena.yposition < 25; nytena.yposition++ {
				for nytena.xposition = 0; nytena.xposition < 80; nytena.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*nytena.yposition+nytena.xposition)*2))) = marikamanokana<<8 | ' '
				}
			}
			nytena.xposition = 0
			nytena.yposition = 0
		}

	}

}
func (nytena *TKonsoly) MHexadecimalAtontay(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	nytena.MAtontay(buffer)
}
func (nytena *TKonsoly) MHexadecimalAtontayxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	nytena.MAtontayxy(buffer, x, y)
}
func (nytena *TKonsoly) MUnsignedinteger16Atontay(key uint16) {
	nytena.MHexadecimalAtontay(uint8(key >> 8))
	nytena.MHexadecimalAtontay(uint8(key))
}
func (nytena *TKonsoly) MUnsignedinteger16Atontayxy(key uint16, x uint16, y uint16) {
	nytena.MHexadecimalAtontayxy(uint8(key>>8), x, y)
	nytena.MHexadecimalAtontayxy(uint8(key), x, y)
}
func (nytena *TKonsoly) MUnsignedinteger32Atontay(data uint32) {
	nytena.MHexadecimalAtontay(uint8(data >> 24))
	nytena.MHexadecimalAtontay(uint8(data >> 16))
	nytena.MHexadecimalAtontay(uint8(data >> 8))
	nytena.MHexadecimalAtontay(uint8(data))
}
func (nytena *TKonsoly) MUnsignedinteger32Atontayxy(data uint32, x uint16, y uint16) {

	nytena.MHexadecimalAtontayxy(uint8(data>>24), x+0, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>16), x+2, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>8), x+4, y)
	nytena.MHexadecimalAtontayxy(uint8(data), x+6, y)
}
func (nytena *TKonsoly) MUnsignedinteger64Atontay(data uint64) {
	nytena.MHexadecimalAtontay(uint8(data >> 56))
	nytena.MHexadecimalAtontay(uint8(data >> 48))
	nytena.MHexadecimalAtontay(uint8(data >> 40))
	nytena.MHexadecimalAtontay(uint8(data >> 32))
	nytena.MHexadecimalAtontay(uint8(data >> 24))
	nytena.MHexadecimalAtontay(uint8(data >> 16))
	nytena.MHexadecimalAtontay(uint8(data >> 8))
	nytena.MHexadecimalAtontay(uint8(data))
}
func (nytena *TKonsoly) MUnsignedinteger64Atontayxy(data uint64, x uint16, y uint16) {
	nytena.MHexadecimalAtontayxy(uint8(data>>56), x+0, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>48), x+2, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>40), x+4, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>32), x+6, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>24), x+8, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>16), x+10, y)
	nytena.MHexadecimalAtontayxy(uint8(data>>8), x+12, y)
	nytena.MHexadecimalAtontayxy(uint8(data), x+14, y)
}
func MAtontay(phyaddr uintptr, data uint8, x uint32, y uint32)

func (nytena *TKonsoly) MAtontayhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MAtontay(uintptr(fbphysaddress), buffer[0], x, y)
	MAtontay(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (nytena *TKonsoly) MAtontayunsignedinteger16(data uint16, x uint32, y uint32) {
	nytena.MAtontayhexadecimal(uint8(data>>8), x+0*2, y)
	nytena.MAtontayhexadecimal(uint8(data), x+2*2, y)
}

func (nytena *TKonsoly) MAtontayunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	nytena.MAtontayhexadecimal(uint8(data>>24), x+0*2, y)
	nytena.MAtontayhexadecimal(uint8(data>>16), x+2*2, y)
	nytena.MAtontayhexadecimal(uint8(data>>8), x+4*2, y)
	nytena.MAtontayhexadecimal(uint8(data), x+6*2, y)
}

func (nytena *TKonsoly) M테스트() {
}
