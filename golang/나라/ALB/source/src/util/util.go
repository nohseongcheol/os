package util

import . "konsolë"
import . "unsafe"
import . "reflect"

var utilKonsolë TKonsolë = TKonsolë{}

func Unsignedinteger16toRreshtimi(number uint16) [2]byte {
	var rreshtimi [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		rreshtimi[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return rreshtimi
}
func Unsignedinteger16toRreshtimibe(number uint16) [2]byte {
	var rreshtimi [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		rreshtimi[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return rreshtimi
}

func Unsignedinteger32toRreshtimi(number uint32) [4]byte {
	var rreshtimi [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		rreshtimi[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return rreshtimi
}
func Unsignedinteger48toRreshtimi(number uint64) [6]byte {
	var rreshtimi [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		rreshtimi[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return rreshtimi
}
func Unsignedinteger48toRreshtimibe(number uint64) [6]byte {
	var rreshtimi [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		rreshtimi[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return rreshtimi
}
func Unsignedinteger64toRreshtimi(number uint64) [8]byte {
	var rreshtimi [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		rreshtimi[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return rreshtimi
}
func Rreshtimitounsignedinteger16(rreshtimi [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(rreshtimi[1-i]) << (8 * i))
	}
	return number
}
func Rreshtimitounsignedinteger32(rreshtimi [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(rreshtimi[3-i]) << (8 * i))
	}
	return number
}
func Rreshtimitounsignedinteger48(rreshtimi [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(rreshtimi[5-i]) << (8 * i))
	}
	return number

}
func Rreshtimitounsignedinteger48be(rreshtimi [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(rreshtimi[i]) << (8 * i))
	}
	return number
}
func Rreshtimitounsignedinteger64(rreshtimi [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(rreshtimi[7-i]) << (8 * i))
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
func Printobytes(dataKursori uintptr, madhësia int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKursori))
	var i int
	utilKonsolë.MPrinto([]byte("util["))
	for i = 0; i < madhësia; i++ {
		utilKonsolë.MHexadecimalPrinto(buffer_2[i])
	}
	utilKonsolë.MPrinto([]byte("]"))
}

func PrintoProvo(params ...interface{}) {
	for _, param := range params {
		utilKonsolë.MPrinto([]byte(TypeOf(param).Name()))

	}
}
func Barasbytes(a, b []byte) bool {
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
func Bytestovarg(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKursoriRreshtimifromKursori(kursori_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursori_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32RreshtimifromKursori(kursori_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursori_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbytesfromKursori(kursori_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kursori_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKursorifromKursori(kursori_2 uintptr) func() {
	code1Kursori_2 := uintptr(Pointer(&kursori_2))
	return *(*func())(Pointer(&code1Kursori_2))
}
