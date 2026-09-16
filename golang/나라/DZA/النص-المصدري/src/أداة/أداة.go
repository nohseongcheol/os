/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package أداة

import . "طرفية"
import . "unsafe"
import . "reflect"

var أداةطرفية Tطرفية = Tطرفية{}

func Unsignedinteger16toمصفوفة(الأرقام uint16) [2]byte {
	var مصفوفة [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		مصفوفة[i] = byte(الأرقام >> (8 * i) & 0x00FF)
	}
	return مصفوفة
}
func Unsignedinteger16toمصفوفةbe(الأرقام uint16) [2]byte {
	var مصفوفة [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		مصفوفة[2-i] = byte(الأرقام >> (8 * i) & 0x00FF)
	}
	return مصفوفة
}

func Unsignedinteger32toمصفوفة(الأرقام uint32) [4]byte {
	var مصفوفة [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		مصفوفة[i] = byte(الأرقام >> (8 * i) & 0x000000FF)
	}
	return مصفوفة
}
func Unsignedinteger48toمصفوفة(الأرقام uint64) [6]byte {
	var مصفوفة [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		مصفوفة[i] = byte(الأرقام >> (8 * i) & 0x00000000FF)
	}
	return مصفوفة
}
func Unsignedinteger48toمصفوفةbe(الأرقام uint64) [6]byte {
	var مصفوفة [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		مصفوفة[5-i] = byte(الأرقام >> (8 * i) & 0x00000000FF)
	}
	return مصفوفة
}
func Unsignedinteger64toمصفوفة(الأرقام uint64) [8]byte {
	var مصفوفة [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		مصفوفة[1-i] = byte(الأرقام >> (8 * i) & 0x00000000000000FF)
	}
	return مصفوفة
}
func Aمصفوفةtounsignedinteger16(مصفوفة [2]byte) uint16 {
	var الأرقام uint16
	var i uint
	for i = 0; i < 2; i++ {
		الأرقام = الأرقام | (uint16(مصفوفة[1-i]) << (8 * i))
	}
	return الأرقام
}
func Aمصفوفةtounsignedinteger32(مصفوفة [4]byte) uint32 {
	var الأرقام uint32
	var i uint
	for i = 0; i < 4; i++ {
		الأرقام = الأرقام | (uint32(مصفوفة[3-i]) << (8 * i))
	}
	return الأرقام
}
func Aمصفوفةtounsignedinteger48(مصفوفة [6]byte) uint64 {
	var الأرقام uint64
	var i uint
	for i = 0; i < 6; i++ {
		الأرقام = الأرقام | (uint64(مصفوفة[5-i]) << (8 * i))
	}
	return الأرقام

}
func Aمصفوفةtounsignedinteger48be(مصفوفة [6]byte) uint64 {
	var الأرقام uint64
	var i uint
	for i = 0; i < 6; i++ {
		الأرقام = الأرقام | (uint64(مصفوفة[i]) << (8 * i))
	}
	return الأرقام
}
func Aمصفوفةtounsignedinteger64(مصفوفة [8]byte) uint64 {
	var الأرقام uint64
	var i uint
	for i = 0; i < 8; i++ {
		الأرقام = الأرقام | (uint64(مصفوفة[7-i]) << (8 * i))
	}
	return الأرقام
}
func Unsignedinteger64r(الأرقام uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(الأرقام>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(الأرقام uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(الأرقام>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(الأرقام uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(الأرقام>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(الأرقام uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(الأرقام>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Pاطبعبايت(بياناتالمؤشر uintptr, الحجم int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(بياناتالمؤشر))
	var i int
	أداةطرفية.Mاطبع([]byte("util["))
	for i = 0; i < الحجم; i++ {
		أداةطرفية.MHexadecimalاطبع(buffer_2[i])
	}
	أداةطرفية.Mاطبع([]byte("]"))
}

func Pاطبعتجريب(المعاملات ...interface{}) {
	for _, param := range المعاملات {
		أداةطرفية.Mاطبع([]byte(TypeOf(param).Name()))

	}
}
func Eمساويبايت(a, b []byte) bool {
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
func Bبايتtoسلسلة(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func Getunsignedintegerالمؤشرمصفوفةfromالمؤشر(مرجع_عنوان_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{مرجع_عنوان_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32مصفوفةfromالمؤشر(مرجع_عنوان_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{مرجع_عنوان_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func Getبايتfromالمؤشر(مرجع_عنوان_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{مرجع_عنوان_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func Getfuncالمؤشرfromالمؤشر(مرجع_عنوان_2 uintptr) func() {
	code1المؤشر_2 := uintptr(Pointer(&مرجع_عنوان_2))
	return *(*func())(Pointer(&code1المؤشر_2))
}
