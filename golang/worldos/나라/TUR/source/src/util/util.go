/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "konsol"
import . "unsafe"
import . "reflect"

var utilKonsol TKonsol = TKonsol{}

func Unsignedinteger16toDizi(sayı uint16) [2]byte {
	var dizi [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		dizi[i] = byte(sayı >> (8 * i) & 0x00FF)
	}
	return dizi
}
func Unsignedinteger16toDizibe(sayı uint16) [2]byte {
	var dizi [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		dizi[2-i] = byte(sayı >> (8 * i) & 0x00FF)
	}
	return dizi
}

func Unsignedinteger32toDizi(sayı uint32) [4]byte {
	var dizi [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		dizi[i] = byte(sayı >> (8 * i) & 0x000000FF)
	}
	return dizi
}
func Unsignedinteger48toDizi(sayı uint64) [6]byte {
	var dizi [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		dizi[i] = byte(sayı >> (8 * i) & 0x00000000FF)
	}
	return dizi
}
func Unsignedinteger48toDizibe(sayı uint64) [6]byte {
	var dizi [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		dizi[5-i] = byte(sayı >> (8 * i) & 0x00000000FF)
	}
	return dizi
}
func Unsignedinteger64toDizi(sayı uint64) [8]byte {
	var dizi [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		dizi[1-i] = byte(sayı >> (8 * i) & 0x00000000000000FF)
	}
	return dizi
}
func Dizitounsignedinteger16(dizi [2]byte) uint16 {
	var sayı uint16
	var i uint
	for i = 0; i < 2; i++ {
		sayı = sayı | (uint16(dizi[1-i]) << (8 * i))
	}
	return sayı
}
func Dizitounsignedinteger32(dizi [4]byte) uint32 {
	var sayı uint32
	var i uint
	for i = 0; i < 4; i++ {
		sayı = sayı | (uint32(dizi[3-i]) << (8 * i))
	}
	return sayı
}
func Dizitounsignedinteger48(dizi [6]byte) uint64 {
	var sayı uint64
	var i uint
	for i = 0; i < 6; i++ {
		sayı = sayı | (uint64(dizi[5-i]) << (8 * i))
	}
	return sayı

}
func Dizitounsignedinteger48be(dizi [6]byte) uint64 {
	var sayı uint64
	var i uint
	for i = 0; i < 6; i++ {
		sayı = sayı | (uint64(dizi[i]) << (8 * i))
	}
	return sayı
}
func Dizitounsignedinteger64(dizi [8]byte) uint64 {
	var sayı uint64
	var i uint
	for i = 0; i < 8; i++ {
		sayı = sayı | (uint64(dizi[7-i]) << (8 * i))
	}
	return sayı
}
func Unsignedinteger64r(sayı uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(sayı>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(sayı uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(sayı>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(sayı uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(sayı>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(sayı uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(sayı>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func YazdırBayt(dataBelirteç uintptr, boyut int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataBelirteç))
	var i int
	utilKonsol.MYazdır([]byte("util["))
	for i = 0; i < boyut; i++ {
		utilKonsol.MHexadecimalYazdır(buffer_2[i])
	}
	utilKonsol.MYazdır([]byte("]"))
}

func YazdırDene(parametreler ...interface{}) {
	for _, param := range parametreler {
		utilKonsol.MYazdır([]byte(TypeOf(param).Name()))

	}
}
func EşitBayt(a, b []byte) bool {
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
func BayttoKatar(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerBelirteçDizifromBelirteç(adres_başvurusu_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adres_başvurusu_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32DizifromBelirteç(adres_başvurusu_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adres_başvurusu_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBaytfromBelirteç(adres_başvurusu_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adres_başvurusu_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncBelirteçfromBelirteç(adres_başvurusu_2 uintptr) func() {
	code1Belirteç_2 := uintptr(Pointer(&adres_başvurusu_2))
	return *(*func())(Pointer(&code1Belirteç_2))
}
