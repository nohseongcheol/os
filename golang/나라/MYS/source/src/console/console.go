package console

import . "unsafe"

const (
	fbLebar			= 80
	fbTinggi		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xKedudukan	uint16
	yKedudukan	uint16
}

var siriSedia bool

func Siriinit()
func SiriTulisbyte(data uint8)

func MSiriloginit() {
	Siriinit()
	siriSedia = true
}

func sirilogbyte(data byte) {
	if !siriSedia {
		return
	}

	if data == '\n' {
		SiriTulisbyte('\r')
	}
	SiriTulisbyte(uint8(data))
}

func MEmergencylogRentetan(data string) {
	for i := 0; i < len(data); i++ {
		sirilogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sirilogbyte(digits[(data>>4)&0x0F])
	sirilogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (diri *TConsole) MCetak(argumentNilai ...interface{}) {
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

	diri.MCetakxy(nilai_3, x, y)

}
func (diri *TConsole) MCetakxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		diri.MCetakBaitxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		diri.MHexadecimalCetakxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		diri.MUnsignedinteger16Cetakxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		diri.MUnsignedinteger32Cetakxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		diri.MUnsignedinteger64Cetakxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		diri.MCetakBaitxy(data_2, x, y)
	}

}
func (diri *TConsole) MCetakBaitxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		diri.xKedudukan = x
	}
	if y <= 999 {
		diri.yKedudukan = y
	}

	atribut := uint16(0x0F)
	had := len(buffer)
	if had > 4096 {
		had = 4096
	}
	for i := 0; i < had; i++ {
		sirilogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			diri.yKedudukan++
			diri.xKedudukan = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*diri.yKedudukan+diri.xKedudukan)*2))) = atribut<<8 | uint16(buffer[i])
			diri.xKedudukan++
		}

		if diri.xKedudukan >= 80 {
			diri.yKedudukan++
			diri.xKedudukan = 0
		}

		if diri.yKedudukan >= 25 {
			for diri.yKedudukan = 0; diri.yKedudukan < 25; diri.yKedudukan++ {
				for diri.xKedudukan = 0; diri.xKedudukan < 80; diri.xKedudukan++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*diri.yKedudukan+diri.xKedudukan)*2))) = atribut<<8 | ' '
				}
			}
			diri.xKedudukan = 0
			diri.yKedudukan = 0
		}

	}

}
func (diri *TConsole) MHexadecimalCetak(kunci uint8) {
	buffer := []byte{'0', '0'}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(kunci>>4)&0xF]
	buffer[1] = heks[kunci&0xF]
	diri.MCetak(buffer)
}
func (diri *TConsole) MHexadecimalCetakxy(kunci uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(kunci>>4)&0xF]
	buffer[1] = heks[kunci&0xF]
	diri.MCetakxy(buffer, x, y)
}
func (diri *TConsole) MUnsignedinteger16Cetak(kunci uint16) {
	diri.MHexadecimalCetak(uint8(kunci >> 8))
	diri.MHexadecimalCetak(uint8(kunci))
}
func (diri *TConsole) MUnsignedinteger16Cetakxy(kunci uint16, x uint16, y uint16) {
	diri.MHexadecimalCetakxy(uint8(kunci>>8), x, y)
	diri.MHexadecimalCetakxy(uint8(kunci), x, y)
}
func (diri *TConsole) MUnsignedinteger32Cetak(data uint32) {
	diri.MHexadecimalCetak(uint8(data >> 24))
	diri.MHexadecimalCetak(uint8(data >> 16))
	diri.MHexadecimalCetak(uint8(data >> 8))
	diri.MHexadecimalCetak(uint8(data))
}
func (diri *TConsole) MUnsignedinteger32Cetakxy(data uint32, x uint16, y uint16) {

	diri.MHexadecimalCetakxy(uint8(data>>24), x+0, y)
	diri.MHexadecimalCetakxy(uint8(data>>16), x+2, y)
	diri.MHexadecimalCetakxy(uint8(data>>8), x+4, y)
	diri.MHexadecimalCetakxy(uint8(data), x+6, y)
}
func (diri *TConsole) MUnsignedinteger64Cetak(data uint64) {
	diri.MHexadecimalCetak(uint8(data >> 56))
	diri.MHexadecimalCetak(uint8(data >> 48))
	diri.MHexadecimalCetak(uint8(data >> 40))
	diri.MHexadecimalCetak(uint8(data >> 32))
	diri.MHexadecimalCetak(uint8(data >> 24))
	diri.MHexadecimalCetak(uint8(data >> 16))
	diri.MHexadecimalCetak(uint8(data >> 8))
	diri.MHexadecimalCetak(uint8(data))
}
func (diri *TConsole) MUnsignedinteger64Cetakxy(data uint64, x uint16, y uint16) {
	diri.MHexadecimalCetakxy(uint8(data>>56), x+0, y)
	diri.MHexadecimalCetakxy(uint8(data>>48), x+2, y)
	diri.MHexadecimalCetakxy(uint8(data>>40), x+4, y)
	diri.MHexadecimalCetakxy(uint8(data>>32), x+6, y)
	diri.MHexadecimalCetakxy(uint8(data>>24), x+8, y)
	diri.MHexadecimalCetakxy(uint8(data>>16), x+10, y)
	diri.MHexadecimalCetakxy(uint8(data>>8), x+12, y)
	diri.MHexadecimalCetakxy(uint8(data), x+14, y)
}
func MCetak(phyaddr uintptr, data uint8, x uint32, y uint32)

func (diri *TConsole) MCetakhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = heks[(data>>4)&0xF]
	buffer[1] = heks[data&0xF]

	MCetak(uintptr(fbphysaddress), buffer[0], x, y)
	MCetak(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (diri *TConsole) MCetakunsignedinteger16(data uint16, x uint32, y uint32) {
	diri.MCetakhexadecimal(uint8(data>>8), x+0*2, y)
	diri.MCetakhexadecimal(uint8(data), x+2*2, y)
}

func (diri *TConsole) MCetakunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	diri.MCetakhexadecimal(uint8(data>>24), x+0*2, y)
	diri.MCetakhexadecimal(uint8(data>>16), x+2*2, y)
	diri.MCetakhexadecimal(uint8(data>>8), x+4*2, y)
	diri.MCetakhexadecimal(uint8(data), x+6*2, y)
}

func (diri *TConsole) M테스트() {
}
