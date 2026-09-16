/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbPlotis		= 80
	fbAukštis		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPozicija	uint16
	yPozicija	uint16
}

var serijinisPasiruošęs bool

func Serijinisinit()
func SerijinisRašymasbyte(data uint8)

func MSerijinisŽurnalasinit() {
	Serijinisinit()
	serijinisPasiruošęs = true
}

func serijinisŽurnalasbyte(data byte) {
	if !serijinisPasiruošęs {
		return
	}

	if data == '\n' {
		SerijinisRašymasbyte('\r')
	}
	SerijinisRašymasbyte(uint8(data))
}

func MEmergencyŽurnalasEilutė(data string) {
	for i := 0; i < len(data); i++ {
		serijinisŽurnalasbyte(data[i])
	}
}

func MEmergencyŽurnalashexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serijinisŽurnalasbyte(digits[(data>>4)&0x0F])
	serijinisŽurnalasbyte(digits[data&0x0F])
}

func MEmergencyŽurnalasunsignedinteger32(data uint32) {
	MEmergencyŽurnalashexadecimal8(uint8(data >> 24))
	MEmergencyŽurnalashexadecimal8(uint8(data >> 16))
	MEmergencyŽurnalashexadecimal8(uint8(data >> 8))
	MEmergencyŽurnalashexadecimal8(uint8(data))
}

func (self *TConsole) MSpausdinti(argumentReikšmė ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var reikšmė_2 interface{}

	for i, p := range argumentReikšmė {
		switch i {
		case 0:
			param, _ := p.(interface{})
			reikšmė_2 = param
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

	self.MSpausdintixy(reikšmė_2, x, y)

}
func (self *TConsole) MSpausdintixy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MSpausdintiBaitųxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalSpausdintixy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Spausdintixy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Spausdintixy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Spausdintixy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MSpausdintiBaitųxy(data_2, x, y)
	}

}
func (self *TConsole) MSpausdintiBaitųxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xPozicija = x
	}
	if y <= 999 {
		self.yPozicija = y
	}

	atributas := uint16(0x0F)
	riba := len(buffer)
	if riba > 4096 {
		riba = 4096
	}
	for i := 0; i < riba; i++ {
		serijinisŽurnalasbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yPozicija++
			self.xPozicija = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yPozicija+self.xPozicija)*2))) = atributas<<8 | uint16(buffer[i])
			self.xPozicija++
		}

		if self.xPozicija >= 80 {
			self.yPozicija++
			self.xPozicija = 0
		}

		if self.yPozicija >= 25 {
			for self.yPozicija = 0; self.yPozicija < 25; self.yPozicija++ {
				for self.xPozicija = 0; self.xPozicija < 80; self.xPozicija++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yPozicija+self.xPozicija)*2))) = atributas<<8 | ' '
				}
			}
			self.xPozicija = 0
			self.yPozicija = 0
		}

	}

}
func (self *TConsole) MHexadecimalSpausdinti(raktas uint8) {
	buffer := []byte{'0', '0'}
	šešioliktainis := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šešioliktainis[(raktas>>4)&0xF]
	buffer[1] = šešioliktainis[raktas&0xF]
	self.MSpausdinti(buffer)
}
func (self *TConsole) MHexadecimalSpausdintixy(raktas uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	šešioliktainis := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šešioliktainis[(raktas>>4)&0xF]
	buffer[1] = šešioliktainis[raktas&0xF]
	self.MSpausdintixy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Spausdinti(raktas uint16) {
	self.MHexadecimalSpausdinti(uint8(raktas >> 8))
	self.MHexadecimalSpausdinti(uint8(raktas))
}
func (self *TConsole) MUnsignedinteger16Spausdintixy(raktas uint16, x uint16, y uint16) {
	self.MHexadecimalSpausdintixy(uint8(raktas>>8), x, y)
	self.MHexadecimalSpausdintixy(uint8(raktas), x, y)
}
func (self *TConsole) MUnsignedinteger32Spausdinti(data uint32) {
	self.MHexadecimalSpausdinti(uint8(data >> 24))
	self.MHexadecimalSpausdinti(uint8(data >> 16))
	self.MHexadecimalSpausdinti(uint8(data >> 8))
	self.MHexadecimalSpausdinti(uint8(data))
}
func (self *TConsole) MUnsignedinteger32Spausdintixy(data uint32, x uint16, y uint16) {

	self.MHexadecimalSpausdintixy(uint8(data>>24), x+0, y)
	self.MHexadecimalSpausdintixy(uint8(data>>16), x+2, y)
	self.MHexadecimalSpausdintixy(uint8(data>>8), x+4, y)
	self.MHexadecimalSpausdintixy(uint8(data), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Spausdinti(data uint64) {
	self.MHexadecimalSpausdinti(uint8(data >> 56))
	self.MHexadecimalSpausdinti(uint8(data >> 48))
	self.MHexadecimalSpausdinti(uint8(data >> 40))
	self.MHexadecimalSpausdinti(uint8(data >> 32))
	self.MHexadecimalSpausdinti(uint8(data >> 24))
	self.MHexadecimalSpausdinti(uint8(data >> 16))
	self.MHexadecimalSpausdinti(uint8(data >> 8))
	self.MHexadecimalSpausdinti(uint8(data))
}
func (self *TConsole) MUnsignedinteger64Spausdintixy(data uint64, x uint16, y uint16) {
	self.MHexadecimalSpausdintixy(uint8(data>>56), x+0, y)
	self.MHexadecimalSpausdintixy(uint8(data>>48), x+2, y)
	self.MHexadecimalSpausdintixy(uint8(data>>40), x+4, y)
	self.MHexadecimalSpausdintixy(uint8(data>>32), x+6, y)
	self.MHexadecimalSpausdintixy(uint8(data>>24), x+8, y)
	self.MHexadecimalSpausdintixy(uint8(data>>16), x+10, y)
	self.MHexadecimalSpausdintixy(uint8(data>>8), x+12, y)
	self.MHexadecimalSpausdintixy(uint8(data), x+14, y)
}
func MSpausdinti(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TConsole) MSpausdintihexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	šešioliktainis := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = šešioliktainis[(data>>4)&0xF]
	buffer[1] = šešioliktainis[data&0xF]

	MSpausdinti(uintptr(fbphysaddress), buffer[0], x, y)
	MSpausdinti(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MSpausdintiunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MSpausdintihexadecimal(uint8(data>>8), x+0*2, y)
	self.MSpausdintihexadecimal(uint8(data), x+2*2, y)
}

func (self *TConsole) MSpausdintiunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MSpausdintihexadecimal(uint8(data>>24), x+0*2, y)
	self.MSpausdintihexadecimal(uint8(data>>16), x+2*2, y)
	self.MSpausdintihexadecimal(uint8(data>>8), x+4*2, y)
	self.MSpausdintihexadecimal(uint8(data), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
