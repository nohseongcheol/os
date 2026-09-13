package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toMassiiv(arv uint16) [2]byte {
	var massiiv [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		massiiv[i] = byte(arv >> (8 * i) & 0x00FF)
	}
	return massiiv
}
func Unsignedinteger16toMassiivbe(arv uint16) [2]byte {
	var massiiv [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		massiiv[2-i] = byte(arv >> (8 * i) & 0x00FF)
	}
	return massiiv
}

func Unsignedinteger32toMassiiv(arv uint32) [4]byte {
	var massiiv [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		massiiv[i] = byte(arv >> (8 * i) & 0x000000FF)
	}
	return massiiv
}
func Unsignedinteger48toMassiiv(arv uint64) [6]byte {
	var massiiv [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		massiiv[i] = byte(arv >> (8 * i) & 0x00000000FF)
	}
	return massiiv
}
func Unsignedinteger48toMassiivbe(arv uint64) [6]byte {
	var massiiv [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		massiiv[5-i] = byte(arv >> (8 * i) & 0x00000000FF)
	}
	return massiiv
}
func Unsignedinteger64toMassiiv(arv uint64) [8]byte {
	var massiiv [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		massiiv[1-i] = byte(arv >> (8 * i) & 0x00000000000000FF)
	}
	return massiiv
}
func Massiivtounsignedinteger16(massiiv [2]byte) uint16 {
	var arv uint16
	var i uint
	for i = 0; i < 2; i++ {
		arv = arv | (uint16(massiiv[1-i]) << (8 * i))
	}
	return arv
}
func Massiivtounsignedinteger32(massiiv [4]byte) uint32 {
	var arv uint32
	var i uint
	for i = 0; i < 4; i++ {
		arv = arv | (uint32(massiiv[3-i]) << (8 * i))
	}
	return arv
}
func Massiivtounsignedinteger48(massiiv [6]byte) uint64 {
	var arv uint64
	var i uint
	for i = 0; i < 6; i++ {
		arv = arv | (uint64(massiiv[5-i]) << (8 * i))
	}
	return arv

}
func Massiivtounsignedinteger48be(massiiv [6]byte) uint64 {
	var arv uint64
	var i uint
	for i = 0; i < 6; i++ {
		arv = arv | (uint64(massiiv[i]) << (8 * i))
	}
	return arv
}
func Massiivtounsignedinteger64(massiiv [8]byte) uint64 {
	var arv uint64
	var i uint
	for i = 0; i < 8; i++ {
		arv = arv | (uint64(massiiv[7-i]) << (8 * i))
	}
	return arv
}
func Unsignedinteger64r(arv uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(arv>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(arv uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(arv>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(arv uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(arv>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(arv uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(arv>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Prindibaiti(dataKursor uintptr, suurus int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKursor))
	var i int
	utilconsole.MPrindi([]byte("util["))
	for i = 0; i < suurus; i++ {
		utilconsole.MHexadecimalPrindi(buffer_2[i])
	}
	utilconsole.MPrindi([]byte("]"))
}

func PrindiTesti(parameetrid ...interface{}) {
	for _, param := range parameetrid {
		utilconsole.MPrindi([]byte(TypeOf(param).Name()))

	}
}
func Võrdnebaiti(a, b []byte) bool {
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
func Baititostring(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKursorMassiivfromKursor(kursor_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursor_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32MassiivfromKursor(kursor_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursor_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbaitifromKursor(kursor_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursor_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKursorfromKursor(kursor_2 uintptr) func() {
	code1Kursor_2 := uintptr(Pointer(&kursor_2))
	return *(*func())(Pointer(&code1Kursor_2))
}
