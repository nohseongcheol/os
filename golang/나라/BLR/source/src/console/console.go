package console

import . "unsafe"

const (
	fbШырыня		= 80
	fbВышыня		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xПазіцыя	uint16
	yПазіцыя	uint16
}

var serialГатова bool

func Serialinit()
func SerialЗапісbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialГатова = true
}

func seriallogbyte(data byte) {
	if !serialГатова {
		return
	}

	if data == '\n' {
		SerialЗапісbyte('\r')
	}
	SerialЗапісbyte(uint8(data))
}

func MEmergencylogРадок(data string) {
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

func (self *TConsole) MДрукаваць(argumentЗначэнне ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var значэнне_2 interface{}

	for i, p := range argumentЗначэнне {
		switch i {
		case 0:
			param, _ := p.(interface{})
			значэнне_2 = param
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

	self.MДрукавацьxy(значэнне_2, x, y)

}
func (self *TConsole) MДрукавацьxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MДрукавацьБайтаўxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalДрукавацьxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Друкавацьxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Друкавацьxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Друкавацьxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MДрукавацьБайтаўxy(data_2, x, y)
	}

}
func (self *TConsole) MДрукавацьБайтаўxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xПазіцыя = x
	}
	if y <= 999 {
		self.yПазіцыя = y
	}

	атрыбут := uint16(0x0F)
	абмежаваць := len(buffer)
	if абмежаваць > 4096 {
		абмежаваць = 4096
	}
	for i := 0; i < абмежаваць; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yПазіцыя++
			self.xПазіцыя = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yПазіцыя+self.xПазіцыя)*2))) = атрыбут<<8 | uint16(buffer[i])
			self.xПазіцыя++
		}

		if self.xПазіцыя >= 80 {
			self.yПазіцыя++
			self.xПазіцыя = 0
		}

		if self.yПазіцыя >= 25 {
			for self.yПазіцыя = 0; self.yПазіцыя < 25; self.yПазіцыя++ {
				for self.xПазіцыя = 0; self.xПазіцыя < 80; self.xПазіцыя++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yПазіцыя+self.xПазіцыя)*2))) = атрыбут<<8 | ' '
				}
			}
			self.xПазіцыя = 0
			self.yПазіцыя = 0
		}

	}

}
func (self *TConsole) MHexadecimalДрукаваць(ключ uint8) {
	buffer := []byte{'0', '0'}
	шаснаццатковы := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шаснаццатковы[(ключ>>4)&0xF]
	buffer[1] = шаснаццатковы[ключ&0xF]
	self.MДрукаваць(buffer)
}
func (self *TConsole) MHexadecimalДрукавацьxy(ключ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	шаснаццатковы := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шаснаццатковы[(ключ>>4)&0xF]
	buffer[1] = шаснаццатковы[ключ&0xF]
	self.MДрукавацьxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Друкаваць(ключ uint16) {
	self.MHexadecimalДрукаваць(uint8(ключ >> 8))
	self.MHexadecimalДрукаваць(uint8(ключ))
}
func (self *TConsole) MUnsignedinteger16Друкавацьxy(ключ uint16, x uint16, y uint16) {
	self.MHexadecimalДрукавацьxy(uint8(ключ>>8), x, y)
	self.MHexadecimalДрукавацьxy(uint8(ключ), x, y)
}
func (self *TConsole) MUnsignedinteger32Друкаваць(data uint32) {
	self.MHexadecimalДрукаваць(uint8(data >> 24))
	self.MHexadecimalДрукаваць(uint8(data >> 16))
	self.MHexadecimalДрукаваць(uint8(data >> 8))
	self.MHexadecimalДрукаваць(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Друкавацьxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalДрукавацьxy(uint8(data>>24), x+0, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>16), x+2, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>8), x+4, y)
	self.MHexadecimalДрукавацьxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Друкаваць(data uint64) {
	self.MHexadecimalДрукаваць(uint8(data >> 56))
	self.MHexadecimalДрукаваць(uint8(data >> 48))
	self.MHexadecimalДрукаваць(uint8(data >> 40))
	self.MHexadecimalДрукаваць(uint8(data >> 32))
	self.MHexadecimalДрукаваць(uint8(data >> 24))
	self.MHexadecimalДрукаваць(uint8(data >> 16))
	self.MHexadecimalДрукаваць(uint8(data >> 8))
	self.MHexadecimalДрукаваць(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Друкавацьxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalДрукавацьxy(uint8(data>>56), x+0, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>48), x+2, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>40), x+4, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>32), x+6, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>24), x+8, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>16), x+10, y)
	self.MHexadecimalДрукавацьxy(uint8(data>>8), x+12, y)
	self.MHexadecimalДрукавацьxy(uint8(data), x+14, y)
}
func MДрукаваць(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MДрукавацьhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	шаснаццатковы := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шаснаццатковы[(data>>4)&0xF]
	buffer[1] = шаснаццатковы[data&0xF]

	MДрукаваць(uintptr(fbphysaddress), buffer[0], x, y)
	MДрукаваць(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MДрукавацьunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MДрукавацьhexadecimal(uint8(data>>8), x+0*2, y)
	self.MДрукавацьhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MДрукавацьunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MДрукавацьhexadecimal(uint8(data>>24), x+0*2, y)
	self.MДрукавацьhexadecimal(uint8(data>>16), x+2*2, y)
	self.MДрукавацьhexadecimal(uint8(data>>8), x+4*2, y)
	self.MДрукавацьhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
