package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toMasīvs(skaitlis uint16) [2]byte {
	var masīvs [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		masīvs[i] = byte(skaitlis >> (8 * i) & 0x00FF)
	}
	return masīvs
}
func Unsignedinteger16toMasīvsbe(skaitlis uint16) [2]byte {
	var masīvs [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		masīvs[2-i] = byte(skaitlis >> (8 * i) & 0x00FF)
	}
	return masīvs
}

func Unsignedinteger32toMasīvs(skaitlis uint32) [4]byte {
	var masīvs [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		masīvs[i] = byte(skaitlis >> (8 * i) & 0x000000FF)
	}
	return masīvs
}
func Unsignedinteger48toMasīvs(skaitlis uint64) [6]byte {
	var masīvs [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		masīvs[i] = byte(skaitlis >> (8 * i) & 0x00000000FF)
	}
	return masīvs
}
func Unsignedinteger48toMasīvsbe(skaitlis uint64) [6]byte {
	var masīvs [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		masīvs[5-i] = byte(skaitlis >> (8 * i) & 0x00000000FF)
	}
	return masīvs
}
func Unsignedinteger64toMasīvs(skaitlis uint64) [8]byte {
	var masīvs [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		masīvs[1-i] = byte(skaitlis >> (8 * i) & 0x00000000000000FF)
	}
	return masīvs
}
func Masīvstounsignedinteger16(masīvs [2]byte) uint16 {
	var skaitlis uint16
	var i uint
	for i = 0; i < 2; i++ {
		skaitlis = skaitlis | (uint16(masīvs[1-i]) << (8 * i))
	}
	return skaitlis
}
func Masīvstounsignedinteger32(masīvs [4]byte) uint32 {
	var skaitlis uint32
	var i uint
	for i = 0; i < 4; i++ {
		skaitlis = skaitlis | (uint32(masīvs[3-i]) << (8 * i))
	}
	return skaitlis
}
func Masīvstounsignedinteger48(masīvs [6]byte) uint64 {
	var skaitlis uint64
	var i uint
	for i = 0; i < 6; i++ {
		skaitlis = skaitlis | (uint64(masīvs[5-i]) << (8 * i))
	}
	return skaitlis

}
func Masīvstounsignedinteger48be(masīvs [6]byte) uint64 {
	var skaitlis uint64
	var i uint
	for i = 0; i < 6; i++ {
		skaitlis = skaitlis | (uint64(masīvs[i]) << (8 * i))
	}
	return skaitlis
}
func Masīvstounsignedinteger64(masīvs [8]byte) uint64 {
	var skaitlis uint64
	var i uint
	for i = 0; i < 8; i++ {
		skaitlis = skaitlis | (uint64(masīvs[7-i]) << (8 * i))
	}
	return skaitlis
}
func Unsignedinteger64r(skaitlis uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(skaitlis>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(skaitlis uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(skaitlis>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(skaitlis uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(skaitlis>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(skaitlis uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(skaitlis>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func DrukātBaiti(dataKursors uintptr, izmērs int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKursors))
	var i int
	utilconsole.MDrukāt([]byte("util["))
	for i = 0; i < izmērs; i++ {
		utilconsole.MHexadecimalDrukāt(buffer_2[i])
	}
	utilconsole.MDrukāt([]byte("]"))
}

func DrukātPārbaudīt(parametri_3 ...interface{}) {
	for _, param := range parametri_3 {
		utilconsole.MDrukāt([]byte(TypeOf(param).Name()))

	}
}
func VienādsBaiti(a, b []byte) bool {
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
func Baititovirkne(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKursorsMasīvsfromKursors(kursors_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursors_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32MasīvsfromKursors(kursors_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursors_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBaitifromKursors(kursors_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursors_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKursorsfromKursors(kursors_2 uintptr) func() {
	code1Kursors_2 := uintptr(Pointer(&kursors_2))
	return *(*func())(Pointer(&code1Kursors_2))
}
