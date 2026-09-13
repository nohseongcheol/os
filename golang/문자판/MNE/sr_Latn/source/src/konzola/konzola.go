package konzola

import . "unsafe"

const (
	fbŠirina		= 80
	fbVisina		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonzola struct {
	xPoložaj	uint16
	yPoložaj	uint16
}

var serijskiSpreman bool

func Serijskiinit()
func SerijskiPišebyte(data uint8)

func MSerijskiDnevnikinit() {
	Serijskiinit()
	serijskiSpreman = true
}

func serijskiDnevnikbyte(data byte) {
	if !serijskiSpreman {
		return
	}

	if data == '\n' {
		SerijskiPišebyte('\r')
	}
	SerijskiPišebyte(uint8(data))
}

func MEmergencyDnevnikniska(data string) {
	for i := 0; i < len(data); i++ {
		serijskiDnevnikbyte(data[i])
	}
}

func MEmergencyDnevnikhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serijskiDnevnikbyte(digits[(data>>4)&0x0F])
	serijskiDnevnikbyte(digits[data&0x0F])
}

func MEmergencyDnevnikunsignedinteger32(data uint32) {
	MEmergencyDnevnikhexadecimal8(uint8(data >> 24))
	MEmergencyDnevnikhexadecimal8(uint8(data >> 16))
	MEmergencyDnevnikhexadecimal8(uint8(data >> 8))
	MEmergencyDnevnikhexadecimal8(uint8(data))
}

func (isti *TKonzola) MŠtampaj(argumentVrednost ...interface{}) {
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

	isti.MŠtampajxy(vrednost_2, x, y)

}
func (isti *TKonzola) MŠtampajxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		isti.MŠtampajBajtovaxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		isti.MHexadecimalŠtampajxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		isti.MUnsignedinteger16Štampajxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		isti.MUnsignedinteger32Štampajxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		isti.MUnsignedinteger64Štampajxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		isti.MŠtampajBajtovaxy(data_2, x, y)
	}

}
func (isti *TKonzola) MŠtampajBajtovaxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		isti.xPoložaj = x
	}
	if y <= 999 {
		isti.yPoložaj = y
	}

	atribut := uint16(0x0F)
	ograniči := len(buffer)
	if ograniči > 4096 {
		ograniči = 4096
	}
	for i := 0; i < ograniči; i++ {
		serijskiDnevnikbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			isti.yPoložaj++
			isti.xPoložaj = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*isti.yPoložaj+isti.xPoložaj)*2))) = atribut<<8 | uint16(buffer[i])
			isti.xPoložaj++
		}

		if isti.xPoložaj >= 80 {
			isti.yPoložaj++
			isti.xPoložaj = 0
		}

		if isti.yPoložaj >= 25 {
			for isti.yPoložaj = 0; isti.yPoložaj < 25; isti.yPoložaj++ {
				for isti.xPoložaj = 0; isti.xPoložaj < 80; isti.xPoložaj++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*isti.yPoložaj+isti.xPoložaj)*2))) = atribut<<8 | ' '
				}
			}
			isti.xPoložaj = 0
			isti.yPoložaj = 0
		}

	}

}
func (isti *TKonzola) MHexadecimalŠtampaj(ključ uint8) {
	buffer := []byte{'0', '0'}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(ključ>>4)&0xF]
	buffer[1] = heksadecimalno[ključ&0xF]
	isti.MŠtampaj(buffer)
}
func (isti *TKonzola) MHexadecimalŠtampajxy(ključ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(ključ>>4)&0xF]
	buffer[1] = heksadecimalno[ključ&0xF]
	isti.MŠtampajxy(buffer, x, y)
}
func (isti *TKonzola) MUnsignedinteger16Štampaj(ključ uint16) {
	isti.MHexadecimalŠtampaj(uint8(ključ >> 8))
	isti.MHexadecimalŠtampaj(uint8(ključ))
}
func (isti *TKonzola) MUnsignedinteger16Štampajxy(ključ uint16, x uint16, y uint16) {
	isti.MHexadecimalŠtampajxy(uint8(ključ>>8), x, y)
	isti.MHexadecimalŠtampajxy(uint8(ključ), x, y)
}
func (isti *TKonzola) MUnsignedinteger32Štampaj(data uint32) {
	isti.MHexadecimalŠtampaj(uint8(data >> 24))
	isti.MHexadecimalŠtampaj(uint8(data >> 16))
	isti.MHexadecimalŠtampaj(uint8(data >> 8))
	isti.MHexadecimalŠtampaj(uint8(data))
}
func (isti *TKonzola) MUnsignedinteger32Štampajxy(data uint32, x uint16, y uint16) {

	isti.MHexadecimalŠtampajxy(uint8(data>>24), x+0, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>16), x+2, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>8), x+4, y)
	isti.MHexadecimalŠtampajxy(uint8(data), x+6, y)
}
func (isti *TKonzola) MUnsignedinteger64Štampaj(data uint64) {
	isti.MHexadecimalŠtampaj(uint8(data >> 56))
	isti.MHexadecimalŠtampaj(uint8(data >> 48))
	isti.MHexadecimalŠtampaj(uint8(data >> 40))
	isti.MHexadecimalŠtampaj(uint8(data >> 32))
	isti.MHexadecimalŠtampaj(uint8(data >> 24))
	isti.MHexadecimalŠtampaj(uint8(data >> 16))
	isti.MHexadecimalŠtampaj(uint8(data >> 8))
	isti.MHexadecimalŠtampaj(uint8(data))
}
func (isti *TKonzola) MUnsignedinteger64Štampajxy(data uint64, x uint16, y uint16) {
	isti.MHexadecimalŠtampajxy(uint8(data>>56), x+0, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>48), x+2, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>40), x+4, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>32), x+6, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>24), x+8, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>16), x+10, y)
	isti.MHexadecimalŠtampajxy(uint8(data>>8), x+12, y)
	isti.MHexadecimalŠtampajxy(uint8(data), x+14, y)
}
func MŠtampaj(phyaddr uintptr, data uint8, x uint32, y uint32)

func (isti *TKonzola) MŠtampajhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksadecimalno[(data>>4)&0xF]
	buffer[1] = heksadecimalno[data&0xF]

	MŠtampaj(uintptr(fbphysaddress), buffer[0], x, y)
	MŠtampaj(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (isti *TKonzola) MŠtampajunsignedinteger16(data uint16, x uint32, y uint32) {
	isti.MŠtampajhexadecimal(uint8(data>>8), x+0*2, y)
	isti.MŠtampajhexadecimal(uint8(data), x+2*2, y)
}

func (isti *TKonzola) MŠtampajunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	isti.MŠtampajhexadecimal(uint8(data>>24), x+0*2, y)
	isti.MŠtampajhexadecimal(uint8(data>>16), x+2*2, y)
	isti.MŠtampajhexadecimal(uint8(data>>8), x+4*2, y)
	isti.MŠtampajhexadecimal(uint8(data), x+6*2, y)
}

func (isti *TKonzola) M테스트() {
}
