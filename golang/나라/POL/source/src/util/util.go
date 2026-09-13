package util

import . "konsola"
import . "unsafe"
import . "reflect"

var utilKonsola TKonsola = TKonsola{}

func Unsignedinteger16toTablica(liczba_2 uint16) [2]byte {
	var tablica [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tablica[i] = byte(liczba_2 >> (8 * i) & 0x00FF)
	}
	return tablica
}
func Unsignedinteger16toTablicabe(liczba_2 uint16) [2]byte {
	var tablica [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tablica[2-i] = byte(liczba_2 >> (8 * i) & 0x00FF)
	}
	return tablica
}

func Unsignedinteger32toTablica(liczba_2 uint32) [4]byte {
	var tablica [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		tablica[i] = byte(liczba_2 >> (8 * i) & 0x000000FF)
	}
	return tablica
}
func Unsignedinteger48toTablica(liczba_2 uint64) [6]byte {
	var tablica [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tablica[i] = byte(liczba_2 >> (8 * i) & 0x00000000FF)
	}
	return tablica
}
func Unsignedinteger48toTablicabe(liczba_2 uint64) [6]byte {
	var tablica [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tablica[5-i] = byte(liczba_2 >> (8 * i) & 0x00000000FF)
	}
	return tablica
}
func Unsignedinteger64toTablica(liczba_2 uint64) [8]byte {
	var tablica [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		tablica[1-i] = byte(liczba_2 >> (8 * i) & 0x00000000000000FF)
	}
	return tablica
}
func Tablicatounsignedinteger16(tablica [2]byte) uint16 {
	var liczba_2 uint16
	var i uint
	for i = 0; i < 2; i++ {
		liczba_2 = liczba_2 | (uint16(tablica[1-i]) << (8 * i))
	}
	return liczba_2
}
func Tablicatounsignedinteger32(tablica [4]byte) uint32 {
	var liczba_2 uint32
	var i uint
	for i = 0; i < 4; i++ {
		liczba_2 = liczba_2 | (uint32(tablica[3-i]) << (8 * i))
	}
	return liczba_2
}
func Tablicatounsignedinteger48(tablica [6]byte) uint64 {
	var liczba_2 uint64
	var i uint
	for i = 0; i < 6; i++ {
		liczba_2 = liczba_2 | (uint64(tablica[5-i]) << (8 * i))
	}
	return liczba_2

}
func Tablicatounsignedinteger48be(tablica [6]byte) uint64 {
	var liczba_2 uint64
	var i uint
	for i = 0; i < 6; i++ {
		liczba_2 = liczba_2 | (uint64(tablica[i]) << (8 * i))
	}
	return liczba_2
}
func Tablicatounsignedinteger64(tablica [8]byte) uint64 {
	var liczba_2 uint64
	var i uint
	for i = 0; i < 8; i++ {
		liczba_2 = liczba_2 | (uint64(tablica[7-i]) << (8 * i))
	}
	return liczba_2
}
func Unsignedinteger64r(liczba_2 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(liczba_2>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(liczba_2 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(liczba_2>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(liczba_2 uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(liczba_2>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(liczba_2 uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(liczba_2>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func WydrukujBajty(dataKursor uintptr, rozmiar int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKursor))
	var i int
	utilKonsola.MWydrukuj([]byte("util["))
	for i = 0; i < rozmiar; i++ {
		utilKonsola.MHexadecimalWydrukuj(buffer_2[i])
	}
	utilKonsola.MWydrukuj([]byte("]"))
}

func WydrukujPrzetestuj(parametry ...interface{}) {
	for _, param := range parametry {
		utilKonsola.MWydrukuj([]byte(TypeOf(param).Name()))

	}
}
func OdpowiedniBajty(a, b []byte) bool {
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
func BajtytoCIĄG(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKursorTablicazKursor(odwołanie_do_adresu_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adres	uintptr
		len	int
		cap	int
	}{odwołanie_do_adresu_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32TablicazKursor(odwołanie_do_adresu_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adres	uintptr
		len	int
		cap	int
	}{odwołanie_do_adresu_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBajtyzKursor(odwołanie_do_adresu_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		adres	uintptr
		len	int
		cap	int
	}{odwołanie_do_adresu_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKursorzKursor(odwołanie_do_adresu_2 uintptr) func() {
	code1Kursor_2 := uintptr(Pointer(&odwołanie_do_adresu_2))
	return *(*func())(Pointer(&code1Kursor_2))
}
