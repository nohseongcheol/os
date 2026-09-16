/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 工具

import . "控制台"
import . "unsafe"
import . "reflect"

var 工具控制台 T控制台 = T控制台{}

func Unsignedinteger16to陣列(數字 uint16) [2]byte {
	var 陣列 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		陣列[i] = byte(數字 >> (8 * i) & 0x00FF)
	}
	return 陣列
}
func Unsignedinteger16to陣列be(數字 uint16) [2]byte {
	var 陣列 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		陣列[2-i] = byte(數字 >> (8 * i) & 0x00FF)
	}
	return 陣列
}

func Unsignedinteger32to陣列(數字 uint32) [4]byte {
	var 陣列 [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		陣列[i] = byte(數字 >> (8 * i) & 0x000000FF)
	}
	return 陣列
}
func Unsignedinteger48to陣列(數字 uint64) [6]byte {
	var 陣列 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		陣列[i] = byte(數字 >> (8 * i) & 0x00000000FF)
	}
	return 陣列
}
func Unsignedinteger48to陣列be(數字 uint64) [6]byte {
	var 陣列 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		陣列[5-i] = byte(數字 >> (8 * i) & 0x00000000FF)
	}
	return 陣列
}
func Unsignedinteger64to陣列(數字 uint64) [8]byte {
	var 陣列 [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		陣列[1-i] = byte(數字 >> (8 * i) & 0x00000000000000FF)
	}
	return 陣列
}
func A陣列tounsignedinteger16(陣列 [2]byte) uint16 {
	var 數字 uint16
	var i uint
	for i = 0; i < 2; i++ {
		數字 = 數字 | (uint16(陣列[1-i]) << (8 * i))
	}
	return 數字
}
func A陣列tounsignedinteger32(陣列 [4]byte) uint32 {
	var 數字 uint32
	var i uint
	for i = 0; i < 4; i++ {
		數字 = 數字 | (uint32(陣列[3-i]) << (8 * i))
	}
	return 數字
}
func A陣列tounsignedinteger48(陣列 [6]byte) uint64 {
	var 數字 uint64
	var i uint
	for i = 0; i < 6; i++ {
		數字 = 數字 | (uint64(陣列[5-i]) << (8 * i))
	}
	return 數字

}
func A陣列tounsignedinteger48be(陣列 [6]byte) uint64 {
	var 數字 uint64
	var i uint
	for i = 0; i < 6; i++ {
		數字 = 數字 | (uint64(陣列[i]) << (8 * i))
	}
	return 數字
}
func A陣列tounsignedinteger64(陣列 [8]byte) uint64 {
	var 數字 uint64
	var i uint
	for i = 0; i < 8; i++ {
		數字 = 數字 | (uint64(陣列[7-i]) << (8 * i))
	}
	return 數字
}
func Unsignedinteger64r(數字 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(數字>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(數字 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(數字>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(數字 uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(數字>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(數字 uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(數字>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func P列印位元組(資料指標 uintptr, 大小 int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(資料指標))
	var i int
	工具控制台.M列印([]byte("util["))
	for i = 0; i < 大小; i++ {
		工具控制台.MHexadecimal列印(buffer_2[i])
	}
	工具控制台.M列印([]byte("]"))
}

func P列印測試(參數_3 ...interface{}) {
	for _, param := range 參數_3 {
		工具控制台.M列印([]byte(TypeOf(param).Name()))

	}
}
func E相等位元組(a, b []byte) bool {
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
func B位元組to字串(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedinteger指標陣列from指標(位址參照_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{位址參照_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32陣列from指標(位址參照_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{位址參照_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Get位元組from指標(位址參照_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{位址參照_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfunc指標from指標(位址參照_2 uintptr) func() {
	code1指標_2 := uintptr(Pointer(&位址參照_2))
	return *(*func())(Pointer(&code1指標_2))
}
