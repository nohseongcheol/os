package util

import . "konsol"
import . "unsafe"
import . "reflect"

var utilKonsol TKonsol = TKonsol{}

func Unsignedinteger16toVektor(nummer uint16) [2]byte {
	var vektor [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		vektor[i] = byte(nummer >> (8 * i) & 0x00FF)
	}
	return vektor
}
func Unsignedinteger16toVektorbe(nummer uint16) [2]byte {
	var vektor [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		vektor[2-i] = byte(nummer >> (8 * i) & 0x00FF)
	}
	return vektor
}

func Unsignedinteger32toVektor(nummer uint32) [4]byte {
	var vektor [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		vektor[i] = byte(nummer >> (8 * i) & 0x000000FF)
	}
	return vektor
}
func Unsignedinteger48toVektor(nummer uint64) [6]byte {
	var vektor [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		vektor[i] = byte(nummer >> (8 * i) & 0x00000000FF)
	}
	return vektor
}
func Unsignedinteger48toVektorbe(nummer uint64) [6]byte {
	var vektor [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		vektor[5-i] = byte(nummer >> (8 * i) & 0x00000000FF)
	}
	return vektor
}
func Unsignedinteger64toVektor(nummer uint64) [8]byte {
	var vektor [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		vektor[1-i] = byte(nummer >> (8 * i) & 0x00000000000000FF)
	}
	return vektor
}
func Vektortounsignedinteger16(vektor [2]byte) uint16 {
	var nummer uint16
	var i uint
	for i = 0; i < 2; i++ {
		nummer = nummer | (uint16(vektor[1-i]) << (8 * i))
	}
	return nummer
}
func Vektortounsignedinteger32(vektor [4]byte) uint32 {
	var nummer uint32
	var i uint
	for i = 0; i < 4; i++ {
		nummer = nummer | (uint32(vektor[3-i]) << (8 * i))
	}
	return nummer
}
func Vektortounsignedinteger48(vektor [6]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 6; i++ {
		nummer = nummer | (uint64(vektor[5-i]) << (8 * i))
	}
	return nummer

}
func Vektortounsignedinteger48be(vektor [6]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 6; i++ {
		nummer = nummer | (uint64(vektor[i]) << (8 * i))
	}
	return nummer
}
func Vektortounsignedinteger64(vektor [8]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 8; i++ {
		nummer = nummer | (uint64(vektor[7-i]) << (8 * i))
	}
	return nummer
}
func Unsignedinteger64r(nummer uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nummer>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nummer uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nummer>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nummer uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nummer>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nummer uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nummer>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func SkrivutByte(dataMuspekare uintptr, storlek int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataMuspekare))
	var i int
	utilKonsol.MSkrivut([]byte("util["))
	for i = 0; i < storlek; i++ {
		utilKonsol.MHexadecimalSkrivut(buffer_2[i])
	}
	utilKonsol.MSkrivut([]byte("]"))
}

func SkrivutTesta(parametrar ...interface{}) {
	for _, param := range parametrar {
		utilKonsol.MSkrivut([]byte(TypeOf(param).Name()))

	}
}
func LikaByte(a, b []byte) bool {
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
func Bytetosträng(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerMuspekareVektorfromMuspekare(adressreferens_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adress	uintptr
		len	int
		cap	int
	}{adressreferens_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32VektorfromMuspekare(adressreferens_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		adress	uintptr
		len	int
		cap	int
	}{adressreferens_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytefromMuspekare(adressreferens_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		adress	uintptr
		len	int
		cap	int
	}{adressreferens_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncMuspekarefromMuspekare(adressreferens_2 uintptr) func() {
	code1Muspekare_2 := uintptr(Pointer(&adressreferens_2))
	return *(*func())(Pointer(&code1Muspekare_2))
}
