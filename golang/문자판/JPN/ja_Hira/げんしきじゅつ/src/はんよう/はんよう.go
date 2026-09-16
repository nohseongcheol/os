/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package はんよう

import . "こんそーる"
import . "unsafe"
import . "reflect"

var はんようこんそーる Tこんそーる = Tこんそーる{}

func Unsignedinteger16toはいれつ(number uint16) [2]byte {
	var はいれつ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		はいれつ[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return はいれつ
}
func Unsignedinteger16toはいれつbe(number uint16) [2]byte {
	var はいれつ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		はいれつ[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return はいれつ
}

func Unsignedinteger32toはいれつ(number uint32) [4]byte {
	var はいれつ [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		はいれつ[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return はいれつ
}
func Unsignedinteger48toはいれつ(number uint64) [6]byte {
	var はいれつ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		はいれつ[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return はいれつ
}
func Unsignedinteger48toはいれつbe(number uint64) [6]byte {
	var はいれつ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		はいれつ[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return はいれつ
}
func Unsignedinteger64toはいれつ(number uint64) [8]byte {
	var はいれつ [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		はいれつ[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return はいれつ
}
func Aはいれつtounsignedinteger16(はいれつ [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(はいれつ[1-i]) << (8 * i))
	}
	return number
}
func Aはいれつtounsignedinteger32(はいれつ [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(はいれつ[3-i]) << (8 * i))
	}
	return number
}
func Aはいれつtounsignedinteger48(はいれつ [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(はいれつ[5-i]) << (8 * i))
	}
	return number

}
func Aはいれつtounsignedinteger48be(はいれつ [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(はいれつ[i]) << (8 * i))
	}
	return number
}
func Aはいれつtounsignedinteger64(はいれつ [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(はいれつ[7-i]) << (8 * i))
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
func Pいんさつばいと(でーたぽいんた uintptr, さいず int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(でーたぽいんた))
	var i int
	はんようこんそーる.Mいんさつ([]byte("util["))
	for i = 0; i < さいず; i++ {
		はんようこんそーる.MHexadecimalいんさつ(buffer_2[i])
	}
	はんようこんそーる.Mいんさつ([]byte("]"))
}

func Pいんさつてすと(ぱらめーた ...interface{}) {
	for _, param := range ぱらめーた {
		はんようこんそーる.Mいんさつ([]byte(TypeOf(param).Name()))

	}
}
func Eすべておなじばいと(a, b []byte) bool {
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
func Bばいとtoもじれつ(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerぽいんたはいれつからぽいんた(ばんちさんしょう_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ばんちさんしょう_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32はいれつからぽいんた(ばんちさんしょう_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ばんちさんしょう_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getばいとからぽいんた(ばんちさんしょう_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ばんちさんしょう_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncぽいんたからぽいんた(ばんちさんしょう_2 uintptr) func() {
	code1ぽいんた_2 := uintptr(Pointer(&ばんちさんしょう_2))
	return *(*func())(Pointer(&code1ぽいんた_2))
}
