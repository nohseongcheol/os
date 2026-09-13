package konsol

import . "unsafe"

const (
	fbGenişlik		= 80
	fbBaşlık		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TKonsol struct {
	xKonum	uint16
	yKonum	uint16
}

var seriHazır bool

func Seriinit()
func SeriYazmabyte(data uint8)

func MSeriGünlükinit() {
	Seriinit()
	seriHazır = true
}

func seriGünlükbyte(data byte) {
	if !seriHazır {
		return
	}

	if data == '\n' {
		SeriYazmabyte('\r')
	}
	SeriYazmabyte(uint8(data))
}

func MEmergencyGünlükKatar(data string) {
	for i := 0; i < len(data); i++ {
		seriGünlükbyte(data[i])
	}
}

func MEmergencyGünlükhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	seriGünlükbyte(digits[(data>>4)&0x0F])
	seriGünlükbyte(digits[data&0x0F])
}

func MEmergencyGünlükunsignedinteger32(data uint32) {
	MEmergencyGünlükhexadecimal8(uint8(data >> 24))
	MEmergencyGünlükhexadecimal8(uint8(data >> 16))
	MEmergencyGünlükhexadecimal8(uint8(data >> 8))
	MEmergencyGünlükhexadecimal8(uint8(data))
}

func (self *TKonsol) MYazdır(argumentDeğer ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var değer_2 interface{}

	for i, p := range argumentDeğer {
		switch i {
		case 0:
			param, _ := p.(interface{})
			değer_2 = param
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

	self.MYazdırxy(değer_2, x, y)

}
func (self *TKonsol) MYazdırxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		self.MYazdırBaytxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		self.MHexadecimalYazdırxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Yazdırxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Yazdırxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Yazdırxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		self.MYazdırBaytxy(data_2, x, y)
	}

}
func (self *TKonsol) MYazdırBaytxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xKonum = x
	}
	if y <= 999 {
		self.yKonum = y
	}

	öznitelik := uint16(0x0F)
	kısıtla := len(buffer)
	if kısıtla > 4096 {
		kısıtla = 4096
	}
	for i := 0; i < kısıtla; i++ {
		seriGünlükbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yKonum++
			self.xKonum = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yKonum+self.xKonum)*2))) = öznitelik<<8 | uint16(buffer[i])
			self.xKonum++
		}

		if self.xKonum >= 80 {
			self.yKonum++
			self.xKonum = 0
		}

		if self.yKonum >= 25 {
			for self.yKonum = 0; self.yKonum < 25; self.yKonum++ {
				for self.xKonum = 0; self.xKonum < 80; self.xKonum++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yKonum+self.xKonum)*2))) = öznitelik<<8 | ' '
				}
			}
			self.xKonum = 0
			self.yKonum = 0
		}

	}

}
func (self *TKonsol) MHexadecimalYazdır(anahtar uint8) {
	buffer := []byte{'0', '0'}
	onaltılık := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = onaltılık[(anahtar>>4)&0xF]
	buffer[1] = onaltılık[anahtar&0xF]
	self.MYazdır(buffer)
}
func (self *TKonsol) MHexadecimalYazdırxy(anahtar uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	onaltılık := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = onaltılık[(anahtar>>4)&0xF]
	buffer[1] = onaltılık[anahtar&0xF]
	self.MYazdırxy(buffer, x, y)
}
func (self *TKonsol) MUnsignedinteger16Yazdır(anahtar uint16) {
	self.MHexadecimalYazdır(uint8(anahtar >> 8))
	self.MHexadecimalYazdır(uint8(anahtar))
}
func (self *TKonsol) MUnsignedinteger16Yazdırxy(anahtar uint16, x uint16, y uint16) {
	self.MHexadecimalYazdırxy(uint8(anahtar>>8), x, y)
	self.MHexadecimalYazdırxy(uint8(anahtar), x, y)
}
func (self *TKonsol) MUnsignedinteger32Yazdır(data uint32) {
	self.MHexadecimalYazdır(uint8(data >> 24))
	self.MHexadecimalYazdır(uint8(data >> 16))
	self.MHexadecimalYazdır(uint8(data >> 8))
	self.MHexadecimalYazdır(uint8(data))
}
func (self *TKonsol) MUnsignedinteger32Yazdırxy(data uint32, x uint16, y uint16) {

	self.MHexadecimalYazdırxy(uint8(data>>24), x+0, y)
	self.MHexadecimalYazdırxy(uint8(data>>16), x+2, y)
	self.MHexadecimalYazdırxy(uint8(data>>8), x+4, y)
	self.MHexadecimalYazdırxy(uint8(data), x+6, y)
}
func (self *TKonsol) MUnsignedinteger64Yazdır(data uint64) {
	self.MHexadecimalYazdır(uint8(data >> 56))
	self.MHexadecimalYazdır(uint8(data >> 48))
	self.MHexadecimalYazdır(uint8(data >> 40))
	self.MHexadecimalYazdır(uint8(data >> 32))
	self.MHexadecimalYazdır(uint8(data >> 24))
	self.MHexadecimalYazdır(uint8(data >> 16))
	self.MHexadecimalYazdır(uint8(data >> 8))
	self.MHexadecimalYazdır(uint8(data))
}
func (self *TKonsol) MUnsignedinteger64Yazdırxy(data uint64, x uint16, y uint16) {
	self.MHexadecimalYazdırxy(uint8(data>>56), x+0, y)
	self.MHexadecimalYazdırxy(uint8(data>>48), x+2, y)
	self.MHexadecimalYazdırxy(uint8(data>>40), x+4, y)
	self.MHexadecimalYazdırxy(uint8(data>>32), x+6, y)
	self.MHexadecimalYazdırxy(uint8(data>>24), x+8, y)
	self.MHexadecimalYazdırxy(uint8(data>>16), x+10, y)
	self.MHexadecimalYazdırxy(uint8(data>>8), x+12, y)
	self.MHexadecimalYazdırxy(uint8(data), x+14, y)
}
func MYazdır(phyaddr uintptr, data uint8, x uint32, y uint32)

func (self *TKonsol) MYazdırhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	onaltılık := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = onaltılık[(data>>4)&0xF]
	buffer[1] = onaltılık[data&0xF]

	MYazdır(uintptr(fbphysaddress), buffer[0], x, y)
	MYazdır(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TKonsol) MYazdırunsignedinteger16(data uint16, x uint32, y uint32) {
	self.MYazdırhexadecimal(uint8(data>>8), x+0*2, y)
	self.MYazdırhexadecimal(uint8(data), x+2*2, y)
}

func (self *TKonsol) MYazdırunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	self.MYazdırhexadecimal(uint8(data>>24), x+0*2, y)
	self.MYazdırhexadecimal(uint8(data>>16), x+2*2, y)
	self.MYazdırhexadecimal(uint8(data>>8), x+4*2, y)
	self.MYazdırhexadecimal(uint8(data), x+6*2, y)
}

func (self *TKonsol) M테스트() {
}
