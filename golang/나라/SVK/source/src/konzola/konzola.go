/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konzola

import . "unsafe"

const (
	fbŠírka			= 80
	fbVýška			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonzola struct {
	xPozícia	uint16
	yPozícia	uint16
}

var sériovéPripravený bool

func Sériovéinit()
func SériovéZápisbyte(data uint8)

func MSériovéZaznamenávanieinit() {
	Sériovéinit()
	sériovéPripravený = true
}

func sériovéZaznamenávaniebyte(data byte) {
	if !sériovéPripravený {
		return
	}

	if data == '\n' {
		SériovéZápisbyte('\r')
	}
	SériovéZápisbyte(uint8(data))
}

func MEmergencyZaznamenávaniereťazec(data string) {
	for i := 0; i < len(data); i++ {
		sériovéZaznamenávaniebyte(data[i])
	}
}

func MEmergencyZaznamenávaniehexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sériovéZaznamenávaniebyte(digits[(data>>4)&0x0F])
	sériovéZaznamenávaniebyte(digits[data&0x0F])
}

func MEmergencyZaznamenávanieunsignedinteger32(data uint32) {
	MEmergencyZaznamenávaniehexadecimal8(uint8(data >> 24))
	MEmergencyZaznamenávaniehexadecimal8(uint8(data >> 16))
	MEmergencyZaznamenávaniehexadecimal8(uint8(data >> 8))
	MEmergencyZaznamenávaniehexadecimal8(uint8(data))
}

func (vlastný *TKonzola) MTlačiť(argumentHodnota ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var hodnota_2 interface{}

	for i, p := range argumentHodnota {
		switch i {
		case 0:
			param, _ := p.(interface{})
			hodnota_2 = param
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

	vlastný.MTlačiťxy(hodnota_2, x, y)

}
func (vlastný *TKonzola) MTlačiťxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		vlastný.MTlačiťBajtyxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		vlastný.MHexadecimalTlačiťxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		vlastný.MUnsignedinteger16Tlačiťxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		vlastný.MUnsignedinteger32Tlačiťxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		vlastný.MUnsignedinteger64Tlačiťxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		vlastný.MTlačiťBajtyxy(data_2, x, y)
	}

}
func (vlastný *TKonzola) MTlačiťBajtyxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		vlastný.xPozícia = x
	}
	if y <= 999 {
		vlastný.yPozícia = y
	}

	vlastnosť := uint16(0x0F)
	obmedzenie := len(buffer)
	if obmedzenie > 4096 {
		obmedzenie = 4096
	}
	for i := 0; i < obmedzenie; i++ {
		sériovéZaznamenávaniebyte(buffer[i])
		switch buffer[i] {
		case '\n':
			vlastný.yPozícia++
			vlastný.xPozícia = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*vlastný.yPozícia+vlastný.xPozícia)*2))) = vlastnosť<<8 | uint16(buffer[i])
			vlastný.xPozícia++
		}

		if vlastný.xPozícia >= 80 {
			vlastný.yPozícia++
			vlastný.xPozícia = 0
		}

		if vlastný.yPozícia >= 25 {
			for vlastný.yPozícia = 0; vlastný.yPozícia < 25; vlastný.yPozícia++ {
				for vlastný.xPozícia = 0; vlastný.xPozícia < 80; vlastný.xPozícia++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*vlastný.yPozícia+vlastný.xPozícia)*2))) = vlastnosť<<8 | ' '
				}
			}
			vlastný.xPozícia = 0
			vlastný.yPozícia = 0
		}

	}

}
func (vlastný *TKonzola) MHexadecimalTlačiť(kľúč uint8) {
	buffer := []byte{'0', '0'}
	šestnástkové := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnástkové[(kľúč>>4)&0xF]
	buffer[1] = šestnástkové[kľúč&0xF]
	vlastný.MTlačiť(buffer)
}
func (vlastný *TKonzola) MHexadecimalTlačiťxy(kľúč uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	šestnástkové := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnástkové[(kľúč>>4)&0xF]
	buffer[1] = šestnástkové[kľúč&0xF]
	vlastný.MTlačiťxy(buffer, x, y)
}
func (vlastný *TKonzola) MUnsignedinteger16Tlačiť(kľúč uint16) {
	vlastný.MHexadecimalTlačiť(uint8(kľúč >> 8))
	vlastný.MHexadecimalTlačiť(uint8(kľúč))
}
func (vlastný *TKonzola) MUnsignedinteger16Tlačiťxy(kľúč uint16, x uint16, y uint16) {
	vlastný.MHexadecimalTlačiťxy(uint8(kľúč>>8), x, y)
	vlastný.MHexadecimalTlačiťxy(uint8(kľúč), x, y)
}
func (vlastný *TKonzola) MUnsignedinteger32Tlačiť(data uint32) {
	vlastný.MHexadecimalTlačiť(uint8(data >> 24))
	vlastný.MHexadecimalTlačiť(uint8(data >> 16))
	vlastný.MHexadecimalTlačiť(uint8(data >> 8))
	vlastný.MHexadecimalTlačiť(uint8(data))
}
func (vlastný *TKonzola) MUnsignedinteger32Tlačiťxy(data uint32, x uint16, y uint16) {

	vlastný.MHexadecimalTlačiťxy(uint8(data>>24), x+0, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>16), x+2, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>8), x+4, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data), x+6, y)
}
func (vlastný *TKonzola) MUnsignedinteger64Tlačiť(data uint64) {
	vlastný.MHexadecimalTlačiť(uint8(data >> 56))
	vlastný.MHexadecimalTlačiť(uint8(data >> 48))
	vlastný.MHexadecimalTlačiť(uint8(data >> 40))
	vlastný.MHexadecimalTlačiť(uint8(data >> 32))
	vlastný.MHexadecimalTlačiť(uint8(data >> 24))
	vlastný.MHexadecimalTlačiť(uint8(data >> 16))
	vlastný.MHexadecimalTlačiť(uint8(data >> 8))
	vlastný.MHexadecimalTlačiť(uint8(data))
}
func (vlastný *TKonzola) MUnsignedinteger64Tlačiťxy(data uint64, x uint16, y uint16) {
	vlastný.MHexadecimalTlačiťxy(uint8(data>>56), x+0, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>48), x+2, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>40), x+4, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>32), x+6, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>24), x+8, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>16), x+10, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data>>8), x+12, y)
	vlastný.MHexadecimalTlačiťxy(uint8(data), x+14, y)
}
func MTlačiť(phyaddr uintptr, data uint8, x uint32, y uint32)

func (vlastný *TKonzola) MTlačiťhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	šestnástkové := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šestnástkové[(data>>4)&0xF]
	buffer[1] = šestnástkové[data&0xF]

	MTlačiť(uintptr(fbphysaddress), buffer[0], x, y)
	MTlačiť(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (vlastný *TKonzola) MTlačiťunsignedinteger16(data uint16, x uint32, y uint32) {
	vlastný.MTlačiťhexadecimal(uint8(data>>8), x+0*2, y)
	vlastný.MTlačiťhexadecimal(uint8(data), x+2*2, y)
}

func (vlastný *TKonzola) MTlačiťunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	vlastný.MTlačiťhexadecimal(uint8(data>>24), x+0*2, y)
	vlastný.MTlačiťhexadecimal(uint8(data>>16), x+2*2, y)
	vlastný.MTlačiťhexadecimal(uint8(data>>8), x+4*2, y)
	vlastný.MTlačiťhexadecimal(uint8(data), x+6*2, y)
}

func (vlastný *TKonzola) M테스트() {
}
