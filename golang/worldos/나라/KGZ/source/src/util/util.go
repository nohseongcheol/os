/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toМассив(нОМЕР uint16) [2]byte {
	var массив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		массив[i] = byte(нОМЕР >> (8 * i) & 0x00FF)
	}
	return массив
}
func Unsignedinteger16toМассивbe(нОМЕР uint16) [2]byte {
	var массив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		массив[2-i] = byte(нОМЕР >> (8 * i) & 0x00FF)
	}
	return массив
}

func Unsignedinteger32toМассив(нОМЕР uint32) [4]byte {
	var массив [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		массив[i] = byte(нОМЕР >> (8 * i) & 0x000000FF)
	}
	return массив
}
func Unsignedinteger48toМассив(нОМЕР uint64) [6]byte {
	var массив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		массив[i] = byte(нОМЕР >> (8 * i) & 0x00000000FF)
	}
	return массив
}
func Unsignedinteger48toМассивbe(нОМЕР uint64) [6]byte {
	var массив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		массив[5-i] = byte(нОМЕР >> (8 * i) & 0x00000000FF)
	}
	return массив
}
func Unsignedinteger64toМассив(нОМЕР uint64) [8]byte {
	var массив [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		массив[1-i] = byte(нОМЕР >> (8 * i) & 0x00000000000000FF)
	}
	return массив
}
func Массивtounsignedinteger16(массив [2]byte) uint16 {
	var нОМЕР uint16
	var i uint
	for i = 0; i < 2; i++ {
		нОМЕР = нОМЕР | (uint16(массив[1-i]) << (8 * i))
	}
	return нОМЕР
}
func Массивtounsignedinteger32(массив [4]byte) uint32 {
	var нОМЕР uint32
	var i uint
	for i = 0; i < 4; i++ {
		нОМЕР = нОМЕР | (uint32(массив[3-i]) << (8 * i))
	}
	return нОМЕР
}
func Массивtounsignedinteger48(массив [6]byte) uint64 {
	var нОМЕР uint64
	var i uint
	for i = 0; i < 6; i++ {
		нОМЕР = нОМЕР | (uint64(массив[5-i]) << (8 * i))
	}
	return нОМЕР

}
func Массивtounsignedinteger48be(массив [6]byte) uint64 {
	var нОМЕР uint64
	var i uint
	for i = 0; i < 6; i++ {
		нОМЕР = нОМЕР | (uint64(массив[i]) << (8 * i))
	}
	return нОМЕР
}
func Массивtounsignedinteger64(массив [8]byte) uint64 {
	var нОМЕР uint64
	var i uint
	for i = 0; i < 8; i++ {
		нОМЕР = нОМЕР | (uint64(массив[7-i]) << (8 * i))
	}
	return нОМЕР
}
func Unsignedinteger64r(нОМЕР uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(нОМЕР>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(нОМЕР uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(нОМЕР>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(нОМЕР uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(нОМЕР>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(нОМЕР uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(нОМЕР>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func БасмаБайт(dataКөрсөткүч uintptr, өлчөм int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataКөрсөткүч))
	var i int
	utilconsole.MБасма([]byte("util["))
	for i = 0; i < өлчөм; i++ {
		utilconsole.MHexadecimalБасма(buffer_2[i])
	}
	utilconsole.MБасма([]byte("]"))
}

func БасмаТекшерүү(params ...interface{}) {
	for _, param := range params {
		utilconsole.MБасма([]byte(TypeOf(param).Name()))

	}
}
func EqualБайт(a, b []byte) bool {
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
func БайтtoСАП(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerКөрсөткүчМассивfromКөрсөткүч(көрсөткүч_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{көрсөткүч_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32МассивfromКөрсөткүч(көрсөткүч_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{көрсөткүч_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБайтfromКөрсөткүч(көрсөткүч_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{көрсөткүч_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncКөрсөткүчfromКөрсөткүч(көрсөткүч_2 uintptr) func() {
	code1Көрсөткүч_2 := uintptr(Pointer(&көрсөткүч_2))
	return *(*func())(Pointer(&code1Көрсөткүч_2))
}
