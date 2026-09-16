/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package コンソール

import . "unsafe"

const (
	fbハバ			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type Tコンソール struct {
	xハイチ	uint16
	yハイチ	uint16
}

var チョクレツジュンビOK bool

func Sチョクレツinit()
func Sチョクレツカキコミバイト(データ uint8)

func Mチョクレツログinit() {
	Sチョクレツinit()
	チョクレツジュンビOK = true
}

func チョクレツログバイト(データ byte) {
	if !チョクレツジュンビOK {
		return
	}

	if データ == '\n' {
		Sチョクレツカキコミバイト('\r')
	}
	Sチョクレツカキコミバイト(uint8(データ))
}

func MEmergencyログモジレツ(データ string) {
	for i := 0; i < len(データ); i++ {
		チョクレツログバイト(データ[i])
	}
}

func MEmergencyログhexadecimal8(データ uint8) {
	const digits = "0123456789ABCDEF"
	チョクレツログバイト(digits[(データ>>4)&0x0F])
	チョクレツログバイト(digits[データ&0x0F])
}

func MEmergencyログunsignedinteger32(データ uint32) {
	MEmergencyログhexadecimal8(uint8(データ >> 24))
	MEmergencyログhexadecimal8(uint8(データ >> 16))
	MEmergencyログhexadecimal8(uint8(データ >> 8))
	MEmergencyログhexadecimal8(uint8(データ))
}

func (self *Tコンソール) Mインサツ(argumentアタイ ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var アタイ_2 interface{}

	for i, p := range argumentアタイ {
		switch i {
		case 0:
			param, _ := p.(interface{})
			アタイ_2 = param
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

	self.Mインサツxy(アタイ_2, x, y)

}
func (self *Tコンソール) Mインサツxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		データ_2, _ := temporary_2.(string)
		self.Mインサツバイトxy(([]byte)(データ_2), x, y)
	case uint8:
		データ_2, _ := temporary_2.(uint8)
		self.MHexadecimalインサツxy(データ_2, x, y)
	case uint16:
		データ_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16インサツxy(データ_2, x, y)
	case uint32:
		データ_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32インサツxy(データ_2, x, y)
	case uint64:
		データ_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64インサツxy(データ_2, x, y)
	default:
		データ_2, _ := temporary_2.([]byte)
		self.Mインサツバイトxy(データ_2, x, y)
	}

}
func (self *Tコンソール) Mインサツバイトxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xハイチ = x
	}
	if y <= 999 {
		self.yハイチ = y
	}

	ゾクセイ := uint16(0x0F)
	セイゲン := len(buffer)
	if セイゲン > 4096 {
		セイゲン = 4096
	}
	for i := 0; i < セイゲン; i++ {
		チョクレツログバイト(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yハイチ++
			self.xハイチ = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yハイチ+self.xハイチ)*2))) = ゾクセイ<<8 | uint16(buffer[i])
			self.xハイチ++
		}

		if self.xハイチ >= 80 {
			self.yハイチ++
			self.xハイチ = 0
		}

		if self.yハイチ >= 25 {
			for self.yハイチ = 0; self.yハイチ < 25; self.yハイチ++ {
				for self.xハイチ = 0; self.xハイチ < 80; self.xハイチ++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yハイチ+self.xハイチ)*2))) = ゾクセイ<<8 | ' '
				}
			}
			self.xハイチ = 0
			self.yハイチ = 0
		}

	}

}
func (self *Tコンソール) MHexadecimalインサツ(カギ uint8) {
	buffer := []byte{'0', '0'}
	アタイ16ススム := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = アタイ16ススム[(カギ>>4)&0xF]
	buffer[1] = アタイ16ススム[カギ&0xF]
	self.Mインサツ(buffer)
}
func (self *Tコンソール) MHexadecimalインサツxy(カギ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	アタイ16ススム := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = アタイ16ススム[(カギ>>4)&0xF]
	buffer[1] = アタイ16ススム[カギ&0xF]
	self.Mインサツxy(buffer, x, y)
}
func (self *Tコンソール) MUnsignedinteger16インサツ(カギ uint16) {
	self.MHexadecimalインサツ(uint8(カギ >> 8))
	self.MHexadecimalインサツ(uint8(カギ))
}
func (self *Tコンソール) MUnsignedinteger16インサツxy(カギ uint16, x uint16, y uint16) {
	self.MHexadecimalインサツxy(uint8(カギ>>8), x, y)
	self.MHexadecimalインサツxy(uint8(カギ), x, y)
}
func (self *Tコンソール) MUnsignedinteger32インサツ(データ uint32) {
	self.MHexadecimalインサツ(uint8(データ >> 24))
	self.MHexadecimalインサツ(uint8(データ >> 16))
	self.MHexadecimalインサツ(uint8(データ >> 8))
	self.MHexadecimalインサツ(uint8(データ))
}
func (self *Tコンソール) MUnsignedinteger32インサツxy(データ uint32, x uint16, y uint16) {

	self.MHexadecimalインサツxy(uint8(データ>>24), x+0, y)
	self.MHexadecimalインサツxy(uint8(データ>>16), x+2, y)
	self.MHexadecimalインサツxy(uint8(データ>>8), x+4, y)
	self.MHexadecimalインサツxy(uint8(データ), x+6, y)
}
func (self *Tコンソール) MUnsignedinteger64インサツ(データ uint64) {
	self.MHexadecimalインサツ(uint8(データ >> 56))
	self.MHexadecimalインサツ(uint8(データ >> 48))
	self.MHexadecimalインサツ(uint8(データ >> 40))
	self.MHexadecimalインサツ(uint8(データ >> 32))
	self.MHexadecimalインサツ(uint8(データ >> 24))
	self.MHexadecimalインサツ(uint8(データ >> 16))
	self.MHexadecimalインサツ(uint8(データ >> 8))
	self.MHexadecimalインサツ(uint8(データ))
}
func (self *Tコンソール) MUnsignedinteger64インサツxy(データ uint64, x uint16, y uint16) {
	self.MHexadecimalインサツxy(uint8(データ>>56), x+0, y)
	self.MHexadecimalインサツxy(uint8(データ>>48), x+2, y)
	self.MHexadecimalインサツxy(uint8(データ>>40), x+4, y)
	self.MHexadecimalインサツxy(uint8(データ>>32), x+6, y)
	self.MHexadecimalインサツxy(uint8(データ>>24), x+8, y)
	self.MHexadecimalインサツxy(uint8(データ>>16), x+10, y)
	self.MHexadecimalインサツxy(uint8(データ>>8), x+12, y)
	self.MHexadecimalインサツxy(uint8(データ), x+14, y)
}
func Mインサツ(phyaddr uintptr, データ uint8, x uint32, y uint32)

func (self *Tコンソール) Mインサツhexadecimal(データ uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	アタイ16ススム := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = アタイ16ススム[(データ>>4)&0xF]
	buffer[1] = アタイ16ススム[データ&0xF]

	Mインサツ(uintptr(fbphysaddress), buffer[0], x, y)
	Mインサツ(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *Tコンソール) Mインサツunsignedinteger16(データ uint16, x uint32, y uint32) {
	self.Mインサツhexadecimal(uint8(データ>>8), x+0*2, y)
	self.Mインサツhexadecimal(uint8(データ), x+2*2, y)
}

func (self *Tコンソール) Mインサツunsignedinteger32(データ uint32, x uint32, y uint32) {
	x = x * 2
	self.Mインサツhexadecimal(uint8(データ>>24), x+0*2, y)
	self.Mインサツhexadecimal(uint8(データ>>16), x+2*2, y)
	self.Mインサツhexadecimal(uint8(データ>>8), x+4*2, y)
	self.Mインサツhexadecimal(uint8(データ), x+6*2, y)
}

func (self *Tコンソール) M테스트() {
}
