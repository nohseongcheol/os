package консоль

import . "unsafe"

const (
	fbШирина		= 80
	fbВисота		= 25
	fbphysАдреса	uintptr	= 0xb8000
)

type TКонсоль struct {
	xПозиція	uint16
	yПозиція	uint16
}

var послідовнийГотово bool

func Послідовнийinit()
func ПослідовнийЗаписbyte(data uint8)

func MПослідовнийЖурналinit() {
	Послідовнийinit()
	послідовнийГотово = true
}

func послідовнийЖурналbyte(data byte) {
	if !послідовнийГотово {
		return
	}

	if data == '\n' {
		ПослідовнийЗаписbyte('\r')
	}
	ПослідовнийЗаписbyte(uint8(data))
}

func MEmergencyЖурналРядок(data string) {
	for i := 0; i < len(data); i++ {
		послідовнийЖурналbyte(data[i])
	}
}

func MEmergencyЖурналhexadecimal8(data uint8) {
	const digits = "0123456789ABCDEF"
	послідовнийЖурналbyte(digits[(data>>4)&0x0F])
	послідовнийЖурналbyte(digits[data&0x0F])
}

func MEmergencyЖурналunsignedinteger32(data uint32) {
	MEmergencyЖурналhexadecimal8(uint8(data >> 24))
	MEmergencyЖурналhexadecimal8(uint8(data >> 16))
	MEmergencyЖурналhexadecimal8(uint8(data >> 8))
	MEmergencyЖурналhexadecimal8(uint8(data))
}

