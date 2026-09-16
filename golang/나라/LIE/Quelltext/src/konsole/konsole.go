/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package konsole

import . "unsafe"

const (
	fbBreite		= 80
	fbHöhe			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonsole struct {
	xposition	uint16
	yposition	uint16
}

var seriellBereit bool

func Seriellinit()
func SeriellSchreibenByte(daten uint8)

func MSeriellProtokollinit() {
	Seriellinit()
	seriellBereit = true
}

func seriellProtokollByte(daten byte) {
	if !seriellBereit {
		return
	}

	if daten == '\n' {
		SeriellSchreibenByte('\r')
	}
	SeriellSchreibenByte(uint8(daten))
}

func MEmergencyProtokollZeichenkette(daten string) {
	for i := 0; i < len(daten); i++ {
		seriellProtokollByte(daten[i])
	}
}

func MEmergencyProtokollhexadecimal8(daten uint8) {
	const digits = "0123456789ABCDEF"
	seriellProtokollByte(digits[(daten>>4)&0x0F])
	seriellProtokollByte(digits[daten&0x0F])
}

func MEmergencyProtokollunsignedinteger32(daten uint32) {
	MEmergencyProtokollhexadecimal8(uint8(daten >> 24))
	MEmergencyProtokollhexadecimal8(uint8(daten >> 16))
	MEmergencyProtokollhexadecimal8(uint8(daten >> 8))
	MEmergencyProtokollhexadecimal8(uint8(daten))
}

func (selbst *TKonsole) MDrucken(argumentWert ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var wert_2 interface{}

	for i, p := range argumentWert {
		switch i {
		case 0:
			param, _ := p.(interface{})
			wert_2 = param
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

	selbst.MDruckenxy(wert_2, x, y)

}
func (selbst *TKonsole) MDruckenxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		daten_2, _ := temporary_2.(string)
		selbst.MDruckenBytexy(([]byte)(daten_2), x, y)
	case uint8:
		daten_2, _ := temporary_2.(uint8)
		selbst.MHexadecimalDruckenxy(daten_2, x, y)
	case uint16:
		daten_2, _ := temporary_2.(uint16)
		selbst.MUnsignedinteger16Druckenxy(daten_2, x, y)
	case uint32:
		daten_2, _ := temporary_2.(uint32)
		selbst.MUnsignedinteger32Druckenxy(daten_2, x, y)
	case uint64:
		daten_2, _ := temporary_2.(uint64)
		selbst.MUnsignedinteger64Druckenxy(daten_2, x, y)
	default:
		daten_2, _ := temporary_2.([]byte)
		selbst.MDruckenBytexy(daten_2, x, y)
	}

}
func (selbst *TKonsole) MDruckenBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		selbst.xposition = x
	}
	if y <= 999 {
		selbst.yposition = y
	}

	attribut := uint16(0x0F)
	beschränkung := len(buffer)
	if beschränkung > 4096 {
		beschränkung = 4096
	}
	for i := 0; i < beschränkung; i++ {
		seriellProtokollByte(buffer[i])
		switch buffer[i] {
		case '\n':
			selbst.yposition++
			selbst.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*selbst.yposition+selbst.xposition)*2))) = attribut<<8 | uint16(buffer[i])
			selbst.xposition++
		}

		if selbst.xposition >= 80 {
			selbst.yposition++
			selbst.xposition = 0
		}

		if selbst.yposition >= 25 {
			for selbst.yposition = 0; selbst.yposition < 25; selbst.yposition++ {
				for selbst.xposition = 0; selbst.xposition < 80; selbst.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*selbst.yposition+selbst.xposition)*2))) = attribut<<8 | ' '
				}
			}
			selbst.xposition = 0
			selbst.yposition = 0
		}

	}

}
func (selbst *TKonsole) MHexadecimalDrucken(schlüssel uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(schlüssel>>4)&0xF]
	buffer[1] = hex[schlüssel&0xF]
	selbst.MDrucken(buffer)
}
func (selbst *TKonsole) MHexadecimalDruckenxy(schlüssel uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(schlüssel>>4)&0xF]
	buffer[1] = hex[schlüssel&0xF]
	selbst.MDruckenxy(buffer, x, y)
}
func (selbst *TKonsole) MUnsignedinteger16Drucken(schlüssel uint16) {
	selbst.MHexadecimalDrucken(uint8(schlüssel >> 8))
	selbst.MHexadecimalDrucken(uint8(schlüssel))
}
func (selbst *TKonsole) MUnsignedinteger16Druckenxy(schlüssel uint16, x uint16, y uint16) {
	selbst.MHexadecimalDruckenxy(uint8(schlüssel>>8), x, y)
	selbst.MHexadecimalDruckenxy(uint8(schlüssel), x, y)
}
func (selbst *TKonsole) MUnsignedinteger32Drucken(daten uint32) {
	selbst.MHexadecimalDrucken(uint8(daten >> 24))
	selbst.MHexadecimalDrucken(uint8(daten >> 16))
	selbst.MHexadecimalDrucken(uint8(daten >> 8))
	selbst.MHexadecimalDrucken(uint8(daten))
}
func (selbst *TKonsole) MUnsignedinteger32Druckenxy(daten uint32, x uint16, y uint16) {

	selbst.MHexadecimalDruckenxy(uint8(daten>>24), x+0, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>16), x+2, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>8), x+4, y)
	selbst.MHexadecimalDruckenxy(uint8(daten), x+6, y)
}
func (selbst *TKonsole) MUnsignedinteger64Drucken(daten uint64) {
	selbst.MHexadecimalDrucken(uint8(daten >> 56))
	selbst.MHexadecimalDrucken(uint8(daten >> 48))
	selbst.MHexadecimalDrucken(uint8(daten >> 40))
	selbst.MHexadecimalDrucken(uint8(daten >> 32))
	selbst.MHexadecimalDrucken(uint8(daten >> 24))
	selbst.MHexadecimalDrucken(uint8(daten >> 16))
	selbst.MHexadecimalDrucken(uint8(daten >> 8))
	selbst.MHexadecimalDrucken(uint8(daten))
}
func (selbst *TKonsole) MUnsignedinteger64Druckenxy(daten uint64, x uint16, y uint16) {
	selbst.MHexadecimalDruckenxy(uint8(daten>>56), x+0, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>48), x+2, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>40), x+4, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>32), x+6, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>24), x+8, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>16), x+10, y)
	selbst.MHexadecimalDruckenxy(uint8(daten>>8), x+12, y)
	selbst.MHexadecimalDruckenxy(uint8(daten), x+14, y)
}
func MDrucken(phyaddr uintptr, daten uint8, x uint32, y uint32)

func (selbst *TKonsole) MDruckenhexadecimal(daten uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(daten>>4)&0xF]
	buffer[1] = hex[daten&0xF]

	MDrucken(uintptr(fbphysaddress), buffer[0], x, y)
	MDrucken(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (selbst *TKonsole) MDruckenunsignedinteger16(daten uint16, x uint32, y uint32) {
	selbst.MDruckenhexadecimal(uint8(daten>>8), x+0*2, y)
	selbst.MDruckenhexadecimal(uint8(daten), x+2*2, y)
}

func (selbst *TKonsole) MDruckenunsignedinteger32(daten uint32, x uint32, y uint32) {
	x = x * 2
	selbst.MDruckenhexadecimal(uint8(daten>>24), x+0*2, y)
	selbst.MDruckenhexadecimal(uint8(daten>>16), x+2*2, y)
	selbst.MDruckenhexadecimal(uint8(daten>>8), x+4*2, y)
	selbst.MDruckenhexadecimal(uint8(daten), x+6*2, y)
}

func (selbst *TKonsole) M테스트() {
}
