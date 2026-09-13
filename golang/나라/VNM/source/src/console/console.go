package console

import . "unsafe"

const (
	fbĐộrộng		= 80
	fbĐộcao			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xVịtrí	uint16
	yVịtrí	uint16
}

var sốxêriSẵnsàng bool

func Sốxêriinit()
func SốxêriGhibyte(data uint8)

func MSốxêriloginit() {
	Sốxêriinit()
	sốxêriSẵnsàng = true
}

func sốxêrilogbyte(data byte) {
	if !sốxêriSẵnsàng {
		return
	}

	if data == '\n' {
		SốxêriGhibyte('\r')
	}
	SốxêriGhibyte(uint8(data))
}

func MEmergencylogCHUỖI(data string) {
	for i := 0; i < len(data); i++ {
		sốxêrilogbyte(data[i])
	}
}

func MEmergencyloghexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sốxêrilogbyte(digits[(data>>4)&0x0F])
	sốxêrilogbyte(digits[data&0x0F])
}

func MEmergencylogunsignedinteger32(data uint32) {
	MEmergencyloghexadecimal8(uint8(data >> 24))
	MEmergencyloghexadecimal8(uint8(data >> 16))
	MEmergencyloghexadecimal8(uint8(data >> 8))
	MEmergencyloghexadecimal8(uint8(data))
}

func (mình *TConsole) MIn(argumentGiátrị ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var giátrị_2 interface{}

	for i, p := range argumentGiátrị {
		switch i {
		case 0:
			param, _ := p.(interface{})
			giátrị_2 = param
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

	mình.MInxy(giátrị_2, x, y)

}
func (mình *TConsole) MInxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		mình.MInBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		mình.MHexadecimalInxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		mình.MUnsignedinteger16Inxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		mình.MUnsignedinteger32Inxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		mình.MUnsignedinteger64Inxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		mình.MInBytexy(data_2, x, y)
	}

}
func (mình *TConsole) MInBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		mình.xVịtrí = x
	}
	if y <= 999 {
		mình.yVịtrí = y
	}

	thuộctính := uint16(0x0F)
	giớihạn := len(buffer)
	if giớihạn > 4096 {
		giớihạn = 4096
	}
	for i := 0; i < giớihạn; i++ {
		sốxêrilogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			mình.yVịtrí++
			mình.xVịtrí = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*mình.yVịtrí+mình.xVịtrí)*2))) = thuộctính<<8 | uint16(buffer[i])
			mình.xVịtrí++
		}

		if mình.xVịtrí >= 80 {
			mình.yVịtrí++
			mình.xVịtrí = 0
		}

		if mình.yVịtrí >= 25 {
			for mình.yVịtrí = 0; mình.yVịtrí < 25; mình.yVịtrí++ {
				for mình.xVịtrí = 0; mình.xVịtrí < 80; mình.xVịtrí++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*mình.yVịtrí+mình.xVịtrí)*2))) = thuộctính<<8 | ' '
				}
			}
			mình.xVịtrí = 0
			mình.yVịtrí = 0
		}

	}

}
func (mình *TConsole) MHexadecimalIn(key uint8) {
	buffer := []byte{'0', '0'}
	thậplục := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = thậplục[(key>>4)&0xF]
	buffer[1] = thậplục[key&0xF]
	mình.MIn(buffer)
}
func (mình *TConsole) MHexadecimalInxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	thậplục := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = thậplục[(key>>4)&0xF]
	buffer[1] = thậplục[key&0xF]
	mình.MInxy(buffer, x, y)
}
func (mình *TConsole) MUnsignedinteger16In(key uint16) {
	mình.MHexadecimalIn(uint8(key >> 8))
	mình.MHexadecimalIn(uint8(key))
}
func (mình *TConsole) MUnsignedinteger16Inxy(key uint16, x uint16, y uint16) {
	mình.MHexadecimalInxy(uint8(key>>8), x, y)
	mình.MHexadecimalInxy(uint8(key), x, y)
}
func (mình *TConsole) MUnsignedinteger32In(data uint32) {
	mình.MHexadecimalIn(uint8(data >> 24))
	mình.MHexadecimalIn(uint8(data >> 16))
	mình.MHexadecimalIn(uint8(data >> 8))
	mình.MHexadecimalIn(uint8(data))
}
func (mình *TConsole) MUnsignedinteger32Inxy(data uint32, x uint16, y uint16) {

	mình.MHexadecimalInxy(uint8(data>>24), x+0, y)
	mình.MHexadecimalInxy(uint8(data>>16), x+2, y)
	mình.MHexadecimalInxy(uint8(data>>8), x+4, y)
	mình.MHexadecimalInxy(uint8(data), x+6, y)
}
func (mình *TConsole) MUnsignedinteger64In(data uint64) {
	mình.MHexadecimalIn(uint8(data >> 56))
	mình.MHexadecimalIn(uint8(data >> 48))
	mình.MHexadecimalIn(uint8(data >> 40))
	mình.MHexadecimalIn(uint8(data >> 32))
	mình.MHexadecimalIn(uint8(data >> 24))
	mình.MHexadecimalIn(uint8(data >> 16))
	mình.MHexadecimalIn(uint8(data >> 8))
	mình.MHexadecimalIn(uint8(data))
}
func (mình *TConsole) MUnsignedinteger64Inxy(data uint64, x uint16, y uint16) {
	mình.MHexadecimalInxy(uint8(data>>56), x+0, y)
	mình.MHexadecimalInxy(uint8(data>>48), x+2, y)
	mình.MHexadecimalInxy(uint8(data>>40), x+4, y)
	mình.MHexadecimalInxy(uint8(data>>32), x+6, y)
	mình.MHexadecimalInxy(uint8(data>>24), x+8, y)
	mình.MHexadecimalInxy(uint8(data>>16), x+10, y)
	mình.MHexadecimalInxy(uint8(data>>8), x+12, y)
	mình.MHexadecimalInxy(uint8(data), x+14, y)
}
func MIn(phyaddr uintptr, data uint8, x uint32, y uint32)

func (mình *TConsole) MInhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	thậplục := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = thậplục[(data>>4)&0xF]
	buffer[1] = thậplục[data&0xF]

	MIn(uintptr(fbphysaddress), buffer[0], x, y)
	MIn(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (mình *TConsole) MInunsignedinteger16(data uint16, x uint32, y uint32) {
	mình.MInhexadecimal(uint8(data>>8), x+0*2, y)
	mình.MInhexadecimal(uint8(data), x+2*2, y)
}

func (mình *TConsole) MInunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	mình.MInhexadecimal(uint8(data>>24), x+0*2, y)
	mình.MInhexadecimal(uint8(data>>16), x+2*2, y)
	mình.MInhexadecimal(uint8(data>>8), x+4*2, y)
	mình.MInhexadecimal(uint8(data), x+6*2, y)
}

func (mình *TConsole) M테스트() {
}
