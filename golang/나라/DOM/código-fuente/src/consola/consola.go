package consola

import . "unsafe"

const (
	fbAncho			= 80
	fbAltura		= 25
	fbphysDirección	uintptr	= 0xb8000
)

type TConsola struct {
	xPosición	uint16
	yPosición	uint16
}

var seriePreparado bool

func Serieinit()
func Serieescribirocteto(datos uint8)

func MSerieRegistroinit() {
	Serieinit()
	seriePreparado = true
}

func serieRegistroocteto(datos byte) {
	if !seriePreparado {
		return
	}

	if datos == '\n' {
		Serieescribirocteto('\r')
	}
	Serieescribirocteto(uint8(datos))
}

func MEmergencyRegistroCadena(datos string) {
	for i := 0; i < len(datos); i++ {
		serieRegistroocteto(datos[i])
	}
}

func MEmergencyRegistrohexadecimal8(datos uint8) {
	const digits = "0123456789ABCDEF"
	serieRegistroocteto(digits[(datos>>4)&0x0F])
	serieRegistroocteto(digits[datos&0x0F])
}

func MEmergencyRegistrounsignedinteger32(datos uint32) {
	MEmergencyRegistrohexadecimal8(uint8(datos >> 24))
	MEmergencyRegistrohexadecimal8(uint8(datos >> 16))
	MEmergencyRegistrohexadecimal8(uint8(datos >> 8))
	MEmergencyRegistrohexadecimal8(uint8(datos))
}

