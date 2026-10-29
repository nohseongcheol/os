/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toMasyvas(skaičius uint16) [2]byte {
	var masyvas [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		masyvas[i] = byte(skaičius >> (8 * i) & 0x00FF)
	}
	return masyvas
}
func Unsignedinteger16toMasyvasbe(skaičius uint16) [2]byte {
	var masyvas [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		masyvas[2-i] = byte(skaičius >> (8 * i) & 0x00FF)
	}
	return masyvas
}

func Unsignedinteger32toMasyvas(skaičius uint32) [4]byte {
	var masyvas [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		masyvas[i] = byte(skaičius >> (8 * i) & 0x000000FF)
	}
	return masyvas
}
func Unsignedinteger48toMasyvas(skaičius uint64) [6]byte {
	var masyvas [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		masyvas[i] = byte(skaičius >> (8 * i) & 0x00000000FF)
	}
	return masyvas
}
func Unsignedinteger48toMasyvasbe(skaičius uint64) [6]byte {
	var masyvas [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		masyvas[5-i] = byte(skaičius >> (8 * i) & 0x00000000FF)
	}
	return masyvas
}
func Unsignedinteger64toMasyvas(skaičius uint64) [8]byte {
	var masyvas [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		masyvas[1-i] = byte(skaičius >> (8 * i) & 0x00000000000000FF)
	}
	return masyvas
}
func Masyvastounsignedinteger16(masyvas [2]byte) uint16 {
	var skaičius uint16
	var i uint
	for i = 0; i < 2; i++ {
		skaičius = skaičius | (uint16(masyvas[1-i]) << (8 * i))
	}
	return skaičius
}
func Masyvastounsignedinteger32(masyvas [4]byte) uint32 {
	var skaičius uint32
	var i uint
	for i = 0; i < 4; i++ {
		skaičius = skaičius | (uint32(masyvas[3-i]) << (8 * i))
	}
	return skaičius
}
func Masyvastounsignedinteger48(masyvas [6]byte) uint64 {
	var skaičius uint64
	var i uint
	for i = 0; i < 6; i++ {
		skaičius = skaičius | (uint64(masyvas[5-i]) << (8 * i))
	}
	return skaičius

}
func Masyvastounsignedinteger48be(masyvas [6]byte) uint64 {
	var skaičius uint64
	var i uint
	for i = 0; i < 6; i++ {
		skaičius = skaičius | (uint64(masyvas[i]) << (8 * i))
	}
	return skaičius
}
func Masyvastounsignedinteger64(masyvas [8]byte) uint64 {
	var skaičius uint64
	var i uint
	for i = 0; i < 8; i++ {
		skaičius = skaičius | (uint64(masyvas[7-i]) << (8 * i))
	}
	return skaičius
}
func Unsignedinteger64r(skaičius uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(skaičius>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(skaičius uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(skaičius>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(skaičius uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(skaičius>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(skaičius uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(skaičius>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func SpausdintiBaitų(dataRodyklė uintptr, dydis int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataRodyklė))
	var i int
	utilconsole.MSpausdinti([]byte("util["))
	for i = 0; i < dydis; i++ {
		utilconsole.MHexadecimalSpausdinti(buffer_2[i])
	}
	utilconsole.MSpausdinti([]byte("]"))
}

func SpausdintiTestas(parametrai_2 ...interface{}) {
	for _, param := range parametrai_2 {
		utilconsole.MSpausdinti([]byte(TypeOf(param).Name()))

	}
}
func SuvienodintiBaitų(a, b []byte) bool {
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
func BaitųtoEilutė(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerRodyklėMasyvasfromRodyklė(rodyklė_3 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rodyklė_3, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32MasyvasfromRodyklė(rodyklė_3 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rodyklė_3, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBaitųfromRodyklė(rodyklė_3 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rodyklė_3, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncRodyklėfromRodyklė(rodyklė_3 uintptr) func() {
	code1Rodyklė_2 := uintptr(Pointer(&rodyklė_3))
	return *(*func())(Pointer(&code1Rodyklė_2))
}
