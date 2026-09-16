/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsol

import . "unsafe"

const (
	fbBredd			= 80
	fbHöjd			= 25
	fbphysAdress	uintptr	= 0xb8000
)

type TKonsol struct {
	xposition	uint16
	yposition	uint16
}

var seriellRedo bool

func Seriellinit()
func SeriellSkrivbyte(data uint8)

func MSeriellLogginit() {
	Seriellinit()
	seriellRedo = true
}

func seriellLoggbyte(data byte) {
	if !seriellRedo {
		return
	}

	if data == '\n' {
		SeriellSkrivbyte('\r')
	}
	SeriellSkrivbyte(uint8(data))
}

func MEmergencyLoggsträng(data string) {
	for i := 0; i < len(data); i++ {
		seriellLoggbyte(data[i])
	}
}

func MEmergencyLogghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	seriellLoggbyte(digits[(data>>4)&0x0F])
	seriellLoggbyte(digits[data&0x0F])
}

func MEmergencyLoggunsignedinteger32(data uint32) {
	MEmergencyLogghexadecimal8(uint8(data >> 24))
	MEmergencyLogghexadecimal8(uint8(data >> 16))
	MEmergencyLogghexadecimal8(uint8(data >> 8))
	MEmergencyLogghexadecimal8(uint8(data))
}

func (själv *TKonsol) MSkrivut(argumentVärde ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var värde_2 interface{}

	for i, p := range argumentVärde {
		switch i {
		case 0:
			param, _ := p.(interface{})
			värde_2 = param
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

	själv.MSkrivutxy(värde_2, x, y)

}
func (själv *TKonsol) MSkrivutxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		själv.MSkrivutBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		själv.MHexadecimalSkrivutxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		själv.MUnsignedinteger16Skrivutxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		själv.MUnsignedinteger32Skrivutxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		själv.MUnsignedinteger64Skrivutxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		själv.MSkrivutBytexy(data_2, x, y)
	}

}
func (själv *TKonsol) MSkrivutBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		själv.xposition = x
	}
	if y <= 999 {
		själv.yposition = y
	}

	attribut := uint16(0x0F)
	gräns := len(buffer)
	if gräns > 4096 {
		gräns = 4096
	}
	for i := 0; i < gräns; i++ {
		seriellLoggbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			själv.yposition++
			själv.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysAdress + uintptr((80*själv.yposition+själv.xposition)*2))) = attribut<<8 | uint16(buffer[i])
			själv.xposition++
		}

		if själv.xposition >= 80 {
			själv.yposition++
			själv.xposition = 0
		}

		if själv.yposition >= 25 {
			for själv.yposition = 0; själv.yposition < 25; själv.yposition++ {
				for själv.xposition = 0; själv.xposition < 80; själv.xposition++ {
					*(*uint16)(Pointer(fbphysAdress + uintptr((80*själv.yposition+själv.xposition)*2))) = attribut<<8 | ' '
				}
			}
			själv.xposition = 0
			själv.yposition = 0
		}

	}

}
func (själv *TKonsol) MHexadecimalSkrivut(nyckel uint8) {
	buffer := []byte{'0', '0'}
	hexadecimalt := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimalt[(nyckel>>4)&0xF]
	buffer[1] = hexadecimalt[nyckel&0xF]
	själv.MSkrivut(buffer)
}
func (själv *TKonsol) MHexadecimalSkrivutxy(nyckel uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hexadecimalt := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimalt[(nyckel>>4)&0xF]
	buffer[1] = hexadecimalt[nyckel&0xF]
	själv.MSkrivutxy(buffer, x, y)
}
func (själv *TKonsol) MUnsignedinteger16Skrivut(nyckel uint16) {
	själv.MHexadecimalSkrivut(uint8(nyckel >> 8))
	själv.MHexadecimalSkrivut(uint8(nyckel))
}
func (själv *TKonsol) MUnsignedinteger16Skrivutxy(nyckel uint16, x uint16, y uint16) {
	själv.MHexadecimalSkrivutxy(uint8(nyckel>>8), x, y)
	själv.MHexadecimalSkrivutxy(uint8(nyckel), x, y)
}
func (själv *TKonsol) MUnsignedinteger32Skrivut(data uint32) {
	själv.MHexadecimalSkrivut(uint8(data >> 24))
	själv.MHexadecimalSkrivut(uint8(data >> 16))
	själv.MHexadecimalSkrivut(uint8(data >> 8))
	själv.MHexadecimalSkrivut(uint8(data))
}
func (själv *TKonsol) MUnsignedinteger32Skrivutxy(data uint32, x uint16, y uint16) {

	själv.MHexadecimalSkrivutxy(uint8(data>>24), x+0, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>16), x+2, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>8), x+4, y)
	själv.MHexadecimalSkrivutxy(uint8(data), x+6, y)
}
func (själv *TKonsol) MUnsignedinteger64Skrivut(data uint64) {
	själv.MHexadecimalSkrivut(uint8(data >> 56))
	själv.MHexadecimalSkrivut(uint8(data >> 48))
	själv.MHexadecimalSkrivut(uint8(data >> 40))
	själv.MHexadecimalSkrivut(uint8(data >> 32))
	själv.MHexadecimalSkrivut(uint8(data >> 24))
	själv.MHexadecimalSkrivut(uint8(data >> 16))
	själv.MHexadecimalSkrivut(uint8(data >> 8))
	själv.MHexadecimalSkrivut(uint8(data))
}
func (själv *TKonsol) MUnsignedinteger64Skrivutxy(data uint64, x uint16, y uint16) {
	själv.MHexadecimalSkrivutxy(uint8(data>>56), x+0, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>48), x+2, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>40), x+4, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>32), x+6, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>24), x+8, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>16), x+10, y)
	själv.MHexadecimalSkrivutxy(uint8(data>>8), x+12, y)
	själv.MHexadecimalSkrivutxy(uint8(data), x+14, y)
}
func MSkrivut(phyaddr uintptr, data uint8, x uint32, y uint32)

func (själv *TKonsol) MSkrivuthexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hexadecimalt := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimalt[(data>>4)&0xF]
	buffer[1] = hexadecimalt[data&0xF]

	MSkrivut(uintptr(fbphysAdress), buffer[0], x, y)
	MSkrivut(uintptr(fbphysAdress), buffer[1], x+2, y)
}

func (själv *TKonsol) MSkrivutunsignedinteger16(data uint16, x uint32, y uint32) {
	själv.MSkrivuthexadecimal(uint8(data>>8), x+0*2, y)
	själv.MSkrivuthexadecimal(uint8(data), x+2*2, y)
}

func (själv *TKonsol) MSkrivutunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	själv.MSkrivuthexadecimal(uint8(data>>24), x+0*2, y)
	själv.MSkrivuthexadecimal(uint8(data>>16), x+2*2, y)
	själv.MSkrivuthexadecimal(uint8(data>>8), x+4*2, y)
	själv.MSkrivuthexadecimal(uint8(data), x+6*2, y)
}

func (själv *TKonsol) M테스트() {
}
