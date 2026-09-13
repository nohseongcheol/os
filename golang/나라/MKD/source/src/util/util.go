package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toПострои(number uint16) [2]byte {
	var построи [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		построи[i] = byte(number >> (8 * i) & 0x00FF)
	}
	return построи
}
func Unsignedinteger16toПостроиbe(number uint16) [2]byte {
	var построи [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		построи[2-i] = byte(number >> (8 * i) & 0x00FF)
	}
	return построи
}

func Unsignedinteger32toПострои(number uint32) [4]byte {
	var построи [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		построи[i] = byte(number >> (8 * i) & 0x000000FF)
	}
	return построи
}
func Unsignedinteger48toПострои(number uint64) [6]byte {
	var построи [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		построи[i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return построи
}
func Unsignedinteger48toПостроиbe(number uint64) [6]byte {
	var построи [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		построи[5-i] = byte(number >> (8 * i) & 0x00000000FF)
	}
	return построи
}
func Unsignedinteger64toПострои(number uint64) [8]byte {
	var построи [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		построи[1-i] = byte(number >> (8 * i) & 0x00000000000000FF)
	}
	return построи
}
func Построиtounsignedinteger16(построи [2]byte) uint16 {
	var number uint16
	var i uint
	for i = 0; i < 2; i++ {
		number = number | (uint16(построи[1-i]) << (8 * i))
	}
	return number
}
func Построиtounsignedinteger32(построи [4]byte) uint32 {
	var number uint32
	var i uint
	for i = 0; i < 4; i++ {
		number = number | (uint32(построи[3-i]) << (8 * i))
	}
	return number
}
func Построиtounsignedinteger48(построи [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(построи[5-i]) << (8 * i))
	}
	return number

}
func Построиtounsignedinteger48be(построи [6]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 6; i++ {
		number = number | (uint64(построи[i]) << (8 * i))
	}
	return number
}
func Построиtounsignedinteger64(построи [8]byte) uint64 {
	var number uint64
	var i uint
	for i = 0; i < 8; i++ {
		number = number | (uint64(построи[7-i]) << (8 * i))
	}
	return number
}
func Unsignedinteger64r(number uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(number>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(number uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(number>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(number uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(number>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(number uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(number>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Печатибајти(dataСтрелка uintptr, големина int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataСтрелка))
	var i int
	utilconsole.MПечати([]byte("util["))
	for i = 0; i < големина; i++ {
		utilconsole.MHexadecimalПечати(buffer_2[i])
	}
	utilconsole.MПечати([]byte("]"))
}

func Печатиtest(params ...interface{}) {
	for _, param := range params {
		utilconsole.MПечати([]byte(TypeOf(param).Name()))

	}
}
func Equalбајти(a, b []byte) bool {
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
func Бајтиtostring(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerСтрелкаПостроиfromСтрелка(стрелка_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{стрелка_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ПостроиfromСтрелка(стрелка_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{стрелка_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetбајтиfromСтрелка(стрелка_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{стрелка_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncСтрелкаfromСтрелка(стрелка_2 uintptr) func() {
	code1Стрелка_2 := uintptr(Pointer(&стрелка_2))
	return *(*func())(Pointer(&code1Стрелка_2))
}
