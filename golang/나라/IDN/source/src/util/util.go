package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toJajaran(nomor uint16) [2]byte {
	var jajaran [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		jajaran[i] = byte(nomor >> (8 * i) & 0x00FF)
	}
	return jajaran
}
func Unsignedinteger16toJajaranbe(nomor uint16) [2]byte {
	var jajaran [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		jajaran[2-i] = byte(nomor >> (8 * i) & 0x00FF)
	}
	return jajaran
}

func Unsignedinteger32toJajaran(nomor uint32) [4]byte {
	var jajaran [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		jajaran[i] = byte(nomor >> (8 * i) & 0x000000FF)
	}
	return jajaran
}
func Unsignedinteger48toJajaran(nomor uint64) [6]byte {
	var jajaran [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		jajaran[i] = byte(nomor >> (8 * i) & 0x00000000FF)
	}
	return jajaran
}
func Unsignedinteger48toJajaranbe(nomor uint64) [6]byte {
	var jajaran [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		jajaran[5-i] = byte(nomor >> (8 * i) & 0x00000000FF)
	}
	return jajaran
}
func Unsignedinteger64toJajaran(nomor uint64) [8]byte {
	var jajaran [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		jajaran[1-i] = byte(nomor >> (8 * i) & 0x00000000000000FF)
	}
	return jajaran
}
func Jajarantounsignedinteger16(jajaran [2]byte) uint16 {
	var nomor uint16
	var i uint
	for i = 0; i < 2; i++ {
		nomor = nomor | (uint16(jajaran[1-i]) << (8 * i))
	}
	return nomor
}
func Jajarantounsignedinteger32(jajaran [4]byte) uint32 {
	var nomor uint32
	var i uint
	for i = 0; i < 4; i++ {
		nomor = nomor | (uint32(jajaran[3-i]) << (8 * i))
	}
	return nomor
}
func Jajarantounsignedinteger48(jajaran [6]byte) uint64 {
	var nomor uint64
	var i uint
	for i = 0; i < 6; i++ {
		nomor = nomor | (uint64(jajaran[5-i]) << (8 * i))
	}
	return nomor

}
func Jajarantounsignedinteger48be(jajaran [6]byte) uint64 {
	var nomor uint64
	var i uint
	for i = 0; i < 6; i++ {
		nomor = nomor | (uint64(jajaran[i]) << (8 * i))
	}
	return nomor
}
func Jajarantounsignedinteger64(jajaran [8]byte) uint64 {
	var nomor uint64
	var i uint
	for i = 0; i < 8; i++ {
		nomor = nomor | (uint64(jajaran[7-i]) << (8 * i))
	}
	return nomor
}
func Unsignedinteger64r(nomor uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nomor>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nomor uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nomor>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nomor uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nomor>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nomor uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nomor>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func CetakByte(dataPenunjuk uintptr, ukuran int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPenunjuk))
	var i int
	utilconsole.MCetak([]byte("util["))
	for i = 0; i < ukuran; i++ {
		utilconsole.MHexadecimalCetak(buffer_2[i])
	}
	utilconsole.MCetak([]byte("]"))
}

func CetakTes(param_2 ...interface{}) {
	for _, param := range param_2 {
		utilconsole.MCetak([]byte(TypeOf(param).Name()))

	}
}
func SamaByte(a, b []byte) bool {
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
func BytetoBenang(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPenunjukJajaranfromPenunjuk(acuan_alamat_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{acuan_alamat_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32JajaranfromPenunjuk(acuan_alamat_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{acuan_alamat_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytefromPenunjuk(acuan_alamat_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{acuan_alamat_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPenunjukfromPenunjuk(acuan_alamat_2 uintptr) func() {
	code1Penunjuk_2 := uintptr(Pointer(&acuan_alamat_2))
	return *(*func())(Pointer(&code1Penunjuk_2))
}
