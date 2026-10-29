/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toFylki(number uint16) [2]byte {
	var fylki [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		fylki[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return fylki
}
func Unsignedinteger16toFylkibe(number uint16) [2]byte {
	var fylki [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		fylki[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return fylki
}

func Unsignedinteger32toFylki(number uint32) [4]byte {
	var fylki [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		fylki[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return fylki
}
func Unsignedinteger48toFylki(number uint64) [6]byte {
	var fylki [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		fylki[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return fylki
}
func Unsignedinteger48toFylkibe(number uint64) [6]byte {
	var fylki [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		fylki[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return fylki
}
func Unsignedinteger64toFylki(number uint64) [8]byte {
	var fylki [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		fylki[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return fylki
}
func Fylkitounsignedinteger16(fylki [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(fylki[1-i]) << (8 * i))
	}
	return number
}
func Fylkitounsignedinteger32(fylki [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(fylki[3-i]) << (8 * i))
	}
	return number
}
func Fylkitounsignedinteger48(fylki [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(fylki[5-i]) << (8 * i))
	}
	return number

}
func Fylkitounsignedinteger48be(fylki [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(fylki[i]) << (8 * i))
	}
	return number
}
func Fylkitounsignedinteger64(fylki [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(fylki[7-i]) << (8 * i))
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
func PrentaBæti(dataBendill uintptr, stærð int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataBendill))
	var i int
	utilconsole.MPrenta([]byte("util["))
	for i = 0; i < stærð; i++ {
		utilconsole.MHexadecimalPrenta(buffer_2[i])
	}
	utilconsole.MPrenta([]byte("]"))
}

func PrentaPrófun(params ...interface{}) {
	for _, param := range params {
		utilconsole.MPrenta([]byte(TypeOf(param).Name()))

	}
}
func EqualBæti(a, b []byte) bool {
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
func BætitoStrengur(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerBendillFylkifromBendill(bendill_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{bendill_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32FylkifromBendill(bendill_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{bendill_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBætifromBendill(bendill_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{bendill_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncBendillfromBendill(bendill_2 uintptr) func() {
	code1Bendill_2 := uintptr(Pointer(&bendill_2))
	return *(*func())(Pointer(&code1Bendill_2))
}
