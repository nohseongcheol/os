package consola

import . "unsafe"

const (
	fbAmplada		= 80
	fbAlçada		= 25
	fbphysAdreça	uintptr	= 0xb8000
)

type TConsola struct {
	xPosició	uint16
	yPosició	uint16
}

var sèriePreparat bool

func Sèrieinit()
func SèrieEscripturabyte(data uint8)

func MSèrieRegistreinit() {
	Sèrieinit()
	sèriePreparat = true
}

func sèrieRegistrebyte(data byte) {
	if !sèriePreparat {
		return
	}

	if data == '\n' {
		SèrieEscripturabyte('\r')
	}
	SèrieEscripturabyte(uint8(data))
}

func MEmergencyRegistreCadena(data string) {
	for i := 0; i < len(data); i++ {
		sèrieRegistrebyte(data[i])
	}
}

func MEmergencyRegistrehexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	sèrieRegistrebyte(digits[(data>>4)&0x0F])
	sèrieRegistrebyte(digits[data&0x0F])
}

func MEmergencyRegistreunsignedinteger32(data uint32) {
	MEmergencyRegistrehexadecimal8(uint8(data >> 24))
	MEmergencyRegistrehexadecimal8(uint8(data >> 16))
	MEmergencyRegistrehexadecimal8(uint8(data >> 8))
	MEmergencyRegistrehexadecimal8(uint8(data))
}

func (unmateix *TConsola) MImprimeix(argumentValor ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var valor_2 interface{}

	for i, p := range argumentValor {
		switch i {
		case 0:
			param, _ := p.(interface{})
			valor_2 = param
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

	unmateix.MImprimeixxy(valor_2, x, y)

}
func (unmateix *TConsola) MImprimeixxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		unmateix.MImprimeixbytesxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		unmateix.MHexadecimalImprimeixxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		unmateix.MUnsignedinteger16Imprimeixxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		unmateix.MUnsignedinteger32Imprimeixxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		unmateix.MUnsignedinteger64Imprimeixxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		unmateix.MImprimeixbytesxy(data_2, x, y)
	}

}
func (unmateix *TConsola) MImprimeixbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		unmateix.xPosició = x
	}
	if y <= 999 {
		unmateix.yPosició = y
	}

	atribut := uint16(0x0F)
	límit := len(buffer)
	if límit > 4096 {
		límit = 4096
	}
	for i := 0; i < límit; i++ {
		sèrieRegistrebyte(buffer[i])
		switch buffer[i] {
		case '\n':
			unmateix.yPosició++
			unmateix.xPosició = 0
		default:
			*(*uint16)(Pointer(fbphysAdreça + uintptr((80*unmateix.yPosició+unmateix.xPosició)*2))) = atribut<<8 | uint16(buffer[i])
			unmateix.xPosició++
		}

		if unmateix.xPosició >= 80 {
			unmateix.yPosició++
			unmateix.xPosició = 0
		}

		if unmateix.yPosició >= 25 {
			for unmateix.yPosició = 0; unmateix.yPosició < 25; unmateix.yPosició++ {
				for unmateix.xPosició = 0; unmateix.xPosició < 80; unmateix.xPosició++ {
					*(*uint16)(Pointer(fbphysAdreça + uintptr((80*unmateix.yPosició+unmateix.xPosició)*2))) = atribut<<8 | ' '
				}
			}
			unmateix.xPosició = 0
			unmateix.yPosició = 0
		}

	}

}
func (unmateix *TConsola) MHexadecimalImprimeix(clau uint8) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(clau>>4)&0xF]
	buffer[1] = hexadecimal[clau&0xF]
	unmateix.MImprimeix(buffer)
}
func (unmateix *TConsola) MHexadecimalImprimeixxy(clau uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(clau>>4)&0xF]
	buffer[1] = hexadecimal[clau&0xF]
	unmateix.MImprimeixxy(buffer, x, y)
}
func (unmateix *TConsola) MUnsignedinteger16Imprimeix(clau uint16) {
	unmateix.MHexadecimalImprimeix(uint8(clau >> 8))
	unmateix.MHexadecimalImprimeix(uint8(clau))
}
func (unmateix *TConsola) MUnsignedinteger16Imprimeixxy(clau uint16, x uint16, y uint16) {
	unmateix.MHexadecimalImprimeixxy(uint8(clau>>8), x, y)
	unmateix.MHexadecimalImprimeixxy(uint8(clau), x, y)
}
func (unmateix *TConsola) MUnsignedinteger32Imprimeix(data uint32) {
	unmateix.MHexadecimalImprimeix(uint8(data >> 24))
	unmateix.MHexadecimalImprimeix(uint8(data >> 16))
	unmateix.MHexadecimalImprimeix(uint8(data >> 8))
	unmateix.MHexadecimalImprimeix(uint8(data))
}
func (unmateix *TConsola) MUnsignedinteger32Imprimeixxy(data uint32, x uint16, y uint16) {

	unmateix.MHexadecimalImprimeixxy(uint8(data>>24), x+0, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>16), x+2, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>8), x+4, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data), x+6, y)
}
func (unmateix *TConsola) MUnsignedinteger64Imprimeix(data uint64) {
	unmateix.MHexadecimalImprimeix(uint8(data >> 56))
	unmateix.MHexadecimalImprimeix(uint8(data >> 48))
	unmateix.MHexadecimalImprimeix(uint8(data >> 40))
	unmateix.MHexadecimalImprimeix(uint8(data >> 32))
	unmateix.MHexadecimalImprimeix(uint8(data >> 24))
	unmateix.MHexadecimalImprimeix(uint8(data >> 16))
	unmateix.MHexadecimalImprimeix(uint8(data >> 8))
	unmateix.MHexadecimalImprimeix(uint8(data))
}
func (unmateix *TConsola) MUnsignedinteger64Imprimeixxy(data uint64, x uint16, y uint16) {
	unmateix.MHexadecimalImprimeixxy(uint8(data>>56), x+0, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>48), x+2, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>40), x+4, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>32), x+6, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>24), x+8, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>16), x+10, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data>>8), x+12, y)
	unmateix.MHexadecimalImprimeixxy(uint8(data), x+14, y)
}
func MImprimeix(phyaddr uintptr, data uint8, x uint32, y uint32)

func (unmateix *TConsola) MImprimeixhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(data>>4)&0xF]
	buffer[1] = hexadecimal[data&0xF]

	MImprimeix(uintptr(fbphysAdreça), buffer[0], x, y)
	MImprimeix(uintptr(fbphysAdreça), buffer[1], x+2, y)
}

func (unmateix *TConsola) MImprimeixunsignedinteger16(data uint16, x uint32, y uint32) {
	unmateix.MImprimeixhexadecimal(uint8(data>>8), x+0*2, y)
	unmateix.MImprimeixhexadecimal(uint8(data), x+2*2, y)
}

func (unmateix *TConsola) MImprimeixunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	unmateix.MImprimeixhexadecimal(uint8(data>>24), x+0*2, y)
	unmateix.MImprimeixhexadecimal(uint8(data>>16), x+2*2, y)
	unmateix.MImprimeixhexadecimal(uint8(data>>8), x+4*2, y)
	unmateix.MImprimeixhexadecimal(uint8(data), x+6*2, y)
}

func (unmateix *TConsola) M테스트() {
}
