/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbLățime		= 80
	fbÎnălțime		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPoziție	uint16
	yPoziție	uint16
}

var seriePregătit bool

func Serieinit()
func SerieScrierebyte(data uint8)

func MSerieloginit() {
	Serieinit()
	seriePregătit = true
}

func serielogbyte(data byte) {
	if !seriePregătit {
		return
	}

	if data == '\n' {
		SerieScrierebyte('\r')
	}
	SerieScrierebyte(uint8(data))
}

func MEmergencylogȘir(data string) {
	for i := 0; i < len(data); i++ {
		serielogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serielogbyte(digits[(data>>4)&0x0F])
	serielogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (sine *TConsole) MTipărește(argumentValoare ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var valoare_2 interface{}

	for i, p := range argumentValoare {
		switch i {
		case 0:
			param, _ := p.(interface{})
			valoare_2 = param
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

	sine.MTipăreștexy(valoare_2, x, y)

}
func (sine *TConsole) MTipăreștexy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		sine.MTipăreșteOctețixy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		sine.MHexadecimalTipăreștexy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		sine.MUnsignedinteger16Tipăreștexy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		sine.MUnsignedinteger32Tipăreștexy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		sine.MUnsignedinteger64Tipăreștexy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		sine.MTipăreșteOctețixy(data_2, x, y)
	}

}
func (sine *TConsole) MTipăreșteOctețixy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		sine.xPoziție = x
	}
	if y <= 999 {
		sine.yPoziție = y
	}

	atribut := uint16(0x0F)
	limită := len(buffer)
	if limită > 4096 {
		limită = 4096
	}
	for i := 0; i < limită; i++ {
		serielogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			sine.yPoziție++
			sine.xPoziție = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*sine.yPoziție+sine.xPoziție)*2))) = atribut<<8 | uint16(buffer[i])
			sine.xPoziție++
		}

		if sine.xPoziție >= 80 {
			sine.yPoziție++
			sine.xPoziție = 0
		}

		if sine.yPoziție >= 25 {
			for sine.yPoziție = 0; sine.yPoziție < 25; sine.yPoziție++ {
				for sine.xPoziție = 0; sine.xPoziție < 80; sine.xPoziție++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*sine.yPoziție+sine.xPoziție)*2))) = atribut<<8 | ' '
				}
			}
			sine.xPoziție = 0
			sine.yPoziție = 0
		}

	}

}
func (sine *TConsole) MHexadecimalTipărește(cheie uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(cheie>>4)&0xF]
	buffer[1] = hex[cheie&0xF]
	sine.MTipărește(buffer)
}
func (sine *TConsole) MHexadecimalTipăreștexy(cheie uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(cheie>>4)&0xF]
	buffer[1] = hex[cheie&0xF]
	sine.MTipăreștexy(buffer, x, y)
}
func (sine *TConsole) MUnsignedinteger16Tipărește(cheie uint16) {
	sine.MHexadecimalTipărește(uint8(cheie >> 8))
	sine.MHexadecimalTipărește(uint8(cheie))
}
func (sine *TConsole) MUnsignedinteger16Tipăreștexy(cheie uint16, x uint16, y uint16) {
	sine.MHexadecimalTipăreștexy(uint8(cheie>>8), x, y)
	sine.MHexadecimalTipăreștexy(uint8(cheie), x, y)
}
func (sine *TConsole) MUnsignedinteger32Tipărește(data uint32) {
	sine.MHexadecimalTipărește(uint8(data >> 24))
	sine.MHexadecimalTipărește(uint8(data >> 16))
	sine.MHexadecimalTipărește(uint8(data >> 8))
	sine.MHexadecimalTipărește(uint8(data))
}
func (sine *TConsole) MUnsignedinteger32Tipăreștexy(data uint32, x uint16, y uint16) {

	sine.MHexadecimalTipăreștexy(uint8(data>>24), x+0, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>16), x+2, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>8), x+4, y)
	sine.MHexadecimalTipăreștexy(uint8(data), x+6, y)
}
func (sine *TConsole) MUnsignedinteger64Tipărește(data uint64) {
	sine.MHexadecimalTipărește(uint8(data >> 56))
	sine.MHexadecimalTipărește(uint8(data >> 48))
	sine.MHexadecimalTipărește(uint8(data >> 40))
	sine.MHexadecimalTipărește(uint8(data >> 32))
	sine.MHexadecimalTipărește(uint8(data >> 24))
	sine.MHexadecimalTipărește(uint8(data >> 16))
	sine.MHexadecimalTipărește(uint8(data >> 8))
	sine.MHexadecimalTipărește(uint8(data))
}
func (sine *TConsole) MUnsignedinteger64Tipăreștexy(data uint64, x uint16, y uint16) {
	sine.MHexadecimalTipăreștexy(uint8(data>>56), x+0, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>48), x+2, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>40), x+4, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>32), x+6, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>24), x+8, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>16), x+10, y)
	sine.MHexadecimalTipăreștexy(uint8(data>>8), x+12, y)
	sine.MHexadecimalTipăreștexy(uint8(data), x+14, y)
}
func MTipărește(phyaddr uintptr, data uint8, x uint32, y uint32)

func (sine *TConsole) MTipăreștehexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MTipărește(uintptr(fbphysaddress), buffer[0], x, y)
	MTipărește(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (sine *TConsole) MTipăreșteunsignedinteger16(data uint16, x uint32, y uint32) {
	sine.MTipăreștehexadecimal(uint8(data>>8), x+0*2, y)
	sine.MTipăreștehexadecimal(uint8(data), x+2*2, y)
}

func (sine *TConsole) MTipăreșteunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	sine.MTipăreștehexadecimal(uint8(data>>24), x+0*2, y)
	sine.MTipăreștehexadecimal(uint8(data>>16), x+2*2, y)
	sine.MTipăreștehexadecimal(uint8(data>>8), x+4*2, y)
	sine.MTipăreștehexadecimal(uint8(data), x+6*2, y)
}

func (sine *TConsole) M테스트() {
}
