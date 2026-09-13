package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toVector(număr uint16) [2]byte {
	var vector [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		vector[i] = byte(număr >> (8 * i) & 0x00FF)
	}
	return vector
}
func Unsignedinteger16toVectorbe(număr uint16) [2]byte {
	var vector [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		vector[2-i] = byte(număr >> (8 * i) & 0x00FF)
	}
	return vector
}

func Unsignedinteger32toVector(număr uint32) [4]byte {
	var vector [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		vector[i] = byte(număr >> (8 * i) & 0x000000FF)
	}
	return vector
}
func Unsignedinteger48toVector(număr uint64) [6]byte {
	var vector [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		vector[i] = byte(număr >> (8 * i) & 0x00000000FF)
	}
	return vector
}
func Unsignedinteger48toVectorbe(număr uint64) [6]byte {
	var vector [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		vector[5-i] = byte(număr >> (8 * i) & 0x00000000FF)
	}
	return vector
}
func Unsignedinteger64toVector(număr uint64) [8]byte {
	var vector [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		vector[1-i] = byte(număr >> (8 * i) & 0x00000000000000FF)
	}
	return vector
}
func Vectortounsignedinteger16(vector [2]byte) uint16 {
	var număr uint16
	var i uint
	for i = 0; i < 2; i++ {
		număr = număr | (uint16(vector[1-i]) << (8 * i))
	}
	return număr
}
func Vectortounsignedinteger32(vector [4]byte) uint32 {
	var număr uint32
	var i uint
	for i = 0; i < 4; i++ {
		număr = număr | (uint32(vector[3-i]) << (8 * i))
	}
	return număr
}
func Vectortounsignedinteger48(vector [6]byte) uint64 {
	var număr uint64
	var i uint
	for i = 0; i < 6; i++ {
		număr = număr | (uint64(vector[5-i]) << (8 * i))
	}
	return număr

}
func Vectortounsignedinteger48be(vector [6]byte) uint64 {
	var număr uint64
	var i uint
	for i = 0; i < 6; i++ {
		număr = număr | (uint64(vector[i]) << (8 * i))
	}
	return număr
}
func Vectortounsignedinteger64(vector [8]byte) uint64 {
	var număr uint64
	var i uint
	for i = 0; i < 8; i++ {
		număr = număr | (uint64(vector[7-i]) << (8 * i))
	}
	return număr
}
func Unsignedinteger64r(număr uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(număr>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(număr uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(număr>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(număr uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(număr>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(număr uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(număr>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func TipăreșteOcteți(dataIndicator uintptr, mărime int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataIndicator))
	var i int
	utilconsole.MTipărește([]byte("util["))
	for i = 0; i < mărime; i++ {
		utilconsole.MHexadecimalTipărește(buffer_2[i])
	}
	utilconsole.MTipărește([]byte("]"))
}

func TipăreșteTestează(parametri ...interface{}) {
	for _, param := range parametri {
		utilconsole.MTipărește([]byte(TypeOf(param).Name()))

	}
}
func EqualOcteți(a, b []byte) bool {
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
func OctețitoȘir(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerIndicatorVectorfromIndicator(indicator_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{indicator_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32VectorfromIndicator(indicator_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{indicator_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetOctețifromIndicator(indicator_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{indicator_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncIndicatorfromIndicator(indicator_2 uintptr) func() {
	code1Indicator_2 := uintptr(Pointer(&indicator_2))
	return *(*func())(Pointer(&code1Indicator_2))
}
