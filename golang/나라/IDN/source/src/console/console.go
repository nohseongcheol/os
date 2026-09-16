/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbLebar			= 80
	fbTinggi		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPosisi	uint16
	yPosisi	uint16
}

var serialSiap bool

func Serialinit()
func SerialTulisbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialSiap = true
}

func seriallogbyte(data byte) {
	if !serialSiap {
		return
	}

	if data == '\n' {
		SerialTulisbyte('\r')
	}
	SerialTulisbyte(uint8(data))
}

func MEmergencylogBenang(data string) {
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

func (dirisendiri *TConsole) MCetak(argumentNilai ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var nilai_3 interface{}

	for i, p := range argumentNilai {
		switch i {
		case 0:
			param, _ := p.(interface{})
			nilai_3 = param
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

	dirisendiri.MCetakxy(nilai_3, x, y)

}
func (dirisendiri *TConsole) MCetakxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		dirisendiri.MCetakBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		dirisendiri.MHexadecimalCetakxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		dirisendiri.MUnsignedinteger16Cetakxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		dirisendiri.MUnsignedinteger32Cetakxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		dirisendiri.MUnsignedinteger64Cetakxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		dirisendiri.MCetakBytexy(data_2, x, y)
	}

}
func (dirisendiri *TConsole) MCetakBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		dirisendiri.xPosisi = x
	}
	if y <= 999 {
		dirisendiri.yPosisi = y
	}

	atribut := uint16(0x0F)
	batas := len(buffer)
	if batas > 4096 {
		batas = 4096
	}
	for i := 0; i < batas; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			dirisendiri.yPosisi++
			dirisendiri.xPosisi = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*dirisendiri.yPosisi+dirisendiri.xPosisi)*2))) = atribut<<8 | uint16(buffer[i])
			dirisendiri.xPosisi++
		}

		if dirisendiri.xPosisi >= 80 {
			dirisendiri.yPosisi++
			dirisendiri.xPosisi = 0
		}

		if dirisendiri.yPosisi >= 25 {
			for dirisendiri.yPosisi = 0; dirisendiri.yPosisi < 25; dirisendiri.yPosisi++ {
				for dirisendiri.xPosisi = 0; dirisendiri.xPosisi < 80; dirisendiri.xPosisi++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*dirisendiri.yPosisi+dirisendiri.xPosisi)*2))) = atribut<<8 | ' '
				}
			}
			dirisendiri.xPosisi = 0
			dirisendiri.yPosisi = 0
		}

	}

}
func (dirisendiri *TConsole) MHexadecimalCetak(kunci uint8) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(kunci>>4)&0xF]
	buffer[1] = heksa[kunci&0xF]
	dirisendiri.MCetak(buffer)
}
func (dirisendiri *TConsole) MHexadecimalCetakxy(kunci uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(kunci>>4)&0xF]
	buffer[1] = heksa[kunci&0xF]
	dirisendiri.MCetakxy(buffer, x, y)
}
func (dirisendiri *TConsole) MUnsignedinteger16Cetak(kunci uint16) {
	dirisendiri.MHexadecimalCetak(uint8(kunci >> 8))
	dirisendiri.MHexadecimalCetak(uint8(kunci))
}
func (dirisendiri *TConsole) MUnsignedinteger16Cetakxy(kunci uint16, x uint16, y uint16) {
	dirisendiri.MHexadecimalCetakxy(uint8(kunci>>8), x, y)
	dirisendiri.MHexadecimalCetakxy(uint8(kunci), x, y)
}
func (dirisendiri *TConsole) MUnsignedinteger32Cetak(data uint32) {
	dirisendiri.MHexadecimalCetak(uint8(data >> 24))
	dirisendiri.MHexadecimalCetak(uint8(data >> 16))
	dirisendiri.MHexadecimalCetak(uint8(data >> 8))
	dirisendiri.MHexadecimalCetak(uint8(data))
}
func (dirisendiri *TConsole) MUnsignedinteger32Cetakxy(data uint32, x uint16, y uint16) {

	dirisendiri.MHexadecimalCetakxy(uint8(data>>24), x+0, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>16), x+2, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>8), x+4, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data), x+6, y)
}
func (dirisendiri *TConsole) MUnsignedinteger64Cetak(data uint64) {
	dirisendiri.MHexadecimalCetak(uint8(data >> 56))
	dirisendiri.MHexadecimalCetak(uint8(data >> 48))
	dirisendiri.MHexadecimalCetak(uint8(data >> 40))
	dirisendiri.MHexadecimalCetak(uint8(data >> 32))
	dirisendiri.MHexadecimalCetak(uint8(data >> 24))
	dirisendiri.MHexadecimalCetak(uint8(data >> 16))
	dirisendiri.MHexadecimalCetak(uint8(data >> 8))
	dirisendiri.MHexadecimalCetak(uint8(data))
}
func (dirisendiri *TConsole) MUnsignedinteger64Cetakxy(data uint64, x uint16, y uint16) {
	dirisendiri.MHexadecimalCetakxy(uint8(data>>56), x+0, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>48), x+2, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>40), x+4, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>32), x+6, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>24), x+8, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>16), x+10, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data>>8), x+12, y)
	dirisendiri.MHexadecimalCetakxy(uint8(data), x+14, y)
}
func MCetak(phyaddr uintptr, data uint8, x uint32, y uint32)

func (dirisendiri *TConsole) MCetakhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heksa[(data>>4)&0xF]
	buffer[1] = heksa[data&0xF]

	MCetak(uintptr(fbphysaddress), buffer[0], x, y)
	MCetak(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (dirisendiri *TConsole) MCetakunsignedinteger16(data uint16, x uint32, y uint32) {
	dirisendiri.MCetakhexadecimal(uint8(data>>8), x+0*2, y)
	dirisendiri.MCetakhexadecimal(uint8(data), x+2*2, y)
}

func (dirisendiri *TConsole) MCetakunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	dirisendiri.MCetakhexadecimal(uint8(data>>24), x+0*2, y)
	dirisendiri.MCetakhexadecimal(uint8(data>>16), x+2*2, y)
	dirisendiri.MCetakhexadecimal(uint8(data>>8), x+4*2, y)
	dirisendiri.MCetakhexadecimal(uint8(data), x+6*2, y)
}

func (dirisendiri *TConsole) M테스트() {
}
