package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toማዘጋጃ(ቁጥር uint16) [2]byte {
	var ማዘጋጃ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		ማዘጋጃ[i] = byte(ቁጥር >> (8 * i) & 0x00FF)
	}
	return ማዘጋጃ
}
func Unsignedinteger16toማዘጋጃbe(ቁጥር uint16) [2]byte {
	var ማዘጋጃ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		ማዘጋጃ[2-i] = byte(ቁጥር >> (8 * i) & 0x00FF)
	}
	return ማዘጋጃ
}

func Unsignedinteger32toማዘጋጃ(ቁጥር uint32) [4]byte {
	var ማዘጋጃ [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		ማዘጋጃ[i] = byte(ቁጥር >> (8 * i) & 0x000000FF)
	}
	return ማዘጋጃ
}
func Unsignedinteger48toማዘጋጃ(ቁጥር uint64) [6]byte {
	var ማዘጋጃ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		ማዘጋጃ[i] = byte(ቁጥር >> (8 * i) & 0x00000000FF)
	}
	return ማዘጋጃ
}
func Unsignedinteger48toማዘጋጃbe(ቁጥር uint64) [6]byte {
	var ማዘጋጃ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		ማዘጋጃ[5-i] = byte(ቁጥር >> (8 * i) & 0x00000000FF)
	}
	return ማዘጋጃ
}
func Unsignedinteger64toማዘጋጃ(ቁጥር uint64) [8]byte {
	var ማዘጋጃ [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		ማዘጋጃ[1-i] = byte(ቁጥር >> (8 * i) & 0x00000000000000FF)
	}
	return ማዘጋጃ
}
func Aማዘጋጃtounsignedinteger16(ማዘጋጃ [2]byte) uint16 {
	var ቁጥር uint16
	var i uint
	for i = 0; i < 2; i++ {
		ቁጥር = ቁጥር | (uint16(ማዘጋጃ[1-i]) << (8 * i))
	}
	return ቁጥር
}
func Aማዘጋጃtounsignedinteger32(ማዘጋጃ [4]byte) uint32 {
	var ቁጥር uint32
	var i uint
	for i = 0; i < 4; i++ {
		ቁጥር = ቁጥር | (uint32(ማዘጋጃ[3-i]) << (8 * i))
	}
	return ቁጥር
}
func Aማዘጋጃtounsignedinteger48(ማዘጋጃ [6]byte) uint64 {
	var ቁጥር uint64
	var i uint
	for i = 0; i < 6; i++ {
		ቁጥር = ቁጥር | (uint64(ማዘጋጃ[5-i]) << (8 * i))
	}
	return ቁጥር

}
func Aማዘጋጃtounsignedinteger48be(ማዘጋጃ [6]byte) uint64 {
	var ቁጥር uint64
	var i uint
	for i = 0; i < 6; i++ {
		ቁጥር = ቁጥር | (uint64(ማዘጋጃ[i]) << (8 * i))
	}
	return ቁጥር
}
func Aማዘጋጃtounsignedinteger64(ማዘጋጃ [8]byte) uint64 {
	var ቁጥር uint64
	var i uint
	for i = 0; i < 8; i++ {
		ቁጥር = ቁጥር | (uint64(ማዘጋጃ[7-i]) << (8 * i))
	}
	return ቁጥር
}
func Unsignedinteger64r(ቁጥር uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(ቁጥር>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(ቁጥር uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(ቁጥር>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(ቁጥር uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(ቁጥር>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(ቁጥር uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(ቁጥር>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Pማተሚያባይትስ(dataጠቋሚ uintptr, መጠን int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataጠቋሚ))
	var i int
	utilconsole.Mማተሚያ([]byte("util["))
	for i = 0; i < መጠን; i++ {
		utilconsole.MHexadecimalማተሚያ(buffer_2[i])
	}
	utilconsole.Mማተሚያ([]byte("]"))
}

func Pማተሚያመሞከሪያ(params ...interface{}) {
	for _, param := range params {
		utilconsole.Mማተሚያ([]byte(TypeOf(param).Name()))

	}
}
func Equalባይትስ(a, b []byte) bool {
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
func Bባይትስtoሐረግ(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerጠቋሚማዘጋጃfromጠቋሚ(ጠቋሚ_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ጠቋሚ_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ማዘጋጃfromጠቋሚ(ጠቋሚ_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ጠቋሚ_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getባይትስfromጠቋሚ(ጠቋሚ_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ጠቋሚ_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncጠቋሚfromጠቋሚ(ጠቋሚ_2 uintptr) func() {
	code1ጠቋሚ_2 := uintptr(Pointer(&ጠቋሚ_2))
	return *(*func())(Pointer(&code1ጠቋሚ_2))
}
