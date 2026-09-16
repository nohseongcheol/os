/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbስፋት			= 80
	fbእርዝመት			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xአካባቢ	uint16
	yአካባቢ	uint16
}

var serialዝግጁ bool

func Serialinit()
func Serialመጻፊያbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialዝግጁ = true
}

func seriallogbyte(data byte) {
	if !serialዝግጁ {
		return
	}

	if data == '\n' {
		Serialመጻፊያbyte('\r')
	}
	Serialመጻፊያbyte(uint8(data))
}

func MEmergencylogሐረግ(data string) {
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

func (self *TConsole) Mማተሚያ(argumentዋጋ ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var ዋጋ_2 interface{}

	for i, p := range argumentዋጋ {
		switch i {
		case 0:
			param, _ := p.(interface{})
			ዋጋ_2 = param
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

	self.Mማተሚያxy(ዋጋ_2, x, y)

}
func (self *TConsole) Mማተሚያxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.Mማተሚያባይትስxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalማተሚያxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16ማተሚያxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32ማተሚያxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64ማተሚያxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.Mማተሚያባይትስxy(data_2, x, y)
	}

}
func (self *TConsole) Mማተሚያባይትስxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xአካባቢ = x
	}
	if y <= 999 {
		self.yአካባቢ = y
	}

	መለያ := uint16(0x0F)
	ገደብ := len(buffer)
	if ገደብ > 4096 {
		ገደብ = 4096
	}
	for i := 0; i < ገደብ; i++ {
		seriallogbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yአካባቢ++
			self.xአካባቢ = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yአካባቢ+self.xአካባቢ)*2))) = መለያ<<8 | uint16(buffer[i])
			self.xአካባቢ++
		}

		if self.xአካባቢ >= 80 {
			self.yአካባቢ++
			self.xአካባቢ = 0
		}

		if self.yአካባቢ >= 25 {
			for self.yአካባቢ = 0; self.yአካባቢ < 25; self.yአካባቢ++ {
				for self.xአካባቢ = 0; self.xአካባቢ < 80; self.xአካባቢ++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yአካባቢ+self.xአካባቢ)*2))) = መለያ<<8 | ' '
				}
			}
			self.xአካባቢ = 0
			self.yአካባቢ = 0
		}

	}

}
func (self *TConsole) MHexadecimalማተሚያ(ቁልፍ uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ቁልፍ>>4)&0xF]
	buffer[1] = hex[ቁልፍ&0xF]
	self.Mማተሚያ(buffer)
}
func (self *TConsole) MHexadecimalማተሚያxy(ቁልፍ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(ቁልፍ>>4)&0xF]
	buffer[1] = hex[ቁልፍ&0xF]
	self.Mማተሚያxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16ማተሚያ(ቁልፍ uint16) {
	self.MHexadecimalማተሚያ(uint8(ቁልፍ >> 8))
	self.MHexadecimalማተሚያ(uint8(ቁልፍ))
}
func (self *TConsole) MUnsignedinteger16ማተሚያxy(ቁልፍ uint16, x uint16, y uint16) {
	self.MHexadecimalማተሚያxy(uint8(ቁልፍ>>8), x, y)
	self.MHexadecimalማተሚያxy(uint8(ቁልፍ), x, y)
}
func (self *TConsole) MUnsignedinteger32ማተሚያ(data uint32) {
	self.MHexadecimalማተሚያ(uint8(data >> 24))
	self.MHexadecimalማተሚያ(uint8(data >> 16))
	self.MHexadecimalማተሚያ(uint8(data >> 8))
	self.MHexadecimalማተሚያ(uint8(data))
}
func (self *TConsole) MUnsignedinteger32ማተሚያxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalማተሚያxy(uint8(data>>24), x+0, y)
	self.MHexadecimalማተሚያxy(uint8(data>>16), x+2, y)
	self.MHexadecimalማተሚያxy(uint8(data>>8), x+4, y)
	self.MHexadecimalማተሚያxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64ማተሚያ(data uint64) {
	self.MHexadecimalማተሚያ(uint8(data >> 56))
	self.MHexadecimalማተሚያ(uint8(data >> 48))
	self.MHexadecimalማተሚያ(uint8(data >> 40))
	self.MHexadecimalማተሚያ(uint8(data >> 32))
	self.MHexadecimalማተሚያ(uint8(data >> 24))
	self.MHexadecimalማተሚያ(uint8(data >> 16))
	self.MHexadecimalማተሚያ(uint8(data >> 8))
	self.MHexadecimalማተሚያ(uint8(data))
}
func (self *TConsole) MUnsignedinteger64ማተሚያxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalማተሚያxy(uint8(data>>56), x+0, y)
	self.MHexadecimalማተሚያxy(uint8(data>>48), x+2, y)
	self.MHexadecimalማተሚያxy(uint8(data>>40), x+4, y)
	self.MHexadecimalማተሚያxy(uint8(data>>32), x+6, y)
	self.MHexadecimalማተሚያxy(uint8(data>>24), x+8, y)
	self.MHexadecimalማተሚያxy(uint8(data>>16), x+10, y)
	self.MHexadecimalማተሚያxy(uint8(data>>8), x+12, y)
	self.MHexadecimalማተሚያxy(uint8(data), x+14, y)
}
func Mማተሚያ(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) Mማተሚያhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	Mማተሚያ(uintptr(fbphysaddress), buffer[0], x, y)
	Mማተሚያ(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) Mማተሚያunsignedinteger16(data uint16, x uint32, y uint32) {
	self.Mማተሚያhexadecimal(uint8(data>>8), x+0*2, y)
	self.Mማተሚያhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) Mማተሚያunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.Mማተሚያhexadecimal(uint8(data>>24), x+0*2, y)
	self.Mማተሚያhexadecimal(uint8(data>>16), x+2*2, y)
	self.Mማተሚያhexadecimal(uint8(data>>8), x+4*2, y)
	self.Mማተሚያhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
