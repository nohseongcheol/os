package util

import . "consola"
import . "unsafe"
import . "reflect"

var utilConsola TConsola = TConsola{}

func Unsignedinteger16toMatriu(nombre uint16) [2]byte {
	var matriu [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		matriu[i] = byte(nombre >> (8 * i) & 0x00FF)
	}
	return matriu
}
func Unsignedinteger16toMatriube(nombre uint16) [2]byte {
	var matriu [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		matriu[2-i] = byte(nombre >> (8 * i) & 0x00FF)
	}
	return matriu
}

func Unsignedinteger32toMatriu(nombre uint32) [4]byte {
	var matriu [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		matriu[i] = byte(nombre >> (8 * i) & 0x000000FF)
	}
	return matriu
}
func Unsignedinteger48toMatriu(nombre uint64) [6]byte {
	var matriu [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		matriu[i] = byte(nombre >> (8 * i) & 0x00000000FF)
	}
	return matriu
}
func Unsignedinteger48toMatriube(nombre uint64) [6]byte {
	var matriu [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		matriu[5-i] = byte(nombre >> (8 * i) & 0x00000000FF)
	}
	return matriu
}
func Unsignedinteger64toMatriu(nombre uint64) [8]byte {
	var matriu [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		matriu[1-i] = byte(nombre >> (8 * i) & 0x00000000000000FF)
	}
	return matriu
}
func Matriutounsignedinteger16(matriu [2]byte) uint16 {
	var nombre uint16
	var i uint
	for i = 0; i < 2; i++ {
		nombre = nombre | (uint16(matriu[1-i]) << (8 * i))
	}
	return nombre
}
func Matriutounsignedinteger32(matriu [4]byte) uint32 {
	var nombre uint32
	var i uint
	for i = 0; i < 4; i++ {
		nombre = nombre | (uint32(matriu[3-i]) << (8 * i))
	}
	return nombre
}
func Matriutounsignedinteger48(matriu [6]byte) uint64 {
	var nombre uint64
	var i uint
	for i = 0; i < 6; i++ {
		nombre = nombre | (uint64(matriu[5-i]) << (8 * i))
	}
	return nombre

}
func Matriutounsignedinteger48be(matriu [6]byte) uint64 {
	var nombre uint64
	var i uint
	for i = 0; i < 6; i++ {
		nombre = nombre | (uint64(matriu[i]) << (8 * i))
	}
	return nombre
}
func Matriutounsignedinteger64(matriu [8]byte) uint64 {
	var nombre uint64
	var i uint
	for i = 0; i < 8; i++ {
		nombre = nombre | (uint64(matriu[7-i]) << (8 * i))
	}
	return nombre
}
func Unsignedinteger64r(nombre uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nombre>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nombre uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nombre>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nombre uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nombre>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nombre uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nombre>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Imprimeixbytes(dataPunter uintptr, mida int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPunter))
	var i int
	utilConsola.MImprimeix([]byte("util["))
	for i = 0; i < mida; i++ {
		utilConsola.MHexadecimalImprimeix(buffer_2[i])
	}
	utilConsola.MImprimeix([]byte("]"))
}

func ImprimeixProva(paràmetres ...interface{}) {
	for _, param := range paràmetres {
		utilConsola.MImprimeix([]byte(TypeOf(param).Name()))

	}
}
func Igualbytes(a, b []byte) bool {
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
func BytestoCadena(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPunterMatriudesdePunter(punter_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adreça	uintptr
		len	int
		cap	int
	}{punter_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32MatriudesdePunter(punter_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adreça	uintptr
		len	int
		cap	int
	}{punter_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbytesdesdePunter(punter_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		adreça	uintptr
		len	int
		cap	int
	}{punter_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPunterdesdePunter(punter_2 uintptr) func() {
	code1Punter_2 := uintptr(Pointer(&punter_2))
	return *(*func())(Pointer(&code1Punter_2))
}
