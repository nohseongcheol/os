package console

import . "unsafe"

const (
	fbعرض			= 80
	fbارتفاع		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xposition	uint16
	yposition	uint16
}

var serialآماده bool

func Serialinit()
func Serialنوشتنbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialآماده = true
}

func seriallogbyte(data byte) {
	if !serialآماده {
		return
	}

	if data == '\n' {
		Serialنوشتنbyte('\r')
	}
	Serialنوشتنbyte(uint8(data))
}

func MEmergencylogرشته(data string) {
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

func (خود *TConsole) Mچاپ(argumentمقدار ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var مقدار_2 interface{}

	for i, p := range argumentمقدار {
		switch i {
		case 0:
			param, _ := p.(interface{})
			مقدار_2 = param
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

	خود.Mچاپxy(مقدار_2, x, y)

}
func (خود *TConsole) Mچاپxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		خود.Mچاپبایتxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		خود.MHexadecimalچاپxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		خود.MUnsignedinteger16چاپxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		خود.MUnsignedinteger32چاپxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		خود.MUnsignedinteger64چاپxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		خود.Mچاپبایتxy(data_2, x, y)
	}

}
func (خود *TConsole) Mچاپبایتxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		خود.xposition = x
	}
	if y <= 999 {
		خود.yposition = y
	}

	مشخصه := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			خود.yposition++
			خود.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*خود.yposition+خود.xposition)*2))) = مشخصه<<8 | uint16(buffer[i])
			خود.xposition++
		}

		if خود.xposition >= 80 {
			خود.yposition++
			خود.xposition = 0
		}

		if خود.yposition >= 25 {
			for خود.yposition = 0; خود.yposition < 25; خود.yposition++ {
				for خود.xposition = 0; خود.xposition < 80; خود.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*خود.yposition+خود.xposition)*2))) = مشخصه<<8 | ' '
				}
			}
			خود.xposition = 0
			خود.yposition = 0
		}

	}

}
func (خود *TConsole) MHexadecimalچاپ(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	خود.Mچاپ(buffer)
}
func (خود *TConsole) MHexadecimalچاپxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	خود.Mچاپxy(buffer, x, y)
}
func (خود *TConsole) MUnsignedinteger16چاپ(key uint16) {
	خود.MHexadecimalچاپ(uint8(key >> 8))
	خود.MHexadecimalچاپ(uint8(key))
}
func (خود *TConsole) MUnsignedinteger16چاپxy(key uint16, x uint16, y uint16) {
	خود.MHexadecimalچاپxy(uint8(key>>8), x, y)
	خود.MHexadecimalچاپxy(uint8(key), x, y)
}
func (خود *TConsole) MUnsignedinteger32چاپ(data uint32) {
	خود.MHexadecimalچاپ(uint8(data >> 24))
	خود.MHexadecimalچاپ(uint8(data >> 16))
	خود.MHexadecimalچاپ(uint8(data >> 8))
	خود.MHexadecimalچاپ(uint8(data))
}
func (خود *TConsole) MUnsignedinteger32چاپxy(data uint32, x uint16, y uint16) {

	خود.MHexadecimalچاپxy(uint8(data>>24), x+0, y)
	خود.MHexadecimalچاپxy(uint8(data>>16), x+2, y)
	خود.MHexadecimalچاپxy(uint8(data>>8), x+4, y)
	خود.MHexadecimalچاپxy(uint8(data), x+6, y)
}
func (خود *TConsole) MUnsignedinteger64چاپ(data uint64) {
	خود.MHexadecimalچاپ(uint8(data >> 56))
	خود.MHexadecimalچاپ(uint8(data >> 48))
	خود.MHexadecimalچاپ(uint8(data >> 40))
	خود.MHexadecimalچاپ(uint8(data >> 32))
	خود.MHexadecimalچاپ(uint8(data >> 24))
	خود.MHexadecimalچاپ(uint8(data >> 16))
	خود.MHexadecimalچاپ(uint8(data >> 8))
	خود.MHexadecimalچاپ(uint8(data))
}
func (خود *TConsole) MUnsignedinteger64چاپxy(data uint64, x uint16, y uint16) {
	خود.MHexadecimalچاپxy(uint8(data>>56), x+0, y)
	خود.MHexadecimalچاپxy(uint8(data>>48), x+2, y)
	خود.MHexadecimalچاپxy(uint8(data>>40), x+4, y)
	خود.MHexadecimalچاپxy(uint8(data>>32), x+6, y)
	خود.MHexadecimalچاپxy(uint8(data>>24), x+8, y)
	خود.MHexadecimalچاپxy(uint8(data>>16), x+10, y)
	خود.MHexadecimalچاپxy(uint8(data>>8), x+12, y)
	خود.MHexadecimalچاپxy(uint8(data), x+14, y)
}
func Mچاپ(phyaddr uintptr, data uint8, x uint32, y uint32)

func (خود *TConsole) Mچاپhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	Mچاپ(uintptr(fbphysaddress), buffer[0], x, y)
	Mچاپ(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (خود *TConsole) Mچاپunsignedinteger16(data uint16, x uint32, y uint32) {
	خود.Mچاپhexadecimal(uint8(data>>8), x+0*2, y)
	خود.Mچاپhexadecimal(uint8(data), x+2*2, y)
}

func (خود *TConsole) Mچاپunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	خود.Mچاپhexadecimal(uint8(data>>24), x+0*2, y)
	خود.Mچاپhexadecimal(uint8(data>>16), x+2*2, y)
	خود.Mچاپhexadecimal(uint8(data>>8), x+4*2, y)
	خود.Mچاپhexadecimal(uint8(data), x+6*2, y)
}

func (خود *TConsole) M테스트() {
}
