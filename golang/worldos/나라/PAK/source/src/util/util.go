/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toلڑی(number uint16) [2]byte {
	var لڑی [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		لڑی[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return لڑی
}
func Unsignedinteger16toلڑیbe(number uint16) [2]byte {
	var لڑی [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		لڑی[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return لڑی
}

func Unsignedinteger32toلڑی(number uint32) [4]byte {
	var لڑی [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		لڑی[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return لڑی
}
func Unsignedinteger48toلڑی(number uint64) [6]byte {
	var لڑی [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		لڑی[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return لڑی
}
func Unsignedinteger48toلڑیbe(number uint64) [6]byte {
	var لڑی [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		لڑی[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return لڑی
}
func Unsignedinteger64toلڑی(number uint64) [8]byte {
	var لڑی [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		لڑی[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return لڑی
}
func Aلڑیtounsignedinteger16(لڑی [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(لڑی[1-i]) << (8 * i))
	}
	return number
}
func Aلڑیtounsignedinteger32(لڑی [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(لڑی[3-i]) << (8 * i))
	}
	return number
}
func Aلڑیtounsignedinteger48(لڑی [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(لڑی[5-i]) << (8 * i))
	}
	return number

}
func Aلڑیtounsignedinteger48be(لڑی [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(لڑی[i]) << (8 * i))
	}
	return number
}
func Aلڑیtounsignedinteger64(لڑی [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(لڑی[7-i]) << (8 * i))
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
func Pچھاپیںبائٹس(dataپؤائنٹر uintptr, حجم int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataپؤائنٹر))
	var i int
	utilconsole.Mچھاپیں([]byte("util["))
	for i = 0; i < حجم; i++ {
		utilconsole.MHexadecimalچھاپیں(buffer_2[i])
	}
	utilconsole.Mچھاپیں([]byte("]"))
}

func Pچھاپیںٹیسٹ(params ...interface{}) {
	for _, param := range params {
		utilconsole.Mچھاپیں([]byte(TypeOf(param).Name()))

	}
}
func Eبرابربائٹس(a, b []byte) bool {
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
func Bبائٹسtoڈورا(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerپؤائنٹرلڑیfromپؤائنٹر(پؤائنٹر_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{پؤائنٹر_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32لڑیfromپؤائنٹر(پؤائنٹر_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{پؤائنٹر_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getبائٹسfromپؤائنٹر(پؤائنٹر_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{پؤائنٹر_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncپؤائنٹرfromپؤائنٹر(پؤائنٹر_2 uintptr) func() {
	code1پؤائنٹر_2 := uintptr(Pointer(&پؤائنٹر_2))
	return *(*func())(Pointer(&code1پؤائنٹر_2))
}
