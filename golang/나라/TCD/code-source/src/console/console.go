package console

import . "unsafe"

const (
	fbLargeur		= 80
	fbHauteur		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xposition	uint16
	yposition	uint16
}

var sériePrêt bool

func Sérieinit()
func Sérieécrireoctet(données uint8)

func MSérieJournalinit() {
	Sérieinit()
	sériePrêt = true
}

func sérieJournaloctet(données byte) {
	if !sériePrêt {
		return
	}

	if données == '\n' {
		Sérieécrireoctet('\r')
	}
	Sérieécrireoctet(uint8(données))
}

func MEmergencyJournalChaîne(données string) {
	for i := 0; i < len(données); i++ {
		sérieJournaloctet(données[i])
	}
}

func MEmergencyJournalhexadecimal8(données uint8) {
	const digits = "0123456789ABCDEF"
	sérieJournaloctet(digits[(données>>4)&0x0F])
	sérieJournaloctet(digits[données&0x0F])
}

func MEmergencyJournalunsignedinteger32(données uint32) {
	MEmergencyJournalhexadecimal8(uint8(données >> 24))
	MEmergencyJournalhexadecimal8(uint8(données >> 16))
	MEmergencyJournalhexadecimal8(uint8(données >> 8))
	MEmergencyJournalhexadecimal8(uint8(données))
}

func (self *TConsole) MImprimer(argumentValeur ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var valeur_2 interface{}

	for i, p := range argumentValeur {
		switch i {
		case 0:
			param, _ := p.(interface{})
			valeur_2 = param
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

	self.MImprimerxy(valeur_2, x, y)

}
func (self *TConsole) MImprimerxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		données_2, _ := temporary_2.(string)
		self.MImprimerOctetsxy(([]byte)(données_2), x, y)
	case uint8:
		données_2, _ := temporary_2.(uint8)
		self.MHexadecimalImprimerxy(données_2, x, y)
	case uint16:
		données_2, _ := temporary_2.(uint16)
		self.MUnsignedinteger16Imprimerxy(données_2, x, y)
	case uint32:
		données_2, _ := temporary_2.(uint32)
		self.MUnsignedinteger32Imprimerxy(données_2, x, y)
	case uint64:
		données_2, _ := temporary_2.(uint64)
		self.MUnsignedinteger64Imprimerxy(données_2, x, y)
	default:
		données_2, _ := temporary_2.([]byte)
		self.MImprimerOctetsxy(données_2, x, y)
	}

}
func (self *TConsole) MImprimerOctetsxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		self.xposition = x
	}
	if y <= 999 {
		self.yposition = y
	}

	attribut := uint16(0x0F)
	limite := len(buffer)
	if limite > 4096 {
		limite = 4096
	}
	for i := 0; i < limite; i++ {
		sérieJournaloctet(buffer[i])
		switch buffer[i] {
		case '\n':
			self.yposition++
			self.xposition = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribut<<8 | uint16(buffer[i])
			self.xposition++
		}

		if self.xposition >= 80 {
			self.yposition++
			self.xposition = 0
		}

		if self.yposition >= 25 {
			for self.yposition = 0; self.yposition < 25; self.yposition++ {
				for self.xposition = 0; self.xposition < 80; self.xposition++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*self.yposition+self.xposition)*2))) = attribut<<8 | ' '
				}
			}
			self.xposition = 0
			self.yposition = 0
		}

	}

}
func (self *TConsole) MHexadecimalImprimer(clé uint8) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(clé>>4)&0xF]
	buffer[1] = hex[clé&0xF]
	self.MImprimer(buffer)
}
func (self *TConsole) MHexadecimalImprimerxy(clé uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(clé>>4)&0xF]
	buffer[1] = hex[clé&0xF]
	self.MImprimerxy(buffer, x, y)
}
func (self *TConsole) MUnsignedinteger16Imprimer(clé uint16) {
	self.MHexadecimalImprimer(uint8(clé >> 8))
	self.MHexadecimalImprimer(uint8(clé))
}
func (self *TConsole) MUnsignedinteger16Imprimerxy(clé uint16, x uint16, y uint16) {
	self.MHexadecimalImprimerxy(uint8(clé>>8), x, y)
	self.MHexadecimalImprimerxy(uint8(clé), x, y)
}
func (self *TConsole) MUnsignedinteger32Imprimer(données uint32) {
	self.MHexadecimalImprimer(uint8(données >> 24))
	self.MHexadecimalImprimer(uint8(données >> 16))
	self.MHexadecimalImprimer(uint8(données >> 8))
	self.MHexadecimalImprimer(uint8(données))
}
func (self *TConsole) MUnsignedinteger32Imprimerxy(données uint32, x uint16, y uint16) {

	self.MHexadecimalImprimerxy(uint8(données>>24), x+0, y)
	self.MHexadecimalImprimerxy(uint8(données>>16), x+2, y)
	self.MHexadecimalImprimerxy(uint8(données>>8), x+4, y)
	self.MHexadecimalImprimerxy(uint8(données), x+6, y)
}
func (self *TConsole) MUnsignedinteger64Imprimer(données uint64) {
	self.MHexadecimalImprimer(uint8(données >> 56))
	self.MHexadecimalImprimer(uint8(données >> 48))
	self.MHexadecimalImprimer(uint8(données >> 40))
	self.MHexadecimalImprimer(uint8(données >> 32))
	self.MHexadecimalImprimer(uint8(données >> 24))
	self.MHexadecimalImprimer(uint8(données >> 16))
	self.MHexadecimalImprimer(uint8(données >> 8))
	self.MHexadecimalImprimer(uint8(données))
}
func (self *TConsole) MUnsignedinteger64Imprimerxy(données uint64, x uint16, y uint16) {
	self.MHexadecimalImprimerxy(uint8(données>>56), x+0, y)
	self.MHexadecimalImprimerxy(uint8(données>>48), x+2, y)
	self.MHexadecimalImprimerxy(uint8(données>>40), x+4, y)
	self.MHexadecimalImprimerxy(uint8(données>>32), x+6, y)
	self.MHexadecimalImprimerxy(uint8(données>>24), x+8, y)
	self.MHexadecimalImprimerxy(uint8(données>>16), x+10, y)
	self.MHexadecimalImprimerxy(uint8(données>>8), x+12, y)
	self.MHexadecimalImprimerxy(uint8(données), x+14, y)
}
func MImprimer(phyaddr uintptr, données uint8, x uint32, y uint32)

func (self *TConsole) MImprimerhexadecimal(données uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hex[(données>>4)&0xF]
	buffer[1] = hex[données&0xF]

	MImprimer(uintptr(fbphysaddress), buffer[0], x, y)
	MImprimer(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (self *TConsole) MImprimerunsignedinteger16(données uint16, x uint32, y uint32) {
	self.MImprimerhexadecimal(uint8(données>>8), x+0*2, y)
	self.MImprimerhexadecimal(uint8(données), x+2*2, y)
}

func (self *TConsole) MImprimerunsignedinteger32(données uint32, x uint32, y uint32) {
	x = x * 2
	self.MImprimerhexadecimal(uint8(données>>24), x+0*2, y)
	self.MImprimerhexadecimal(uint8(données>>16), x+2*2, y)
	self.MImprimerhexadecimal(uint8(données>>8), x+4*2, y)
	self.MImprimerhexadecimal(uint8(données), x+6*2, y)
}

func (self *TConsole) M테스트() {
}
