/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package طرفية

import . "unsafe"

const (
	fbالعرض			= 80
	fbالارتفاع		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type Tطرفية struct {
	xالموضع	uint16
	yالموضع	uint16
}

var تسلسليجاهز bool

func Sتسلسليinit()
func Sتسلسليكتابةبايت(بيانات uint8)

func Mتسلسليالسجلinit() {
	Sتسلسليinit()
	تسلسليجاهز = true
}

func تسلسليالسجلبايت(بيانات byte) {
	if !تسلسليجاهز {
		return
	}

	if بيانات == '\n' {
		Sتسلسليكتابةبايت('\r')
	}
	Sتسلسليكتابةبايت(uint8(بيانات))
}

func MEmergencyالسجلسلسلة(بيانات string) {
	for i := 0; i < len(بيانات); i++ {
		تسلسليالسجلبايت(بيانات[i])
	}
}

func MEmergencyالسجلhexadecimal8(بيانات uint8) {
	const digits = "0123456789ABCDEF"
	تسلسليالسجلبايت(digits[(بيانات>>4)&0x0F])
	تسلسليالسجلبايت(digits[بيانات&0x0F])
}

func MEmergencyالسجلunsignedinteger32(بيانات uint32) {
	MEmergencyالسجلhexadecimal8(uint8(بيانات >> 24))
	MEmergencyالسجلhexadecimal8(uint8(بيانات >> 16))
	MEmergencyالسجلhexadecimal8(uint8(بيانات >> 8))
	MEmergencyالسجلhexadecimal8(uint8(بيانات))
}

func (نفسه *Tطرفية) Mاطبع(argumentالقيمة ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var القيمة_2 interface{}

	for i, p := range argumentالقيمة {
		switch i {
		case 0:
			param, _ := p.(interface{})
			القيمة_2 = param
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

	نفسه.Mاطبعxy(القيمة_2, x, y)

}
func (نفسه *Tطرفية) Mاطبعxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		بيانات_2, _ := temporary_2.(string)
		نفسه.Mاطبعبايتxy(([]byte)(بيانات_2), x, y)
	case uint8:
		بيانات_2, _ := temporary_2.(uint8)
		نفسه.MHexadecimalاطبعxy(بيانات_2, x, y)
	case uint16:
		بيانات_2, _ := temporary_2.(uint16)
		نفسه.MUnsignedinteger16اطبعxy(بيانات_2, x, y)
	case uint32:
		بيانات_2, _ := temporary_2.(uint32)
		نفسه.MUnsignedinteger32اطبعxy(بيانات_2, x, y)
	case uint64:
		بيانات_2, _ := temporary_2.(uint64)
		نفسه.MUnsignedinteger64اطبعxy(بيانات_2, x, y)
	default:
		بيانات_2, _ := temporary_2.([]byte)
		نفسه.Mاطبعبايتxy(بيانات_2, x, y)
	}

}
func (نفسه *Tطرفية) Mاطبعبايتxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		نفسه.xالموضع = x
	}
	if y <= 999 {
		نفسه.yالموضع = y
	}

	خاصية := uint16(0x0F)
	تحديد := len(buffer)
	if تحديد > 4096 {
		تحديد = 4096
	}
	for i := 0; i < تحديد; i++ {
		تسلسليالسجلبايت(buffer[i])
		switch buffer[i] {
		case '\n':
			نفسه.yالموضع++
			نفسه.xالموضع = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*نفسه.yالموضع+نفسه.xالموضع)*2))) = خاصية<<8 | uint16(buffer[i])
			نفسه.xالموضع++
		}

		if نفسه.xالموضع >= 80 {
			نفسه.yالموضع++
			نفسه.xالموضع = 0
		}

		if نفسه.yالموضع >= 25 {
			for نفسه.yالموضع = 0; نفسه.yالموضع < 25; نفسه.yالموضع++ {
				for نفسه.xالموضع = 0; نفسه.xالموضع < 80; نفسه.xالموضع++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*نفسه.yالموضع+نفسه.xالموضع)*2))) = خاصية<<8 | ' '
				}
			}
			نفسه.xالموضع = 0
			نفسه.yالموضع = 0
		}

	}

}
func (نفسه *Tطرفية) MHexadecimalاطبع(مفتاح uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(مفتاح>>4)&0xF]
	buffer[1] = hex[مفتاح&0xF]
	نفسه.Mاطبع(buffer)
}
func (نفسه *Tطرفية) MHexadecimalاطبعxy(مفتاح uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(مفتاح>>4)&0xF]
	buffer[1] = hex[مفتاح&0xF]
	نفسه.Mاطبعxy(buffer, x, y)
}
func (نفسه *Tطرفية) MUnsignedinteger16اطبع(مفتاح uint16) {
	نفسه.MHexadecimalاطبع(uint8(مفتاح >> 8))
	نفسه.MHexadecimalاطبع(uint8(مفتاح))
}
func (نفسه *Tطرفية) MUnsignedinteger16اطبعxy(مفتاح uint16, x uint16, y uint16) {
	نفسه.MHexadecimalاطبعxy(uint8(مفتاح>>8), x, y)
	نفسه.MHexadecimalاطبعxy(uint8(مفتاح), x, y)
}
func (نفسه *Tطرفية) MUnsignedinteger32اطبع(بيانات uint32) {
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 24))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 16))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 8))
	نفسه.MHexadecimalاطبع(uint8(بيانات))
}
func (نفسه *Tطرفية) MUnsignedinteger32اطبعxy(بيانات uint32, x uint16, y uint16) {

	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>24), x+0, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>16), x+2, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>8), x+4, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات), x+6, y)
}
func (نفسه *Tطرفية) MUnsignedinteger64اطبع(بيانات uint64) {
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 56))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 48))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 40))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 32))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 24))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 16))
	نفسه.MHexadecimalاطبع(uint8(بيانات >> 8))
	نفسه.MHexadecimalاطبع(uint8(بيانات))
}
func (نفسه *Tطرفية) MUnsignedinteger64اطبعxy(بيانات uint64, x uint16, y uint16) {
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>56), x+0, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>48), x+2, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>40), x+4, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>32), x+6, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>24), x+8, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>16), x+10, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات>>8), x+12, y)
	نفسه.MHexadecimalاطبعxy(uint8(بيانات), x+14, y)
}
func Mاطبع(phyaddr uintptr, بيانات uint8, x uint32, y uint32)

func (نفسه *Tطرفية) Mاطبعhexadecimal(بيانات uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(بيانات>>4)&0xF]
	buffer[1] = hex[بيانات&0xF]

	Mاطبع(uintptr(fbphysaddress), buffer[0], x, y)
	Mاطبع(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (نفسه *Tطرفية) Mاطبعunsignedinteger16(بيانات uint16, x uint32, y uint32) {
	نفسه.Mاطبعhexadecimal(uint8(بيانات>>8), x+0*2, y)
	نفسه.Mاطبعhexadecimal(uint8(بيانات), x+2*2, y)
}

func (نفسه *Tطرفية) Mاطبعunsignedinteger32(بيانات uint32, x uint32, y uint32) {
	x = x * 2
	نفسه.Mاطبعhexadecimal(uint8(بيانات>>24), x+0*2, y)
	نفسه.Mاطبعhexadecimal(uint8(بيانات>>16), x+2*2, y)
	نفسه.Mاطبعhexadecimal(uint8(بيانات>>8), x+4*2, y)
	نفسه.Mاطبعhexadecimal(uint8(بيانات), x+6*2, y)
}

func (نفسه *Tطرفية) M테스트() {
}
