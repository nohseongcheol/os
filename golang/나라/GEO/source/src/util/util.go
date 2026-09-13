package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toმასივი(რიცხვი uint16) [2]byte {
	var მასივი [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		მასივი[i] = byte(რიცხვი >> (8 * i) & 0x00FF)
	}
	return მასივი
}
func Unsignedinteger16toმასივიbe(რიცხვი uint16) [2]byte {
	var მასივი [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		მასივი[2-i] = byte(რიცხვი >> (8 * i) & 0x00FF)
	}
	return მასივი
}

func Unsignedinteger32toმასივი(რიცხვი uint32) [4]byte {
	var მასივი [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		მასივი[i] = byte(რიცხვი >> (8 * i) & 0x000000FF)
	}
	return მასივი
}
func Unsignedinteger48toმასივი(რიცხვი uint64) [6]byte {
	var მასივი [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		მასივი[i] = byte(რიცხვი >> (8 * i) & 0x00000000FF)
	}
	return მასივი
}
func Unsignedinteger48toმასივიbe(რიცხვი uint64) [6]byte {
	var მასივი [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		მასივი[5-i] = byte(რიცხვი >> (8 * i) & 0x00000000FF)
	}
	return მასივი
}
func Unsignedinteger64toმასივი(რიცხვი uint64) [8]byte {
	var მასივი [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		მასივი[1-i] = byte(რიცხვი >> (8 * i) & 0x00000000000000FF)
	}
	return მასივი
}
func Aმასივიtounsignedinteger16(მასივი [2]byte) uint16 {
	var რიცხვი uint16
	var i uint
	for i = 0; i < 2; i++ {
		რიცხვი = რიცხვი | (uint16(მასივი[1-i]) << (8 * i))
	}
	return რიცხვი
}
func Aმასივიtounsignedinteger32(მასივი [4]byte) uint32 {
	var რიცხვი uint32
	var i uint
	for i = 0; i < 4; i++ {
		რიცხვი = რიცხვი | (uint32(მასივი[3-i]) << (8 * i))
	}
	return რიცხვი
}
func Aმასივიtounsignedinteger48(მასივი [6]byte) uint64 {
	var რიცხვი uint64
	var i uint
	for i = 0; i < 6; i++ {
		რიცხვი = რიცხვი | (uint64(მასივი[5-i]) << (8 * i))
	}
	return რიცხვი

}
func Aმასივიtounsignedinteger48be(მასივი [6]byte) uint64 {
	var რიცხვი uint64
	var i uint
	for i = 0; i < 6; i++ {
		რიცხვი = რიცხვი | (uint64(მასივი[i]) << (8 * i))
	}
	return რიცხვი
}
func Aმასივიtounsignedinteger64(მასივი [8]byte) uint64 {
	var რიცხვი uint64
	var i uint
	for i = 0; i < 8; i++ {
		რიცხვი = რიცხვი | (uint64(მასივი[7-i]) << (8 * i))
	}
	return რიცხვი
}
func Unsignedinteger64r(რიცხვი uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(რიცხვი>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(რიცხვი uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(რიცხვი>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(რიცხვი uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(რიცხვი>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(რიცხვი uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(რიცხვი>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Pბეჭდვაბაიტი(dataკურსორი uintptr, ზომა int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataკურსორი))
	var i int
	utilconsole.Mბეჭდვა([]byte("util["))
	for i = 0; i < ზომა; i++ {
		utilconsole.MHexadecimalბეჭდვა(buffer_2[i])
	}
	utilconsole.Mბეჭდვა([]byte("]"))
}

func Pბეჭდვაtest(params ...interface{}) {
	for _, param := range params {
		utilconsole.Mბეჭდვა([]byte(TypeOf(param).Name()))

	}
}
func Equalბაიტი(a, b []byte) bool {
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
func Bბაიტიtostring(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerკურსორიმასივიfromკურსორი(კურსორი_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{კურსორი_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32მასივიfromკურსორი(კურსორი_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{კურსორი_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getბაიტიfromკურსორი(კურსორი_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{კურსორი_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncკურსორიfromკურსორი(კურსორი_2 uintptr) func() {
	code1კურსორი_2 := uintptr(Pointer(&კურსორი_2))
	return *(*func())(Pointer(&code1კურსორი_2))
}
