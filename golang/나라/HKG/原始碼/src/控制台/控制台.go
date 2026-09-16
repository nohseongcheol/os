/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 控制台

import . "unsafe"

const (
	fb寬度			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type T控制台 struct {
	x位置	uint16
	y位置	uint16
}

var 串列準備就緒 bool

func S串列init()
func S串列寫入位元組(資料 uint8)

func M串列記錄init() {
	S串列init()
	串列準備就緒 = true
}

func 串列記錄位元組(資料 byte) {
	if !串列準備就緒 {
		return
	}

	if 資料 == '\n' {
		S串列寫入位元組('\r')
	}
	S串列寫入位元組(uint8(資料))
}

func MEmergency記錄字串(資料 string) {
	for i := 0; i < len(資料); i++ {
		串列記錄位元組(資料[i])
	}
}

func MEmergency記錄hexadecimal8(資料 uint8) {
	const digits = "0123456789ABCDEF"
	串列記錄位元組(digits[(資料>>4)&0x0F])
	串列記錄位元組(digits[資料&0x0F])
}

func MEmergency記錄unsignedinteger32(資料 uint32) {
	MEmergency記錄hexadecimal8(uint8(資料 >> 24))
	MEmergency記錄hexadecimal8(uint8(資料 >> 16))
	MEmergency記錄hexadecimal8(uint8(資料 >> 8))
	MEmergency記錄hexadecimal8(uint8(資料))
}

func (self *T控制台) M列印(argument數值 ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var 數值_2 interface{}

	for i, p := range argument數值 {
		switch i {
		case 0:
			param, _ := p.(interface{})
			數值_2 = param
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

	self.M列印xy(數值_2, x, y)

}
func (self *T控制台) M列印xy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		資料_2, _ := temporary_2.(string)
		self.M列印位元組xy(([]byte)(資料_2), x, y)
	case uint8:
		資料_2, _ := temporary_2.(uint8)
		self.MHexadecimal列印xy(資料_2, x, y)
	case uint16:
		資料_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16列印xy(資料_2, x, y)
	case uint32:
		資料_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32列印xy(資料_2, x, y)
	case uint64:
		資料_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64列印xy(資料_2, x, y)
	default:
		資料_2, _ := temporary_2.([]byte)
		self.M列印位元組xy(資料_2, x, y)
	}

}
func (self *T控制台) M列印位元組xy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.x位置 = x
	}
	if y <= 999 {
		self.y位置 = y
	}

	屬性 := uint16(0x0F)
	限制 := len(buffer)
	if 限制 > 4096 {
		限制 = 4096
	}
	for i := 0; i < 限制; i++ {
		串列記錄位元組(buffer[i])
		switch buffer[i] {
		case '\n':
			self.y位置++
			self.x位置 = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y位置+self.x位置)*2))) = 屬性<<8 | uint16(buffer[i])
			self.x位置++
		}

		if self.x位置 >= 80 {
			self.y位置++
			self.x位置 = 0
		}

		if self.y位置 >= 25 {
			for self.y位置 = 0; self.y位置 < 25; self.y位置++ {
				for self.x位置 = 0; self.x位置 < 80; self.x位置++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y位置+self.x位置)*2))) = 屬性<<8 | ' '
				}
			}
			self.x位置 = 0
			self.y位置 = 0
		}

	}

}
func (self *T控制台) MHexadecimal列印(設定鍵 uint8) {
	buffer := []byte{'0', '0'}
	十六進位 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六進位[(設定鍵>>4)&0xF]
	buffer[1] = 十六進位[設定鍵&0xF]
	self.M列印(buffer)
}
func (self *T控制台) MHexadecimal列印xy(設定鍵 uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	十六進位 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六進位[(設定鍵>>4)&0xF]
	buffer[1] = 十六進位[設定鍵&0xF]
	self.M列印xy(buffer, x, y)
}
func (self *T控制台) MUnsignedinteger16列印(設定鍵 uint16) {
	self.MHexadecimal列印(uint8(設定鍵 >> 8))
	self.MHexadecimal列印(uint8(設定鍵))
}
func (self *T控制台) MUnsignedinteger16列印xy(設定鍵 uint16, x uint16, y uint16) {
	self.MHexadecimal列印xy(uint8(設定鍵>>8), x, y)
	self.MHexadecimal列印xy(uint8(設定鍵), x, y)
}
func (self *T控制台) MUnsignedinteger32列印(資料 uint32) {
	self.MHexadecimal列印(uint8(資料 >> 24))
	self.MHexadecimal列印(uint8(資料 >> 16))
	self.MHexadecimal列印(uint8(資料 >> 8))
	self.MHexadecimal列印(uint8(資料))
}
func (self *T控制台) MUnsignedinteger32列印xy(資料 uint32, x uint16, y uint16) {

	self.MHexadecimal列印xy(uint8(資料>>24), x+0, y)
	self.MHexadecimal列印xy(uint8(資料>>16), x+2, y)
	self.MHexadecimal列印xy(uint8(資料>>8), x+4, y)
	self.MHexadecimal列印xy(uint8(資料), x+6, y)
}
func (self *T控制台) MUnsignedinteger64列印(資料 uint64) {
	self.MHexadecimal列印(uint8(資料 >> 56))
	self.MHexadecimal列印(uint8(資料 >> 48))
	self.MHexadecimal列印(uint8(資料 >> 40))
	self.MHexadecimal列印(uint8(資料 >> 32))
	self.MHexadecimal列印(uint8(資料 >> 24))
	self.MHexadecimal列印(uint8(資料 >> 16))
	self.MHexadecimal列印(uint8(資料 >> 8))
	self.MHexadecimal列印(uint8(資料))
}
func (self *T控制台) MUnsignedinteger64列印xy(資料 uint64, x uint16, y uint16) {
	self.MHexadecimal列印xy(uint8(資料>>56), x+0, y)
	self.MHexadecimal列印xy(uint8(資料>>48), x+2, y)
	self.MHexadecimal列印xy(uint8(資料>>40), x+4, y)
	self.MHexadecimal列印xy(uint8(資料>>32), x+6, y)
	self.MHexadecimal列印xy(uint8(資料>>24), x+8, y)
	self.MHexadecimal列印xy(uint8(資料>>16), x+10, y)
	self.MHexadecimal列印xy(uint8(資料>>8), x+12, y)
	self.MHexadecimal列印xy(uint8(資料), x+14, y)
}
func M列印(phyaddr uintptr, 資料 uint8, x uint32, y uint32)

func (self *T控制台) M列印hexadecimal(資料 uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	十六進位 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六進位[(資料>>4)&0xF]
	buffer[1] = 十六進位[資料&0xF]

	M列印(uintptr(fbphysaddress), buffer[0], x, y)
	M列印(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *T控制台) M列印unsignedinteger16(資料 uint16, x uint32, y uint32) {
	self.M列印hexadecimal(uint8(資料>>8), x+0*2, y)
	self.M列印hexadecimal(uint8(資料), x+2*2, y)
}

func (self *T控制台) M列印unsignedinteger32(資料 uint32, x uint32, y uint32) {
	x = x * 2
	self.M列印hexadecimal(uint8(資料>>24), x+0*2, y)
	self.M列印hexadecimal(uint8(資料>>16), x+2*2, y)
	self.M列印hexadecimal(uint8(資料>>8), x+4*2, y)
	self.M列印hexadecimal(uint8(資料), x+6*2, y)
}

func (self *T控制台) M테스트() {
}
