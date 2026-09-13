package console

import . "unsafe"

const (
	fbŠirina		= 80
	fbVišina		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPoložaj	uint16
	yPoložaj	uint16
}

var zaporednaštevilkaPripravljen bool

func Zaporednaštevilkainit()
func ZaporednaštevilkaPisanjebyte(data uint8)

func MZaporednaštevilkaloginit() {
	Zaporednaštevilkainit()
	zaporednaštevilkaPripravljen = true
}

func zaporednaštevilkalogbyte(data byte) {
	if !zaporednaštevilkaPripravljen {
		return
	}

	if data == '\n' {
		ZaporednaštevilkaPisanjebyte('\r')
	}
	ZaporednaštevilkaPisanjebyte(uint8(data))
}

func MEmergencylogNiz(data string) {
	for i := 0; i < len(data); i++ {
		zaporednaštevilkalogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	zaporednaštevilkalogbyte(digits[(data>>4)&0x0F])
	zaporednaštevilkalogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (sam *TConsole) MNatisni(argumentVrednost ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var vrednost_2 interface{}

	for i, p := range argumentVrednost {
		switch i {
		case 0:
			param, _ := p.(interface{})
			vrednost_2 = param
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

	sam.MNatisnixy(vrednost_2, x, y)

}
func (sam *TConsole) MNatisnixy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		sam.MNatisniBajtovxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		sam.MHexadecimalNatisnixy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		sam.MUnsignedinteger16Natisnixy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		sam.MUnsignedinteger32Natisnixy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		sam.MUnsignedinteger64Natisnixy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		sam.MNatisniBajtovxy(data_2, x, y)
	}

}
func (sam *TConsole) MNatisniBajtovxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		sam.xPoložaj = x
	}
	if y <= 999 {
		sam.yPoložaj = y
	}

	atribut := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		zaporednaštevilkalogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			sam.yPoložaj++
			sam.xPoložaj = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*sam.yPoložaj+sam.xPoložaj)*2))) = atribut<<8 | uint16(buffer[i])
			sam.xPoložaj++
		}

		if sam.xPoložaj >= 80 {
			sam.yPoložaj++
			sam.xPoložaj = 0
		}

		if sam.yPoložaj >= 25 {
			for sam.yPoložaj = 0; sam.yPoložaj < 25; sam.yPoložaj++ {
				for sam.xPoložaj = 0; sam.xPoložaj < 80; sam.xPoložaj++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*sam.yPoložaj+sam.xPoložaj)*2))) = atribut<<8 | ' '
				}
			}
			sam.xPoložaj = 0
			sam.yPoložaj = 0
		}

	}

}
func (sam *TConsole) MHexadecimalNatisni(ključ uint8) {
	buffer := []byte{'0', '0'}
	šestnajstiško := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnajstiško[(ključ>>4)&0xF]
	buffer[1] = šestnajstiško[ključ&0xF]
	sam.MNatisni(buffer)
}
func (sam *TConsole) MHexadecimalNatisnixy(ključ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	šestnajstiško := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnajstiško[(ključ>>4)&0xF]
	buffer[1] = šestnajstiško[ključ&0xF]
	sam.MNatisnixy(buffer, x, y)
}
func (sam *TConsole) MUnsignedinteger16Natisni(ključ uint16) {
	sam.MHexadecimalNatisni(uint8(ključ >> 8))
	sam.MHexadecimalNatisni(uint8(ključ))
}
func (sam *TConsole) MUnsignedinteger16Natisnixy(ključ uint16, x uint16, y uint16) {
	sam.MHexadecimalNatisnixy(uint8(ključ>>8), x, y)
	sam.MHexadecimalNatisnixy(uint8(ključ), x, y)
}
func (sam *TConsole) MUnsignedinteger32Natisni(data uint32) {
	sam.MHexadecimalNatisni(uint8(data >> 24))
	sam.MHexadecimalNatisni(uint8(data >> 16))
	sam.MHexadecimalNatisni(uint8(data >> 8))
	sam.MHexadecimalNatisni(uint8(data))
}
func (sam *TConsole) MUnsignedinteger32Natisnixy(data uint32, x uint16, y uint16) {

	sam.MHexadecimalNatisnixy(uint8(data>>24), x+0, y)
	sam.MHexadecimalNatisnixy(uint8(data>>16), x+2, y)
	sam.MHexadecimalNatisnixy(uint8(data>>8), x+4, y)
	sam.MHexadecimalNatisnixy(uint8(data), x+6, y)
}
func (sam *TConsole) MUnsignedinteger64Natisni(data uint64) {
	sam.MHexadecimalNatisni(uint8(data >> 56))
	sam.MHexadecimalNatisni(uint8(data >> 48))
	sam.MHexadecimalNatisni(uint8(data >> 40))
	sam.MHexadecimalNatisni(uint8(data >> 32))
	sam.MHexadecimalNatisni(uint8(data >> 24))
	sam.MHexadecimalNatisni(uint8(data >> 16))
	sam.MHexadecimalNatisni(uint8(data >> 8))
	sam.MHexadecimalNatisni(uint8(data))
}
func (sam *TConsole) MUnsignedinteger64Natisnixy(data uint64, x uint16, y uint16) {
	sam.MHexadecimalNatisnixy(uint8(data>>56), x+0, y)
	sam.MHexadecimalNatisnixy(uint8(data>>48), x+2, y)
	sam.MHexadecimalNatisnixy(uint8(data>>40), x+4, y)
	sam.MHexadecimalNatisnixy(uint8(data>>32), x+6, y)
	sam.MHexadecimalNatisnixy(uint8(data>>24), x+8, y)
	sam.MHexadecimalNatisnixy(uint8(data>>16), x+10, y)
	sam.MHexadecimalNatisnixy(uint8(data>>8), x+12, y)
	sam.MHexadecimalNatisnixy(uint8(data), x+14, y)
}
func MNatisni(phyaddr uintptr, data uint8, x uint32, y uint32)

func (sam *TConsole) MNatisnihexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	šestnajstiško := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnajstiško[(data>>4)&0xF]
	buffer[1] = šestnajstiško[data&0xF]

	MNatisni(uintptr(fbphysaddress), buffer[0], x, y)
	MNatisni(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (sam *TConsole) MNatisniunsignedinteger16(data uint16, x uint32, y uint32) {
	sam.MNatisnihexadecimal(uint8(data>>8), x+0*2, y)
	sam.MNatisnihexadecimal(uint8(data), x+2*2, y)
}

func (sam *TConsole) MNatisniunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	sam.MNatisnihexadecimal(uint8(data>>24), x+0*2, y)
	sam.MNatisnihexadecimal(uint8(data>>16), x+2*2, y)
	sam.MNatisnihexadecimal(uint8(data>>8), x+4*2, y)
	sam.MNatisnihexadecimal(uint8(data), x+6*2, y)
}

func (sam *TConsole) M테스트() {
}
