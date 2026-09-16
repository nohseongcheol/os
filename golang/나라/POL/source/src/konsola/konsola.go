/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsola

import . "unsafe"

const (
	fbSzerokość		= 80
	fbWysokość		= 25
	fbphysAdres	uintptr	= 0xb8000
)

type TKonsola struct {
	xPozycja	uint16
	yPozycja	uint16
}

var szeregowoGotowy bool

func Szeregowoinit()
func SzeregowoZapisbyte(data uint8)

func MSzeregowoDziennikinit() {
	Szeregowoinit()
	szeregowoGotowy = true
}

func szeregowoDziennikbyte(data byte) {
	if !szeregowoGotowy {
		return
	}

	if data == '\n' {
		SzeregowoZapisbyte('\r')
	}
	SzeregowoZapisbyte(uint8(data))
}

func MEmergencyDziennikCIĄG(data string) {
	for i := 0; i < len(data); i++ {
		szeregowoDziennikbyte(data[i])
	}
}

func MEmergencyDziennikhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	szeregowoDziennikbyte(digits[(data>>4)&0x0F])
	szeregowoDziennikbyte(digits[data&0x0F])
}

func MEmergencyDziennikunsignedinteger32(data uint32) {
	MEmergencyDziennikhexadecimal8(uint8(data >> 24))
	MEmergencyDziennikhexadecimal8(uint8(data >> 16))
	MEmergencyDziennikhexadecimal8(uint8(data >> 8))
	MEmergencyDziennikhexadecimal8(uint8(data))
}

func (bieżący *TKonsola) MWydrukuj(argumentWartość ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var wartość_2 interface{}

	for i, p := range argumentWartość {
		switch i {
		case 0:
			param, _ := p.(interface{})
			wartość_2 = param
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

	bieżący.MWydrukujxy(wartość_2, x, y)

}
func (bieżący *TKonsola) MWydrukujxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		bieżący.MWydrukujBajtyxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		bieżący.MHexadecimalWydrukujxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		bieżący.MUnsignedinteger16Wydrukujxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		bieżący.MUnsignedinteger32Wydrukujxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		bieżący.MUnsignedinteger64Wydrukujxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		bieżący.MWydrukujBajtyxy(data_2, x, y)
	}

}
func (bieżący *TKonsola) MWydrukujBajtyxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		bieżący.xPozycja = x
	}
	if y <= 999 {
		bieżący.yPozycja = y
	}

	atrybut := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		szeregowoDziennikbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			bieżący.yPozycja++
			bieżący.xPozycja = 0
		default:
			*(*uint16)(Pointer(fbphysAdres + uintptr((80*bieżący.yPozycja+bieżący.xPozycja)*2))) = atrybut<<8 | uint16(buffer[i])
			bieżący.xPozycja++
		}

		if bieżący.xPozycja >= 80 {
			bieżący.yPozycja++
			bieżący.xPozycja = 0
		}

		if bieżący.yPozycja >= 25 {
			for bieżący.yPozycja = 0; bieżący.yPozycja < 25; bieżący.yPozycja++ {
				for bieżący.xPozycja = 0; bieżący.xPozycja < 80; bieżący.xPozycja++ {
					*(*uint16)(Pointer(fbphysAdres + uintptr((80*bieżący.yPozycja+bieżący.xPozycja)*2))) = atrybut<<8 | ' '
				}
			}
			bieżący.xPozycja = 0
			bieżący.yPozycja = 0
		}

	}

}
func (bieżący *TKonsola) MHexadecimalWydrukuj(klucz uint8) {
	buffer := []byte{'0', '0'}
	szesnastkowo := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = szesnastkowo[(klucz>>4)&0xF]
	buffer[1] = szesnastkowo[klucz&0xF]
	bieżący.MWydrukuj(buffer)
}
func (bieżący *TKonsola) MHexadecimalWydrukujxy(klucz uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	szesnastkowo := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = szesnastkowo[(klucz>>4)&0xF]
	buffer[1] = szesnastkowo[klucz&0xF]
	bieżący.MWydrukujxy(buffer, x, y)
}
func (bieżący *TKonsola) MUnsignedinteger16Wydrukuj(klucz uint16) {
	bieżący.MHexadecimalWydrukuj(uint8(klucz >> 8))
	bieżący.MHexadecimalWydrukuj(uint8(klucz))
}
func (bieżący *TKonsola) MUnsignedinteger16Wydrukujxy(klucz uint16, x uint16, y uint16) {
	bieżący.MHexadecimalWydrukujxy(uint8(klucz>>8), x, y)
	bieżący.MHexadecimalWydrukujxy(uint8(klucz), x, y)
}
func (bieżący *TKonsola) MUnsignedinteger32Wydrukuj(data uint32) {
	bieżący.MHexadecimalWydrukuj(uint8(data >> 24))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 16))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 8))
	bieżący.MHexadecimalWydrukuj(uint8(data))
}
func (bieżący *TKonsola) MUnsignedinteger32Wydrukujxy(data uint32, x uint16, y uint16) {

	bieżący.MHexadecimalWydrukujxy(uint8(data>>24), x+0, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>16), x+2, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>8), x+4, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data), x+6, y)
}
func (bieżący *TKonsola) MUnsignedinteger64Wydrukuj(data uint64) {
	bieżący.MHexadecimalWydrukuj(uint8(data >> 56))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 48))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 40))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 32))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 24))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 16))
	bieżący.MHexadecimalWydrukuj(uint8(data >> 8))
	bieżący.MHexadecimalWydrukuj(uint8(data))
}
func (bieżący *TKonsola) MUnsignedinteger64Wydrukujxy(data uint64, x uint16, y uint16) {
	bieżący.MHexadecimalWydrukujxy(uint8(data>>56), x+0, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>48), x+2, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>40), x+4, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>32), x+6, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>24), x+8, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>16), x+10, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data>>8), x+12, y)
	bieżący.MHexadecimalWydrukujxy(uint8(data), x+14, y)
}
func MWydrukuj(phyaddr uintptr, data uint8, x uint32, y uint32)

func (bieżący *TKonsola) MWydrukujhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	szesnastkowo := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = szesnastkowo[(data>>4)&0xF]
	buffer[1] = szesnastkowo[data&0xF]

	MWydrukuj(uintptr(fbphysAdres), buffer[0], x, y)
	MWydrukuj(uintptr(fbphysAdres), buffer[1], x+2, y)
}

func (bieżący *TKonsola) MWydrukujunsignedinteger16(data uint16, x uint32, y uint32) {
	bieżący.MWydrukujhexadecimal(uint8(data>>8), x+0*2, y)
	bieżący.MWydrukujhexadecimal(uint8(data), x+2*2, y)
}

func (bieżący *TKonsola) MWydrukujunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	bieżący.MWydrukujhexadecimal(uint8(data>>24), x+0*2, y)
	bieżący.MWydrukujhexadecimal(uint8(data>>16), x+2*2, y)
	bieżący.MWydrukujhexadecimal(uint8(data>>8), x+4*2, y)
	bieżący.MWydrukujhexadecimal(uint8(data), x+6*2, y)
}

func (bieżący *TKonsola) M테스트() {
}
