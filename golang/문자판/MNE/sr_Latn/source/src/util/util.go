package util

import . "konzola"
import . "unsafe"
import . "reflect"

var utilKonzola TKonzola = TKonzola{}

func Unsignedinteger16toNiz(broj uint16) [2]byte {
	var niz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		niz[i] = byte(broj >> (8 * i) & 0x00FF)
	}
	return niz
}
func Unsignedinteger16toNizbe(broj uint16) [2]byte {
	var niz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		niz[2-i] = byte(broj >> (8 * i) & 0x00FF)
	}
	return niz
}

func Unsignedinteger32toNiz(broj uint32) [4]byte {
	var niz [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		niz[i] = byte(broj >> (8 * i) & 0x000000FF)
	}
	return niz
}
func Unsignedinteger48toNiz(broj uint64) [6]byte {
	var niz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		niz[i] = byte(broj >> (8 * i) & 0x00000000FF)
	}
	return niz
}
func Unsignedinteger48toNizbe(broj uint64) [6]byte {
	var niz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		niz[5-i] = byte(broj >> (8 * i) & 0x00000000FF)
	}
	return niz
}
func Unsignedinteger64toNiz(broj uint64) [8]byte {
	var niz [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		niz[1-i] = byte(broj >> (8 * i) & 0x00000000000000FF)
	}
	return niz
}
func Niztounsignedinteger16(niz [2]byte) uint16 {
	var broj uint16
	var i uint
	for i = 0; i < 2; i++ {
		broj = broj | (uint16(niz[1-i]) << (8 * i))
	}
	return broj
}
func Niztounsignedinteger32(niz [4]byte) uint32 {
	var broj uint32
	var i uint
	for i = 0; i < 4; i++ {
		broj = broj | (uint32(niz[3-i]) << (8 * i))
	}
	return broj
}
func Niztounsignedinteger48(niz [6]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 6; i++ {
		broj = broj | (uint64(niz[5-i]) << (8 * i))
	}
	return broj

}
func Niztounsignedinteger48be(niz [6]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 6; i++ {
		broj = broj | (uint64(niz[i]) << (8 * i))
	}
	return broj
}
func Niztounsignedinteger64(niz [8]byte) uint64 {
	var broj uint64
	var i uint
	for i = 0; i < 8; i++ {
		broj = broj | (uint64(niz[7-i]) << (8 * i))
	}
	return broj
}
func Unsignedinteger64r(broj uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(broj>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(broj uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(broj>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(broj uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(broj>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(broj uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(broj>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ŠtampajBajtova(dataPokazivač uintptr, veličina int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPokazivač))
	var i int
	utilKonzola.MŠtampaj([]byte("util["))
	for i = 0; i < veličina; i++ {
		utilKonzola.MHexadecimalŠtampaj(buffer_2[i])
	}
	utilKonzola.MŠtampaj([]byte("]"))
}

func ŠtampajTest(parametri_2 ...interface{}) {
	for _, param := range parametri_2 {
		utilKonzola.MŠtampaj([]byte(TypeOf(param).Name()))

	}
}
func IstaBajtova(a, b []byte) bool {
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
func Bajtovatoniska(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPokazivačNizsaPokazivač(pokazivač_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32NizsaPokazivač(pokazivač_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBajtovasaPokazivač(pokazivač_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPokazivačsaPokazivač(pokazivač_2 uintptr) func() {
	code1Pokazivač_2 := uintptr(Pointer(&pokazivač_2))
	return *(*func())(Pointer(&code1Pokazivač_2))
}
