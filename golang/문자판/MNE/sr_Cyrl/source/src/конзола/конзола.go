package конзола

import . "unsafe"

const (
	fbШирина		= 80
	fbВисина		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TКонзола struct {
	xПоложај	uint16
	yПоложај	uint16
}

var серијскиСпреман bool

func Серијскиinit()
func СеријскиПишеbyte(data uint8)

func MСеријскиДневникinit() {
	Серијскиinit()
	серијскиСпреман = true
}

func серијскиДневникbyte(data byte) {
	if !серијскиСпреман {
		return
	}

	if data == '\n' {
		СеријскиПишеbyte('\r')
	}
	СеријскиПишеbyte(uint8(data))
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

func (исти *TКонзола) MШтампај(argumentВредност ...interface{}) {
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

	исти.MШтампајxy(вредност_2, x, y)

}
func (исти *TКонзола) MШтампајxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		исти.MШтампајБајтоваxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		исти.MHexadecimalШтампајxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		исти.MUnsignedinteger16Штампајxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		исти.MUnsignedinteger32Штампајxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		исти.MUnsignedinteger64Штампајxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		исти.MШтампајБајтоваxy(data_2, x, y)
	}

}
func (исти *TКонзола) MШтампајБајтоваxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		исти.xПоложај = x
	}
	if y <= 999 {
		исти.yПоложај = y
	}

	атрибут := uint16(0x0F)
	ограничи := len(buffer)
	if ограничи > 4096 {
		ограничи = 4096
	}
	for i := 0; i < ограничи; i++ {
		серијскиДневникbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			исти.yПоложај++
			исти.xПоложај = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*исти.yПоложај+исти.xПоложај)*2))) = атрибут<<8 | uint16(buffer[i])
			исти.xПоложај++
		}

		if исти.xПоложај >= 80 {
			исти.yПоложај++
			исти.xПоложај = 0
		}

		if исти.yПоложај >= 25 {
			for исти.yПоложај = 0; исти.yПоложај < 25; исти.yПоложај++ {
				for исти.xПоложај = 0; исти.xПоложај < 80; исти.xПоложај++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*исти.yПоложај+исти.xПоложај)*2))) = атрибут<<8 | ' '
				}
			}
			исти.xПоложај = 0
			исти.yПоложај = 0
		}

	}

}
func (исти *TКонзола) MHexadecimalШтампај(кључ uint8) {
	buffer := []byte{'0', '0'}
	хексадецимално := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хексадецимално[(кључ>>4)&0xF]
	buffer[1] = хексадецимално[кључ&0xF]
	исти.MШтампај(buffer)
}
func (исти *TКонзола) MHexadecimalШтампајxy(кључ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	хексадецимално := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хексадецимално[(кључ>>4)&0xF]
	buffer[1] = хексадецимално[кључ&0xF]
	исти.MШтампајxy(buffer, x, y)
}
func (исти *TКонзола) MUnsignedinteger16Штампај(кључ uint16) {
	исти.MHexadecimalШтампај(uint8(кључ >> 8))
	исти.MHexadecimalШтампај(uint8(кључ))
}
func (исти *TКонзола) MUnsignedinteger16Штампајxy(кључ uint16, x uint16, y uint16) {
	исти.MHexadecimalШтампајxy(uint8(кључ>>8), x, y)
	исти.MHexadecimalШтампајxy(uint8(кључ), x, y)
}
func (исти *TКонзола) MUnsignedinteger32Штампај(data uint32) {
	исти.MHexadecimalШтампај(uint8(data >> 24))
	исти.MHexadecimalШтампај(uint8(data >> 16))
	исти.MHexadecimalШтампај(uint8(data >> 8))
	исти.MHexadecimalШтампај(uint8(data))
}
func (исти *TКонзола) MUnsignedinteger32Штампајxy(data uint32, x uint16, y uint16) {

	исти.MHexadecimalШтампајxy(uint8(data>>24), x+0, y)
	исти.MHexadecimalШтампајxy(uint8(data>>16), x+2, y)
	исти.MHexadecimalШтампајxy(uint8(data>>8), x+4, y)
	исти.MHexadecimalШтампајxy(uint8(data), x+6, y)
}
func (исти *TКонзола) MUnsignedinteger64Штампај(data uint64) {
	исти.MHexadecimalШтампај(uint8(data >> 56))
	исти.MHexadecimalШтампај(uint8(data >> 48))
	исти.MHexadecimalШтампај(uint8(data >> 40))
	исти.MHexadecimalШтампај(uint8(data >> 32))
	исти.MHexadecimalШтампај(uint8(data >> 24))
	исти.MHexadecimalШтампај(uint8(data >> 16))
	исти.MHexadecimalШтампај(uint8(data >> 8))
	исти.MHexadecimalШтампај(uint8(data))
}
func (исти *TКонзола) MUnsignedinteger64Штампајxy(data uint64, x uint16, y uint16) {
	исти.MHexadecimalШтампајxy(uint8(data>>56), x+0, y)
	исти.MHexadecimalШтампајxy(uint8(data>>48), x+2, y)
	исти.MHexadecimalШтампајxy(uint8(data>>40), x+4, y)
	исти.MHexadecimalШтампајxy(uint8(data>>32), x+6, y)
	исти.MHexadecimalШтампајxy(uint8(data>>24), x+8, y)
	исти.MHexadecimalШтампајxy(uint8(data>>16), x+10, y)
	исти.MHexadecimalШтампајxy(uint8(data>>8), x+12, y)
	исти.MHexadecimalШтампајxy(uint8(data), x+14, y)
}
func MШтампај(phyaddr uintptr, data uint8, x uint32, y uint32)

func (исти *TКонзола) MШтампајhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	хексадецимално := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = хексадецимално[(data>>4)&0xF]
	buffer[1] = хексадецимално[data&0xF]

	MШтампај(uintptr(fbphysaddress), buffer[0], x, y)
	MШтампај(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (исти *TКонзола) MШтампајunsignedinteger16(data uint16, x uint32, y uint32) {
	исти.MШтампајhexadecimal(uint8(data>>8), x+0*2, y)
	исти.MШтампајhexadecimal(uint8(data), x+2*2, y)
}

func (исти *TКонзола) MШтампајunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	исти.MШтампајhexadecimal(uint8(data>>24), x+0*2, y)
	исти.MШтампајhexadecimal(uint8(data>>16), x+2*2, y)
	исти.MШтампајhexadecimal(uint8(data>>8), x+4*2, y)
	исти.MШтампајhexadecimal(uint8(data), x+6*2, y)
}

func (исти *TКонзола) M테스트() {
}
