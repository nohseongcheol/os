package ハンヨウ

import . "コンソール"
import . "unsafe"
import . "reflect"

var ハンヨウコンソール Tコンソール = Tコンソール{}

func Unsignedinteger16toハイレツ(number uint16) [2]byte {
	var ハイレツ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		ハイレツ[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return ハイレツ
}
func Unsignedinteger16toハイレツbe(number uint16) [2]byte {
	var ハイレツ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		ハイレツ[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return ハイレツ
}

func Unsignedinteger32toハイレツ(number uint32) [4]byte {
	var ハイレツ [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		ハイレツ[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return ハイレツ
}
func Unsignedinteger48toハイレツ(number uint64) [6]byte {
	var ハイレツ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		ハイレツ[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return ハイレツ
}
func Unsignedinteger48toハイレツbe(number uint64) [6]byte {
	var ハイレツ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		ハイレツ[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return ハイレツ
}
func Unsignedinteger64toハイレツ(number uint64) [8]byte {
	var ハイレツ [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		ハイレツ[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return ハイレツ
}
func Aハイレツtounsignedinteger16(ハイレツ [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(ハイレツ[1-i]) << (8 * i))
	}
	return number
}
func Aハイレツtounsignedinteger32(ハイレツ [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(ハイレツ[3-i]) << (8 * i))
	}
	return number
}
func Aハイレツtounsignedinteger48(ハイレツ [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(ハイレツ[5-i]) << (8 * i))
	}
	return number

}
func Aハイレツtounsignedinteger48be(ハイレツ [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(ハイレツ[i]) << (8 * i))
	}
	return number
}
func Aハイレツtounsignedinteger64(ハイレツ [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(ハイレツ[7-i]) << (8 * i))
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
func Pインサツバイト(データポインタ uintptr, サイズ int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(データポインタ))
	var i int
	ハンヨウコンソール.Mインサツ([]byte("util["))
	for i = 0; i < サイズ; i++ {
		ハンヨウコンソール.MHexadecimalインサツ(buffer_2[i])
	}
	ハンヨウコンソール.Mインサツ([]byte("]"))
}

func Pインサツテスト(パラメータ ...interface{}) {
	for _, param := range パラメータ {
		ハンヨウコンソール.Mインサツ([]byte(TypeOf(param).Name()))

	}
}
func Eスベテオナジバイト(a, b []byte) bool {
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
func Bバイトtoモジレツ(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerポインタハイレツカラポインタ(バンチサンショウ_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{バンチサンショウ_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ハイレツカラポインタ(バンチサンショウ_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{バンチサンショウ_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getバイトカラポインタ(バンチサンショウ_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{バンチサンショウ_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncポインタカラポインタ(バンチサンショウ_2 uintptr) func() {
	code1ポインタ_2 := uintptr(Pointer(&バンチサンショウ_2))
	return *(*func())(Pointer(&code1ポインタ_2))
}
