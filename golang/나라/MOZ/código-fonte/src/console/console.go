/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package console

import . "unsafe"

const (
	fbLargura		= 80
	fbAltura		= 25
	fbphysEndereço	uintptr	= 0xb8000
)

type TConsole struct {
	xPosição	uint16
	yPosição	uint16
}

var sériePronto bool

func Sérieinit()
func Sérieescreverocteto(dados uint8)

func MSérieRegistoinit() {
	Sérieinit()
	sériePronto = true
}

func sérieRegistoocteto(dados byte) {
	if !sériePronto {
		return
	}

	if dados == '\n' {
		Sérieescreverocteto('\r')
	}
	Sérieescreverocteto(uint8(dados))
}

func MEmergencyRegistolinha(dados string) {
	for i := 0; i < len(dados); i++ {
		sérieRegistoocteto(dados[i])
	}
}

func MEmergencyRegistohexadecimal8(dados uint8) {
	const digits = "0123456789ABCDEF"
	sérieRegistoocteto(digits[(dados>>4)&0x0F])
	sérieRegistoocteto(digits[dados&0x0F])
}

func MEmergencyRegistounsignedinteger32(dados uint32) {
	MEmergencyRegistohexadecimal8(uint8(dados >> 24))
	MEmergencyRegistohexadecimal8(uint8(dados >> 16))
	MEmergencyRegistohexadecimal8(uint8(dados >> 8))
	MEmergencyRegistohexadecimal8(uint8(dados))
}

