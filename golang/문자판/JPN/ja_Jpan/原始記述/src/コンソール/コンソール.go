/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package コンソール

import . "unsafe"

const (
	fb幅			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type Tコンソール struct {
	x配置	uint16
	y配置	uint16
}

var 直列準備OK bool

func S直列init()
func S直列書込みバイト(データ uint8)

func M直列ログinit() {
	S直列init()
	直列準備OK = true
}

func 直列ログバイト(データ byte) {
	if !直列準備OK {
		return
	}

	if データ == '\n' {
		S直列書込みバイト('\r')
	}
	S直列書込みバイト(uint8(データ))
}

func MEmergencyログ文字列(データ string) {
	for i := 0; i < len(データ); i++ {
		直列ログバイト(データ[i])
	}
}

func MEmergencyログhexadecimal8(データ uint8) {
	const digits = "0123456789ABCDEF"
	直列ログバイト(digits[(データ>>4)&0x0F])
	直列ログバイト(digits[データ&0x0F])
}

func MEmergencyログunsignedinteger32(データ uint32) {
	MEmergencyログhexadecimal8(uint8(データ >> 24))
	MEmergencyログhexadecimal8(uint8(データ >> 16))
	MEmergencyログhexadecimal8(uint8(データ >> 8))
	MEmergencyログhexadecimal8(uint8(データ))
}

func (self *Tコンソール) M印刷(argument値 ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var 値_2 interface{}

	for i, p := range argument値 {
		switch i {
		case 0:
			param, _ := p.(interface{})
			値_2 = param
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

	self.M印刷xy(値_2, x, y)

}
func (self *Tコンソール) M印刷xy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		データ_2, _ := temporary_2.(string)
		self.M印刷バイトxy(([]byte)(データ_2), x, y)
	case uint8:
		データ_2, _ := temporary_2.(uint8)
		self.MHexadecimal印刷xy(データ_2, x, y)
	case uint16:
		データ_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16印刷xy(データ_2, x, y)
	case uint32:
		データ_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32印刷xy(データ_2, x, y)
	case uint64:
		データ_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64印刷xy(データ_2, x, y)
	default:
		データ_2, _ := temporary_2.([]byte)
		self.M印刷バイトxy(データ_2, x, y)
	}

}
func (self *Tコンソール) M印刷バイトxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.x配置 = x
	}
	if y <= 999 {
		self.y配置 = y
	}

	属性 := uint16(0x0F)
	制限 := len(buffer)
	if 制限 > 4096 {
		制限 = 4096
	}
	for i := 0; i < 制限; i++ {
		直列ログバイト(buffer[i])
		switch buffer[i] {
		case '\n':
			self.y配置++
			self.x配置 = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y配置+self.x配置)*2))) = 属性<<8 | uint16(buffer[i])
			self.x配置++
		}

		if self.x配置 >= 80 {
			self.y配置++
			self.x配置 = 0
		}

		if self.y配置 >= 25 {
			for self.y配置 = 0; self.y配置 < 25; self.y配置++ {
				for self.x配置 = 0; self.x配置 < 80; self.x配置++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y配置+self.x配置)*2))) = 属性<<8 | ' '
				}
			}
			self.x配置 = 0
			self.y配置 = 0
		}

	}

}
func (self *Tコンソール) MHexadecimal印刷(鍵 uint8) {
	buffer := []byte{'0', '0'}
	値16進 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 値16進[(鍵>>4)&0xF]
	buffer[1] = 値16進[鍵&0xF]
	self.M印刷(buffer)
}
func (self *Tコンソール) MHexadecimal印刷xy(鍵 uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	値16進 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 値16進[(鍵>>4)&0xF]
	buffer[1] = 値16進[鍵&0xF]
	self.M印刷xy(buffer, x, y)
}
func (self *Tコンソール) MUnsignedinteger16印刷(鍵 uint16) {
	self.MHexadecimal印刷(uint8(鍵 >> 8))
	self.MHexadecimal印刷(uint8(鍵))
}
func (self *Tコンソール) MUnsignedinteger16印刷xy(鍵 uint16, x uint16, y uint16) {
	self.MHexadecimal印刷xy(uint8(鍵>>8), x, y)
	self.MHexadecimal印刷xy(uint8(鍵), x, y)
}
func (self *Tコンソール) MUnsignedinteger32印刷(データ uint32) {
	self.MHexadecimal印刷(uint8(データ >> 24))
	self.MHexadecimal印刷(uint8(データ >> 16))
	self.MHexadecimal印刷(uint8(データ >> 8))
	self.MHexadecimal印刷(uint8(データ))
}
func (self *Tコンソール) MUnsignedinteger32印刷xy(データ uint32, x uint16, y uint16) {

	self.MHexadecimal印刷xy(uint8(データ>>24), x+0, y)
	self.MHexadecimal印刷xy(uint8(データ>>16), x+2, y)
	self.MHexadecimal印刷xy(uint8(データ>>8), x+4, y)
	self.MHexadecimal印刷xy(uint8(データ), x+6, y)
}
func (self *Tコンソール) MUnsignedinteger64印刷(データ uint64) {
	self.MHexadecimal印刷(uint8(データ >> 56))
	self.MHexadecimal印刷(uint8(データ >> 48))
	self.MHexadecimal印刷(uint8(データ >> 40))
	self.MHexadecimal印刷(uint8(データ >> 32))
	self.MHexadecimal印刷(uint8(データ >> 24))
	self.MHexadecimal印刷(uint8(データ >> 16))
	self.MHexadecimal印刷(uint8(データ >> 8))
	self.MHexadecimal印刷(uint8(データ))
}
func (self *Tコンソール) MUnsignedinteger64印刷xy(データ uint64, x uint16, y uint16) {
	self.MHexadecimal印刷xy(uint8(データ>>56), x+0, y)
	self.MHexadecimal印刷xy(uint8(データ>>48), x+2, y)
	self.MHexadecimal印刷xy(uint8(データ>>40), x+4, y)
	self.MHexadecimal印刷xy(uint8(データ>>32), x+6, y)
	self.MHexadecimal印刷xy(uint8(データ>>24), x+8, y)
	self.MHexadecimal印刷xy(uint8(データ>>16), x+10, y)
	self.MHexadecimal印刷xy(uint8(データ>>8), x+12, y)
	self.MHexadecimal印刷xy(uint8(データ), x+14, y)
}
func M印刷(phyaddr uintptr, データ uint8, x uint32, y uint32)

func (self *Tコンソール) M印刷hexadecimal(データ uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	値16進 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 値16進[(データ>>4)&0xF]
	buffer[1] = 値16進[データ&0xF]

	M印刷(uintptr(fbphysaddress), buffer[0], x, y)
	M印刷(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *Tコンソール) M印刷unsignedinteger16(データ uint16, x uint32, y uint32) {
	self.M印刷hexadecimal(uint8(データ>>8), x+0*2, y)
	self.M印刷hexadecimal(uint8(データ), x+2*2, y)
}

func (self *Tコンソール) M印刷unsignedinteger32(データ uint32, x uint32, y uint32) {
	x = x * 2
	self.M印刷hexadecimal(uint8(データ>>24), x+0*2, y)
	self.M印刷hexadecimal(uint8(データ>>16), x+2*2, y)
	self.M印刷hexadecimal(uint8(データ>>8), x+4*2, y)
	self.M印刷hexadecimal(uint8(データ), x+6*2, y)
}

func (self *Tコンソール) M테스트() {
}
