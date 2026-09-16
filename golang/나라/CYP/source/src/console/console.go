/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbΠλάτος		= 80
	fbΎψος			= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xΘέση	uint16
	yΘέση	uint16
}

var σειριακόςαριθμόςΈτοιμο bool

func Σειριακόςαριθμόςinit()
func ΣειριακόςαριθμόςΕγγραφήbyte(data uint8)

func MΣειριακόςαριθμόςΚαταγραφήinit() {
	Σειριακόςαριθμόςinit()
	σειριακόςαριθμόςΈτοιμο = true
}

func σειριακόςαριθμόςΚαταγραφήbyte(data byte) {
	if !σειριακόςαριθμόςΈτοιμο {
		return
	}

	if data == '\n' {
		ΣειριακόςαριθμόςΕγγραφήbyte('\r')
	}
	ΣειριακόςαριθμόςΕγγραφήbyte(uint8(data))
}

func MEmergencyΚαταγραφήΣυμβολοσειρά(data string) {
	for i := 0; i < len(data); i++ {
		σειριακόςαριθμόςΚαταγραφήbyte(data[i])
	}
}

func MEmergencyΚαταγραφήhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	σειριακόςαριθμόςΚαταγραφήbyte(digits[(data>>4)&0x0F])
	σειριακόςαριθμόςΚαταγραφήbyte(digits[data&0x0F])
}

func MEmergencyΚαταγραφήunsignedinteger32(data uint32) {
	MEmergencyΚαταγραφήhexadecimal8(uint8(data >> 24))
	MEmergencyΚαταγραφήhexadecimal8(uint8(data >> 16))
	MEmergencyΚαταγραφήhexadecimal8(uint8(data >> 8))
	MEmergencyΚαταγραφήhexadecimal8(uint8(data))
}

func (self *TConsole) MΕκτύπωση(argumentΤιμή ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var τιμή_2 interface{}

	for i, p := range argumentΤιμή {
		switch i {
		case 0:
			param, _ := p.(interface{})
			τιμή_2 = param
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

	self.MΕκτύπωσηxy(τιμή_2, x, y)

}
func (self *TConsole) MΕκτύπωσηxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MΕκτύπωσηbytesxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalΕκτύπωσηxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Εκτύπωσηxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Εκτύπωσηxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Εκτύπωσηxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MΕκτύπωσηbytesxy(data_2, x, y)
	}

}
func (self *TConsole) MΕκτύπωσηbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xΘέση = x
	}
	if y <= 999 {
		self.yΘέση = y
	}

	γνώρισμα := uint16(0x0F)
	όριο := len(buffer)
	if όριο > 4096 {
		όριο = 4096
	}
	for i := 0; i < όριο; i++ {
		σειριακόςαριθμόςΚαταγραφήbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yΘέση++
			self.xΘέση = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yΘέση+self.xΘέση)*2))) = γνώρισμα<<8 | uint16(buffer[i])
			self.xΘέση++
		}

		if self.xΘέση >= 80 {
			self.yΘέση++
			self.xΘέση = 0
		}

		if self.yΘέση >= 25 {
			for self.yΘέση = 0; self.yΘέση < 25; self.yΘέση++ {
				for self.xΘέση = 0; self.xΘέση < 80; self.xΘέση++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yΘέση+self.xΘέση)*2))) = γνώρισμα<<8 | ' '
				}
			}
			self.xΘέση = 0
			self.yΘέση = 0
		}

	}

}
func (self *TConsole) MHexadecimalΕκτύπωση(κλειδί uint8) {
	buffer := []byte{'0', '0'}
	δεκαεξαδικό := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = δεκαεξαδικό[(κλειδί>>4)&0xF]
	buffer[1] = δεκαεξαδικό[κλειδί&0xF]
	self.MΕκτύπωση(buffer)
}
func (self *TConsole) MHexadecimalΕκτύπωσηxy(κλειδί uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	δεκαεξαδικό := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = δεκαεξαδικό[(κλειδί>>4)&0xF]
	buffer[1] = δεκαεξαδικό[κλειδί&0xF]
	self.MΕκτύπωσηxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Εκτύπωση(κλειδί uint16) {
	self.MHexadecimalΕκτύπωση(uint8(κλειδί >> 8))
	self.MHexadecimalΕκτύπωση(uint8(κλειδί))
}
func (self *TConsole) MUnsignedinteger16Εκτύπωσηxy(κλειδί uint16, x uint16, y uint16) {
	self.MHexadecimalΕκτύπωσηxy(uint8(κλειδί>>8), x, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(κλειδί), x, y)
}
func (self *TConsole) MUnsignedinteger32Εκτύπωση(data uint32) {
	self.MHexadecimalΕκτύπωση(uint8(data >> 24))
	self.MHexadecimalΕκτύπωση(uint8(data >> 16))
	self.MHexadecimalΕκτύπωση(uint8(data >> 8))
	self.MHexadecimalΕκτύπωση(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Εκτύπωσηxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalΕκτύπωσηxy(uint8(data>>24), x+0, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>16), x+2, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>8), x+4, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Εκτύπωση(data uint64) {
	self.MHexadecimalΕκτύπωση(uint8(data >> 56))
	self.MHexadecimalΕκτύπωση(uint8(data >> 48))
	self.MHexadecimalΕκτύπωση(uint8(data >> 40))
	self.MHexadecimalΕκτύπωση(uint8(data >> 32))
	self.MHexadecimalΕκτύπωση(uint8(data >> 24))
	self.MHexadecimalΕκτύπωση(uint8(data >> 16))
	self.MHexadecimalΕκτύπωση(uint8(data >> 8))
	self.MHexadecimalΕκτύπωση(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Εκτύπωσηxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>56), x+0, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>48), x+2, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>40), x+4, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>32), x+6, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>24), x+8, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>16), x+10, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data>>8), x+12, y)
	self.MHexadecimalΕκτύπωσηxy(uint8(data), x+14, y)
}
func MΕκτύπωση(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MΕκτύπωσηhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	δεκαεξαδικό := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = δεκαεξαδικό[(data>>4)&0xF]
	buffer[1] = δεκαεξαδικό[data&0xF]

	MΕκτύπωση(uintptr(fbphysaddress), buffer[0], x, y)
	MΕκτύπωση(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MΕκτύπωσηunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MΕκτύπωσηhexadecimal(uint8(data>>8), x+0*2, y)
	self.MΕκτύπωσηhexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MΕκτύπωσηunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MΕκτύπωσηhexadecimal(uint8(data>>24), x+0*2, y)
	self.MΕκτύπωσηhexadecimal(uint8(data>>16), x+2*2, y)
	self.MΕκτύπωσηhexadecimal(uint8(data>>8), x+4*2, y)
	self.MΕκτύπωσηhexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
