/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsoli

import . "unsafe"

const (
	fbLeveys		= 80
	fbKorkeus		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonsoli struct {
	xSijainti	uint16
	ySijainti	uint16
}

var sarjaValmis bool

func Sarjainit()
func SarjaKirjoitusbyte(data uint8)

func MSarjaKäytälokiainit() {
	Sarjainit()
	sarjaValmis = true
}

func sarjaKäytälokiabyte(data byte) {
	if !sarjaValmis {
		return
	}

	if data == '\n' {
		SarjaKirjoitusbyte('\r')
	}
	SarjaKirjoitusbyte(uint8(data))
}

func MEmergencyKäytälokiaMerkkijono(data string) {
	for i := 0; i < len(data); i++ {
		sarjaKäytälokiabyte(data[i])
	}
}

func MEmergencyKäytälokiahexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sarjaKäytälokiabyte(digits[(data>>4)&0x0F])
	sarjaKäytälokiabyte(digits[data&0x0F])
}

func MEmergencyKäytälokiaunsignedinteger32(data uint32) {
	MEmergencyKäytälokiahexadecimal8(uint8(data >> 24))
	MEmergencyKäytälokiahexadecimal8(uint8(data >> 16))
	MEmergencyKäytälokiahexadecimal8(uint8(data >> 8))
	MEmergencyKäytälokiahexadecimal8(uint8(data))
}

func (itse *TKonsoli) MTulosta(argumentArvo ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var arvo_2 interface{}

	for i, p := range argumentArvo {
		switch i {
		case 0:
			param, _ := p.(interface{})
			arvo_2 = param
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

	itse.MTulostaxy(arvo_2, x, y)

}
func (itse *TKonsoli) MTulostaxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		itse.MTulostatavuaxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		itse.MHexadecimalTulostaxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		itse.MUnsignedinteger16Tulostaxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		itse.MUnsignedinteger32Tulostaxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		itse.MUnsignedinteger64Tulostaxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		itse.MTulostatavuaxy(data_2, x, y)
	}

}
func (itse *TKonsoli) MTulostatavuaxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		itse.xSijainti = x
	}
	if y <= 999 {
		itse.ySijainti = y
	}

	määre := uint16(0x0F)
	rajoitus := len(buffer)
	if rajoitus > 4096 {
		rajoitus = 4096
	}
	for i := 0; i < rajoitus; i++ {
		sarjaKäytälokiabyte(buffer[i])
		switch buffer[i] {
		case '\n':
			itse.ySijainti++
			itse.xSijainti = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*itse.ySijainti+itse.xSijainti)*2))) = määre<<8 | uint16(buffer[i])
			itse.xSijainti++
		}

		if itse.xSijainti >= 80 {
			itse.ySijainti++
			itse.xSijainti = 0
		}

		if itse.ySijainti >= 25 {
			for itse.ySijainti = 0; itse.ySijainti < 25; itse.ySijainti++ {
				for itse.xSijainti = 0; itse.xSijainti < 80; itse.xSijainti++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*itse.ySijainti+itse.xSijainti)*2))) = määre<<8 | ' '
				}
			}
			itse.xSijainti = 0
			itse.ySijainti = 0
		}

	}

}
func (itse *TKonsoli) MHexadecimalTulosta(avain uint8) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(avain>>4)&0xF]
	buffer[1] = heksa[avain&0xF]
	itse.MTulosta(buffer)
}
func (itse *TKonsoli) MHexadecimalTulostaxy(avain uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(avain>>4)&0xF]
	buffer[1] = heksa[avain&0xF]
	itse.MTulostaxy(buffer, x, y)
}
func (itse *TKonsoli) MUnsignedinteger16Tulosta(avain uint16) {
	itse.MHexadecimalTulosta(uint8(avain >> 8))
	itse.MHexadecimalTulosta(uint8(avain))
}
func (itse *TKonsoli) MUnsignedinteger16Tulostaxy(avain uint16, x uint16, y uint16) {
	itse.MHexadecimalTulostaxy(uint8(avain>>8), x, y)
	itse.MHexadecimalTulostaxy(uint8(avain), x, y)
}
func (itse *TKonsoli) MUnsignedinteger32Tulosta(data uint32) {
	itse.MHexadecimalTulosta(uint8(data >> 24))
	itse.MHexadecimalTulosta(uint8(data >> 16))
	itse.MHexadecimalTulosta(uint8(data >> 8))
	itse.MHexadecimalTulosta(uint8(data))
}
func (itse *TKonsoli) MUnsignedinteger32Tulostaxy(data uint32, x uint16, y uint16) {

	itse.MHexadecimalTulostaxy(uint8(data>>24), x+0, y)
	itse.MHexadecimalTulostaxy(uint8(data>>16), x+2, y)
	itse.MHexadecimalTulostaxy(uint8(data>>8), x+4, y)
	itse.MHexadecimalTulostaxy(uint8(data), x+6, y)
}
func (itse *TKonsoli) MUnsignedinteger64Tulosta(data uint64) {
	itse.MHexadecimalTulosta(uint8(data >> 56))
	itse.MHexadecimalTulosta(uint8(data >> 48))
	itse.MHexadecimalTulosta(uint8(data >> 40))
	itse.MHexadecimalTulosta(uint8(data >> 32))
	itse.MHexadecimalTulosta(uint8(data >> 24))
	itse.MHexadecimalTulosta(uint8(data >> 16))
	itse.MHexadecimalTulosta(uint8(data >> 8))
	itse.MHexadecimalTulosta(uint8(data))
}
func (itse *TKonsoli) MUnsignedinteger64Tulostaxy(data uint64, x uint16, y uint16) {
	itse.MHexadecimalTulostaxy(uint8(data>>56), x+0, y)
	itse.MHexadecimalTulostaxy(uint8(data>>48), x+2, y)
	itse.MHexadecimalTulostaxy(uint8(data>>40), x+4, y)
	itse.MHexadecimalTulostaxy(uint8(data>>32), x+6, y)
	itse.MHexadecimalTulostaxy(uint8(data>>24), x+8, y)
	itse.MHexadecimalTulostaxy(uint8(data>>16), x+10, y)
	itse.MHexadecimalTulostaxy(uint8(data>>8), x+12, y)
	itse.MHexadecimalTulostaxy(uint8(data), x+14, y)
}
func MTulosta(phyaddr uintptr, data uint8, x uint32, y uint32)

func (itse *TKonsoli) MTulostahexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(data>>4)&0xF]
	buffer[1] = heksa[data&0xF]

	MTulosta(uintptr(fbphysaddress), buffer[0], x, y)
	MTulosta(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (itse *TKonsoli) MTulostaunsignedinteger16(data uint16, x uint32, y uint32) {
	itse.MTulostahexadecimal(uint8(data>>8), x+0*2, y)
	itse.MTulostahexadecimal(uint8(data), x+2*2, y)
}

func (itse *TKonsoli) MTulostaunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	itse.MTulostahexadecimal(uint8(data>>24), x+0*2, y)
	itse.MTulostahexadecimal(uint8(data>>16), x+2*2, y)
	itse.MTulostahexadecimal(uint8(data>>8), x+4*2, y)
	itse.MTulostahexadecimal(uint8(data), x+6*2, y)
}

func (itse *TKonsoli) M테스트() {
}
