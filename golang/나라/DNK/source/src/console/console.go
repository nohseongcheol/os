package console

import . "unsafe"

const (
	fbBredde		= 80
	fbHøjde			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPlacering	uint16
	yPlacering	uint16
}

var serielKlar bool

func Serielinit()
func SerielSkrivebyte(data uint8)

func MSerielloginit() {
	Serielinit()
	serielKlar = true
}

func seriellogbyte(data byte) {
	if !serielKlar {
		return
	}

	if data == '\n' {
		SerielSkrivebyte('\r')
	}
	SerielSkrivebyte(uint8(data))
}

func MEmergencylogStreng(data string) {
	for i := 0; i < len(data); i++ {
		seriellogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	seriellogbyte(digits[(data>>4)&0x0F])
	seriellogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (selv *TConsole) MUdskriv(argumentVærdi ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var værdi_2 interface{}

	for i, p := range argumentVærdi {
		switch i {
		case 0:
			param, _ := p.(interface{})
			værdi_2 = param
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

	selv.MUdskrivxy(værdi_2, x, y)

}
func (selv *TConsole) MUdskrivxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		selv.MUdskrivBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		selv.MHexadecimalUdskrivxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		selv.MUnsignedinteger16Udskrivxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		selv.MUnsignedinteger32Udskrivxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		selv.MUnsignedinteger64Udskrivxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		selv.MUdskrivBytexy(data_2, x, y)
	}

}
func (selv *TConsole) MUdskrivBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		selv.xPlacering = x
	}
	if y <= 999 {
		selv.yPlacering = y
	}

	egenskab := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriellogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			selv.yPlacering++
			selv.xPlacering = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*selv.yPlacering+selv.xPlacering)*2))) = egenskab<<8 | uint16(buffer[i])
			selv.xPlacering++
		}

		if selv.xPlacering >= 80 {
			selv.yPlacering++
			selv.xPlacering = 0
		}

		if selv.yPlacering >= 25 {
			for selv.yPlacering = 0; selv.yPlacering < 25; selv.yPlacering++ {
				for selv.xPlacering = 0; selv.xPlacering < 80; selv.xPlacering++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*selv.yPlacering+selv.xPlacering)*2))) = egenskab<<8 | ' '
				}
			}
			selv.xPlacering = 0
			selv.yPlacering = 0
		}

	}

}
func (selv *TConsole) MHexadecimalUdskriv(nøgle uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(nøgle>>4)&0xF]
	buffer[1] = hex[nøgle&0xF]
	selv.MUdskriv(buffer)
}
func (selv *TConsole) MHexadecimalUdskrivxy(nøgle uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(nøgle>>4)&0xF]
	buffer[1] = hex[nøgle&0xF]
	selv.MUdskrivxy(buffer, x, y)
}
func (selv *TConsole) MUnsignedinteger16Udskriv(nøgle uint16) {
	selv.MHexadecimalUdskriv(uint8(nøgle >> 8))
	selv.MHexadecimalUdskriv(uint8(nøgle))
}
func (selv *TConsole) MUnsignedinteger16Udskrivxy(nøgle uint16, x uint16, y uint16) {
	selv.MHexadecimalUdskrivxy(uint8(nøgle>>8), x, y)
	selv.MHexadecimalUdskrivxy(uint8(nøgle), x, y)
}
func (selv *TConsole) MUnsignedinteger32Udskriv(data uint32) {
	selv.MHexadecimalUdskriv(uint8(data >> 24))
	selv.MHexadecimalUdskriv(uint8(data >> 16))
	selv.MHexadecimalUdskriv(uint8(data >> 8))
	selv.MHexadecimalUdskriv(uint8(data))
}
func (selv *TConsole) MUnsignedinteger32Udskrivxy(data uint32, x uint16, y uint16) {

	selv.MHexadecimalUdskrivxy(uint8(data>>24), x+0, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>16), x+2, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>8), x+4, y)
	selv.MHexadecimalUdskrivxy(uint8(data), x+6, y)
}
func (selv *TConsole) MUnsignedinteger64Udskriv(data uint64) {
	selv.MHexadecimalUdskriv(uint8(data >> 56))
	selv.MHexadecimalUdskriv(uint8(data >> 48))
	selv.MHexadecimalUdskriv(uint8(data >> 40))
	selv.MHexadecimalUdskriv(uint8(data >> 32))
	selv.MHexadecimalUdskriv(uint8(data >> 24))
	selv.MHexadecimalUdskriv(uint8(data >> 16))
	selv.MHexadecimalUdskriv(uint8(data >> 8))
	selv.MHexadecimalUdskriv(uint8(data))
}
func (selv *TConsole) MUnsignedinteger64Udskrivxy(data uint64, x uint16, y uint16) {
	selv.MHexadecimalUdskrivxy(uint8(data>>56), x+0, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>48), x+2, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>40), x+4, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>32), x+6, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>24), x+8, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>16), x+10, y)
	selv.MHexadecimalUdskrivxy(uint8(data>>8), x+12, y)
	selv.MHexadecimalUdskrivxy(uint8(data), x+14, y)
}
func MUdskriv(phyaddr uintptr, data uint8, x uint32, y uint32)

func (selv *TConsole) MUdskrivhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MUdskriv(uintptr(fbphysaddress), buffer[0], x, y)
	MUdskriv(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (selv *TConsole) MUdskrivunsignedinteger16(data uint16, x uint32, y uint32) {
	selv.MUdskrivhexadecimal(uint8(data>>8), x+0*2, y)
	selv.MUdskrivhexadecimal(uint8(data), x+2*2, y)
}

func (selv *TConsole) MUdskrivunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	selv.MUdskrivhexadecimal(uint8(data>>24), x+0*2, y)
	selv.MUdskrivhexadecimal(uint8(data>>16), x+2*2, y)
	selv.MUdskrivhexadecimal(uint8(data>>8), x+4*2, y)
	selv.MUdskrivhexadecimal(uint8(data), x+6*2, y)
}

func (selv *TConsole) M테스트() {
}
