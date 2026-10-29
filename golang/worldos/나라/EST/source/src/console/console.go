/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbKõrgus		= 80
	fbLaius			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xAsukoht	uint16
	yAsukoht	uint16
}

var järjenumberValmis bool

func Järjenumberinit()
func JärjenumberKirjutaminebyte(data uint8)

func MJärjenumberloginit() {
	Järjenumberinit()
	järjenumberValmis = true
}

func järjenumberlogbyte(data byte) {
	if !järjenumberValmis {
		return
	}

	if data == '\n' {
		JärjenumberKirjutaminebyte('\r')
	}
	JärjenumberKirjutaminebyte(uint8(data))
}

func MEmergencylogstring(data string) {
	for i := 0; i < len(data); i++ {
		järjenumberlogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	järjenumberlogbyte(digits[(data>>4)&0x0F])
	järjenumberlogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (ise *TConsole) MPrindi(argumentVäärtus ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var väärtus_2 interface{}

	for i, p := range argumentVäärtus {
		switch i {
		case 0:
			param, _ := p.(interface{})
			väärtus_2 = param
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

	ise.MPrindixy(väärtus_2, x, y)

}
func (ise *TConsole) MPrindixy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		ise.MPrindibaitixy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		ise.MHexadecimalPrindixy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		ise.MUnsignedinteger16Prindixy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		ise.MUnsignedinteger32Prindixy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		ise.MUnsignedinteger64Prindixy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		ise.MPrindibaitixy(data_2, x, y)
	}

}
func (ise *TConsole) MPrindibaitixy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		ise.xAsukoht = x
	}
	if y <= 999 {
		ise.yAsukoht = y
	}

	atribuut := uint16(0x0F)
	piir := len(buffer)
	if piir > 4096 {
		piir = 4096
	}
	for i := 0; i < piir; i++ {
		järjenumberlogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			ise.yAsukoht++
			ise.xAsukoht = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*ise.yAsukoht+ise.xAsukoht)*2))) = atribuut<<8 | uint16(buffer[i])
			ise.xAsukoht++
		}

		if ise.xAsukoht >= 80 {
			ise.yAsukoht++
			ise.xAsukoht = 0
		}

		if ise.yAsukoht >= 25 {
			for ise.yAsukoht = 0; ise.yAsukoht < 25; ise.yAsukoht++ {
				for ise.xAsukoht = 0; ise.xAsukoht < 80; ise.xAsukoht++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*ise.yAsukoht+ise.xAsukoht)*2))) = atribuut<<8 | ' '
				}
			}
			ise.xAsukoht = 0
			ise.yAsukoht = 0
		}

	}

}
func (ise *TConsole) MHexadecimalPrindi(võti uint8) {
	buffer := []byte{'0', '0'}
	väärtus16ndsüsteem := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = väärtus16ndsüsteem[(võti>>4)&0xF]
	buffer[1] = väärtus16ndsüsteem[võti&0xF]
	ise.MPrindi(buffer)
}
func (ise *TConsole) MHexadecimalPrindixy(võti uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	väärtus16ndsüsteem := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = väärtus16ndsüsteem[(võti>>4)&0xF]
	buffer[1] = väärtus16ndsüsteem[võti&0xF]
	ise.MPrindixy(buffer, x, y)
}
func (ise *TConsole) MUnsignedinteger16Prindi(võti uint16) {
	ise.MHexadecimalPrindi(uint8(võti >> 8))
	ise.MHexadecimalPrindi(uint8(võti))
}
func (ise *TConsole) MUnsignedinteger16Prindixy(võti uint16, x uint16, y uint16) {
	ise.MHexadecimalPrindixy(uint8(võti>>8), x, y)
	ise.MHexadecimalPrindixy(uint8(võti), x, y)
}
func (ise *TConsole) MUnsignedinteger32Prindi(data uint32) {
	ise.MHexadecimalPrindi(uint8(data >> 24))
	ise.MHexadecimalPrindi(uint8(data >> 16))
	ise.MHexadecimalPrindi(uint8(data >> 8))
	ise.MHexadecimalPrindi(uint8(data))
}
func (ise *TConsole) MUnsignedinteger32Prindixy(data uint32, x uint16, y uint16) {

	ise.MHexadecimalPrindixy(uint8(data>>24), x+0, y)
	ise.MHexadecimalPrindixy(uint8(data>>16), x+2, y)
	ise.MHexadecimalPrindixy(uint8(data>>8), x+4, y)
	ise.MHexadecimalPrindixy(uint8(data), x+6, y)
}
func (ise *TConsole) MUnsignedinteger64Prindi(data uint64) {
	ise.MHexadecimalPrindi(uint8(data >> 56))
	ise.MHexadecimalPrindi(uint8(data >> 48))
	ise.MHexadecimalPrindi(uint8(data >> 40))
	ise.MHexadecimalPrindi(uint8(data >> 32))
	ise.MHexadecimalPrindi(uint8(data >> 24))
	ise.MHexadecimalPrindi(uint8(data >> 16))
	ise.MHexadecimalPrindi(uint8(data >> 8))
	ise.MHexadecimalPrindi(uint8(data))
}
func (ise *TConsole) MUnsignedinteger64Prindixy(data uint64, x uint16, y uint16) {
	ise.MHexadecimalPrindixy(uint8(data>>56), x+0, y)
	ise.MHexadecimalPrindixy(uint8(data>>48), x+2, y)
	ise.MHexadecimalPrindixy(uint8(data>>40), x+4, y)
	ise.MHexadecimalPrindixy(uint8(data>>32), x+6, y)
	ise.MHexadecimalPrindixy(uint8(data>>24), x+8, y)
	ise.MHexadecimalPrindixy(uint8(data>>16), x+10, y)
	ise.MHexadecimalPrindixy(uint8(data>>8), x+12, y)
	ise.MHexadecimalPrindixy(uint8(data), x+14, y)
}
func MPrindi(phyaddr uintptr, data uint8, x uint32, y uint32)

func (ise *TConsole) MPrindihexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	väärtus16ndsüsteem := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = väärtus16ndsüsteem[(data>>4)&0xF]
	buffer[1] = väärtus16ndsüsteem[data&0xF]

	MPrindi(uintptr(fbphysaddress), buffer[0], x, y)
	MPrindi(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (ise *TConsole) MPrindiunsignedinteger16(data uint16, x uint32, y uint32) {
	ise.MPrindihexadecimal(uint8(data>>8), x+0*2, y)
	ise.MPrindihexadecimal(uint8(data), x+2*2, y)
}

func (ise *TConsole) MPrindiunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	ise.MPrindihexadecimal(uint8(data>>24), x+0*2, y)
	ise.MPrindihexadecimal(uint8(data>>16), x+2*2, y)
	ise.MPrindihexadecimal(uint8(data>>8), x+4*2, y)
	ise.MPrindihexadecimal(uint8(data), x+6*2, y)
}

func (ise *TConsole) M테스트() {
}
