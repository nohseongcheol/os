/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toarray(rAQAM uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[i] = byte(rAQAM >> (8 * i) & 0x00FF)
	}
	return array
}
func Unsignedinteger16toarraybe(rAQAM uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[2-i] = byte(rAQAM >> (8 * i) & 0x00FF)
	}
	return array
}

func Unsignedinteger32toarray(rAQAM uint32) [4]byte {
	var array [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[i] = byte(rAQAM >> (8 * i) & 0x000000FF)
	}
	return array
}
func Unsignedinteger48toarray(rAQAM uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[i] = byte(rAQAM >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger48toarraybe(rAQAM uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[5-i] = byte(rAQAM >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger64toarray(rAQAM uint64) [8]byte {
	var array [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[1-i] = byte(rAQAM >> (8 * i) & 0x00000000000000FF)
	}
	return array
}
func Arraytounsignedinteger16(array [2]byte) uint16 {
	var rAQAM uint16
	var i uint
	for i = 0; i < 2; i++ {
		rAQAM = rAQAM | (uint16(array[1-i]) << (8 * i))
	}
	return rAQAM
}
func Arraytounsignedinteger32(array [4]byte) uint32 {
	var rAQAM uint32
	var i uint
	for i = 0; i < 4; i++ {
		rAQAM = rAQAM | (uint32(array[3-i]) << (8 * i))
	}
	return rAQAM
}
func Arraytounsignedinteger48(array [6]byte) uint64 {
	var rAQAM uint64
	var i uint
	for i = 0; i < 6; i++ {
		rAQAM = rAQAM | (uint64(array[5-i]) << (8 * i))
	}
	return rAQAM

}
func Arraytounsignedinteger48be(array [6]byte) uint64 {
	var rAQAM uint64
	var i uint
	for i = 0; i < 6; i++ {
		rAQAM = rAQAM | (uint64(array[i]) << (8 * i))
	}
	return rAQAM
}
func Arraytounsignedinteger64(array [8]byte) uint64 {
	var rAQAM uint64
	var i uint
	for i = 0; i < 8; i++ {
		rAQAM = rAQAM | (uint64(array[7-i]) << (8 * i))
	}
	return rAQAM
}
func Unsignedinteger64r(rAQAM uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(rAQAM>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(rAQAM uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(rAQAM>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(rAQAM uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(rAQAM>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(rAQAM uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(rAQAM>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ChopetishBaytlar(dataKorsatgich uintptr, hajmi int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKorsatgich))
	var i int
	utilconsole.MChopetish([]byte("util["))
	for i = 0; i < hajmi; i++ {
		utilconsole.MHexadecimalChopetish(buffer_2[i])
	}
	utilconsole.MChopetish([]byte("]"))
}

func ChopetishSinash(params ...interface{}) {
	for _, param := range params {
		utilconsole.MChopetish([]byte(TypeOf(param).Name()))

	}
}
func EqualBaytlar(a, b []byte) bool {
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
func Baytlartostring(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKorsatgicharrayfromKorsatgich(korsatgich_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{korsatgich_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32arrayfromKorsatgich(korsatgich_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{korsatgich_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBaytlarfromKorsatgich(korsatgich_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{korsatgich_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKorsatgichfromKorsatgich(korsatgich_2 uintptr) func() {
	code1Korsatgich_2 := uintptr(Pointer(&korsatgich_2))
	return *(*func())(Pointer(&code1Korsatgich_2))
}
