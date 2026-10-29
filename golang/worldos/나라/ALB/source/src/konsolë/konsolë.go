/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsolë

import . "unsafe"

const (
	fbGjerësia		= 80
	fbLartësia		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonsolë struct {
	xPozicion	uint16
	yPozicion	uint16
}

var serialGati bool

func Serialinit()
func SerialShkrimibyte(data uint8)

func MSerialRegjistërinit() {
	Serialinit()
	serialGati = true
}

func serialRegjistërbyte(data byte) {
	if !serialGati {
		return
	}

	if data == '\n' {
		SerialShkrimibyte('\r')
	}
	SerialShkrimibyte(uint8(data))
}

func MEmergencyRegjistërvarg(data string) {
	for i := 0; i < len(data); i++ {
		serialRegjistërbyte(data[i])
	}
}

func MEmergencyRegjistërhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serialRegjistërbyte(digits[(data>>4)&0x0F])
	serialRegjistërbyte(digits[data&0x0F])
}

func MEmergencyRegjistërunsignedinteger32(data uint32) {
	MEmergencyRegjistërhexadecimal8(uint8(data >> 24))
	MEmergencyRegjistërhexadecimal8(uint8(data >> 16))
	MEmergencyRegjistërhexadecimal8(uint8(data >> 8))
	MEmergencyRegjistërhexadecimal8(uint8(data))
}

func (vetvetja *TKonsolë) MPrinto(argumentVlera ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var vlera_2 interface{}

	for i, p := range argumentVlera {
		switch i {
		case 0:
			param, _ := p.(interface{})
			vlera_2 = param
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

	vetvetja.MPrintoxy(vlera_2, x, y)

}
func (vetvetja *TKonsolë) MPrintoxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		vetvetja.MPrintobytesxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		vetvetja.MHexadecimalPrintoxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		vetvetja.MUnsignedinteger16Printoxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		vetvetja.MUnsignedinteger32Printoxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		vetvetja.MUnsignedinteger64Printoxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		vetvetja.MPrintobytesxy(data_2, x, y)
	}

}
func (vetvetja *TKonsolë) MPrintobytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		vetvetja.xPozicion = x
	}
	if y <= 999 {
		vetvetja.yPozicion = y
	}

	karakteristika := uint16(0x0F)
	kufi := len(buffer)
	if kufi > 4096 {
		kufi = 4096
	}
	for i := 0; i < kufi; i++ {
		serialRegjistërbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			vetvetja.yPozicion++
			vetvetja.xPozicion = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*vetvetja.yPozicion+vetvetja.xPozicion)*2))) = karakteristika<<8 | uint16(buffer[i])
			vetvetja.xPozicion++
		}

		if vetvetja.xPozicion >= 80 {
			vetvetja.yPozicion++
			vetvetja.xPozicion = 0
		}

		if vetvetja.yPozicion >= 25 {
			for vetvetja.yPozicion = 0; vetvetja.yPozicion < 25; vetvetja.yPozicion++ {
				for vetvetja.xPozicion = 0; vetvetja.xPozicion < 80; vetvetja.xPozicion++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*vetvetja.yPozicion+vetvetja.xPozicion)*2))) = karakteristika<<8 | ' '
				}
			}
			vetvetja.xPozicion = 0
			vetvetja.yPozicion = 0
		}

	}

}
func (vetvetja *TKonsolë) MHexadecimalPrinto(çeles uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(çeles>>4)&0xF]
	buffer[1] = hex[çeles&0xF]
	vetvetja.MPrinto(buffer)
}
func (vetvetja *TKonsolë) MHexadecimalPrintoxy(çeles uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(çeles>>4)&0xF]
	buffer[1] = hex[çeles&0xF]
	vetvetja.MPrintoxy(buffer, x, y)
}
func (vetvetja *TKonsolë) MUnsignedinteger16Printo(çeles uint16) {
	vetvetja.MHexadecimalPrinto(uint8(çeles >> 8))
	vetvetja.MHexadecimalPrinto(uint8(çeles))
}
func (vetvetja *TKonsolë) MUnsignedinteger16Printoxy(çeles uint16, x uint16, y uint16) {
	vetvetja.MHexadecimalPrintoxy(uint8(çeles>>8), x, y)
	vetvetja.MHexadecimalPrintoxy(uint8(çeles), x, y)
}
func (vetvetja *TKonsolë) MUnsignedinteger32Printo(data uint32) {
	vetvetja.MHexadecimalPrinto(uint8(data >> 24))
	vetvetja.MHexadecimalPrinto(uint8(data >> 16))
	vetvetja.MHexadecimalPrinto(uint8(data >> 8))
	vetvetja.MHexadecimalPrinto(uint8(data))
}
func (vetvetja *TKonsolë) MUnsignedinteger32Printoxy(data uint32, x uint16, y uint16) {

	vetvetja.MHexadecimalPrintoxy(uint8(data>>24), x+0, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>16), x+2, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>8), x+4, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data), x+6, y)
}
func (vetvetja *TKonsolë) MUnsignedinteger64Printo(data uint64) {
	vetvetja.MHexadecimalPrinto(uint8(data >> 56))
	vetvetja.MHexadecimalPrinto(uint8(data >> 48))
	vetvetja.MHexadecimalPrinto(uint8(data >> 40))
	vetvetja.MHexadecimalPrinto(uint8(data >> 32))
	vetvetja.MHexadecimalPrinto(uint8(data >> 24))
	vetvetja.MHexadecimalPrinto(uint8(data >> 16))
	vetvetja.MHexadecimalPrinto(uint8(data >> 8))
	vetvetja.MHexadecimalPrinto(uint8(data))
}
func (vetvetja *TKonsolë) MUnsignedinteger64Printoxy(data uint64, x uint16, y uint16) {
	vetvetja.MHexadecimalPrintoxy(uint8(data>>56), x+0, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>48), x+2, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>40), x+4, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>32), x+6, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>24), x+8, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>16), x+10, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data>>8), x+12, y)
	vetvetja.MHexadecimalPrintoxy(uint8(data), x+14, y)
}
func MPrinto(phyaddr uintptr, data uint8, x uint32, y uint32)

func (vetvetja *TKonsolë) MPrintohexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MPrinto(uintptr(fbphysaddress), buffer[0], x, y)
	MPrinto(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (vetvetja *TKonsolë) MPrintounsignedinteger16(data uint16, x uint32, y uint32) {
	vetvetja.MPrintohexadecimal(uint8(data>>8), x+0*2, y)
	vetvetja.MPrintohexadecimal(uint8(data), x+2*2, y)
}

func (vetvetja *TKonsolë) MPrintounsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	vetvetja.MPrintohexadecimal(uint8(data>>24), x+0*2, y)
	vetvetja.MPrintohexadecimal(uint8(data>>16), x+2*2, y)
	vetvetja.MPrintohexadecimal(uint8(data>>8), x+4*2, y)
	vetvetja.MPrintohexadecimal(uint8(data), x+6*2, y)
}

func (vetvetja *TKonsolë) M테스트() {
}
