package console

import . "unsafe"

const (
	fbLarghezza		= 80
	fbAltezza		= 25
	fbphysaddress	uintptr	= 0xb8000
)

type TConsole struct {
	xPosizione	uint16
	yPosizione	uint16
}

var serialePronto bool

func Serialeinit()
func SerialeScritturabyte(data uint8)

func MSerialeRegistroinit() {
	Serialeinit()
	serialePronto = true
}

func serialeRegistrobyte(data byte) {
	if !serialePronto {
		return
	}

	if data == '\n' {
		SerialeScritturabyte('\r')
	}
	SerialeScritturabyte(uint8(data))
}

func MEmergencyRegistroStringa(data string) {
	for i := 0; i < len(data); i++ {
		serialeRegistrobyte(data[i])
	}
}

func MEmergencyRegistrohexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	serialeRegistrobyte(digits[(data>>4)&0x0F])
	serialeRegistrobyte(digits[data&0x0F])
}

func MEmergencyRegistrounsignedinteger32(data uint32) {
	MEmergencyRegistrohexadecimal8(uint8(data >> 24))
	MEmergencyRegistrohexadecimal8(uint8(data >> 16))
	MEmergencyRegistrohexadecimal8(uint8(data >> 8))
	MEmergencyRegistrohexadecimal8(uint8(data))
}

func (séstesso *TConsole) MStampa(argumentValore ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var valore_2 interface{}

	for i, p := range argumentValore {
		switch i {
		case 0:
			param, _ := p.(interface{})
			valore_2 = param
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

	séstesso.MStampaxy(valore_2, x, y)

}
func (séstesso *TConsole) MStampaxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		séstesso.MStampaBytexy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		séstesso.MHexadecimalStampaxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		séstesso.MUnsignedinteger16Stampaxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		séstesso.MUnsignedinteger32Stampaxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		séstesso.MUnsignedinteger64Stampaxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		séstesso.MStampaBytexy(data_2, x, y)
	}

}
func (séstesso *TConsole) MStampaBytexy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		séstesso.xPosizione = x
	}
	if y <= 999 {
		séstesso.yPosizione = y
	}

	attributo := uint16(0x0F)
	limite := len(buffer)
	if limite > 4096 {
		limite = 4096
	}
	for i := 0; i < limite; i++ {
		serialeRegistrobyte(buffer[i])
		switch buffer[i] {
		case '\n':
			séstesso.yPosizione++
			séstesso.xPosizione = 0
		default:
			*(*uint16)(Pointer(fbphysaddress + uintptr((80*séstesso.yPosizione+séstesso.xPosizione)*2))) = attributo<<8 | uint16(buffer[i])
			séstesso.xPosizione++
		}

		if séstesso.xPosizione >= 80 {
			séstesso.yPosizione++
			séstesso.xPosizione = 0
		}

		if séstesso.yPosizione >= 25 {
			for séstesso.yPosizione = 0; séstesso.yPosizione < 25; séstesso.yPosizione++ {
				for séstesso.xPosizione = 0; séstesso.xPosizione < 80; séstesso.xPosizione++ {
					*(*uint16)(Pointer(fbphysaddress + uintptr((80*séstesso.yPosizione+séstesso.xPosizione)*2))) = attributo<<8 | ' '
				}
			}
			séstesso.xPosizione = 0
			séstesso.yPosizione = 0
		}

	}

}
func (séstesso *TConsole) MHexadecimalStampa(chiave uint8) {
	buffer := []byte{'0', '0'}
	esadecimale := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = esadecimale[(chiave>>4)&0xF]
	buffer[1] = esadecimale[chiave&0xF]
	séstesso.MStampa(buffer)
}
func (séstesso *TConsole) MHexadecimalStampaxy(chiave uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	esadecimale := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = esadecimale[(chiave>>4)&0xF]
	buffer[1] = esadecimale[chiave&0xF]
	séstesso.MStampaxy(buffer, x, y)
}
func (séstesso *TConsole) MUnsignedinteger16Stampa(chiave uint16) {
	séstesso.MHexadecimalStampa(uint8(chiave >> 8))
	séstesso.MHexadecimalStampa(uint8(chiave))
}
func (séstesso *TConsole) MUnsignedinteger16Stampaxy(chiave uint16, x uint16, y uint16) {
	séstesso.MHexadecimalStampaxy(uint8(chiave>>8), x, y)
	séstesso.MHexadecimalStampaxy(uint8(chiave), x, y)
}
func (séstesso *TConsole) MUnsignedinteger32Stampa(data uint32) {
	séstesso.MHexadecimalStampa(uint8(data >> 24))
	séstesso.MHexadecimalStampa(uint8(data >> 16))
	séstesso.MHexadecimalStampa(uint8(data >> 8))
	séstesso.MHexadecimalStampa(uint8(data))
}
func (séstesso *TConsole) MUnsignedinteger32Stampaxy(data uint32, x uint16, y uint16) {

	séstesso.MHexadecimalStampaxy(uint8(data>>24), x+0, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>16), x+2, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>8), x+4, y)
	séstesso.MHexadecimalStampaxy(uint8(data), x+6, y)
}
func (séstesso *TConsole) MUnsignedinteger64Stampa(data uint64) {
	séstesso.MHexadecimalStampa(uint8(data >> 56))
	séstesso.MHexadecimalStampa(uint8(data >> 48))
	séstesso.MHexadecimalStampa(uint8(data >> 40))
	séstesso.MHexadecimalStampa(uint8(data >> 32))
	séstesso.MHexadecimalStampa(uint8(data >> 24))
	séstesso.MHexadecimalStampa(uint8(data >> 16))
	séstesso.MHexadecimalStampa(uint8(data >> 8))
	séstesso.MHexadecimalStampa(uint8(data))
}
func (séstesso *TConsole) MUnsignedinteger64Stampaxy(data uint64, x uint16, y uint16) {
	séstesso.MHexadecimalStampaxy(uint8(data>>56), x+0, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>48), x+2, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>40), x+4, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>32), x+6, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>24), x+8, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>16), x+10, y)
	séstesso.MHexadecimalStampaxy(uint8(data>>8), x+12, y)
	séstesso.MHexadecimalStampaxy(uint8(data), x+14, y)
}
func MStampa(phyaddr uintptr, data uint8, x uint32, y uint32)

func (séstesso *TConsole) MStampahexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	esadecimale := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = esadecimale[(data>>4)&0xF]
	buffer[1] = esadecimale[data&0xF]

	MStampa(uintptr(fbphysaddress), buffer[0], x, y)
	MStampa(uintptr(fbphysaddress), buffer[1], x+2, y)
}

func (séstesso *TConsole) MStampaunsignedinteger16(data uint16, x uint32, y uint32) {
	séstesso.MStampahexadecimal(uint8(data>>8), x+0*2, y)
	séstesso.MStampahexadecimal(uint8(data), x+2*2, y)
}

func (séstesso *TConsole) MStampaunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	séstesso.MStampahexadecimal(uint8(data>>24), x+0*2, y)
	séstesso.MStampahexadecimal(uint8(data>>16), x+2*2, y)
	séstesso.MStampahexadecimal(uint8(data>>8), x+4*2, y)
	séstesso.MStampahexadecimal(uint8(data), x+6*2, y)
}

func (séstesso *TConsole) M테스트() {
}
