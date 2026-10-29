/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package конзола

import . "unsafe"

const (
	fbŠirina		= 80
	fbVisina		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TКонзола struct {
	xПоложај	uint16
	yПоложај	uint16
}

var серијскиСпреман bool

func Серијскиinit()
func Серијскиupisbyte(data uint8)

func MСеријскиДневникinit() {
	Серијскиinit()
	серијскиСпреман = true
}

func серијскиДневникbyte(data byte) {
	if !серијскиСпреман {
		return
	}

	if data == '\n' {
		Серијскиupisbyte('\r')
	}
	Серијскиupisbyte(uint8(data))
}

func MEmergencyДневникниска(data string) {
	for i := 0; i < len(data); i++ {
		серијскиДневникbyte(data[i])
	}
}

func MEmergencyДневникhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	серијскиДневникbyte(digits[(data>>4)&0x0F])
	серијскиДневникbyte(digits[data&0x0F])
}

func MEmergencyДневникunsignedinteger32(data uint32) {
	MEmergencyДневникhexadecimal8(uint8(data >> 24))
	MEmergencyДневникhexadecimal8(uint8(data >> 16))
	MEmergencyДневникhexadecimal8(uint8(data >> 8))
	MEmergencyДневникhexadecimal8(uint8(data))
}

func (isti *TКонзола) MŠtampaj(argumentВредност ...interface{}) {
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

	isti.MŠtampajxy(вредност_2, x, y)

}
func (isti *TКонзола) MŠtampajxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		isti.MŠtampajBajtovaxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		isti.MHexadecimalŠtampajxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		isti.MUnsignedinteger16Štampajxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		isti.MUnsignedinteger32Štampajxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		isti.MUnsignedinteger64Štampajxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		isti.MŠtampajBajtovaxy(data_2, x, y)
	}

}
func (isti *TКонзола) MŠtampajBajtovaxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		isti.xПоложај = x
	}
	if y <= 999 {
		isti.yПоложај = y
	}

	atribut := uint16(0x0F)
	ограничи := len(buffer)
	if ограничи > 4096 {
		ограничи = 4096
	}
	for i := 0; i < ограничи; i++ {
		серијскиДневникbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			isti.yПоложај++
			isti.xПоложај = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*isti.yПоложај+isti.xПоложај)*2))) = atribut<<8 | uint16(buffer[i])
			isti.xПоложај++
		}

		if isti.xПоложај >= 80 {
			isti.yПоложај++
			isti.xПоложај = 0
		}

		if isti.yПоложај >= 25 {
			for isti.yПоложај = 0; isti.yПоложај < 25; isti.yПоложај++ {
				for isti.xПоложај = 0; isti.xПоложај < 80; isti.xПоложај++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*isti.yПоложај+isti.xПоложај)*2))) = atribut<<8 | ' '
				}
			}
			isti.xПоложај = 0
			isti.yПоложај = 0
		}

	}

}
func (isti *TКонзола) MHexadecimalŠtampaj(кључ uint8) {
	buffer := []byte{'0', '0'}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(кључ>>4)&0xF]
	buffer[1] = heksadecimalno[кључ&0xF]
	isti.MŠtampaj(buffer)
}
func (isti *TКонзола) MHexadecimalŠtampajxy(кључ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(кључ>>4)&0xF]
	buffer[1] = heksadecimalno[кључ&0xF]
	isti.MŠtampajxy(buffer, x, y)
}
func (isti *TКонзола) MUnsignedinteger16Štampaj(кључ uint16) {
	isti.MHexadecimalŠtampaj(uint8(кључ >> 8))
	isti.MHexadecimalŠtampaj(uint8(кључ))
}
func (isti *TКонзола) MUnsignedinteger16Štampajxy(кључ uint16, x uint16, y uint16) {
	isti.MHexadecimalŠtampajxy(uint8(кључ>>8), x, y)
	isti.MHexadecimalŠtampajxy(uint8(кључ), x, y)
}
func (isti *TКонзола) MUnsignedinteger32Štampaj(data uint32) {
	isti.MHexadecimalŠtampaj(uint8(data >> 24))
	isti.MHexadecimalŠtampaj(uint8(data >> 16))
	isti.MHexadecimalŠtampaj(uint8(data >> 8))
	isti.MHexadecimalŠtampaj(uint8(data))
}
func (isti *TКонзола) MUnsignedinteger32Štampajxy(data uint32, x uint16, y uint16) {

	isti.MHexadecimalŠtampajxy(uint8(data>>24), x+0, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>16), x+2, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>8), x+4, y)
	isti.MHexadecimalŠtampajxy(uint8(data), x+6, y)
}
func (isti *TКонзола) MUnsignedinteger64Štampaj(data uint64) {
	isti.MHexadecimalŠtampaj(uint8(data >> 56))
	isti.MHexadecimalŠtampaj(uint8(data >> 48))
	isti.MHexadecimalŠtampaj(uint8(data >> 40))
	isti.MHexadecimalŠtampaj(uint8(data >> 32))
	isti.MHexadecimalŠtampaj(uint8(data >> 24))
	isti.MHexadecimalŠtampaj(uint8(data >> 16))
	isti.MHexadecimalŠtampaj(uint8(data >> 8))
	isti.MHexadecimalŠtampaj(uint8(data))
}
func (isti *TКонзола) MUnsignedinteger64Štampajxy(data uint64, x uint16, y uint16) {
	isti.MHexadecimalŠtampajxy(uint8(data>>56), x+0, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>48), x+2, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>40), x+4, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>32), x+6, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>24), x+8, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>16), x+10, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>8), x+12, y)
	isti.MHexadecimalŠtampajxy(uint8(data), x+14, y)
}
func MŠtampaj(phyaddr uintptr, data uint8, x uint32, y uint32)

func (isti *TКонзола) MŠtampajhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(data>>4)&0xF]
	buffer[1] = heksadecimalno[data&0xF]

	MŠtampaj(uintptr(fbphysaddress), buffer[0], x, y)
	MŠtampaj(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (isti *TКонзола) MŠtampajunsignedinteger16(data uint16, x uint32, y uint32) {
	isti.MŠtampajhexadecimal(uint8(data>>8), x+0*2, y)
	isti.MŠtampajhexadecimal(uint8(data), x+2*2, y)
}

func (isti *TКонзола) MŠtampajunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	isti.MŠtampajhexadecimal(uint8(data>>24), x+0*2, y)
	isti.MŠtampajhexadecimal(uint8(data>>16), x+2*2, y)
	isti.MŠtampajhexadecimal(uint8(data>>8), x+4*2, y)
	isti.MŠtampajhexadecimal(uint8(data), x+6*2, y)
}

func (isti *TКонзола) M테스트() {
}
