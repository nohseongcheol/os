package util

import . "konsoli"
import . "unsafe"
import . "reflect"

var utilKonsoli TKonsoli = TKonsoli{}

func Unsignedinteger16toTaulukko(numero uint16) [2]byte {
	var taulukko [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		taulukko[i] = byte(numero >> (8 * i) & 0x00FF)
	}
	return taulukko
}
func Unsignedinteger16toTaulukkobe(numero uint16) [2]byte {
	var taulukko [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		taulukko[2-i] = byte(numero >> (8 * i) & 0x00FF)
	}
	return taulukko
}

func Unsignedinteger32toTaulukko(numero uint32) [4]byte {
	var taulukko [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		taulukko[i] = byte(numero >> (8 * i) & 0x000000FF)
	}
	return taulukko
}
func Unsignedinteger48toTaulukko(numero uint64) [6]byte {
	var taulukko [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		taulukko[i] = byte(numero >> (8 * i) & 0x00000000FF)
	}
	return taulukko
}
func Unsignedinteger48toTaulukkobe(numero uint64) [6]byte {
	var taulukko [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		taulukko[5-i] = byte(numero >> (8 * i) & 0x00000000FF)
	}
	return taulukko
}
func Unsignedinteger64toTaulukko(numero uint64) [8]byte {
	var taulukko [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		taulukko[1-i] = byte(numero >> (8 * i) & 0x00000000000000FF)
	}
	return taulukko
}
func Taulukkotounsignedinteger16(taulukko [2]byte) uint16 {
	var numero uint16
	var i uint
	for i = 0; i < 2; i++ {
		numero = numero | (uint16(taulukko[1-i]) << (8 * i))
	}
	return numero
}
func Taulukkotounsignedinteger32(taulukko [4]byte) uint32 {
	var numero uint32
	var i uint
	for i = 0; i < 4; i++ {
		numero = numero | (uint32(taulukko[3-i]) << (8 * i))
	}
	return numero
}
func Taulukkotounsignedinteger48(taulukko [6]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 6; i++ {
		numero = numero | (uint64(taulukko[5-i]) << (8 * i))
	}
	return numero

}
func Taulukkotounsignedinteger48be(taulukko [6]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 6; i++ {
		numero = numero | (uint64(taulukko[i]) << (8 * i))
	}
	return numero
}
func Taulukkotounsignedinteger64(taulukko [8]byte) uint64 {
	var numero uint64
	var i uint
	for i = 0; i < 8; i++ {
		numero = numero | (uint64(taulukko[7-i]) << (8 * i))
	}
	return numero
}
func Unsignedinteger64r(numero uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(numero>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(numero uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(numero>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(numero uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(numero>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(numero uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(numero>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Tulostatavua(dataOsoitin uintptr, koko int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataOsoitin))
	var i int
	utilKonsoli.MTulosta([]byte("util["))
	for i = 0; i < koko; i++ {
		utilKonsoli.MHexadecimalTulosta(buffer_2[i])
	}
	utilKonsoli.MTulosta([]byte("]"))
}

func TulostaKokeile(parametrit_3 ...interface{}) {
	for _, param := range parametrit_3 {
		utilKonsoli.MTulosta([]byte(TypeOf(param).Name()))

	}
}
func Samankokoinentavua(a, b []byte) bool {
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
func TavuatoMerkkijono(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerOsoitinTaulukkolähteestäOsoitin(osoiteviite_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{osoiteviite_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32TaulukkolähteestäOsoitin(osoiteviite_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{osoiteviite_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GettavualähteestäOsoitin(osoiteviite_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{osoiteviite_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncOsoitinlähteestäOsoitin(osoiteviite_2 uintptr) func() {
	code1Osoitin_2 := uintptr(Pointer(&osoiteviite_2))
	return *(*func())(Pointer(&code1Osoitin_2))
}
