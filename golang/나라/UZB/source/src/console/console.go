package console

import . "unsafe"

const (
	fbwidth			= 80
	fbBoyi			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xHolati	uint16
	yHolati	uint16
}

var serialTayyor bool

func Serialinit()
func SerialYozishbyte(data uint8)

func MSerialloginit() {
	Serialinit()
	serialTayyor = true
}

func seriallogbyte(data byte) {
	if !serialTayyor {
		return
	}

	if data == '\n' {
		SerialYozishbyte('\r')
	}
	SerialYozishbyte(uint8(data))
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

func (self *TConsole) MChopetish(argumentQiymat ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var qiymat_2 interface{}

	for i, p := range argumentQiymat {
		switch i {
		case 0:
			param, _ := p.(interface{})
			qiymat_2 = param
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

	self.MChopetishxy(qiymat_2, x, y)

}
func (self *TConsole) MChopetishxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MChopetishBaytlarxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalChopetishxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Chopetishxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Chopetishxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Chopetishxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MChopetishBaytlarxy(data_2, x, y)
	}

}
func (self *TConsole) MChopetishBaytlarxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xHolati = x
	}
	if y <= 999 {
		self.yHolati = y
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
			self.yHolati++
			self.xHolati = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yHolati+self.xHolati)*2))) = attribute<<8 | uint16(buffer[i])
			self.xHolati++
		}

		if self.xHolati >= 80 {
			self.yHolati++
			self.xHolati = 0
		}

		if self.yHolati >= 25 {
			for self.yHolati = 0; self.yHolati < 25; self.yHolati++ {
				for self.xHolati = 0; self.xHolati < 80; self.xHolati++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yHolati+self.xHolati)*2))) = attribute<<8 | ' '
				}
			}
			self.xHolati = 0
			self.yHolati = 0
		}

	}

}
func (self *TConsole) MHexadecimalChopetish(kalit uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(kalit>>4)&0xF]
	buffer[1] = hex[kalit&0xF]
	self.MChopetish(buffer)
}
func (self *TConsole) MHexadecimalChopetishxy(kalit uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(kalit>>4)&0xF]
	buffer[1] = hex[kalit&0xF]
	self.MChopetishxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Chopetish(kalit uint16) {
	self.MHexadecimalChopetish(uint8(kalit >> 8))
	self.MHexadecimalChopetish(uint8(kalit))
}
func (self *TConsole) MUnsignedinteger16Chopetishxy(kalit uint16, x uint16, y uint16) {
	self.MHexadecimalChopetishxy(uint8(kalit>>8), x, y)
	self.MHexadecimalChopetishxy(uint8(kalit), x, y)
}
func (self *TConsole) MUnsignedinteger32Chopetish(data uint32) {
	self.MHexadecimalChopetish(uint8(data >> 24))
	self.MHexadecimalChopetish(uint8(data >> 16))
	self.MHexadecimalChopetish(uint8(data >> 8))
	self.MHexadecimalChopetish(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Chopetishxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalChopetishxy(uint8(data>>24), x+0, y)
	self.MHexadecimalChopetishxy(uint8(data>>16), x+2, y)
	self.MHexadecimalChopetishxy(uint8(data>>8), x+4, y)
	self.MHexadecimalChopetishxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Chopetish(data uint64) {
	self.MHexadecimalChopetish(uint8(data >> 56))
	self.MHexadecimalChopetish(uint8(data >> 48))
	self.MHexadecimalChopetish(uint8(data >> 40))
	self.MHexadecimalChopetish(uint8(data >> 32))
	self.MHexadecimalChopetish(uint8(data >> 24))
	self.MHexadecimalChopetish(uint8(data >> 16))
	self.MHexadecimalChopetish(uint8(data >> 8))
	self.MHexadecimalChopetish(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Chopetishxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalChopetishxy(uint8(data>>56), x+0, y)
	self.MHexadecimalChopetishxy(uint8(data>>48), x+2, y)
	self.MHexadecimalChopetishxy(uint8(data>>40), x+4, y)
	self.MHexadecimalChopetishxy(uint8(data>>32), x+6, y)
	self.MHexadecimalChopetishxy(uint8(data>>24), x+8, y)
	self.MHexadecimalChopetishxy(uint8(data>>16), x+10, y)
	self.MHexadecimalChopetishxy(uint8(data>>8), x+12, y)
	self.MHexadecimalChopetishxy(uint8(data), x+14, y)
}
func MChopetish(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MChopetishhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(data>>4)&0xF]
	buffer[1] = hex[data&0xF]

	MChopetish(uintptr(fbphysaddress), buffer[0], x, y)
	MChopetish(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MChopetishunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MChopetishhexadecimal(uint8(data>>8), x+0*2, y)
	self.MChopetishhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MChopetishunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MChopetishhexadecimal(uint8(data>>24), x+0*2, y)
	self.MChopetishhexadecimal(uint8(data>>16), x+2*2, y)
	self.MChopetishhexadecimal(uint8(data>>8), x+4*2, y)
	self.MChopetishhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
