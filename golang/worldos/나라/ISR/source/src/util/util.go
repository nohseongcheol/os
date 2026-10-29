/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toמערך(מספר uint16) [2]byte {
	var מערך [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		מערך[i] = byte(מספר >> (8 * i) & 0x00FF)
	}
	return מערך
}
func Unsignedinteger16toמערךbe(מספר uint16) [2]byte {
	var מערך [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		מערך[2-i] = byte(מספר >> (8 * i) & 0x00FF)
	}
	return מערך
}

func Unsignedinteger32toמערך(מספר uint32) [4]byte {
	var מערך [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		מערך[i] = byte(מספר >> (8 * i) & 0x000000FF)
	}
	return מערך
}
func Unsignedinteger48toמערך(מספר uint64) [6]byte {
	var מערך [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		מערך[i] = byte(מספר >> (8 * i) & 0x00000000FF)
	}
	return מערך
}
func Unsignedinteger48toמערךbe(מספר uint64) [6]byte {
	var מערך [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		מערך[5-i] = byte(מספר >> (8 * i) & 0x00000000FF)
	}
	return מערך
}
func Unsignedinteger64toמערך(מספר uint64) [8]byte {
	var מערך [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		מערך[1-i] = byte(מספר >> (8 * i) & 0x00000000000000FF)
	}
	return מערך
}
func Aמערךtounsignedinteger16(מערך [2]byte) uint16 {
	var מספר uint16
	var i uint
	for i = 0; i < 2; i++ {
		מספר = מספר | (uint16(מערך[1-i]) << (8 * i))
	}
	return מספר
}
func Aמערךtounsignedinteger32(מערך [4]byte) uint32 {
	var מספר uint32
	var i uint
	for i = 0; i < 4; i++ {
		מספר = מספר | (uint32(מערך[3-i]) << (8 * i))
	}
	return מספר
}
func Aמערךtounsignedinteger48(מערך [6]byte) uint64 {
	var מספר uint64
	var i uint
	for i = 0; i < 6; i++ {
		מספר = מספר | (uint64(מערך[5-i]) << (8 * i))
	}
	return מספר

}
func Aמערךtounsignedinteger48be(מערך [6]byte) uint64 {
	var מספר uint64
	var i uint
	for i = 0; i < 6; i++ {
		מספר = מספר | (uint64(מערך[i]) << (8 * i))
	}
	return מספר
}
func Aמערךtounsignedinteger64(מערך [8]byte) uint64 {
	var מספר uint64
	var i uint
	for i = 0; i < 8; i++ {
		מספר = מספר | (uint64(מערך[7-i]) << (8 * i))
	}
	return מספר
}
func Unsignedinteger64r(מספר uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(מספר>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(מספר uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(מספר>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(מספר uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(מספר>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(מספר uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(מספר>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Pהדפסהבתים(dataסמן uintptr, גודל int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataסמן))
	var i int
	utilconsole.Mהדפסה([]byte("util["))
	for i = 0; i < גודל; i++ {
		utilconsole.MHexadecimalהדפסה(buffer_2[i])
	}
	utilconsole.Mהדפסה([]byte("]"))
}

func Pהדפסהבדיקה(ארגומרנטים ...interface{}) {
	for _, param := range ארגומרנטים {
		utilconsole.Mהדפסה([]byte(TypeOf(param).Name()))

	}
}
func Equalבתים(a, b []byte) bool {
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
func Bבתיםtoמחרוזת(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerסמןמערךfromסמן(סמן_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{סמן_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32מערךfromסמן(סמן_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{סמן_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getבתיםfromסמן(סמן_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{סמן_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncסמןfromסמן(סמן_2 uintptr) func() {
	code1סמן_2 := uintptr(Pointer(&סמן_2))
	return *(*func())(Pointer(&code1סמן_2))
}
