package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toPolje(številka uint16) [2]byte {
	var polje [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		polje[i] = byte(številka >> (8 * i) & 0x00FF)
	}
	return polje
}
func Unsignedinteger16toPoljebe(številka uint16) [2]byte {
	var polje [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		polje[2-i] = byte(številka >> (8 * i) & 0x00FF)
	}
	return polje
}

func Unsignedinteger32toPolje(številka uint32) [4]byte {
	var polje [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		polje[i] = byte(številka >> (8 * i) & 0x000000FF)
	}
	return polje
}
func Unsignedinteger48toPolje(številka uint64) [6]byte {
	var polje [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		polje[i] = byte(številka >> (8 * i) & 0x00000000FF)
	}
	return polje
}
func Unsignedinteger48toPoljebe(številka uint64) [6]byte {
	var polje [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		polje[5-i] = byte(številka >> (8 * i) & 0x00000000FF)
	}
	return polje
}
func Unsignedinteger64toPolje(številka uint64) [8]byte {
	var polje [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		polje[1-i] = byte(številka >> (8 * i) & 0x00000000000000FF)
	}
	return polje
}
func Poljetounsignedinteger16(polje [2]byte) uint16 {
	var številka uint16
	var i uint
	for i = 0; i < 2; i++ {
		številka = številka | (uint16(polje[1-i]) << (8 * i))
	}
	return številka
}
func Poljetounsignedinteger32(polje [4]byte) uint32 {
	var številka uint32
	var i uint
	for i = 0; i < 4; i++ {
		številka = številka | (uint32(polje[3-i]) << (8 * i))
	}
	return številka
}
func Poljetounsignedinteger48(polje [6]byte) uint64 {
	var številka uint64
	var i uint
	for i = 0; i < 6; i++ {
		številka = številka | (uint64(polje[5-i]) << (8 * i))
	}
	return številka

}
func Poljetounsignedinteger48be(polje [6]byte) uint64 {
	var številka uint64
	var i uint
	for i = 0; i < 6; i++ {
		številka = številka | (uint64(polje[i]) << (8 * i))
	}
	return številka
}
func Poljetounsignedinteger64(polje [8]byte) uint64 {
	var številka uint64
	var i uint
	for i = 0; i < 8; i++ {
		številka = številka | (uint64(polje[7-i]) << (8 * i))
	}
	return številka
}
func Unsignedinteger64r(številka uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(številka>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(številka uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(številka>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(številka uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(številka>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(številka uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(številka>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func NatisniBajtov(dataKazalnik uintptr, velikost int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataKazalnik))
	var i int
	utilconsole.MNatisni([]byte("util["))
	for i = 0; i < velikost; i++ {
		utilconsole.MHexadecimalNatisni(buffer_2[i])
	}
	utilconsole.MNatisni([]byte("]"))
}

func NatisniPreizkus(parametri ...interface{}) {
	for _, param := range parametri {
		utilconsole.MNatisni([]byte(TypeOf(param).Name()))

	}
}
func EqualBajtov(a, b []byte) bool {
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
func BajtovtoNiz(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerKazalnikPoljefromKazalnik(kazalnik_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kazalnik_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32PoljefromKazalnik(kazalnik_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kazalnik_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBajtovfromKazalnik(kazalnik_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{kazalnik_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncKazalnikfromKazalnik(kazalnik_2 uintptr) func() {
	code1Kazalnik_2 := uintptr(Pointer(&kazalnik_2))
	return *(*func())(Pointer(&code1Kazalnik_2))
}
