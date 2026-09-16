/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toarray(broj uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[i] = byte(broj >> (8 * i) & 0x00FF)
	}
	return array
}
func Unsignedinteger16toarraybe(broj uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[2-i] = byte(broj >> (8 * i) & 0x00FF)
	}
	return array
}

func Unsignedinteger32toarray(broj uint32) [4]byte {
	var array [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[i] = byte(broj >> (8 * i) & 0x000000FF)
	}
	return array
}
func Unsignedinteger48toarray(broj uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[i] = byte(broj >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger48toarraybe(broj uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[5-i] = byte(broj >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger64toarray(broj uint64) [8]byte {
	var array [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[1-i] = byte(broj >> (8 * i) & 0x00000000000000FF)
	}
	return array
}
func Arraytounsignedinteger16(array [2]byte) uint16 {
	var broj uint16
	var i uint
	for i = 0; i < 2; i++ {
		broj = broj | (uint16(array[1-i]) << (8 * i))
	}
	return broj
}
func Arraytounsignedinteger32(array [4]byte) uint32 {
	var broj uint32
	var i uint
	for i = 0; i < 4; i++ {
		broj = broj | (uint32(array[3-i]) << (8 * i))
	}
	return broj
}
func Arraytounsignedinteger48(array [6]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 6; i++ {
		broj = broj | (uint64(array[5-i]) << (8 * i))
	}
	return broj

}
func Arraytounsignedinteger48be(array [6]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 6; i++ {
		broj = broj | (uint64(array[i]) << (8 * i))
	}
	return broj
}
func Arraytounsignedinteger64(array [8]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 8; i++ {
		broj = broj | (uint64(array[7-i]) << (8 * i))
	}
	return broj
}
func Unsignedinteger64r(broj uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(broj>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(broj uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(broj>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(broj uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(broj>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(broj uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(broj>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ŠtampajBajtova(datapointer uintptr, veličina int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(datapointer))
	var i int
	utilconsole.MŠtampaj([]byte("util["))
	for i = 0; i < veličina; i++ {
		utilconsole.MHexadecimalŠtampaj(buffer_2[i])
	}
	utilconsole.MŠtampaj([]byte("]"))
}

func Štampajtest(parametri ...interface{}) {
	for _, param := range parametri {
		utilconsole.MŠtampaj([]byte(TypeOf(param).Name()))

	}
}
func EqualBajtova(a, b []byte) bool {
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
func BajtovatoNIZ(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerpointerarrayfrompointer(pointer_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32arrayfrompointer(pointer_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBajtovafrompointer(pointer_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncpointerfrompointer(pointer_2 uintptr) func() {
	code1pointer_2 := uintptr(Pointer(&pointer_2))
	return *(*func())(Pointer(&code1pointer_2))
}
