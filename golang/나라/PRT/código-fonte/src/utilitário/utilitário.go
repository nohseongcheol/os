/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package utilitário

import . "console"
import . "unsafe"
import . "reflect"

var utilitárioconsole TConsole = TConsole{}

func Unsignedinteger16paramatriz(número uint16) [2]byte {
	var matriz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		matriz[i] = byte(número >> (8 * i) & 0x00FF)
	}
	return matriz
}
func Unsignedinteger16paramatrizbe(número uint16) [2]byte {
	var matriz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		matriz[2-i] = byte(número >> (8 * i) & 0x00FF)
	}
	return matriz
}

func Unsignedinteger32paramatriz(número uint32) [4]byte {
	var matriz [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		matriz[i] = byte(número >> (8 * i) & 0x000000FF)
	}
	return matriz
}
func Unsignedinteger48paramatriz(número uint64) [6]byte {
	var matriz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		matriz[i] = byte(número >> (8 * i) & 0x00000000FF)
	}
	return matriz
}
func Unsignedinteger48paramatrizbe(número uint64) [6]byte {
	var matriz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		matriz[5-i] = byte(número >> (8 * i) & 0x00000000FF)
	}
	return matriz
}
func Unsignedinteger64paramatriz(número uint64) [8]byte {
	var matriz [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		matriz[1-i] = byte(número >> (8 * i) & 0x00000000000000FF)
	}
	return matriz
}
func Matrizparaunsignedinteger16(matriz [2]byte) uint16 {
	var número uint16
	var i uint
	for i = 0; i < 2; i++ {
		número = número | (uint16(matriz[1-i]) << (8 * i))
	}
	return número
}
func Matrizparaunsignedinteger32(matriz [4]byte) uint32 {
	var número uint32
	var i uint
	for i = 0; i < 4; i++ {
		número = número | (uint32(matriz[3-i]) << (8 * i))
	}
	return número
}
func Matrizparaunsignedinteger48(matriz [6]byte) uint64 {
	var número uint64
	var i uint
	for i = 0; i < 6; i++ {
		número = número | (uint64(matriz[5-i]) << (8 * i))
	}
	return número

}
func Matrizparaunsignedinteger48be(matriz [6]byte) uint64 {
	var número uint64
	var i uint
	for i = 0; i < 6; i++ {
		número = número | (uint64(matriz[i]) << (8 * i))
	}
	return número
}
func Matrizparaunsignedinteger64(matriz [8]byte) uint64 {
	var número uint64
	var i uint
	for i = 0; i < 8; i++ {
		número = número | (uint64(matriz[7-i]) << (8 * i))
	}
	return número
}
func Unsignedinteger64r(número uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(número>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(número uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(número>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(número uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(número>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(número uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(número>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Imprimirbytes(dadosPonteiro uintptr, tamanho int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dadosPonteiro))
	var i int
	utilitárioconsole.MImprimir([]byte("util["))
	for i = 0; i < tamanho; i++ {
		utilitárioconsole.MHexadecimalImprimir(buffer_2[i])
	}
	utilitárioconsole.MImprimir([]byte("]"))
}

func ImprimirTestar(parâmetros_2 ...interface{}) {
	for _, param := range parâmetros_2 {
		utilitárioconsole.MImprimir([]byte(TypeOf(param).Name()))

	}
}
func Igualbytes(a, b []byte) bool {
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
func Bytesparalinha(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPonteiromatrizdePonteiro(referência_de_memória_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		endereço	uintptr
		len		int
		cap		int
	}{referência_de_memória_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32matrizdePonteiro(referência_de_memória_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		endereço	uintptr
		len		int
		cap		int
	}{referência_de_memória_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbytesdePonteiro(referência_de_memória_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		endereço	uintptr
		len		int
		cap		int
	}{referência_de_memória_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPonteirodePonteiro(referência_de_memória_2 uintptr) func() {
	code1Ponteiro_2 := uintptr(Pointer(&referência_de_memória_2))
	return *(*func())(Pointer(&code1Ponteiro_2))
}
