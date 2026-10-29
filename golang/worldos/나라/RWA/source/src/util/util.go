/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toImbonerahamwe(number uint16) [2]byte {
	var imbonerahamwe [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		imbonerahamwe[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return imbonerahamwe
}
func Unsignedinteger16toImbonerahamwebe(number uint16) [2]byte {
	var imbonerahamwe [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		imbonerahamwe[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return imbonerahamwe
}

func Unsignedinteger32toImbonerahamwe(number uint32) [4]byte {
	var imbonerahamwe [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		imbonerahamwe[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return imbonerahamwe
}
func Unsignedinteger48toImbonerahamwe(number uint64) [6]byte {
	var imbonerahamwe [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		imbonerahamwe[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return imbonerahamwe
}
func Unsignedinteger48toImbonerahamwebe(number uint64) [6]byte {
	var imbonerahamwe [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		imbonerahamwe[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return imbonerahamwe
}
func Unsignedinteger64toImbonerahamwe(number uint64) [8]byte {
	var imbonerahamwe [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		imbonerahamwe[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return imbonerahamwe
}
func Imbonerahamwetounsignedinteger16(imbonerahamwe [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(imbonerahamwe[1-i]) << (8 * i))
	}
	return number
}
func Imbonerahamwetounsignedinteger32(imbonerahamwe [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(imbonerahamwe[3-i]) << (8 * i))
	}
	return number
}
func Imbonerahamwetounsignedinteger48(imbonerahamwe [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(imbonerahamwe[5-i]) << (8 * i))
	}
	return number

}
func Imbonerahamwetounsignedinteger48be(imbonerahamwe [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(imbonerahamwe[i]) << (8 * i))
	}
	return number
}
func Imbonerahamwetounsignedinteger64(imbonerahamwe [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(imbonerahamwe[7-i]) << (8 * i))
	}
	return number
}
func Unsignedinteger64r(number uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(number>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(number uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(number>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(number uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(number>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(number uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(number>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func GucapaBayite(datapointer uintptr, ingano int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(datapointer))
	var i int
	utilconsole.MGucapa([]byte("util["))
	for i = 0; i < ingano; i++ {
		utilconsole.MHexadecimalGucapa(buffer_2[i])
	}
	utilconsole.MGucapa([]byte("]"))
}

func Gucapatest(params ...interface{}) {
	for _, param := range params {
		utilconsole.MGucapa([]byte(TypeOf(param).Name()))

	}
}
func EqualBayite(a, b []byte) bool {
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
func Bayitetostring(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerpointerImbonerahamwefrompointer(pointer_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32Imbonerahamwefrompointer(pointer_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBayitefrompointer(pointer_2 uintptr, len int, cap int) []byte {
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
