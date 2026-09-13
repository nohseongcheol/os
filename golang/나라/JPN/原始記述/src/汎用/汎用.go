package 汎用

import . "コンソール"
import . "unsafe"
import . "reflect"

var 汎用コンソール Tコンソール = Tコンソール{}

func Unsignedinteger16to配列(number uint16) [2]byte {
	var 配列 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		配列[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return 配列
}
func Unsignedinteger16to配列be(number uint16) [2]byte {
	var 配列 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		配列[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return 配列
}

func Unsignedinteger32to配列(number uint32) [4]byte {
	var 配列 [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		配列[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return 配列
}
func Unsignedinteger48to配列(number uint64) [6]byte {
	var 配列 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		配列[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return 配列
}
func Unsignedinteger48to配列be(number uint64) [6]byte {
	var 配列 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		配列[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return 配列
}
func Unsignedinteger64to配列(number uint64) [8]byte {
	var 配列 [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		配列[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return 配列
}
func A配列tounsignedinteger16(配列 [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(配列[1-i]) << (8 * i))
	}
	return number
}
func A配列tounsignedinteger32(配列 [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(配列[3-i]) << (8 * i))
	}
	return number
}
func A配列tounsignedinteger48(配列 [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(配列[5-i]) << (8 * i))
	}
	return number

}
func A配列tounsignedinteger48be(配列 [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(配列[i]) << (8 * i))
	}
	return number
}
func A配列tounsignedinteger64(配列 [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(配列[7-i]) << (8 * i))
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
func P印刷バイト(データポインタ uintptr, サイズ int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(データポインタ))
	var i int
	汎用コンソール.M印刷([]byte("util["))
	for i = 0; i < サイズ; i++ {
		汎用コンソール.MHexadecimal印刷(buffer_2[i])
	}
	汎用コンソール.M印刷([]byte("]"))
}

func P印刷テスト(パラメータ ...interface{}) {
	for _, param := range パラメータ {
		汎用コンソール.M印刷([]byte(TypeOf(param).Name()))

	}
}
func Eすべて同じバイト(a, b []byte) bool {
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
func Bバイトto文字列(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerポインタ配列からポインタ(番地参照_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{番地参照_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32配列からポインタ(番地参照_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{番地参照_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getバイトからポインタ(番地参照_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{番地参照_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncポインタからポインタ(番地参照_2 uintptr) func() {
	code1ポインタ_2 := uintptr(Pointer(&番地参照_2))
	return *(*func())(Pointer(&code1ポインタ_2))
}
