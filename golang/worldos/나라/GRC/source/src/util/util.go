/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toΔιάταξη(αριθμός uint16) [2]byte {
	var διάταξη [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		διάταξη[i] = byte(αριθμός >> (8 * i) & 0x00FF)
	}
	return διάταξη
}
func Unsignedinteger16toΔιάταξηbe(αριθμός uint16) [2]byte {
	var διάταξη [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		διάταξη[2-i] = byte(αριθμός >> (8 * i) & 0x00FF)
	}
	return διάταξη
}

func Unsignedinteger32toΔιάταξη(αριθμός uint32) [4]byte {
	var διάταξη [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		διάταξη[i] = byte(αριθμός >> (8 * i) & 0x000000FF)
	}
	return διάταξη
}
func Unsignedinteger48toΔιάταξη(αριθμός uint64) [6]byte {
	var διάταξη [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		διάταξη[i] = byte(αριθμός >> (8 * i) & 0x00000000FF)
	}
	return διάταξη
}
func Unsignedinteger48toΔιάταξηbe(αριθμός uint64) [6]byte {
	var διάταξη [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		διάταξη[5-i] = byte(αριθμός >> (8 * i) & 0x00000000FF)
	}
	return διάταξη
}
func Unsignedinteger64toΔιάταξη(αριθμός uint64) [8]byte {
	var διάταξη [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		διάταξη[1-i] = byte(αριθμός >> (8 * i) & 0x00000000000000FF)
	}
	return διάταξη
}
func Διάταξηtounsignedinteger16(διάταξη [2]byte) uint16 {
	var αριθμός uint16
	var i uint
	for i = 0; i < 2; i++ {
		αριθμός = αριθμός | (uint16(διάταξη[1-i]) << (8 * i))
	}
	return αριθμός
}
func Διάταξηtounsignedinteger32(διάταξη [4]byte) uint32 {
	var αριθμός uint32
	var i uint
	for i = 0; i < 4; i++ {
		αριθμός = αριθμός | (uint32(διάταξη[3-i]) << (8 * i))
	}
	return αριθμός
}
func Διάταξηtounsignedinteger48(διάταξη [6]byte) uint64 {
	var αριθμός uint64
	var i uint
	for i = 0; i < 6; i++ {
		αριθμός = αριθμός | (uint64(διάταξη[5-i]) << (8 * i))
	}
	return αριθμός

}
func Διάταξηtounsignedinteger48be(διάταξη [6]byte) uint64 {
	var αριθμός uint64
	var i uint
	for i = 0; i < 6; i++ {
		αριθμός = αριθμός | (uint64(διάταξη[i]) << (8 * i))
	}
	return αριθμός
}
func Διάταξηtounsignedinteger64(διάταξη [8]byte) uint64 {
	var αριθμός uint64
	var i uint
	for i = 0; i < 8; i++ {
		αριθμός = αριθμός | (uint64(διάταξη[7-i]) << (8 * i))
	}
	return αριθμός
}
func Unsignedinteger64r(αριθμός uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(αριθμός>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(αριθμός uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(αριθμός>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(αριθμός uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(αριθμός>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(αριθμός uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(αριθμός>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Εκτύπωσηbytes(dataΔείκτης uintptr, μέγεθος int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataΔείκτης))
	var i int
	utilconsole.MΕκτύπωση([]byte("util["))
	for i = 0; i < μέγεθος; i++ {
		utilconsole.MHexadecimalΕκτύπωση(buffer_2[i])
	}
	utilconsole.MΕκτύπωση([]byte("]"))
}

func ΕκτύπωσηΔοκιμή(παράμετροι_3 ...interface{}) {
	for _, param := range παράμετροι_3 {
		utilconsole.MΕκτύπωση([]byte(TypeOf(param).Name()))

	}
}
func Ίσοbytes(a, b []byte) bool {
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
func BytestoΣυμβολοσειρά(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerΔείκτηςΔιάταξηfromΔείκτης(δείκτης_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{δείκτης_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ΔιάταξηfromΔείκτης(δείκτης_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{δείκτης_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbytesfromΔείκτης(δείκτης_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{δείκτης_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncΔείκτηςfromΔείκτης(δείκτης_2 uintptr) func() {
	code1Δείκτης_2 := uintptr(Pointer(&δείκτης_2))
	return *(*func())(Pointer(&code1Δείκτης_2))
}
