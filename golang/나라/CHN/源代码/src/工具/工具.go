/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 工具

import . "控制台"
import . "unsafe"
import . "reflect"

var 工具控制台 T控制台 = T控制台{}

func Unsignedinteger16to数组(数字 uint16) [2]byte {
	var 数组 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		数组[i] = byte(数字 >> (8 * i) & 0x00FF)
	}
	return 数组
}
func Unsignedinteger16to数组be(数字 uint16) [2]byte {
	var 数组 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		数组[2-i] = byte(数字 >> (8 * i) & 0x00FF)
	}
	return 数组
}

func Unsignedinteger32to数组(数字 uint32) [4]byte {
	var 数组 [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		数组[i] = byte(数字 >> (8 * i) & 0x000000FF)
	}
	return 数组
}
func Unsignedinteger48to数组(数字 uint64) [6]byte {
	var 数组 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		数组[i] = byte(数字 >> (8 * i) & 0x00000000FF)
	}
	return 数组
}
func Unsignedinteger48to数组be(数字 uint64) [6]byte {
	var 数组 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		数组[5-i] = byte(数字 >> (8 * i) & 0x00000000FF)
	}
	return 数组
}
func Unsignedinteger64to数组(数字 uint64) [8]byte {
	var 数组 [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		数组[1-i] = byte(数字 >> (8 * i) & 0x00000000000000FF)
	}
	return 数组
}
func A数组tounsignedinteger16(数组 [2]byte) uint16 {
	var 数字 uint16
	var i uint
	for i = 0; i < 2; i++ {
		数字 = 数字 | (uint16(数组[1-i]) << (8 * i))
	}
	return 数字
}
func A数组tounsignedinteger32(数组 [4]byte) uint32 {
	var 数字 uint32
	var i uint
	for i = 0; i < 4; i++ {
		数字 = 数字 | (uint32(数组[3-i]) << (8 * i))
	}
	return 数字
}
func A数组tounsignedinteger48(数组 [6]byte) uint64 {
	var 数字 uint64
	var i uint
	for i = 0; i < 6; i++ {
		数字 = 数字 | (uint64(数组[5-i]) << (8 * i))
	}
	return 数字

}
func A数组tounsignedinteger48be(数组 [6]byte) uint64 {
	var 数字 uint64
	var i uint
	for i = 0; i < 6; i++ {
		数字 = 数字 | (uint64(数组[i]) << (8 * i))
	}
	return 数字
}
func A数组tounsignedinteger64(数组 [8]byte) uint64 {
	var 数字 uint64
	var i uint
	for i = 0; i < 8; i++ {
		数字 = 数字 | (uint64(数组[7-i]) << (8 * i))
	}
	return 数字
}
func Unsignedinteger64r(数字 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(数字>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(数字 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(数字>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(数字 uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(数字>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(数字 uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(数字>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func P打印字节(数据指针 uintptr, 大小 int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(数据指针))
	var i int
	工具控制台.M打印([]byte("util["))
	for i = 0; i < 大小; i++ {
		工具控制台.MHexadecimal打印(buffer_2[i])
	}
	工具控制台.M打印([]byte("]"))
}

func P打印测试(参数_3 ...interface{}) {
	for _, param := range 参数_3 {
		工具控制台.M打印([]byte(TypeOf(param).Name()))

	}
}
func E相同字节(a, b []byte) bool {
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
func B字节to字符串(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedinteger指针数组from指针(地址引用_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{地址引用_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32数组from指针(地址引用_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{地址引用_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Get字节from指针(地址引用_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{地址引用_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfunc指针from指针(地址引用_2 uintptr) func() {
	code1指针_2 := uintptr(Pointer(&地址引用_2))
	return *(*func())(Pointer(&code1指针_2))
}
