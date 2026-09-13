package консоль

import . "unsafe"

const (
	fbШирина		= 80
	fbВысота		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TКонсоль struct {
	xПозиция	uint16
	yПозиция	uint16
}

var последовательныйГотово bool

func Последовательныйinit()
func Последовательныйписатьбайт(данные uint8)

func MПоследовательныйЖурналinit() {
	Последовательныйinit()
	последовательныйГотово = true
}

func последовательныйЖурналбайт(данные byte) {
	if !последовательныйГотово {
		return
	}

	if данные == '\n' {
		Последовательныйписатьбайт('\r')
	}
	Последовательныйписатьбайт(uint8(данные))
}

func MEmergencyЖурналСтрока(данные string) {
	for i := 0; i < len(данные); i++ {
		последовательныйЖурналбайт(данные[i])
	}
}

func MEmergencyЖурналhexadecimal8(данные uint8) {
	const digits = "0123456789ABCDEF"
	последовательныйЖурналбайт(digits[(данные>>4)&0x0F])
	последовательныйЖурналбайт(digits[данные&0x0F])
}

func MEmergencyЖурналunsignedinteger32(данные uint32) {
	MEmergencyЖурналhexadecimal8(uint8(данные >> 24))
	MEmergencyЖурналhexadecimal8(uint8(данные >> 16))
	MEmergencyЖурналhexadecimal8(uint8(данные >> 8))
	MEmergencyЖурналhexadecimal8(uint8(данные))
}

func (текущий *TКонсоль) MПечать(argumentЗначение ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var значение_2 interface{}

	for i, p := range argumentЗначение {
		switch i {
		case 0:
			param, _ := p.(interface{})
			значение_2 = param
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

	текущий.MПечатьxy(значение_2, x, y)

}
func (текущий *TКонсоль) MПечатьxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		данные_2, _ := temporary_2.(string)
		текущий.MПечатьБайтxy(([]byte)(данные_2), x, y)
	case uint8:
		данные_2, _ := temporary_2.(uint8)
		текущий.MHexadecimalПечатьxy(данные_2, x, y)
	case uint16:
		данные_2, _ := temporary_2.(uint16)
		текущий.MUnsignedinteger16Печатьxy(данные_2, x, y)
	case uint32:
		данные_2, _ := temporary_2.(uint32)
		текущий.MUnsignedinteger32Печатьxy(данные_2, x, y)
	case uint64:
		данные_2, _ := temporary_2.(uint64)
		текущий.MUnsignedinteger64Печатьxy(данные_2, x, y)
	default:
		данные_2, _ := temporary_2.([]byte)
		текущий.MПечатьБайтxy(данные_2, x, y)
	}

}
func (текущий *TКонсоль) MПечатьБайтxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		текущий.xПозиция = x
	}
	if y <= 999 {
		текущий.yПозиция = y
	}

	атрибут := uint16(0x0F)
	ограничение := len(buffer)
	if ограничение > 4096 {
		ограничение = 4096
	}
	for i := 0; i < ограничение; i++ {
		последовательныйЖурналбайт(buffer[i])
		switch buffer[i] {
		case '\n':
			текущий.yПозиция++
			текущий.xПозиция = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*текущий.yПозиция+текущий.xПозиция)*2))) = атрибут<<8 | uint16(buffer[i])
			текущий.xПозиция++
		}

		if текущий.xПозиция >= 80 {
			текущий.yПозиция++
			текущий.xПозиция = 0
		}

		if текущий.yПозиция >= 25 {
			for текущий.yПозиция = 0; текущий.yПозиция < 25; текущий.yПозиция++ {
				for текущий.xПозиция = 0; текущий.xПозиция < 80; текущий.xПозиция++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*текущий.yПозиция+текущий.xПозиция)*2))) = атрибут<<8 | ' '
				}
			}
			текущий.xПозиция = 0
			текущий.yПозиция = 0
		}

	}

}
func (текущий *TКонсоль) MHexadecimalПечать(ключ uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ключ>>4)&0xF]
	buffer[1] = hex[ключ&0xF]
	текущий.MПечать(buffer)
}
func (текущий *TКонсоль) MHexadecimalПечатьxy(ключ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ключ>>4)&0xF]
	buffer[1] = hex[ключ&0xF]
	текущий.MПечатьxy(buffer, x, y)
}
func (текущий *TКонсоль) MUnsignedinteger16Печать(ключ uint16) {
	текущий.MHexadecimalПечать(uint8(ключ >> 8))
	текущий.MHexadecimalПечать(uint8(ключ))
}
func (текущий *TКонсоль) MUnsignedinteger16Печатьxy(ключ uint16, x uint16, y uint16) {
	текущий.MHexadecimalПечатьxy(uint8(ключ>>8), x, y)
	текущий.MHexadecimalПечатьxy(uint8(ключ), x, y)
}
func (текущий *TКонсоль) MUnsignedinteger32Печать(данные uint32) {
	текущий.MHexadecimalПечать(uint8(данные >> 24))
	текущий.MHexadecimalПечать(uint8(данные >> 16))
	текущий.MHexadecimalПечать(uint8(данные >> 8))
	текущий.MHexadecimalПечать(uint8(данные))
}
func (текущий *TКонсоль) MUnsignedinteger32Печатьxy(данные uint32, x uint16, y uint16) {

	текущий.MHexadecimalПечатьxy(uint8(данные>>24), x+0, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>16), x+2, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>8), x+4, y)
	текущий.MHexadecimalПечатьxy(uint8(данные), x+6, y)
}
func (текущий *TКонсоль) MUnsignedinteger64Печать(данные uint64) {
	текущий.MHexadecimalПечать(uint8(данные >> 56))
	текущий.MHexadecimalПечать(uint8(данные >> 48))
	текущий.MHexadecimalПечать(uint8(данные >> 40))
	текущий.MHexadecimalПечать(uint8(данные >> 32))
	текущий.MHexadecimalПечать(uint8(данные >> 24))
	текущий.MHexadecimalПечать(uint8(данные >> 16))
	текущий.MHexadecimalПечать(uint8(данные >> 8))
	текущий.MHexadecimalПечать(uint8(данные))
}
func (текущий *TКонсоль) MUnsignedinteger64Печатьxy(данные uint64, x uint16, y uint16) {
	текущий.MHexadecimalПечатьxy(uint8(данные>>56), x+0, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>48), x+2, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>40), x+4, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>32), x+6, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>24), x+8, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>16), x+10, y)
	текущий.MHexadecimalПечатьxy(uint8(данные>>8), x+12, y)
	текущий.MHexadecimalПечатьxy(uint8(данные), x+14, y)
}
func MПечать(phyaddr uintptr, данные uint8, x uint32, y uint32)

func (текущий *TКонсоль) MПечатьhexadecimal(данные uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(данные>>4)&0xF]
	buffer[1] = hex[данные&0xF]

	MПечать(uintptr(fbphysaddress), buffer[0], x, y)
	MПечать(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (текущий *TКонсоль) MПечатьunsignedinteger16(данные uint16, x uint32, y uint32) {
	текущий.MПечатьhexadecimal(uint8(данные>>8), x+0*2, y)
	текущий.MПечатьhexadecimal(uint8(данные), x+2*2, y)
}

func (текущий *TКонсоль) MПечатьunsignedinteger32(данные uint32, x uint32, y uint32) {
	x = x * 2
	текущий.MПечатьhexadecimal(uint8(данные>>24), x+0*2, y)
	текущий.MПечатьhexadecimal(uint8(данные>>16), x+2*2, y)
	текущий.MПечатьhexadecimal(uint8(данные>>8), x+4*2, y)
	текущий.MПечатьhexadecimal(uint8(данные), x+6*2, y)
}

func (текущий *TКонсоль) M테스트() {
}