func (propio *TConsola) MImprimir(argumentValor ...interface{}) {
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

	propio.MImprimirxy(valor_2, x, y)

}
func (propio *TConsola) MImprimirxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		datos_2, _ := temporary_2.(string)
		propio.MImprimirbytesxy(([]byte)(datos_2), x, y)
	case uint8:
		datos_2, _ := temporary_2.(uint8)
		propio.MHexadecimalImprimirxy(datos_2, x, y)
	case uint16:
		datos_2, _ := temporary_2.(uint16)
		propio.MUnsignedinteger16Imprimirxy(datos_2, x, y)
	case uint32:
		datos_2, _ := temporary_2.(uint32)
		propio.MUnsignedinteger32Imprimirxy(datos_2, x, y)
	case uint64:
		datos_2, _ := temporary_2.(uint64)
		propio.MUnsignedinteger64Imprimirxy(datos_2, x, y)
	default:
		datos_2, _ := temporary_2.([]byte)
		propio.MImprimirbytesxy(datos_2, x, y)
	}

}
func (propio *TConsola) MImprimirbytesxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		propio.xPosición = x
	}
	if y <= 999 {
		propio.yPosición = y
	}

	atributo := uint16(0x0F)
	limitar := len(buffer)
	if limitar > 4096 {
		limitar = 4096
	}
	for i := 0; i < limitar; i++ {
		serieRegistroocteto(buffer[i])
		switch buffer[i] {
		case '\n':
			propio.yPosición++
			propio.xPosición = 0
		default:
			*(*uint16)(Pointer(fbphysDirección + uintptr((80*propio.yPosición+propio.xPosición)*2))) = atributo<<8 | uint16(buffer[i])
			propio.xPosición++
		}

		if propio.xPosición >= 80 {
			propio.yPosición++
			propio.xPosición = 0
		}

		if propio.yPosición >= 25 {
			for propio.yPosición = 0; propio.yPosición < 25; propio.yPosición++ {
				for propio.xPosición = 0; propio.xPosición < 80; propio.xPosición++ {
					*(*uint16)(Pointer(fbphysDirección + uintptr((80*propio.yPosición+propio.xPosición)*2))) = atributo<<8 | ' '
				}
			}
			propio.xPosición = 0
			propio.yPosición = 0
		}

	}

}
func (propio *TConsola) MHexadecimalImprimir(clave uint8) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(clave>>4)&0xF]
	buffer[1] = hexadecimal[clave&0xF]
	propio.MImprimir(buffer)
}
func (propio *TConsola) MHexadecimalImprimirxy(clave uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(clave>>4)&0xF]
	buffer[1] = hexadecimal[clave&0xF]
	propio.MImprimirxy(buffer, x, y)
}
func (propio *TConsola) MUnsignedinteger16Imprimir(clave uint16) {
	propio.MHexadecimalImprimir(uint8(clave >> 8))
	propio.MHexadecimalImprimir(uint8(clave))
}
func (propio *TConsola) MUnsignedinteger16Imprimirxy(clave uint16, x uint16, y uint16) {
	propio.MHexadecimalImprimirxy(uint8(clave>>8), x, y)
	propio.MHexadecimalImprimirxy(uint8(clave), x, y)
}
func (propio *TConsola) MUnsignedinteger32Imprimir(datos uint32) {
	propio.MHexadecimalImprimir(uint8(datos >> 24))
	propio.MHexadecimalImprimir(uint8(datos >> 16))
	propio.MHexadecimalImprimir(uint8(datos >> 8))
	propio.MHexadecimalImprimir(uint8(datos))
}
func (propio *TConsola) MUnsignedinteger32Imprimirxy(datos uint32, x uint16, y uint16) {

	propio.MHexadecimalImprimirxy(uint8(datos>>24), x+0, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>16), x+2, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>8), x+4, y)
	propio.MHexadecimalImprimirxy(uint8(datos), x+6, y)
}
func (propio *TConsola) MUnsignedinteger64Imprimir(datos uint64) {
	propio.MHexadecimalImprimir(uint8(datos >> 56))
	propio.MHexadecimalImprimir(uint8(datos >> 48))
	propio.MHexadecimalImprimir(uint8(datos >> 40))
	propio.MHexadecimalImprimir(uint8(datos >> 32))
	propio.MHexadecimalImprimir(uint8(datos >> 24))
	propio.MHexadecimalImprimir(uint8(datos >> 16))
	propio.MHexadecimalImprimir(uint8(datos >> 8))
	propio.MHexadecimalImprimir(uint8(datos))
}
func (propio *TConsola) MUnsignedinteger64Imprimirxy(datos uint64, x uint16, y uint16) {
	propio.MHexadecimalImprimirxy(uint8(datos>>56), x+0, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>48), x+2, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>40), x+4, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>32), x+6, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>24), x+8, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>16), x+10, y)
	propio.MHexadecimalImprimirxy(uint8(datos>>8), x+12, y)
	propio.MHexadecimalImprimirxy(uint8(datos), x+14, y)
}
func MImprimir(phyaddr uintptr, datos uint8, x uint32, y uint32)

func (propio *TConsola) MImprimirhexadecimal(datos uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = hexadecimal[(datos>>4)&0xF]
	buffer[1] = hexadecimal[datos&0xF]

	MImprimir(uintptr(fbphysDirección), buffer[0], x, y)
	MImprimir(uintptr(fbphysDirección), buffer[1], x+2, y)
}

func (propio *TConsola) MImprimirunsignedinteger16(datos uint16, x uint32, y uint32) {
	propio.MImprimirhexadecimal(uint8(datos>>8), x+0*2, y)
	propio.MImprimirhexadecimal(uint8(datos), x+2*2, y)
}

func (propio *TConsola) MImprimirunsignedinteger32(datos uint32, x uint32, y uint32) {
	x = x * 2
	propio.MImprimirhexadecimal(uint8(datos>>24), x+0*2, y)
	propio.MImprimirhexadecimal(uint8(datos>>16), x+2*2, y)
	propio.MImprimirhexadecimal(uint8(datos>>8), x+4*2, y)
	propio.MImprimirhexadecimal(uint8(datos), x+6*2, y)
}

func (propio *TConsola) M테스트() {
}
