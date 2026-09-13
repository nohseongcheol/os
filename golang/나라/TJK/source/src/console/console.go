package console

import . "unsafe"

const (
	fbwidth			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xposition	uint16
	yposition	uint16
}

var serialready bool

func Serialinit()
func SerialНавиштанbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialready = true
}

func seriallogbyte(data byte) {
	if !serialready {
		return
	}

	if data == '\n' {
		SerialНавиштанbyte('\r')
	}
	SerialНавиштанbyte(uint8(data))
}

func MEmergencylogstring(data string) {
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

func (self *TConsole) MЧопкардан(argumentvalue ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var value_2 interface{}

	for i, p := range argumentvalue {
		switch i {
		case 0:
			param, _ := p.(interface{})
			value_2 = param
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

	self.MЧопкарданxy(value_2, x, y)

}
func (self *TConsole) MЧопкарданxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MЧопкарданbytesxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalЧопкарданxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Чопкарданxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Чопкарданxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Чопкарданxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MЧопкарданbytesxy(data_2, x, y)
	}

}
func (self *TConsole) MЧопкарданbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xposition = x
	}
	if y <= 999 {
		self.yposition = y
	}

	attribute := uint16(0x0F)
	limit := len(buffer)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yposition++
			self.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribute<<8 | uint16(buffer[i])
			self.xposition++
		}

		if self.xposition >= 80 {
			self.yposition++
			self.xposition = 0
		}

		if self.yposition >= 25 {
			for self.yposition = 0; self.yposition < 25; self.yposition++ {
				for self.xposition = 0; self.xposition < 80; self.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribute<<8 | ' '
				}
			}
			self.xposition = 0
			self.yposition = 0
		}

	}

}
func (self *TConsole) MHexadecimalЧопкардан(key uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.MЧопкардан(buffer)
}
func (self *TConsole) MHexadecimalЧопкарданxy(key uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(key>>4)&0xF]
	buffer[1] = hex[key&0xF]
	self.MЧопкарданxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Чопкардан(key uint16) {
	self.MHexadecimalЧопкардан(uint8(key >> 8))
	self.MHexadecimalЧопкардан(uint8(key))
}
func (self *TConsole) MUnsignedinteger16Чопкарданxy(key uint16, x uint16, y uint16) {
	self.MHexadecimalЧопкарданxy(uint8(key>>8), x, y)
	self.MHexadecimalЧопкарданxy(uint8(key), x, y)
}
func (self *TConsole) MUnsignedinteger32Чопкардан(data uint32) {
	self.MHexadecimalЧопкардан(uint8(data >> 24))
	self.MHexadecimalЧопкардан(uint8(data >> 16))
	self.MHexadecimalЧопкардан(uint8(data >> 8))
	self.MHexadecimalЧопкардан(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Чопкарданxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalЧопкарданxy(uint8(data>>24), x+0, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>16), x+2, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>8), x+4, y)
	self.MHexadecimalЧопкарданxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Чопкардан(data uint64) {
	self.MHexadecimalЧопкардан(uint8(data >> 56))
	self.MHexadecimalЧопкардан(uint8(data >> 48))
	self.MHexadecimalЧопкардан(uint8(data >> 40))
	self.MHexadecimalЧопкардан(uint8(data >> 32))
	self.MHexadecimalЧопкардан(uint8(data >> 24))
	self.MHexadecimalЧопкардан(uint8(data >> 16))
	self.MHexadecimalЧопкардан(uint8(data >> 8))
	self.MHexadecimalЧопкардан(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Чопкарданxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalЧопкарданxy(uint8(data>>56), x+0, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>48), x+2, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>40), x+4, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>32), x+6, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>24), x+8, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>16), x+10, y)
	self.MHexadecimalЧопкарданxy(uint8(data>>8), x+12, y)
	self.MHexadecimalЧопкарданxy(uint8(data), x+14, y)
}
func MЧопкардан(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MЧопкарданhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MЧопкардан(uintptr(fbphysaddress), buffer[0], x, y)
	MЧопкардан(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MЧопкарданunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MЧопкарданhexadecimal(uint8(data>>8), x+0*2, y)
	self.MЧопкарданhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MЧопкарданunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MЧопкарданhexadecimal(uint8(data>>24), x+0*2, y)
	self.MЧопкарданhexadecimal(uint8(data>>16), x+2*2, y)
	self.MЧопкарданhexadecimal(uint8(data>>8), x+4*2, y)
	self.MЧопкарданhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
