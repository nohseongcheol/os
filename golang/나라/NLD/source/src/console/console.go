package console

import . "unsafe"

const (
	fbBreedte		= 80
	fbHoogte		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPositie	uint16
	yPositie	uint16
}

var serienummerKlaar bool

func Serienummerinit()
func SerienummerSchrijvenbyte(data uint8)

func MSerienummerLogboekinit() {
	Serienummerinit()
	serienummerKlaar = true
}

func serienummerLogboekbyte(data byte) {
	if !serienummerKlaar {
		return
	}

	if data == '\n' {
		SerienummerSchrijvenbyte('\r')
	}
	SerienummerSchrijvenbyte(uint8(data))
}

func MEmergencyLogboekTekstsnoer(data string) {
	for i := 0; i < len(data); i++ {
		serienummerLogboekbyte(data[i])
	}
}

func MEmergencyLogboekhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serienummerLogboekbyte(digits[(data>>4)&0x0F])
	serienummerLogboekbyte(digits[data&0x0F])
}

func MEmergencyLogboekunsignedinteger32(data uint32) {
	MEmergencyLogboekhexadecimal8(uint8(data >> 24))
	MEmergencyLogboekhexadecimal8(uint8(data >> 16))
	MEmergencyLogboekhexadecimal8(uint8(data >> 8))
	MEmergencyLogboekhexadecimal8(uint8(data))
}

func (zelf *TConsole) MAfdrukken(argumentWaarde ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var waarde_2 interface{}

	for i, p := range argumentWaarde {
		switch i {
		case 0:
			param, _ := p.(interface{})
			waarde_2 = param
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

	zelf.MAfdrukkenxy(waarde_2, x, y)

}
func (zelf *TConsole) MAfdrukkenxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		zelf.MAfdrukkenbytesxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		zelf.MHexadecimalAfdrukkenxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		zelf.MUnsignedinteger16Afdrukkenxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		zelf.MUnsignedinteger32Afdrukkenxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		zelf.MUnsignedinteger64Afdrukkenxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		zelf.MAfdrukkenbytesxy(data_2, x, y)
	}

}
func (zelf *TConsole) MAfdrukkenbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		zelf.xPositie = x
	}
	if y <= 999 {
		zelf.yPositie = y
	}

	attribuut := uint16(0x0F)
	beperken := len(buffer)
	if beperken > 4096 {
		beperken = 4096
	}
	for i := 0; i < beperken; i++ {
		serienummerLogboekbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			zelf.yPositie++
			zelf.xPositie = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*zelf.yPositie+zelf.xPositie)*2))) = attribuut<<8 | uint16(buffer[i])
			zelf.xPositie++
		}

		if zelf.xPositie >= 80 {
			zelf.yPositie++
			zelf.xPositie = 0
		}

		if zelf.yPositie >= 25 {
			for zelf.yPositie = 0; zelf.yPositie < 25; zelf.yPositie++ {
				for zelf.xPositie = 0; zelf.xPositie < 80; zelf.xPositie++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*zelf.yPositie+zelf.xPositie)*2))) = attribuut<<8 | ' '
				}
			}
			zelf.xPositie = 0
			zelf.yPositie = 0
		}

	}

}
func (zelf *TConsole) MHexadecimalAfdrukken(sleutel uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(sleutel>>4)&0xF]
	buffer[1] = hex[sleutel&0xF]
	zelf.MAfdrukken(buffer)
}
func (zelf *TConsole) MHexadecimalAfdrukkenxy(sleutel uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(sleutel>>4)&0xF]
	buffer[1] = hex[sleutel&0xF]
	zelf.MAfdrukkenxy(buffer, x, y)
}
func (zelf *TConsole) MUnsignedinteger16Afdrukken(sleutel uint16) {
	zelf.MHexadecimalAfdrukken(uint8(sleutel >> 8))
	zelf.MHexadecimalAfdrukken(uint8(sleutel))
}
func (zelf *TConsole) MUnsignedinteger16Afdrukkenxy(sleutel uint16, x uint16, y uint16) {
	zelf.MHexadecimalAfdrukkenxy(uint8(sleutel>>8), x, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(sleutel), x, y)
}
func (zelf *TConsole) MUnsignedinteger32Afdrukken(data uint32) {
	zelf.MHexadecimalAfdrukken(uint8(data >> 24))
	zelf.MHexadecimalAfdrukken(uint8(data >> 16))
	zelf.MHexadecimalAfdrukken(uint8(data >> 8))
	zelf.MHexadecimalAfdrukken(uint8(data))
}
func (zelf *TConsole) MUnsignedinteger32Afdrukkenxy(data uint32, x uint16, y uint16) {

	zelf.MHexadecimalAfdrukkenxy(uint8(data>>24), x+0, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>16), x+2, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>8), x+4, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data), x+6, y)
}
func (zelf *TConsole) MUnsignedinteger64Afdrukken(data uint64) {
	zelf.MHexadecimalAfdrukken(uint8(data >> 56))
	zelf.MHexadecimalAfdrukken(uint8(data >> 48))
	zelf.MHexadecimalAfdrukken(uint8(data >> 40))
	zelf.MHexadecimalAfdrukken(uint8(data >> 32))
	zelf.MHexadecimalAfdrukken(uint8(data >> 24))
	zelf.MHexadecimalAfdrukken(uint8(data >> 16))
	zelf.MHexadecimalAfdrukken(uint8(data >> 8))
	zelf.MHexadecimalAfdrukken(uint8(data))
}
func (zelf *TConsole) MUnsignedinteger64Afdrukkenxy(data uint64, x uint16, y uint16) {
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>56), x+0, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>48), x+2, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>40), x+4, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>32), x+6, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>24), x+8, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>16), x+10, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data>>8), x+12, y)
	zelf.MHexadecimalAfdrukkenxy(uint8(data), x+14, y)
}
func MAfdrukken(phyaddr uintptr, data uint8, x uint32, y uint32)

func (zelf *TConsole) MAfdrukkenhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MAfdrukken(uintptr(fbphysaddress), buffer[0], x, y)
	MAfdrukken(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (zelf *TConsole) MAfdrukkenunsignedinteger16(data uint16, x uint32, y uint32) {
	zelf.MAfdrukkenhexadecimal(uint8(data>>8), x+0*2, y)
	zelf.MAfdrukkenhexadecimal(uint8(data), x+2*2, y)
}

func (zelf *TConsole) MAfdrukkenunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	zelf.MAfdrukkenhexadecimal(uint8(data>>24), x+0*2, y)
	zelf.MAfdrukkenhexadecimal(uint8(data>>16), x+2*2, y)
	zelf.MAfdrukkenhexadecimal(uint8(data>>8), x+4*2, y)
	zelf.MAfdrukkenhexadecimal(uint8(data), x+6*2, y)
}

func (zelf *TConsole) M테스트() {
}
