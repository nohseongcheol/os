package 控制台

import . "unsafe"

const (
	fb宽度			= 80
	fb高度			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type T控制台 struct {
	x位置	uint16
	y位置	uint16
}

var 串行就绪 bool

func S串行init()
func S串行写入字节(数据 uint8)

func M串行日志init() {
	S串行init()
	串行就绪 = true
}

func 串行日志字节(数据 byte) {
	if !串行就绪 {
		return
	}

	if 数据 == '\n' {
		S串行写入字节('\r')
	}
	S串行写入字节(uint8(数据))
}

func MEmergency日志字符串(数据 string) {
	for i := 0; i < len(数据); i++ {
		串行日志字节(数据[i])
	}
}

func MEmergency日志hexadecimal8(数据 uint8) {
	const digits = "0123456789ABCDEF"
	串行日志字节(digits[(数据>>4)&0x0F])
	串行日志字节(digits[数据&0x0F])
}

func MEmergency日志unsignedinteger32(数据 uint32) {
	MEmergency日志hexadecimal8(uint8(数据 >> 24))
	MEmergency日志hexadecimal8(uint8(数据 >> 16))
	MEmergency日志hexadecimal8(uint8(数据 >> 8))
	MEmergency日志hexadecimal8(uint8(数据))
}

func (self *T控制台) M打印(argument值 ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var 值_2 interface{}

	for i, p := range argument值 {
		switch i {
		case 0:
			param, _ := p.(interface{})
			值_2 = param
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

	self.M打印xy(值_2, x, y)

}
func (self *T控制台) M打印xy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		数据_2, _ := temporary_2.(string)
		self.M打印字节xy(([]byte)(数据_2), x, y)
	case uint8:
		数据_2, _ := temporary_2.(uint8)
		self.MHexadecimal打印xy(数据_2, x, y)
	case uint16:
		数据_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16打印xy(数据_2, x, y)
	case uint32:
		数据_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32打印xy(数据_2, x, y)
	case uint64:
		数据_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64打印xy(数据_2, x, y)
	default:
		数据_2, _ := temporary_2.([]byte)
		self.M打印字节xy(数据_2, x, y)
	}

}
func (self *T控制台) M打印字节xy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.x位置 = x
	}
	if y <= 999 {
		self.y位置 = y
	}

	属性 := uint16(0x0F)
	限定 := len(buffer)
	if 限定 > 4096 {
		限定 = 4096
	}
	for i := 0; i < 限定; i++ {
		串行日志字节(buffer[i])
		switch buffer[i] {
		case '\n':
			self.y位置++
			self.x位置 = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y位置+self.x位置)*2))) = 属性<<8 | uint16(buffer[i])
			self.x位置++
		}

		if self.x位置 >= 80 {
			self.y位置++
			self.x位置 = 0
		}

		if self.y位置 >= 25 {
			for self.y位置 = 0; self.y位置 < 25; self.y位置++ {
				for self.x位置 = 0; self.x位置 < 80; self.x位置++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.y位置+self.x位置)*2))) = 属性<<8 | ' '
				}
			}
			self.x位置 = 0
			self.y位置 = 0
		}

	}

}
func (self *T控制台) MHexadecimal打印(关键 uint8) {
	buffer := []byte{'0', '0'}
	十六进制 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六进制[(关键>>4)&0xF]
	buffer[1] = 十六进制[关键&0xF]
	self.M打印(buffer)
}
func (self *T控制台) MHexadecimal打印xy(关键 uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	十六进制 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六进制[(关键>>4)&0xF]
	buffer[1] = 十六进制[关键&0xF]
	self.M打印xy(buffer, x, y)
}
func (self *T控制台) MUnsignedinteger16打印(关键 uint16) {
	self.MHexadecimal打印(uint8(关键 >> 8))
	self.MHexadecimal打印(uint8(关键))
}
func (self *T控制台) MUnsignedinteger16打印xy(关键 uint16, x uint16, y uint16) {
	self.MHexadecimal打印xy(uint8(关键>>8), x, y)
	self.MHexadecimal打印xy(uint8(关键), x, y)
}
func (self *T控制台) MUnsignedinteger32打印(数据 uint32) {
	self.MHexadecimal打印(uint8(数据 >> 24))
	self.MHexadecimal打印(uint8(数据 >> 16))
	self.MHexadecimal打印(uint8(数据 >> 8))
	self.MHexadecimal打印(uint8(数据))
}
func (self *T控制台) MUnsignedinteger32打印xy(数据 uint32, x uint16, y uint16) {

	self.MHexadecimal打印xy(uint8(数据>>24), x+0, y)
	self.MHexadecimal打印xy(uint8(数据>>16), x+2, y)
	self.MHexadecimal打印xy(uint8(数据>>8), x+4, y)
	self.MHexadecimal打印xy(uint8(数据), x+6, y)
}
func (self *T控制台) MUnsignedinteger64打印(数据 uint64) {
	self.MHexadecimal打印(uint8(数据 >> 56))
	self.MHexadecimal打印(uint8(数据 >> 48))
	self.MHexadecimal打印(uint8(数据 >> 40))
	self.MHexadecimal打印(uint8(数据 >> 32))
	self.MHexadecimal打印(uint8(数据 >> 24))
	self.MHexadecimal打印(uint8(数据 >> 16))
	self.MHexadecimal打印(uint8(数据 >> 8))
	self.MHexadecimal打印(uint8(数据))
}
func (self *T控制台) MUnsignedinteger64打印xy(数据 uint64, x uint16, y uint16) {
	self.MHexadecimal打印xy(uint8(数据>>56), x+0, y)
	self.MHexadecimal打印xy(uint8(数据>>48), x+2, y)
	self.MHexadecimal打印xy(uint8(数据>>40), x+4, y)
	self.MHexadecimal打印xy(uint8(数据>>32), x+6, y)
	self.MHexadecimal打印xy(uint8(数据>>24), x+8, y)
	self.MHexadecimal打印xy(uint8(数据>>16), x+10, y)
	self.MHexadecimal打印xy(uint8(数据>>8), x+12, y)
	self.MHexadecimal打印xy(uint8(数据), x+14, y)
}
func M打印(phyaddr uintptr, 数据 uint8, x uint32, y uint32)

func (self *T控制台) M打印hexadecimal(数据 uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	十六进制 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = 十六进制[(数据>>4)&0xF]
	buffer[1] = 十六进制[数据&0xF]

	M打印(uintptr(fbphysaddress), buffer[0], x, y)
	M打印(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *T控制台) M打印unsignedinteger16(数据 uint16, x uint32, y uint32) {
	self.M打印hexadecimal(uint8(数据>>8), x+0*2, y)
	self.M打印hexadecimal(uint8(数据), x+2*2, y)
}

func (self *T控制台) M打印unsignedinteger32(数据 uint32, x uint32, y uint32) {
	x = x * 2
	self.M打印hexadecimal(uint8(数据>>24), x+0*2, y)
	self.M打印hexadecimal(uint8(数据>>16), x+2*2, y)
	self.M打印hexadecimal(uint8(数据>>8), x+4*2, y)
	self.M打印hexadecimal(uint8(数据), x+6*2, y)
}

func (self *T控制台) M테스트() {
}
