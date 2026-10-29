/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toSerie(numero uint16) [2]byte {
	var serie [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		serie[i] = byte(numero >> (8 * i) & 0x00FF)
	}
	return serie
}
func Unsignedinteger16toSeriebe(numero uint16) [2]byte {
	var serie [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		serie[2-i] = byte(numero >> (8 * i) & 0x00FF)
	}
	return serie
}

func Unsignedinteger32toSerie(numero uint32) [4]byte {
	var serie [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		serie[i] = byte(numero >> (8 * i) & 0x000000FF)
	}
	return serie
}
func Unsignedinteger48toSerie(numero uint64) [6]byte {
	var serie [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		serie[i] = byte(numero >> (8 * i) & 0x00000000FF)
	}
	return serie
}
func Unsignedinteger48toSeriebe(numero uint64) [6]byte {
	var serie [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		serie[5-i] = byte(numero >> (8 * i) & 0x00000000FF)
	}
	return serie
}
func Unsignedinteger64toSerie(numero uint64) [8]byte {
	var serie [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		serie[1-i] = byte(numero >> (8 * i) & 0x00000000000000FF)
	}
	return serie
}
func Serietounsignedinteger16(serie [2]byte) uint16 {
	var numero uint16
	var i uint
	for i = 0; i < 2; i++ {
		numero = numero | (uint16(serie[1-i]) << (8 * i))
	}
	return numero
}
func Serietounsignedinteger32(serie [4]byte) uint32 {
	var numero uint32
	var i uint
	for i = 0; i < 4; i++ {
		numero = numero | (uint32(serie[3-i]) << (8 * i))
	}
	return numero
}
func Serietounsignedinteger48(serie [6]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 6; i++ {
		numero = numero | (uint64(serie[5-i]) << (8 * i))
	}
	return numero

}
func Serietounsignedinteger48be(serie [6]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 6; i++ {
		numero = numero | (uint64(serie[i]) << (8 * i))
	}
	return numero
}
func Serietounsignedinteger64(serie [8]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 8; i++ {
		numero = numero | (uint64(serie[7-i]) << (8 * i))
	}
	return numero
}
func Unsignedinteger64r(numero uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(numero>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(numero uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(numero>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(numero uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(numero>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(numero uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(numero>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func StampaByte(dataPuntatore uintptr, dimensione int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPuntatore))
	var i int
	utilconsole.MStampa([]byte("util["))
	for i = 0; i < dimensione; i++ {
		utilconsole.MHexadecimalStampa(buffer_2[i])
	}
	utilconsole.MStampa([]byte("]"))
}

func StampaProva(parametri ...interface{}) {
	for _, param := range parametri {
		utilconsole.MStampa([]byte(TypeOf(param).Name()))

	}
}
func UgualeByte(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}
func BytetoStringa(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPuntatoreSeriefromPuntatore(riferimento_di_memoria_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{riferimento_di_memoria_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32SeriefromPuntatore(riferimento_di_memoria_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{riferimento_di_memoria_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytefromPuntatore(riferimento_di_memoria_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{riferimento_di_memoria_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPuntatorefromPuntatore(riferimento_di_memoria_2 uintptr) func() {
	code1Puntatore_2 := uintptr(Pointer(&riferimento_di_memoria_2))
	return *(*func())(Pointer(&code1Puntatore_2))
}
