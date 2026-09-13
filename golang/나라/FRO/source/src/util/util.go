package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toarray(number uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return array
}
func Unsignedinteger16toarraybe(number uint16) [2]byte {
	var array [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		array[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return array
}

func Unsignedinteger32toarray(number uint32) [4]byte {
	var array [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return array
}
func Unsignedinteger48toarray(number uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger48toarraybe(number uint64) [6]byte {
	var array [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		array[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return array
}
func Unsignedinteger64toarray(number uint64) [8]byte {
	var array [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		array[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return array
}
func Arraytounsignedinteger16(array [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(array[1-i]) << (8 * i))
	}
	return number
}
func Arraytounsignedinteger32(array [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(array[3-i]) << (8 * i))
	}
	return number
}
func Arraytounsignedinteger48(array [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(array[5-i]) << (8 * i))
	}
	return number

}
func Arraytounsignedinteger48be(array [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(array[i]) << (8 * i))
	}
	return number
}
func Arraytounsignedinteger64(array [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(array[7-i]) << (8 * i))
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
func Printbýt(datapointer uintptr, stødd int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(datapointer))
	var i int
	utilconsole.MPrint([]byte("util["))
	for i = 0; i < stødd; i++ {
		utilconsole.MHexadecimalprint(buffer_2[i])
	}
	utilconsole.MPrint([]byte("]"))
}

func Printtest(params ...interface{}) {
	for _, param := range params {
		utilconsole.MPrint([]byte(TypeOf(param).Name()))

	}
}
func Equalbýt(a, b []byte) bool {
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
func Býttostring(b []byte) string {
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

func Getbýtfrompointer(pointer_2 uintptr, len int, cap int) []byte {
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
