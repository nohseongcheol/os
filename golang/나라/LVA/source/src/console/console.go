/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbPlatums		= 80
	fbAugstums		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xNovietojums	uint16
	yNovietojums	uint16
}

var serialGatavs bool

func Serialinit()
func SerialRakstītbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialGatavs = true
}

func seriallogbyte(data byte) {
	if !serialGatavs {
		return
	}

	if data == '\n' {
		SerialRakstītbyte('\r')
	}
	SerialRakstītbyte(uint8(data))
}

func MEmergencylogvirkne(data string) {
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

func (pats *TConsole) MDrukāt(argumentVērtība ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var vērtība_2 interface{}

	for i, p := range argumentVērtība {
		switch i {
		case 0:
			param, _ := p.(interface{})
			vērtība_2 = param
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

	pats.MDrukātxy(vērtība_2, x, y)

}
func (pats *TConsole) MDrukātxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		pats.MDrukātBaitixy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		pats.MHexadecimalDrukātxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		pats.MUnsignedinteger16Drukātxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		pats.MUnsignedinteger32Drukātxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		pats.MUnsignedinteger64Drukātxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		pats.MDrukātBaitixy(data_2, x, y)
	}

}
func (pats *TConsole) MDrukātBaitixy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		pats.xNovietojums = x
	}
	if y <= 999 {
		pats.yNovietojums = y
	}

	atribūts := uint16(0x0F)
	ierobežot := len(buffer)
	if ierobežot > 4096 {
		ierobežot = 4096
	}
	for i := 0; i < ierobežot; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			pats.yNovietojums++
			pats.xNovietojums = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*pats.yNovietojums+pats.xNovietojums)*2))) = atribūts<<8 | uint16(buffer[i])
			pats.xNovietojums++
		}

		if pats.xNovietojums >= 80 {
			pats.yNovietojums++
			pats.xNovietojums = 0
		}

		if pats.yNovietojums >= 25 {
			for pats.yNovietojums = 0; pats.yNovietojums < 25; pats.yNovietojums++ {
				for pats.xNovietojums = 0; pats.xNovietojums < 80; pats.xNovietojums++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*pats.yNovietojums+pats.xNovietojums)*2))) = atribūts<<8 | ' '
				}
			}
			pats.xNovietojums = 0
			pats.yNovietojums = 0
		}

	}

}
func (pats *TConsole) MHexadecimalDrukāt(atslēga uint8) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(atslēga>>4)&0xF]
	buffer[1] = heksa[atslēga&0xF]
	pats.MDrukāt(buffer)
}
func (pats *TConsole) MHexadecimalDrukātxy(atslēga uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(atslēga>>4)&0xF]
	buffer[1] = heksa[atslēga&0xF]
	pats.MDrukātxy(buffer, x, y)
}
func (pats *TConsole) MUnsignedinteger16Drukāt(atslēga uint16) {
	pats.MHexadecimalDrukāt(uint8(atslēga >> 8))
	pats.MHexadecimalDrukāt(uint8(atslēga))
}
func (pats *TConsole) MUnsignedinteger16Drukātxy(atslēga uint16, x uint16, y uint16) {
	pats.MHexadecimalDrukātxy(uint8(atslēga>>8), x, y)
	pats.MHexadecimalDrukātxy(uint8(atslēga), x, y)
}
func (pats *TConsole) MUnsignedinteger32Drukāt(data uint32) {
	pats.MHexadecimalDrukāt(uint8(data >> 24))
	pats.MHexadecimalDrukāt(uint8(data >> 16))
	pats.MHexadecimalDrukāt(uint8(data >> 8))
	pats.MHexadecimalDrukāt(uint8(data))
}
func (pats *TConsole) MUnsignedinteger32Drukātxy(data uint32, x uint16, y uint16) {

	pats.MHexadecimalDrukātxy(uint8(data>>24), x+0, y)
	pats.MHexadecimalDrukātxy(uint8(data>>16), x+2, y)
	pats.MHexadecimalDrukātxy(uint8(data>>8), x+4, y)
	pats.MHexadecimalDrukātxy(uint8(data), x+6, y)
}
func (pats *TConsole) MUnsignedinteger64Drukāt(data uint64) {
	pats.MHexadecimalDrukāt(uint8(data >> 56))
	pats.MHexadecimalDrukāt(uint8(data >> 48))
	pats.MHexadecimalDrukāt(uint8(data >> 40))
	pats.MHexadecimalDrukāt(uint8(data >> 32))
	pats.MHexadecimalDrukāt(uint8(data >> 24))
	pats.MHexadecimalDrukāt(uint8(data >> 16))
	pats.MHexadecimalDrukāt(uint8(data >> 8))
	pats.MHexadecimalDrukāt(uint8(data))
}
func (pats *TConsole) MUnsignedinteger64Drukātxy(data uint64, x uint16, y uint16) {
	pats.MHexadecimalDrukātxy(uint8(data>>56), x+0, y)
	pats.MHexadecimalDrukātxy(uint8(data>>48), x+2, y)
	pats.MHexadecimalDrukātxy(uint8(data>>40), x+4, y)
	pats.MHexadecimalDrukātxy(uint8(data>>32), x+6, y)
	pats.MHexadecimalDrukātxy(uint8(data>>24), x+8, y)
	pats.MHexadecimalDrukātxy(uint8(data>>16), x+10, y)
	pats.MHexadecimalDrukātxy(uint8(data>>8), x+12, y)
	pats.MHexadecimalDrukātxy(uint8(data), x+14, y)
}
func MDrukāt(phyaddr uintptr, data uint8, x uint32, y uint32)

func (pats *TConsole) MDrukāthexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(data>>4)&0xF]
	buffer[1] = heksa[data&0xF]

	MDrukāt(uintptr(fbphysaddress), buffer[0], x, y)
	MDrukāt(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (pats *TConsole) MDrukātunsignedinteger16(data uint16, x uint32, y uint32) {
	pats.MDrukāthexadecimal(uint8(data>>8), x+0*2, y)
	pats.MDrukāthexadecimal(uint8(data), x+2*2, y)
}

func (pats *TConsole) MDrukātunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	pats.MDrukāthexadecimal(uint8(data>>24), x+0*2, y)
	pats.MDrukāthexadecimal(uint8(data>>16), x+2*2, y)
	pats.MDrukāthexadecimal(uint8(data>>8), x+4*2, y)
	pats.MDrukāthexadecimal(uint8(data), x+6*2, y)
}

func (pats *TConsole) M테스트() {
}
