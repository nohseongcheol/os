/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbШирочина		= 80
	fbВисочина		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xПозиция	uint16
	yПозиция	uint16
}

var сериенномерГотово bool

func Сериенномерinit()
func СериенномерПисанеbyte(data uint8)

func MСериенномерЛогinit() {
	Сериенномерinit()
	сериенномерГотово = true
}

func сериенномерЛогbyte(data byte) {
	if !сериенномерГотово {
		return
	}

	if data == '\n' {
		СериенномерПисанеbyte('\r')
	}
	СериенномерПисанеbyte(uint8(data))
}

func MEmergencyЛогНиз(data string) {
	for i := 0; i < len(data); i++ {
		сериенномерЛогbyte(data[i])
	}
}

func MEmergencyЛогhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	сериенномерЛогbyte(digits[(data>>4)&0x0F])
	сериенномерЛогbyte(digits[data&0x0F])
}

func MEmergencyЛогunsignedinteger32(data uint32) {
	MEmergencyЛогhexadecimal8(uint8(data >> 24))
	MEmergencyЛогhexadecimal8(uint8(data >> 16))
	MEmergencyЛогhexadecimal8(uint8(data >> 8))
	MEmergencyЛогhexadecimal8(uint8(data))
}

func (себеси *TConsole) MПечат(argumentСтойност ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var стойност_2 interface{}

	for i, p := range argumentСтойност {
		switch i {
		case 0:
			param, _ := p.(interface{})
			стойност_2 = param
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

	себеси.MПечатxy(стойност_2, x, y)

}
func (себеси *TConsole) MПечатxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		себеси.MПечатБайтовеxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		себеси.MHexadecimalПечатxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		себеси.MUnsignedinteger16Печатxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		себеси.MUnsignedinteger32Печатxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		себеси.MUnsignedinteger64Печатxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		себеси.MПечатБайтовеxy(data_2, x, y)
	}

}
func (себеси *TConsole) MПечатБайтовеxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		себеси.xПозиция = x
	}
	if y <= 999 {
		себеси.yПозиция = y
	}

	атрибут := uint16(0x0F)
	ограничение := len(buffer)
	if ограничение > 4096 {
		ограничение = 4096
	}
	for i := 0; i < ограничение; i++ {
		сериенномерЛогbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			себеси.yПозиция++
			себеси.xПозиция = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*себеси.yПозиция+себеси.xПозиция)*2))) = атрибут<<8 | uint16(buffer[i])
			себеси.xПозиция++
		}

		if себеси.xПозиция >= 80 {
			себеси.yПозиция++
			себеси.xПозиция = 0
		}

		if себеси.yПозиция >= 25 {
			for себеси.yПозиция = 0; себеси.yПозиция < 25; себеси.yПозиция++ {
				for себеси.xПозиция = 0; себеси.xПозиция < 80; себеси.xПозиция++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*себеси.yПозиция+себеси.xПозиция)*2))) = атрибут<<8 | ' '
				}
			}
			себеси.xПозиция = 0
			себеси.yПозиция = 0
		}

	}

}
func (себеси *TConsole) MHexadecimalПечат(ключ uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ключ>>4)&0xF]
	buffer[1] = hex[ключ&0xF]
	себеси.MПечат(buffer)
}
func (себеси *TConsole) MHexadecimalПечатxy(ключ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ключ>>4)&0xF]
	buffer[1] = hex[ключ&0xF]
	себеси.MПечатxy(buffer, x, y)
}
func (себеси *TConsole) MUnsignedinteger16Печат(ключ uint16) {
	себеси.MHexadecimalПечат(uint8(ключ >> 8))
	себеси.MHexadecimalПечат(uint8(ключ))
}
func (себеси *TConsole) MUnsignedinteger16Печатxy(ключ uint16, x uint16, y uint16) {
	себеси.MHexadecimalПечатxy(uint8(ключ>>8), x, y)
	себеси.MHexadecimalПечатxy(uint8(ключ), x, y)
}
func (себеси *TConsole) MUnsignedinteger32Печат(data uint32) {
	себеси.MHexadecimalПечат(uint8(data >> 24))
	себеси.MHexadecimalПечат(uint8(data >> 16))
	себеси.MHexadecimalПечат(uint8(data >> 8))
	себеси.MHexadecimalПечат(uint8(data))
}
func (себеси *TConsole) MUnsignedinteger32Печатxy(data uint32, x uint16, y uint16) {

	себеси.MHexadecimalПечатxy(uint8(data>>24), x+0, y)
	себеси.MHexadecimalПечатxy(uint8(data>>16), x+2, y)
	себеси.MHexadecimalПечатxy(uint8(data>>8), x+4, y)
	себеси.MHexadecimalПечатxy(uint8(data), x+6, y)
}
func (себеси *TConsole) MUnsignedinteger64Печат(data uint64) {
	себеси.MHexadecimalПечат(uint8(data >> 56))
	себеси.MHexadecimalПечат(uint8(data >> 48))
	себеси.MHexadecimalПечат(uint8(data >> 40))
	себеси.MHexadecimalПечат(uint8(data >> 32))
	себеси.MHexadecimalПечат(uint8(data >> 24))
	себеси.MHexadecimalПечат(uint8(data >> 16))
	себеси.MHexadecimalПечат(uint8(data >> 8))
	себеси.MHexadecimalПечат(uint8(data))
}
func (себеси *TConsole) MUnsignedinteger64Печатxy(data uint64, x uint16, y uint16) {
	себеси.MHexadecimalПечатxy(uint8(data>>56), x+0, y)
	себеси.MHexadecimalПечатxy(uint8(data>>48), x+2, y)
	себеси.MHexadecimalПечатxy(uint8(data>>40), x+4, y)
	себеси.MHexadecimalПечатxy(uint8(data>>32), x+6, y)
	себеси.MHexadecimalПечатxy(uint8(data>>24), x+8, y)
	себеси.MHexadecimalПечатxy(uint8(data>>16), x+10, y)
	себеси.MHexadecimalПечатxy(uint8(data>>8), x+12, y)
	себеси.MHexadecimalПечатxy(uint8(data), x+14, y)
}
func MПечат(phyaddr uintptr, data uint8, x uint32, y uint32)

func (себеси *TConsole) MПечатhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MПечат(uintptr(fbphysaddress), buffer[0], x, y)
	MПечат(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (себеси *TConsole) MПечатunsignedinteger16(data uint16, x uint32, y uint32) {
	себеси.MПечатhexadecimal(uint8(data>>8), x+0*2, y)
	себеси.MПечатhexadecimal(uint8(data), x+2*2, y)
}

func (себеси *TConsole) MПечатunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	себеси.MПечатhexadecimal(uint8(data>>24), x+0*2, y)
	себеси.MПечатhexadecimal(uint8(data>>16), x+2*2, y)
	себеси.MПечатhexadecimal(uint8(data>>8), x+4*2, y)
	себеси.MПечатhexadecimal(uint8(data), x+6*2, y)
}

func (себеси *TConsole) M테스트() {
}