func (поточний *TКонсоль) MДрук(argumentЗначення ...interface{}) {
	var x uint16 = 1000
	var y uint16 = 1000
	var значення_3 interface{}

	for i, p := range argumentЗначення {
		switch i {
		case 0:
			param, _ := p.(interface{})
			значення_3 = param
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

	поточний.MДрукxy(значення_3, x, y)

}
func (поточний *TКонсоль) MДрукxy(temporary_2 interface{}, x uint16, y uint16) {

	switch temporary_2.(type) {
	case string:
		data_2, _ := temporary_2.(string)
		поточний.MДрукБайтxy(([]byte)(data_2), x, y)
	case uint8:
		data_2, _ := temporary_2.(uint8)
		поточний.MHexadecimalДрукxy(data_2, x, y)
	case uint16:
		data_2, _ := temporary_2.(uint16)
		поточний.MUnsignedinteger16Друкxy(data_2, x, y)
	case uint32:
		data_2, _ := temporary_2.(uint32)
		поточний.MUnsignedinteger32Друкxy(data_2, x, y)
	case uint64:
		data_2, _ := temporary_2.(uint64)
		поточний.MUnsignedinteger64Друкxy(data_2, x, y)
	default:
		data_2, _ := temporary_2.([]byte)
		поточний.MДрукБайтxy(data_2, x, y)
	}

}
func (поточний *TКонсоль) MДрукБайтxy(buffer []byte, x uint16, y uint16) {

	if x <= 999 {
		поточний.xПозиція = x
	}
	if y <= 999 {
		поточний.yПозиція = y
	}

	ознака := uint16(0x0F)
	обмеження := len(buffer)
	if обмеження > 4096 {
		обмеження = 4096
	}
	for i := 0; i < обмеження; i++ {
		послідовнийЖурналbyte(buffer[i])
		switch buffer[i] {
		case '\n':
			поточний.yПозиція++
			поточний.xПозиція = 0
		default:
			*(*uint16)(Pointer(fbphysАдреса + uintptr((80*поточний.yПозиція+поточний.xПозиція)*2))) = ознака<<8 | uint16(buffer[i])
			поточний.xПозиція++
		}

		if поточний.xПозиція >= 80 {
			поточний.yПозиція++
			поточний.xПозиція = 0
		}

		if поточний.yПозиція >= 25 {
			for поточний.yПозиція = 0; поточний.yПозиція < 25; поточний.yПозиція++ {
				for поточний.xПозиція = 0; поточний.xПозиція < 80; поточний.xПозиція++ {
					*(*uint16)(Pointer(fbphysАдреса + uintptr((80*поточний.yПозиція+поточний.xПозиція)*2))) = ознака<<8 | ' '
				}
			}
			поточний.xПозиція = 0
			поточний.yПозиція = 0
		}

	}

}
func (поточний *TКонсоль) MHexadecimalДрук(ключ uint8) {
	buffer := []byte{'0', '0'}
	шістнадцяткова := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шістнадцяткова[(ключ>>4)&0xF]
	buffer[1] = шістнадцяткова[ключ&0xF]
	поточний.MДрук(buffer)
}
func (поточний *TКонсоль) MHexadecimalДрукxy(ключ uint8, x uint16, y uint16) {
	buffer := []byte{'0', '0', 0}
	шістнадцяткова := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шістнадцяткова[(ключ>>4)&0xF]
	buffer[1] = шістнадцяткова[ключ&0xF]
	поточний.MДрукxy(buffer, x, y)
}
func (поточний *TКонсоль) MUnsignedinteger16Друк(ключ uint16) {
	поточний.MHexadecimalДрук(uint8(ключ >> 8))
	поточний.MHexadecimalДрук(uint8(ключ))
}
func (поточний *TКонсоль) MUnsignedinteger16Друкxy(ключ uint16, x uint16, y uint16) {
	поточний.MHexadecimalДрукxy(uint8(ключ>>8), x, y)
	поточний.MHexadecimalДрукxy(uint8(ключ), x, y)
}
func (поточний *TКонсоль) MUnsignedinteger32Друк(data uint32) {
	поточний.MHexadecimalДрук(uint8(data >> 24))
	поточний.MHexadecimalДрук(uint8(data >> 16))
	поточний.MHexadecimalДрук(uint8(data >> 8))
	поточний.MHexadecimalДрук(uint8(data))
}
func (поточний *TКонсоль) MUnsignedinteger32Друкxy(data uint32, x uint16, y uint16) {

	поточний.MHexadecimalДрукxy(uint8(data>>24), x+0, y)
	поточний.MHexadecimalДрукxy(uint8(data>>16), x+2, y)
	поточний.MHexadecimalДрукxy(uint8(data>>8), x+4, y)
	поточний.MHexadecimalДрукxy(uint8(data), x+6, y)
}
func (поточний *TКонсоль) MUnsignedinteger64Друк(data uint64) {
	поточний.MHexadecimalДрук(uint8(data >> 56))
	поточний.MHexadecimalДрук(uint8(data >> 48))
	поточний.MHexadecimalДрук(uint8(data >> 40))
	поточний.MHexadecimalДрук(uint8(data >> 32))
	поточний.MHexadecimalДрук(uint8(data >> 24))
	поточний.MHexadecimalДрук(uint8(data >> 16))
	поточний.MHexadecimalДрук(uint8(data >> 8))
	поточний.MHexadecimalДрук(uint8(data))
}
func (поточний *TКонсоль) MUnsignedinteger64Друкxy(data uint64, x uint16, y uint16) {
	поточний.MHexadecimalДрукxy(uint8(data>>56), x+0, y)
	поточний.MHexadecimalДрукxy(uint8(data>>48), x+2, y)
	поточний.MHexadecimalДрукxy(uint8(data>>40), x+4, y)
	поточний.MHexadecimalДрукxy(uint8(data>>32), x+6, y)
	поточний.MHexadecimalДрукxy(uint8(data>>24), x+8, y)
	поточний.MHexadecimalДрукxy(uint8(data>>16), x+10, y)
	поточний.MHexadecimalДрукxy(uint8(data>>8), x+12, y)
	поточний.MHexadecimalДрукxy(uint8(data), x+14, y)
}
func MДрук(phyaddr uintptr, data uint8, x uint32, y uint32)

func (поточний *TКонсоль) MДрукhexadecimal(data uint8, x uint32, y uint32) {
	buffer := []byte{'0', '0'}
	шістнадцяткова := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}
	buffer[0] = шістнадцяткова[(data>>4)&0xF]
	buffer[1] = шістнадцяткова[data&0xF]

	MДрук(uintptr(fbphysАдреса), buffer[0], x, y)
	MДрук(uintptr(fbphysАдреса), buffer[1], x+2, y)
}

func (поточний *TКонсоль) MДрукunsignedinteger16(data uint16, x uint32, y uint32) {
	поточний.MДрукhexadecimal(uint8(data>>8), x+0*2, y)
	поточний.MДрукhexadecimal(uint8(data), x+2*2, y)
}

func (поточний *TКонсоль) MДрукunsignedinteger32(data uint32, x uint32, y uint32) {
	x = x * 2
	поточний.MДрукhexadecimal(uint8(data>>24), x+0*2, y)
	поточний.MДрукhexadecimal(uint8(data>>16), x+2*2, y)
	поточний.MДрукhexadecimal(uint8(data>>8), x+4*2, y)
	поточний.MДрукhexadecimal(uint8(data), x+6*2, y)
}

func (поточний *TКонсоль) M테스트() {
}
