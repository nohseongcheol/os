package console

import . "unsafe"

const (
	fbԼայնություն		= 80
	fbԲարձրություն		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xԴիրք	uint16
	yԴիրք	uint16
}

var serialՊատրաստ bool

func Serialinit()
func SerialԳրելbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialՊատրաստ = true
}

func seriallogbyte(data byte) {
	if !serialՊատրաստ {
		return
	}

	if data == '\n' {
		SerialԳրելbyte('\r')
	}
	SerialԳրելbyte(uint8(data))
}

func MEmergencylogՏՈՂ(data string) {
	for i := 0; i < len(data); i++ {
		seriallogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	seriallogbyte(digits[(data>>4)&0x0F])
	seriallogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (ինքնուրույն *TConsole) MՏպել(argumentԱրժեք ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var արժեք_2 interface{}

	for i, p := range argumentԱրժեք {
		switch i {
		case 0:
			param, _ := p.(interface{})
			արժեք_2 = param
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

	ինքնուրույն.MՏպելxy(արժեք_2, x, y)

}
func (ինքնուրույն *TConsole) MՏպելxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		ինքնուրույն.MՏպելԲայթերxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		ինքնուրույն.MHexadecimalՏպելxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		ինքնուրույն.MUnsignedinteger16Տպելxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		ինքնուրույն.MUnsignedinteger32Տպելxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		ինքնուրույն.MUnsignedinteger64Տպելxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		ինքնուրույն.MՏպելԲայթերxy(data_2, x, y)
	}

}
func (ինքնուրույն *TConsole) MՏպելԲայթերxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		ինքնուրույն.xԴիրք = x
	}
	if y <= 999 {
		ինքնուրույն.yԴիրք = y
	}

	ատրիբուտ := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			ինքնուրույն.yԴիրք++
			ինքնուրույն.xԴիրք = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*ինքնուրույն.yԴիրք+ինքնուրույն.xԴիրք)*2))) = ատրիբուտ<<8 | uint16(buffer[i])
			ինքնուրույն.xԴիրք++
		}

		if ինքնուրույն.xԴիրք >= 80 {
			ինքնուրույն.yԴիրք++
			ինքնուրույն.xԴիրք = 0
		}

		if ինքնուրույն.yԴիրք >= 25 {
			for ինքնուրույն.yԴիրք = 0; ինքնուրույն.yԴիրք < 25; ինքնուրույն.yԴիրք++ {
				for ինքնուրույն.xԴիրք = 0; ինքնուրույն.xԴիրք < 80; ինքնուրույն.xԴիրք++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*ինքնուրույն.yԴիրք+ինքնուրույն.xԴիրք)*2))) = ատրիբուտ<<8 | ' '
				}
			}
			ինքնուրույն.xԴիրք = 0
			ինքնուրույն.yԴիրք = 0
		}

	}

}
func (ինքնուրույն *TConsole) MHexadecimalՏպել(բանալի uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(բանալի>>4)&0xF]
	buffer[1] = hex[բանալի&0xF]
	ինքնուրույն.MՏպել(buffer)
}
func (ինքնուրույն *TConsole) MHexadecimalՏպելxy(բանալի uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(բանալի>>4)&0xF]
	buffer[1] = hex[բանալի&0xF]
	ինքնուրույն.MՏպելxy(buffer, x, y)
}
func (ինքնուրույն *TConsole) MUnsignedinteger16Տպել(բանալի uint16) {
	ինքնուրույն.MHexadecimalՏպել(uint8(բանալի >> 8))
	ինքնուրույն.MHexadecimalՏպել(uint8(բանալի))
}
func (ինքնուրույն *TConsole) MUnsignedinteger16Տպելxy(բանալի uint16, x uint16, y uint16) {
	ինքնուրույն.MHexadecimalՏպելxy(uint8(բանալի>>8), x, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(բանալի), x, y)
}
func (ինքնուրույն *TConsole) MUnsignedinteger32Տպել(data uint32) {
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 24))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 16))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 8))
	ինքնուրույն.MHexadecimalՏպել(uint8(data))
}
func (ինքնուրույն *TConsole) MUnsignedinteger32Տպելxy(data uint32, x uint16, y uint16) {

	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>24), x+0, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>16), x+2, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>8), x+4, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data), x+6, y)
}
func (ինքնուրույն *TConsole) MUnsignedinteger64Տպել(data uint64) {
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 56))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 48))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 40))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 32))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 24))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 16))
	ինքնուրույն.MHexadecimalՏպել(uint8(data >> 8))
	ինքնուրույն.MHexadecimalՏպել(uint8(data))
}
func (ինքնուրույն *TConsole) MUnsignedinteger64Տպելxy(data uint64, x uint16, y uint16) {
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>56), x+0, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>48), x+2, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>40), x+4, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>32), x+6, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>24), x+8, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>16), x+10, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data>>8), x+12, y)
	ինքնուրույն.MHexadecimalՏպելxy(uint8(data), x+14, y)
}
func MՏպել(phyaddr uintptr, data uint8, x uint32, y uint32)

func (ինքնուրույն *TConsole) MՏպելhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MՏպել(uintptr(fbphysaddress), buffer[0], x, y)
	MՏպել(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (ինքնուրույն *TConsole) MՏպելunsignedinteger16(data uint16, x uint32, y uint32) {
	ինքնուրույն.MՏպելhexadecimal(uint8(data>>8), x+0*2, y)
	ինքնուրույն.MՏպելhexadecimal(uint8(data), x+2*2, y)
}

func (ինքնուրույն *TConsole) MՏպելunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	ինքնուրույն.MՏպելhexadecimal(uint8(data>>24), x+0*2, y)
	ինքնուրույն.MՏպելhexadecimal(uint8(data>>16), x+2*2, y)
	ինքնուրույն.MՏպելhexadecimal(uint8(data>>8), x+4*2, y)
	ինքնուրույն.MՏպելhexadecimal(uint8(data), x+6*2, y)
}

func (ինքնուրույն *TConsole) M테스트() {
}
