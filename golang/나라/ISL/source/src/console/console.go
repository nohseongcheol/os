package console

import . "unsafe"

const (
	fbBreidd		= 80
	fbHæð			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xStaða	uint16
	yStaða	uint16
}

var raðnúmerTilbúið bool

func Raðnúmerinit()
func RaðnúmerSkriftbyte(data uint8)

func MRaðnúmerloginit() {
	Raðnúmerinit()
	raðnúmerTilbúið = true
}

func raðnúmerlogbyte(data byte) {
	if !raðnúmerTilbúið {
		return
	}

	if data == '\n' {
		RaðnúmerSkriftbyte('\r')
	}
	RaðnúmerSkriftbyte(uint8(data))
}

func MEmergencylogStrengur(data string) {
	for i := 0; i < len(data); i++ {
		raðnúmerlogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	raðnúmerlogbyte(digits[(data>>4)&0x0F])
	raðnúmerlogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (sjálft *TConsole) MPrenta(argumentGildi ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var gildi_3 interface{}

	for i, p := range argumentGildi {
		switch i {
		case 0:
			param, _ := p.(interface{})
			gildi_3 = param
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

	sjálft.MPrentaxy(gildi_3, x, y)

}
func (sjálft *TConsole) MPrentaxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		sjálft.MPrentaBætixy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		sjálft.MHexadecimalPrentaxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		sjálft.MUnsignedinteger16Prentaxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		sjálft.MUnsignedinteger32Prentaxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		sjálft.MUnsignedinteger64Prentaxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		sjálft.MPrentaBætixy(data_2, x, y)
	}

}
func (sjálft *TConsole) MPrentaBætixy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		sjálft.xStaða = x
	}
	if y <= 999 {
		sjálft.yStaða = y
	}

	eigindi := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		raðnúmerlogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			sjálft.yStaða++
			sjálft.xStaða = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*sjálft.yStaða+sjálft.xStaða)*2))) = eigindi<<8 | uint16(buffer[i])
			sjálft.xStaða++
		}

		if sjálft.xStaða >= 80 {
			sjálft.yStaða++
			sjálft.xStaða = 0
		}

		if sjálft.yStaða >= 25 {
			for sjálft.yStaða = 0; sjálft.yStaða < 25; sjálft.yStaða++ {
				for sjálft.xStaða = 0; sjálft.xStaða < 80; sjálft.xStaða++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*sjálft.yStaða+sjálft.xStaða)*2))) = eigindi<<8 | ' '
				}
			}
			sjálft.xStaða = 0
			sjálft.yStaða = 0
		}

	}

}
func (sjálft *TConsole) MHexadecimalPrenta(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	sjálft.MPrenta(buffer)
}
func (sjálft *TConsole) MHexadecimalPrentaxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	sjálft.MPrentaxy(buffer, x, y)
}
func (sjálft *TConsole) MUnsignedinteger16Prenta(key uint16) {
	sjálft.MHexadecimalPrenta(uint8(key >> 8))
	sjálft.MHexadecimalPrenta(uint8(key))
}
func (sjálft *TConsole) MUnsignedinteger16Prentaxy(key uint16, x uint16, y uint16) {
	sjálft.MHexadecimalPrentaxy(uint8(key>>8), x, y)
	sjálft.MHexadecimalPrentaxy(uint8(key), x, y)
}
func (sjálft *TConsole) MUnsignedinteger32Prenta(data uint32) {
	sjálft.MHexadecimalPrenta(uint8(data >> 24))
	sjálft.MHexadecimalPrenta(uint8(data >> 16))
	sjálft.MHexadecimalPrenta(uint8(data >> 8))
	sjálft.MHexadecimalPrenta(uint8(data))
}
func (sjálft *TConsole) MUnsignedinteger32Prentaxy(data uint32, x uint16, y uint16) {

	sjálft.MHexadecimalPrentaxy(uint8(data>>24), x+0, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>16), x+2, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>8), x+4, y)
	sjálft.MHexadecimalPrentaxy(uint8(data), x+6, y)
}
func (sjálft *TConsole) MUnsignedinteger64Prenta(data uint64) {
	sjálft.MHexadecimalPrenta(uint8(data >> 56))
	sjálft.MHexadecimalPrenta(uint8(data >> 48))
	sjálft.MHexadecimalPrenta(uint8(data >> 40))
	sjálft.MHexadecimalPrenta(uint8(data >> 32))
	sjálft.MHexadecimalPrenta(uint8(data >> 24))
	sjálft.MHexadecimalPrenta(uint8(data >> 16))
	sjálft.MHexadecimalPrenta(uint8(data >> 8))
	sjálft.MHexadecimalPrenta(uint8(data))
}
func (sjálft *TConsole) MUnsignedinteger64Prentaxy(data uint64, x uint16, y uint16) {
	sjálft.MHexadecimalPrentaxy(uint8(data>>56), x+0, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>48), x+2, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>40), x+4, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>32), x+6, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>24), x+8, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>16), x+10, y)
	sjálft.MHexadecimalPrentaxy(uint8(data>>8), x+12, y)
	sjálft.MHexadecimalPrentaxy(uint8(data), x+14, y)
}
func MPrenta(phyaddr uintptr, data uint8, x uint32, y uint32)

func (sjálft *TConsole) MPrentahexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MPrenta(uintptr(fbphysaddress), buffer[0], x, y)
	MPrenta(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (sjálft *TConsole) MPrentaunsignedinteger16(data uint16, x uint32, y uint32) {
	sjálft.MPrentahexadecimal(uint8(data>>8), x+0*2, y)
	sjálft.MPrentahexadecimal(uint8(data), x+2*2, y)
}

func (sjálft *TConsole) MPrentaunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	sjálft.MPrentahexadecimal(uint8(data>>24), x+0*2, y)
	sjálft.MPrentahexadecimal(uint8(data>>16), x+2*2, y)
	sjálft.MPrentahexadecimal(uint8(data>>8), x+4*2, y)
	sjálft.MPrentahexadecimal(uint8(data), x+6*2, y)
}

func (sjálft *TConsole) M테스트() {
}
