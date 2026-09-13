package console

import . "unsafe"

const (
	fbŠirina		= 80
	fbVisina		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPozicija	uint16
	yPozicija	uint16
}

var serijskiSpreman bool

func Serijskiinit()
func SerijskiZapišibyte(data uint8)

func MSerijskiZapisujinit() {
	Serijskiinit()
	serijskiSpreman = true
}

func serijskiZapisujbyte(data byte) {
	if !serijskiSpreman {
		return
	}

	if data == '\n' {
		SerijskiZapišibyte('\r')
	}
	SerijskiZapišibyte(uint8(data))
}

func MEmergencyZapisujZnakovniniz(data string) {
	for i := 0; i < len(data); i++ {
		serijskiZapisujbyte(data[i])
	}
}

func MEmergencyZapisujhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serijskiZapisujbyte(digits[(data>>4)&0x0F])
	serijskiZapisujbyte(digits[data&0x0F])
}

func MEmergencyZapisujunsignedinteger32(data uint32) {
	MEmergencyZapisujhexadecimal8(uint8(data >> 24))
	MEmergencyZapisujhexadecimal8(uint8(data >> 16))
	MEmergencyZapisujhexadecimal8(uint8(data >> 8))
	MEmergencyZapisujhexadecimal8(uint8(data))
}

func (sam *TConsole) MIspis(argumentVrijednost ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var vrijednost_2 interface{}

	for i, p := range argumentVrijednost {
		switch i {
		case 0:
			param, _ := p.(interface{})
			vrijednost_2 = param
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

	sam.MIspisxy(vrijednost_2, x, y)

}
func (sam *TConsole) MIspisxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		sam.MIspisBajtovaxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		sam.MHexadecimalIspisxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		sam.MUnsignedinteger16Ispisxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		sam.MUnsignedinteger32Ispisxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		sam.MUnsignedinteger64Ispisxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		sam.MIspisBajtovaxy(data_2, x, y)
	}

}
func (sam *TConsole) MIspisBajtovaxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		sam.xPozicija = x
	}
	if y <= 999 {
		sam.yPozicija = y
	}

	atribut := uint16(0x0F)
	ograničenje := len(buffer)
	if ograničenje > 4096 {
		ograničenje = 4096
	}
	for i := 0; i < ograničenje; i++ {
		serijskiZapisujbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			sam.yPozicija++
			sam.xPozicija = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*sam.yPozicija+sam.xPozicija)*2))) = atribut<<8 | uint16(buffer[i])
			sam.xPozicija++
		}

		if sam.xPozicija >= 80 {
			sam.yPozicija++
			sam.xPozicija = 0
		}

		if sam.yPozicija >= 25 {
			for sam.yPozicija = 0; sam.yPozicija < 25; sam.yPozicija++ {
				for sam.xPozicija = 0; sam.xPozicija < 80; sam.xPozicija++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*sam.yPozicija+sam.xPozicija)*2))) = atribut<<8 | ' '
				}
			}
			sam.xPozicija = 0
			sam.yPozicija = 0
		}

	}

}
func (sam *TConsole) MHexadecimalIspis(ključ uint8) {
	buffer := []byte{'0', '0'}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(ključ>>4)&0xF]
	buffer[1] = heks[ključ&0xF]
	sam.MIspis(buffer)
}
func (sam *TConsole) MHexadecimalIspisxy(ključ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(ključ>>4)&0xF]
	buffer[1] = heks[ključ&0xF]
	sam.MIspisxy(buffer, x, y)
}
func (sam *TConsole) MUnsignedinteger16Ispis(ključ uint16) {
	sam.MHexadecimalIspis(uint8(ključ >> 8))
	sam.MHexadecimalIspis(uint8(ključ))
}
func (sam *TConsole) MUnsignedinteger16Ispisxy(ključ uint16, x uint16, y uint16) {
	sam.MHexadecimalIspisxy(uint8(ključ>>8), x, y)
	sam.MHexadecimalIspisxy(uint8(ključ), x, y)
}
func (sam *TConsole) MUnsignedinteger32Ispis(data uint32) {
	sam.MHexadecimalIspis(uint8(data >> 24))
	sam.MHexadecimalIspis(uint8(data >> 16))
	sam.MHexadecimalIspis(uint8(data >> 8))
	sam.MHexadecimalIspis(uint8(data))
}
func (sam *TConsole) MUnsignedinteger32Ispisxy(data uint32, x uint16, y uint16) {

	sam.MHexadecimalIspisxy(uint8(data>>24), x+0, y)
	sam.MHexadecimalIspisxy(uint8(data>>16), x+2, y)
	sam.MHexadecimalIspisxy(uint8(data>>8), x+4, y)
	sam.MHexadecimalIspisxy(uint8(data), x+6, y)
}
func (sam *TConsole) MUnsignedinteger64Ispis(data uint64) {
	sam.MHexadecimalIspis(uint8(data >> 56))
	sam.MHexadecimalIspis(uint8(data >> 48))
	sam.MHexadecimalIspis(uint8(data >> 40))
	sam.MHexadecimalIspis(uint8(data >> 32))
	sam.MHexadecimalIspis(uint8(data >> 24))
	sam.MHexadecimalIspis(uint8(data >> 16))
	sam.MHexadecimalIspis(uint8(data >> 8))
	sam.MHexadecimalIspis(uint8(data))
}
func (sam *TConsole) MUnsignedinteger64Ispisxy(data uint64, x uint16, y uint16) {
	sam.MHexadecimalIspisxy(uint8(data>>56), x+0, y)
	sam.MHexadecimalIspisxy(uint8(data>>48), x+2, y)
	sam.MHexadecimalIspisxy(uint8(data>>40), x+4, y)
	sam.MHexadecimalIspisxy(uint8(data>>32), x+6, y)
	sam.MHexadecimalIspisxy(uint8(data>>24), x+8, y)
	sam.MHexadecimalIspisxy(uint8(data>>16), x+10, y)
	sam.MHexadecimalIspisxy(uint8(data>>8), x+12, y)
	sam.MHexadecimalIspisxy(uint8(data), x+14, y)
}
func MIspis(phyaddr uintptr, data uint8, x uint32, y uint32)

func (sam *TConsole) MIspishexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(data>>4)&0xF]
	buffer[1] = heks[data&0xF]

	MIspis(uintptr(fbphysaddress), buffer[0], x, y)
	MIspis(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (sam *TConsole) MIspisunsignedinteger16(data uint16, x uint32, y uint32) {
	sam.MIspishexadecimal(uint8(data>>8), x+0*2, y)
	sam.MIspishexadecimal(uint8(data), x+2*2, y)
}

func (sam *TConsole) MIspisunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	sam.MIspishexadecimal(uint8(data>>24), x+0*2, y)
	sam.MIspishexadecimal(uint8(data>>16), x+2*2, y)
	sam.MIspishexadecimal(uint8(data>>8), x+4*2, y)
	sam.MIspishexadecimal(uint8(data), x+6*2, y)
}

func (sam *TConsole) M테스트() {
}
