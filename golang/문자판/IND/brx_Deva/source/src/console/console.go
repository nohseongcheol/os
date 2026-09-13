package console

import . "unsafe"

const (
	fbWidth			= 80
	fbHeight		= 25
	fbPhysAddr	uintptr	= 0xb8000
)

type T콘솔 struct {
	xPos	uint16
	yPos	uint16
}

var serialReady bool

func SerialInit()
func SerialWriteByte(data uint8)

func M직렬로그초기화() {
	SerialInit()
	serialReady = true
}

func serialLogByte(data byte) {
	if !serialReady {
		return
	}

	if data == '\n' {
		SerialWriteByte('\r')
	}
	SerialWriteByte(uint8(data))
}

func M긴급로그문자열(data string) {
	for i := 0; i < len(data); i++ {
		serialLogByte(data[i])
	}
}

func M긴급로그Hex8(data uint8) {
	const digits = "0123456789ABCDEF"
	serialLogByte(digits[(data>>4)&0x0F])
	serialLogByte(digits[data&0x0F])
}

func M긴급로그Uint32(data uint32) {
	M긴급로그Hex8(uint8(data >> 24))
	M긴급로그Hex8(uint8(data >> 16))
	M긴급로그Hex8(uint8(data >> 8))
	M긴급로그Hex8(uint8(data))
}

func (self *T콘솔) M출력(매개값 ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var 값 interface{}

	for i, p := range 매개값 {
		switch i {
		case 0:
			param, _ := p.(interface{})
			값 = param
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

	self.M출력XY(값, x, y)

}
func (self *T콘솔) M출력XY(임시 interface{}, x uint16, y uint16) {

	switch 임시.(type) {
	case string:
		자료, _ := 임시.(string)
		self.M출력BytesXY(([]byte)(자료), x, y)
	case uint8:
		자료, _ := 임시.(uint8)
		self.MHex출력XY(자료, x, y)
	case uint16:
		자료, _ := 임시.(uint16)
		self.MUint16출력XY(자료, x, y)
	case uint32:
		자료, _ := 임시.(uint32)
		self.MUint32출력XY(자료, x, y)
	case uint64:
		자료, _ := 임시.(uint64)
		self.MUint64출력XY(자료, x, y)
	default:
		자료, _ := 임시.([]byte)
		self.M출력BytesXY(자료, x, y)
	}

}
func (self *T콘솔) M출력BytesXY(buf []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xPos = x
	}
	if y <= 999 {
		self.yPos = y
	}

	attr := uint16(0x0F)
	limit := len(buf)
	if limit > 4096 {
		limit = 4096
	}
	for i := 0; i < limit; i++ {
		serialLogByte(buf[i])
		switch buf[i] {
		case '\n':
			self.yPos++
			self.xPos = 0
		default:
			*(*uint16)(Pointer(fbPhysAddr + uintptr((80*self.yPos+self.xPos)*2))) = attr<<8 | uint16(buf[i])
			self.xPos++
		}

		if self.xPos >= 80 {
			self.yPos++
			self.xPos = 0
		}

		if self.yPos >= 25 {
			for self.yPos = 0; self.yPos < 25; self.yPos++ {
				for self.xPos = 0; self.xPos < 80; self.xPos++ {
					*(*uint16)(Pointer(fbPhysAddr + uintptr((80*self.yPos+self.xPos)*2))) = attr<<8 | ' '
				}
			}
			self.xPos = 0
			self.yPos = 0
		}

	}

}
func (self *T콘솔) MHex출력(key uint8) {
	buf := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buf[0] = hex[(key>>4)&0xF]
	buf[1] = hex[key&0xF]
	self.M출력(buf)
}
func (self *T콘솔) MHex출력XY(key uint8, x uint16, y uint16) {
	buf := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buf[0] = hex[(key>>4)&0xF]
	buf[1] = hex[key&0xF]
	self.M출력XY(buf, x, y)
}
func (self *T콘솔) MUint16출력(key uint16) {
	self.MHex출력(uint8(key >> 8))
	self.MHex출력(uint8(key))
}
func (self *T콘솔) MUint16출력XY(key uint16, x uint16, y uint16) {
	self.MHex출력XY(uint8(key>>8), x, y)
	self.MHex출력XY(uint8(key), x, y)
}
func (self *T콘솔) MUint32출력(data uint32) {
	self.MHex출력(uint8(data >> 24))
	self.MHex출력(uint8(data >> 16))
	self.MHex출력(uint8(data >> 8))
	self.MHex출력(uint8(data))
}
func (self *T콘솔) MUint32출력XY(data uint32, x uint16, y uint16) {

	self.MHex출력XY(uint8(data>>24), x+0, y)
	self.MHex출력XY(uint8(data>>16), x+2, y)
	self.MHex출력XY(uint8(data>>8), x+4, y)
	self.MHex출력XY(uint8(data), x+6, y)
}
func (self *T콘솔) MUint64출력(data uint64) {
	self.MHex출력(uint8(data >> 56))
	self.MHex출력(uint8(data >> 48))
	self.MHex출력(uint8(data >> 40))
	self.MHex출력(uint8(data >> 32))
	self.MHex출력(uint8(data >> 24))
	self.MHex출력(uint8(data >> 16))
	self.MHex출력(uint8(data >> 8))
	self.MHex출력(uint8(data))
}
func (self *T콘솔) MUint64출력XY(data uint64, x uint16, y uint16) {
	self.MHex출력XY(uint8(data>>56), x+0, y)
	self.MHex출력XY(uint8(data>>48), x+2, y)
	self.MHex출력XY(uint8(data>>40), x+4, y)
	self.MHex출력XY(uint8(data>>32), x+6, y)
	self.MHex출력XY(uint8(data>>24), x+8, y)
	self.MHex출력XY(uint8(data>>16), x+10, y)
	self.MHex출력XY(uint8(data>>8), x+12, y)
	self.MHex출력XY(uint8(data), x+14, y)
}
func M출력(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *T콘솔) M출력Hex(data uint8, x uint32, y uint32) {
	buf := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buf[0] = hex[(data>>4)&0xF]
	buf[1] = hex[data&0xF]

	M출력(uintptr(fbPhysAddr), buf[0], x, y)
	M출력(uintptr(fbPhysAddr), buf[1], x+2, y)
}

func (self *T콘솔) M출력Uint16(data uint16, x uint32, y uint32) {
	self.M출력Hex(uint8(data>>8), x+0*2, y)
	self.M출력Hex(uint8(data), x+2*2, y)
}

func (self *T콘솔) M출력Uint32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.M출력Hex(uint8(data>>24), x+0*2, y)
	self.M출력Hex(uint8(data>>16), x+2*2, y)
	self.M출력Hex(uint8(data>>8), x+4*2, y)
	self.M출력Hex(uint8(data), x+6*2, y)
}

func (self *T콘솔) M테스트() {
}
