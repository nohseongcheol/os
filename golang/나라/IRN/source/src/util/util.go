package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toآرایه(number uint16) [2]byte {
	var آرایه [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		آرایه[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return آرایه
}
func Unsignedinteger16toآرایهbe(number uint16) [2]byte {
	var آرایه [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		آرایه[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return آرایه
}

func Unsignedinteger32toآرایه(number uint32) [4]byte {
	var آرایه [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		آرایه[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return آرایه
}
func Unsignedinteger48toآرایه(number uint64) [6]byte {
	var آرایه [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		آرایه[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return آرایه
}
func Unsignedinteger48toآرایهbe(number uint64) [6]byte {
	var آرایه [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		آرایه[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return آرایه
}
func Unsignedinteger64toآرایه(number uint64) [8]byte {
	var آرایه [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		آرایه[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return آرایه
}
func Aآرایهtounsignedinteger16(آرایه [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(آرایه[1-i]) << (8 * i))
	}
	return number
}
func Aآرایهtounsignedinteger32(آرایه [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(آرایه[3-i]) << (8 * i))
	}
	return number
}
func Aآرایهtounsignedinteger48(آرایه [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(آرایه[5-i]) << (8 * i))
	}
	return number

}
func Aآرایهtounsignedinteger48be(آرایه [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(آرایه[i]) << (8 * i))
	}
	return number
}
func Aآرایهtounsignedinteger64(آرایه [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(آرایه[7-i]) << (8 * i))
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
func Pچاپبایت(datapointer uintptr, اندازه int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(datapointer))
	var i int
	utilconsole.Mچاپ([]byte("util["))
	for i = 0; i < اندازه; i++ {
		utilconsole.MHexadecimalچاپ(buffer_2[i])
	}
	utilconsole.Mچاپ([]byte("]"))
}

func Pچاپtest(params ...interface{}) {
	for _, param := range params {
		utilconsole.Mچاپ([]byte(TypeOf(param).Name()))

	}
}
func Equalبایت(a, b []byte) bool {
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
func Bبایتtoرشته(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerpointerآرایهfrompointer(pointer_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32آرایهfrompointer(pointer_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pointer_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getبایتfrompointer(pointer_2 uintptr, len int, cap int) []byte {
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
