/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toМасив(число uint16) [2]byte {
	var масив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масив[i] = byte(число >> (8 * i) & 0x00FF)
	}
	return масив
}
func Unsignedinteger16toМасивbe(число uint16) [2]byte {
	var масив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масив[2-i] = byte(число >> (8 * i) & 0x00FF)
	}
	return масив
}

func Unsignedinteger32toМасив(число uint32) [4]byte {
	var масив [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		масив[i] = byte(число >> (8 * i) & 0x000000FF)
	}
	return масив
}
func Unsignedinteger48toМасив(число uint64) [6]byte {
	var масив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масив[i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return масив
}
func Unsignedinteger48toМасивbe(число uint64) [6]byte {
	var масив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масив[5-i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return масив
}
func Unsignedinteger64toМасив(число uint64) [8]byte {
	var масив [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		масив[1-i] = byte(число >> (8 * i) & 0x00000000000000FF)
	}
	return масив
}
func Масивtounsignedinteger16(масив [2]byte) uint16 {
	var число uint16
	var i uint
	for i = 0; i < 2; i++ {
		число = число | (uint16(масив[1-i]) << (8 * i))
	}
	return число
}
func Масивtounsignedinteger32(масив [4]byte) uint32 {
	var число uint32
	var i uint
	for i = 0; i < 4; i++ {
		число = число | (uint32(масив[3-i]) << (8 * i))
	}
	return число
}
func Масивtounsignedinteger48(масив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(масив[5-i]) << (8 * i))
	}
	return число

}
func Масивtounsignedinteger48be(масив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(масив[i]) << (8 * i))
	}
	return число
}
func Масивtounsignedinteger64(масив [8]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 8; i++ {
		число = число | (uint64(масив[7-i]) << (8 * i))
	}
	return число
}
func Unsignedinteger64r(число uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(число>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(число uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(число>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(число uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(число>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(число uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(число>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ПечатБайтове(dataПоказалци uintptr, размер int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataПоказалци))
	var i int
	utilconsole.MПечат([]byte("util["))
	for i = 0; i < размер; i++ {
		utilconsole.MHexadecimalПечат(buffer_2[i])
	}
	utilconsole.MПечат([]byte("]"))
}

func ПечатТест(params ...interface{}) {
	for _, param := range params {
		utilconsole.MПечат([]byte(TypeOf(param).Name()))

	}
}
func ЕднакъвБайтове(a, b []byte) bool {
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
func БайтовеtoНиз(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerПоказалциМасивfromПоказалци(показалци_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показалци_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32МасивfromПоказалци(показалци_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показалци_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБайтовеfromПоказалци(показалци_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показалци_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncПоказалциfromПоказалци(показалци_2 uintptr) func() {
	code1Показалци_2 := uintptr(Pointer(&показалци_2))
	return *(*func())(Pointer(&code1Показалци_2))
}
