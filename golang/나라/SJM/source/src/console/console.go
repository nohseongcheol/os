/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbBredde		= 80
	fbHøyde			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPosisjon	uint16
	yPosisjon	uint16
}

var serienummerKlar bool

func Serienummerinit()
func SerienummerSkrivbyte(data uint8)

func MSerienummerLogginit() {
	Serienummerinit()
	serienummerKlar = true
}

func serienummerLoggbyte(data byte) {
	if !serienummerKlar {
		return
	}

	if data == '\n' {
		SerienummerSkrivbyte('\r')
	}
	SerienummerSkrivbyte(uint8(data))
}

func MEmergencyLoggStreng(data string) {
	for i := 0; i < len(data); i++ {
		serienummerLoggbyte(data[i])
	}
}

func MEmergencyLogghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serienummerLoggbyte(digits[(data>>4)&0x0F])
	serienummerLoggbyte(digits[data&0x0F])
}

func MEmergencyLoggunsignedinteger32(data uint32) {
	MEmergencyLogghexadecimal8(uint8(data >> 24))
	MEmergencyLogghexadecimal8(uint8(data >> 16))
	MEmergencyLogghexadecimal8(uint8(data >> 8))
	MEmergencyLogghexadecimal8(uint8(data))
}

func (selv *TConsole) MSkrivut(argumentVerdi ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var verdi_2 interface{}

	for i, p := range argumentVerdi {
		switch i {
		case 0:
			param, _ := p.(interface{})
			verdi_2 = param
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

	selv.MSkrivutxy(verdi_2, x, y)

}
func (selv *TConsole) MSkrivutxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		selv.MSkrivutBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		selv.MHexadecimalSkrivutxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		selv.MUnsignedinteger16Skrivutxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		selv.MUnsignedinteger32Skrivutxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		selv.MUnsignedinteger64Skrivutxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		selv.MSkrivutBytexy(data_2, x, y)
	}

}
func (selv *TConsole) MSkrivutBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		selv.xPosisjon = x
	}
	if y <= 999 {
		selv.yPosisjon = y
	}

	egenskap := uint16(0x0F)
	grense := len(buffer)
	if grense > 4096 {
		grense = 4096
	}
	for i := 0; i < grense; i++ {
		serienummerLoggbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			selv.yPosisjon++
			selv.xPosisjon = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*selv.yPosisjon+selv.xPosisjon)*2))) = egenskap<<8 | uint16(buffer[i])
			selv.xPosisjon++
		}

		if selv.xPosisjon >= 80 {
			selv.yPosisjon++
			selv.xPosisjon = 0
		}

		if selv.yPosisjon >= 25 {
			for selv.yPosisjon = 0; selv.yPosisjon < 25; selv.yPosisjon++ {
				for selv.xPosisjon = 0; selv.xPosisjon < 80; selv.xPosisjon++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*selv.yPosisjon+selv.xPosisjon)*2))) = egenskap<<8 | ' '
				}
			}
			selv.xPosisjon = 0
			selv.yPosisjon = 0
		}

	}

}
func (selv *TConsole) MHexadecimalSkrivut(nøkkel uint8) {
	buffer := []byte{'0', '0'}
	heksadesimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadesimal[(nøkkel>>4)&0xF]
	buffer[1] = heksadesimal[nøkkel&0xF]
	selv.MSkrivut(buffer)
}
func (selv *TConsole) MHexadecimalSkrivutxy(nøkkel uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksadesimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadesimal[(nøkkel>>4)&0xF]
	buffer[1] = heksadesimal[nøkkel&0xF]
	selv.MSkrivutxy(buffer, x, y)
}
func (selv *TConsole) MUnsignedinteger16Skrivut(nøkkel uint16) {
	selv.MHexadecimalSkrivut(uint8(nøkkel >> 8))
	selv.MHexadecimalSkrivut(uint8(nøkkel))
}
func (selv *TConsole) MUnsignedinteger16Skrivutxy(nøkkel uint16, x uint16, y uint16) {
	selv.MHexadecimalSkrivutxy(uint8(nøkkel>>8), x, y)
	selv.MHexadecimalSkrivutxy(uint8(nøkkel), x, y)
}
func (selv *TConsole) MUnsignedinteger32Skrivut(data uint32) {
	selv.MHexadecimalSkrivut(uint8(data >> 24))
	selv.MHexadecimalSkrivut(uint8(data >> 16))
	selv.MHexadecimalSkrivut(uint8(data >> 8))
	selv.MHexadecimalSkrivut(uint8(data))
}
func (selv *TConsole) MUnsignedinteger32Skrivutxy(data uint32, x uint16, y uint16) {

	selv.MHexadecimalSkrivutxy(uint8(data>>24), x+0, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>16), x+2, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>8), x+4, y)
	selv.MHexadecimalSkrivutxy(uint8(data), x+6, y)
}
func (selv *TConsole) MUnsignedinteger64Skrivut(data uint64) {
	selv.MHexadecimalSkrivut(uint8(data >> 56))
	selv.MHexadecimalSkrivut(uint8(data >> 48))
	selv.MHexadecimalSkrivut(uint8(data >> 40))
	selv.MHexadecimalSkrivut(uint8(data >> 32))
	selv.MHexadecimalSkrivut(uint8(data >> 24))
	selv.MHexadecimalSkrivut(uint8(data >> 16))
	selv.MHexadecimalSkrivut(uint8(data >> 8))
	selv.MHexadecimalSkrivut(uint8(data))
}
func (selv *TConsole) MUnsignedinteger64Skrivutxy(data uint64, x uint16, y uint16) {
	selv.MHexadecimalSkrivutxy(uint8(data>>56), x+0, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>48), x+2, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>40), x+4, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>32), x+6, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>24), x+8, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>16), x+10, y)
	selv.MHexadecimalSkrivutxy(uint8(data>>8), x+12, y)
	selv.MHexadecimalSkrivutxy(uint8(data), x+14, y)
}
func MSkrivut(phyaddr uintptr, data uint8, x uint32, y uint32)

func (selv *TConsole) MSkrivuthexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksadesimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadesimal[(data>>4)&0xF]
	buffer[1] = heksadesimal[data&0xF]

	MSkrivut(uintptr(fbphysaddress), buffer[0], x, y)
	MSkrivut(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (selv *TConsole) MSkrivutunsignedinteger16(data uint16, x uint32, y uint32) {
	selv.MSkrivuthexadecimal(uint8(data>>8), x+0*2, y)
	selv.MSkrivuthexadecimal(uint8(data), x+2*2, y)
}

func (selv *TConsole) MSkrivutunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	selv.MSkrivuthexadecimal(uint8(data>>24), x+0*2, y)
	selv.MSkrivuthexadecimal(uint8(data>>16), x+2*2, y)
	selv.MSkrivuthexadecimal(uint8(data>>8), x+4*2, y)
	selv.MSkrivuthexadecimal(uint8(data), x+6*2, y)
}

func (selv *TConsole) M테스트() {
}
