package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toNiz(bROJ uint16) [2]byte {
	var niz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		niz[i] = byte(bROJ >> (8 * i) & 0x00FF)
	}
	return niz
}
func Unsignedinteger16toNizbe(bROJ uint16) [2]byte {
	var niz [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		niz[2-i] = byte(bROJ >> (8 * i) & 0x00FF)
	}
	return niz
}

func Unsignedinteger32toNiz(bROJ uint32) [4]byte {
	var niz [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		niz[i] = byte(bROJ >> (8 * i) & 0x000000FF)
	}
	return niz
}
func Unsignedinteger48toNiz(bROJ uint64) [6]byte {
	var niz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		niz[i] = byte(bROJ >> (8 * i) & 0x00000000FF)
	}
	return niz
}
func Unsignedinteger48toNizbe(bROJ uint64) [6]byte {
	var niz [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		niz[5-i] = byte(bROJ >> (8 * i) & 0x00000000FF)
	}
	return niz
}
func Unsignedinteger64toNiz(bROJ uint64) [8]byte {
	var niz [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		niz[1-i] = byte(bROJ >> (8 * i) & 0x00000000000000FF)
	}
	return niz
}
func Niztounsignedinteger16(niz [2]byte) uint16 {
	var bROJ uint16
	var i uint
	for i = 0; i < 2; i++ {
		bROJ = bROJ | (uint16(niz[1-i]) << (8 * i))
	}
	return bROJ
}
func Niztounsignedinteger32(niz [4]byte) uint32 {
	var bROJ uint32
	var i uint
	for i = 0; i < 4; i++ {
		bROJ = bROJ | (uint32(niz[3-i]) << (8 * i))
	}
	return bROJ
}
func Niztounsignedinteger48(niz [6]byte) uint64 {
	var bROJ uint64
	var i uint
	for i = 0; i < 6; i++ {
		bROJ = bROJ | (uint64(niz[5-i]) << (8 * i))
	}
	return bROJ

}
func Niztounsignedinteger48be(niz [6]byte) uint64 {
	var bROJ uint64
	var i uint
	for i = 0; i < 6; i++ {
		bROJ = bROJ | (uint64(niz[i]) << (8 * i))
	}
	return bROJ
}
func Niztounsignedinteger64(niz [8]byte) uint64 {
	var bROJ uint64
	var i uint
	for i = 0; i < 8; i++ {
		bROJ = bROJ | (uint64(niz[7-i]) << (8 * i))
	}
	return bROJ
}
func Unsignedinteger64r(bROJ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(bROJ>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(bROJ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(bROJ>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(bROJ uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(bROJ>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(bROJ uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(bROJ>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func IspisBajtova(dataPokazivač uintptr, veličina int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPokazivač))
	var i int
	utilconsole.MIspis([]byte("util["))
	for i = 0; i < veličina; i++ {
		utilconsole.MHexadecimalIspis(buffer_2[i])
	}
	utilconsole.MIspis([]byte("]"))
}

func IspisProvjeri(params ...interface{}) {
	for _, param := range params {
		utilconsole.MIspis([]byte(TypeOf(param).Name()))

	}
}
func JednakoBajtova(a, b []byte) bool {
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
func BajtovatoZnakovniniz(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPokazivačNizfromPokazivač(pokazivač_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32NizfromPokazivač(pokazivač_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBajtovafromPokazivač(pokazivač_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{pokazivač_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPokazivačfromPokazivač(pokazivač_2 uintptr) func() {
	code1Pokazivač_2 := uintptr(Pointer(&pokazivač_2))
	return *(*func())(Pointer(&code1Pokazivač_2))
}
