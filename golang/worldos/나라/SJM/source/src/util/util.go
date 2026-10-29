/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toTabell(tall uint16) [2]byte {
	var tabell [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tabell[i] = byte(tall >> (8 * i) & 0x00FF)
	}
	return tabell
}
func Unsignedinteger16toTabellbe(tall uint16) [2]byte {
	var tabell [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tabell[2-i] = byte(tall >> (8 * i) & 0x00FF)
	}
	return tabell
}

func Unsignedinteger32toTabell(tall uint32) [4]byte {
	var tabell [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		tabell[i] = byte(tall >> (8 * i) & 0x000000FF)
	}
	return tabell
}
func Unsignedinteger48toTabell(tall uint64) [6]byte {
	var tabell [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tabell[i] = byte(tall >> (8 * i) & 0x00000000FF)
	}
	return tabell
}
func Unsignedinteger48toTabellbe(tall uint64) [6]byte {
	var tabell [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tabell[5-i] = byte(tall >> (8 * i) & 0x00000000FF)
	}
	return tabell
}
func Unsignedinteger64toTabell(tall uint64) [8]byte {
	var tabell [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		tabell[1-i] = byte(tall >> (8 * i) & 0x00000000000000FF)
	}
	return tabell
}
func Tabelltounsignedinteger16(tabell [2]byte) uint16 {
	var tall uint16
	var i uint
	for i = 0; i < 2; i++ {
		tall = tall | (uint16(tabell[1-i]) << (8 * i))
	}
	return tall
}
func Tabelltounsignedinteger32(tabell [4]byte) uint32 {
	var tall uint32
	var i uint
	for i = 0; i < 4; i++ {
		tall = tall | (uint32(tabell[3-i]) << (8 * i))
	}
	return tall
}
func Tabelltounsignedinteger48(tabell [6]byte) uint64 {
	var tall uint64
	var i uint
	for i = 0; i < 6; i++ {
		tall = tall | (uint64(tabell[5-i]) << (8 * i))
	}
	return tall

}
func Tabelltounsignedinteger48be(tabell [6]byte) uint64 {
	var tall uint64
	var i uint
	for i = 0; i < 6; i++ {
		tall = tall | (uint64(tabell[i]) << (8 * i))
	}
	return tall
}
func Tabelltounsignedinteger64(tabell [8]byte) uint64 {
	var tall uint64
	var i uint
	for i = 0; i < 8; i++ {
		tall = tall | (uint64(tabell[7-i]) << (8 * i))
	}
	return tall
}
func Unsignedinteger64r(tall uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(tall>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(tall uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(tall>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(tall uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(tall>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(tall uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(tall>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func SkrivutByte(dataPeker uintptr, størrelse int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPeker))
	var i int
	utilconsole.MSkrivut([]byte("util["))
	for i = 0; i < størrelse; i++ {
		utilconsole.MHexadecimalSkrivut(buffer_2[i])
	}
	utilconsole.MSkrivut([]byte("]"))
}

func Skrivuttest(parametre ...interface{}) {
	for _, param := range parametre {
		utilconsole.MSkrivut([]byte(TypeOf(param).Name()))

	}
}
func LikByte(a, b []byte) bool {
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
func BytetoStreng(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPekerTabellfromPeker(peker_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{peker_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32TabellfromPeker(peker_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{peker_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytefromPeker(peker_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{peker_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPekerfromPeker(peker_2 uintptr) func() {
	code1Peker_2 := uintptr(Pointer(&peker_2))
	return *(*func())(Pointer(&code1Peker_2))
}