func (próprio *TConsole) MImprimir(argumentValor ...interface{}) {
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

	próprio.MImprimirxy(valor_2, x, y)

}
func (próprio *TConsole) MImprimirxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		dados_2, _ := temporary_2.(string)
		próprio.MImprimirbytesxy(([]byte)(dados_2), x, y)
	case uint8:
		dados_2, _ := temporary_2.(uint8)
		próprio.MHexadecimalImprimirxy(dados_2, x, y)
	case uint16:
		dados_2, _ := temporary_2.(uint16)
		próprio.MUnsignedinteger16Imprimirxy(dados_2, x, y)
	case uint32:
		dados_2, _ := temporary_2.(uint32)
		próprio.MUnsignedinteger32Imprimirxy(dados_2, x, y)
	case uint64:
		dados_2, _ := temporary_2.(uint64)
		próprio.MUnsignedinteger64Imprimirxy(dados_2, x, y)
	default:
		dados_2, _ := temporary_2.([]byte)
		próprio.MImprimirbytesxy(dados_2, x, y)
	}

}
func (próprio *TConsole) MImprimirbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		próprio.xPosição = x
	}
	if y <= 999 {
		próprio.yPosição = y
	}

	atributo := uint16(0x0F)
	limite := len(buffer)
	if limite > 4096 {
		limite = 4096
	}
	for i := 0; i < limite; i++ {
		sérieRegistoocteto(buffer[i])
		switch buffer[i] {
		case '\n':
			próprio.yPosição++
			próprio.xPosição = 0
		default:
			*(*uint16)(Pointer(fbphysEndereço + uintptr((80*próprio.yPosição+próprio.xPosição)*2))) = atributo<<8 | uint16(buffer[i])
			próprio.xPosição++
		}

		if próprio.xPosição >= 80 {
			próprio.yPosição++
			próprio.xPosição = 0
		}

		if próprio.yPosição >= 25 {
			for próprio.yPosição = 0; próprio.yPosição < 25; próprio.yPosição++ {
				for próprio.xPosição = 0; próprio.xPosição < 80; próprio.xPosição++ {
					*(*uint16)(Pointer(fbphysEndereço + uintptr((80*próprio.yPosição+próprio.xPosição)*2))) = atributo<<8 | ' '
				}
			}
			próprio.xPosição = 0
			próprio.yPosição = 0
		}

	}

}
func (próprio *TConsole) MHexadecimalImprimir(chave uint8) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(chave>>4)&0xF]
	buffer[1] = hexadecimal[chave&0xF]
	próprio.MImprimir(buffer)
}
func (próprio *TConsole) MHexadecimalImprimirxy(chave uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(chave>>4)&0xF]
	buffer[1] = hexadecimal[chave&0xF]
	próprio.MImprimirxy(buffer, x, y)
}
func (próprio *TConsole) MUnsignedinteger16Imprimir(chave uint16) {
	próprio.MHexadecimalImprimir(uint8(chave >> 8))
	próprio.MHexadecimalImprimir(uint8(chave))
}
func (próprio *TConsole) MUnsignedinteger16Imprimirxy(chave uint16, x uint16, y uint16) {
	próprio.MHexadecimalImprimirxy(uint8(chave>>8), x, y)
	próprio.MHexadecimalImprimirxy(uint8(chave), x, y)
}
func (próprio *TConsole) MUnsignedinteger32Imprimir(dados uint32) {
	próprio.MHexadecimalImprimir(uint8(dados >> 24))
	próprio.MHexadecimalImprimir(uint8(dados >> 16))
	próprio.MHexadecimalImprimir(uint8(dados >> 8))
	próprio.MHexadecimalImprimir(uint8(dados))
}
func (próprio *TConsole) MUnsignedinteger32Imprimirxy(dados uint32, x uint16, y uint16) {

	próprio.MHexadecimalImprimirxy(uint8(dados>>24), x+0, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>16), x+2, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>8), x+4, y)
	próprio.MHexadecimalImprimirxy(uint8(dados), x+6, y)
}
func (próprio *TConsole) MUnsignedinteger64Imprimir(dados uint64) {
	próprio.MHexadecimalImprimir(uint8(dados >> 56))
	próprio.MHexadecimalImprimir(uint8(dados >> 48))
	próprio.MHexadecimalImprimir(uint8(dados >> 40))
	próprio.MHexadecimalImprimir(uint8(dados >> 32))
	próprio.MHexadecimalImprimir(uint8(dados >> 24))
	próprio.MHexadecimalImprimir(uint8(dados >> 16))
	próprio.MHexadecimalImprimir(uint8(dados >> 8))
	próprio.MHexadecimalImprimir(uint8(dados))
}
func (próprio *TConsole) MUnsignedinteger64Imprimirxy(dados uint64, x uint16, y uint16) {
	próprio.MHexadecimalImprimirxy(uint8(dados>>56), x+0, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>48), x+2, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>40), x+4, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>32), x+6, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>24), x+8, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>16), x+10, y)
	próprio.MHexadecimalImprimirxy(uint8(dados>>8), x+12, y)
	próprio.MHexadecimalImprimirxy(uint8(dados), x+14, y)
}
func MImprimir(phyaddr uintptr, dados uint8, x uint32, y uint32)

func (próprio *TConsole) MImprimirhexadecimal(dados uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(dados>>4)&0xF]
	buffer[1] = hexadecimal[dados&0xF]

	MImprimir(uintptr(fbphysEndereço), buffer[0], x, y)
	MImprimir(uintptr(fbphysEndereço), buffer[1], x+2, y)
}

func (próprio *TConsole) MImprimirunsignedinteger16(dados uint16, x uint32, y uint32) {
	próprio.MImprimirhexadecimal(uint8(dados>>8), x+0*2, y)
	próprio.MImprimirhexadecimal(uint8(dados), x+2*2, y)
}

func (próprio *TConsole) MImprimirunsignedinteger32(dados uint32, x uint32, y uint32) {
	x = x * 2
	próprio.MImprimirhexadecimal(uint8(dados>>24), x+0*2, y)
	próprio.MImprimirhexadecimal(uint8(dados>>16), x+2*2, y)
	próprio.MImprimirhexadecimal(uint8(dados>>8), x+4*2, y)
	próprio.MImprimirhexadecimal(uint8(dados), x+6*2, y)
}

func (próprio *TConsole) M테스트() {
}
