package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toMảng(sỐ uint16) [2]byte {
	var mảng [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		mảng[i] = byte(sỐ >> (8 * i) & 0x00FF)
	}
	return mảng
}
func Unsignedinteger16toMảngbe(sỐ uint16) [2]byte {
	var mảng [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		mảng[2-i] = byte(sỐ >> (8 * i) & 0x00FF)
	}
	return mảng
}

func Unsignedinteger32toMảng(sỐ uint32) [4]byte {
	var mảng [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		mảng[i] = byte(sỐ >> (8 * i) & 0x000000FF)
	}
	return mảng
}
func Unsignedinteger48toMảng(sỐ uint64) [6]byte {
	var mảng [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		mảng[i] = byte(sỐ >> (8 * i) & 0x00000000FF)
	}
	return mảng
}
func Unsignedinteger48toMảngbe(sỐ uint64) [6]byte {
	var mảng [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		mảng[5-i] = byte(sỐ >> (8 * i) & 0x00000000FF)
	}
	return mảng
}
func Unsignedinteger64toMảng(sỐ uint64) [8]byte {
	var mảng [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		mảng[1-i] = byte(sỐ >> (8 * i) & 0x00000000000000FF)
	}
	return mảng
}
func Mảngtounsignedinteger16(mảng [2]byte) uint16 {
	var sỐ uint16
	var i uint
	for i = 0; i < 2; i++ {
		sỐ = sỐ | (uint16(mảng[1-i]) << (8 * i))
	}
	return sỐ
}
func Mảngtounsignedinteger32(mảng [4]byte) uint32 {
	var sỐ uint32
	var i uint
	for i = 0; i < 4; i++ {
		sỐ = sỐ | (uint32(mảng[3-i]) << (8 * i))
	}
	return sỐ
}
func Mảngtounsignedinteger48(mảng [6]byte) uint64 {
	var sỐ uint64
	var i uint
	for i = 0; i < 6; i++ {
		sỐ = sỐ | (uint64(mảng[5-i]) << (8 * i))
	}
	return sỐ

}
func Mảngtounsignedinteger48be(mảng [6]byte) uint64 {
	var sỐ uint64
	var i uint
	for i = 0; i < 6; i++ {
		sỐ = sỐ | (uint64(mảng[i]) << (8 * i))
	}
	return sỐ
}
func Mảngtounsignedinteger64(mảng [8]byte) uint64 {
	var sỐ uint64
	var i uint
	for i = 0; i < 8; i++ {
		sỐ = sỐ | (uint64(mảng[7-i]) << (8 * i))
	}
	return sỐ
}
func Unsignedinteger64r(sỐ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(sỐ>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(sỐ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(sỐ>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(sỐ uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(sỐ>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(sỐ uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(sỐ>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func InByte(dataContrỏ uintptr, cỡ int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataContrỏ))
	var i int
	utilconsole.MIn([]byte("util["))
	for i = 0; i < cỡ; i++ {
		utilconsole.MHexadecimalIn(buffer_2[i])
	}
	utilconsole.MIn([]byte("]"))
}

func InThử(params ...interface{}) {
	for _, param := range params {
		utilconsole.MIn([]byte(TypeOf(param).Name()))

	}
}
func EqualByte(a, b []byte) bool {
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
func BytetoCHUỖI(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerContrỏMảngfromContrỏ(tham_chiếu_địa_chỉ_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{tham_chiếu_địa_chỉ_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32MảngfromContrỏ(tham_chiếu_địa_chỉ_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{tham_chiếu_địa_chỉ_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytefromContrỏ(tham_chiếu_địa_chỉ_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{tham_chiếu_địa_chỉ_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncContrỏfromContrỏ(tham_chiếu_địa_chỉ_2 uintptr) func() {
	code1Contrỏ_2 := uintptr(Pointer(&tham_chiếu_địa_chỉ_2))
	return *(*func())(Pointer(&code1Contrỏ_2))
}
