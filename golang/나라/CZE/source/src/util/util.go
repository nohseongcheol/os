package util

import . "konzole"
import . "unsafe"
import . "reflect"

var utilKonzole TKonzole = TKonzole{}

func Unsignedinteger16doPole(číslo uint16) [2]byte {
	var pole [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		pole[i] = byte(číslo >> (8 * i) & 0x00FF)
	}
	return pole
}
func Unsignedinteger16doPolebe(číslo uint16) [2]byte {
	var pole [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		pole[2-i] = byte(číslo >> (8 * i) & 0x00FF)
	}
	return pole
}

func Unsignedinteger32doPole(číslo uint32) [4]byte {
	var pole [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		pole[i] = byte(číslo >> (8 * i) & 0x000000FF)
	}
	return pole
}
func Unsignedinteger48doPole(číslo uint64) [6]byte {
	var pole [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		pole[i] = byte(číslo >> (8 * i) & 0x00000000FF)
	}
	return pole
}
func Unsignedinteger48doPolebe(číslo uint64) [6]byte {
	var pole [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		pole[5-i] = byte(číslo >> (8 * i) & 0x00000000FF)
	}
	return pole
}
func Unsignedinteger64doPole(číslo uint64) [8]byte {
	var pole [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		pole[1-i] = byte(číslo >> (8 * i) & 0x00000000000000FF)
	}
	return pole
}
func Poledounsignedinteger16(pole [2]byte) uint16 {
	var číslo uint16
	var i uint
	for i = 0; i < 2; i++ {
		číslo = číslo | (uint16(pole[1-i]) << (8 * i))
	}
	return číslo
}
func Poledounsignedinteger32(pole [4]byte) uint32 {
	var číslo uint32
	var i uint
	for i = 0; i < 4; i++ {
		číslo = číslo | (uint32(pole[3-i]) << (8 * i))
	}
	return číslo
}
func Poledounsignedinteger48(pole [6]byte) uint64 {
	var číslo uint64
	var i uint
	for i = 0; i < 6; i++ {
		číslo = číslo | (uint64(pole[5-i]) << (8 * i))
	}
	return číslo

}
func Poledounsignedinteger48be(pole [6]byte) uint64 {
	var číslo uint64
	var i uint
	for i = 0; i < 6; i++ {
		číslo = číslo | (uint64(pole[i]) << (8 * i))
	}
	return číslo
}
func Poledounsignedinteger64(pole [8]byte) uint64 {
	var číslo uint64
	var i uint
	for i = 0; i < 8; i++ {
		číslo = číslo | (uint64(pole[7-i]) << (8 * i))
	}
	return číslo
}
func Unsignedinteger64r(číslo uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(číslo>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(číslo uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(číslo>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(číslo uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(číslo>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(číslo uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(číslo>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func TisknoutBytů(dataKurzor uintptr, velikost int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKurzor))
	var i int
	utilKonzole.MTisknout([]byte("util["))
	for i = 0; i < velikost; i++ {
		utilKonzole.MHexadecimalTisknout(buffer_2[i])
	}
	utilKonzole.MTisknout([]byte("]"))
}

func TisknoutOtestovat(parametry ...interface{}) {
	for _, param := range parametry {
		utilKonzole.MTisknout([]byte(TypeOf(param).Name()))

	}
}
func TotožnéBytů(a, b []byte) bool {
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
func Bytůdořetězec(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKurzorPolezKurzor(odkaz_na_adresu_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adresa	uintptr
		len	int
		cap	int
	}{odkaz_na_adresu_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32PolezKurzor(odkaz_na_adresu_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adresa	uintptr
		len	int
		cap	int
	}{odkaz_na_adresu_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytůzKurzor(odkaz_na_adresu_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		adresa	uintptr
		len	int
		cap	int
	}{odkaz_na_adresu_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKurzorzKurzor(odkaz_na_adresu_2 uintptr) func() {
	code1Kurzor_2 := uintptr(Pointer(&odkaz_na_adresu_2))
	return *(*func())(Pointer(&code1Kurzor_2))
}
