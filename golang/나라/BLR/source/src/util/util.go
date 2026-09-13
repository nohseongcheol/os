package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toМасіў(нУМАР uint16) [2]byte {
	var масіў [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масіў[i] = byte(нУМАР >> (8 * i) & 0x00FF)
	}
	return масіў
}
func Unsignedinteger16toМасіўbe(нУМАР uint16) [2]byte {
	var масіў [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масіў[2-i] = byte(нУМАР >> (8 * i) & 0x00FF)
	}
	return масіў
}

func Unsignedinteger32toМасіў(нУМАР uint32) [4]byte {
	var масіў [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		масіў[i] = byte(нУМАР >> (8 * i) & 0x000000FF)
	}
	return масіў
}
func Unsignedinteger48toМасіў(нУМАР uint64) [6]byte {
	var масіў [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масіў[i] = byte(нУМАР >> (8 * i) & 0x00000000FF)
	}
	return масіў
}
func Unsignedinteger48toМасіўbe(нУМАР uint64) [6]byte {
	var масіў [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масіў[5-i] = byte(нУМАР >> (8 * i) & 0x00000000FF)
	}
	return масіў
}
func Unsignedinteger64toМасіў(нУМАР uint64) [8]byte {
	var масіў [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		масіў[1-i] = byte(нУМАР >> (8 * i) & 0x00000000000000FF)
	}
	return масіў
}
func Масіўtounsignedinteger16(масіў [2]byte) uint16 {
	var нУМАР uint16
	var i uint
	for i = 0; i < 2; i++ {
		нУМАР = нУМАР | (uint16(масіў[1-i]) << (8 * i))
	}
	return нУМАР
}
func Масіўtounsignedinteger32(масіў [4]byte) uint32 {
	var нУМАР uint32
	var i uint
	for i = 0; i < 4; i++ {
		нУМАР = нУМАР | (uint32(масіў[3-i]) << (8 * i))
	}
	return нУМАР
}
func Масіўtounsignedinteger48(масіў [6]byte) uint64 {
	var нУМАР uint64
	var i uint
	for i = 0; i < 6; i++ {
		нУМАР = нУМАР | (uint64(масіў[5-i]) << (8 * i))
	}
	return нУМАР

}
func Масіўtounsignedinteger48be(масіў [6]byte) uint64 {
	var нУМАР uint64
	var i uint
	for i = 0; i < 6; i++ {
		нУМАР = нУМАР | (uint64(масіў[i]) << (8 * i))
	}
	return нУМАР
}
func Масіўtounsignedinteger64(масіў [8]byte) uint64 {
	var нУМАР uint64
	var i uint
	for i = 0; i < 8; i++ {
		нУМАР = нУМАР | (uint64(масіў[7-i]) << (8 * i))
	}
	return нУМАР
}
func Unsignedinteger64r(нУМАР uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(нУМАР>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(нУМАР uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(нУМАР>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(нУМАР uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(нУМАР>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(нУМАР uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(нУМАР>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ДрукавацьБайтаў(dataПаказальнік uintptr, памер int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataПаказальнік))
	var i int
	utilconsole.MДрукаваць([]byte("util["))
	for i = 0; i < памер; i++ {
		utilconsole.MHexadecimalДрукаваць(buffer_2[i])
	}
	utilconsole.MДрукаваць([]byte("]"))
}

func ДрукавацьПраверка(params ...interface{}) {
	for _, param := range params {
		utilconsole.MДрукаваць([]byte(TypeOf(param).Name()))

	}
}
func АднолькавыБайтаў(a, b []byte) bool {
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
func БайтаўtoРадок(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerПаказальнікМасіўfromПаказальнік(паказальнік_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{паказальнік_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32МасіўfromПаказальнік(паказальнік_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{паказальнік_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБайтаўfromПаказальнік(паказальнік_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{паказальнік_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncПаказальнікfromПаказальнік(паказальнік_2 uintptr) func() {
	code1Паказальнік_2 := uintptr(Pointer(&паказальнік_2))
	return *(*func())(Pointer(&code1Паказальнік_2))
}
