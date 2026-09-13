package util

import . "конзола"
import . "unsafe"
import . "reflect"

var utilКонзола TКонзола = TКонзола{}

func Unsignedinteger16toНиз(број uint16) [2]byte {
	var низ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		низ[i] = byte(број >> (8 * i) & 0x00FF)
	}
	return низ
}
func Unsignedinteger16toНизbe(број uint16) [2]byte {
	var низ [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		низ[2-i] = byte(број >> (8 * i) & 0x00FF)
	}
	return низ
}

func Unsignedinteger32toНиз(број uint32) [4]byte {
	var низ [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		низ[i] = byte(број >> (8 * i) & 0x000000FF)
	}
	return низ
}
func Unsignedinteger48toНиз(број uint64) [6]byte {
	var низ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		низ[i] = byte(број >> (8 * i) & 0x00000000FF)
	}
	return низ
}
func Unsignedinteger48toНизbe(број uint64) [6]byte {
	var низ [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		низ[5-i] = byte(број >> (8 * i) & 0x00000000FF)
	}
	return низ
}
func Unsignedinteger64toНиз(број uint64) [8]byte {
	var низ [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		низ[1-i] = byte(број >> (8 * i) & 0x00000000000000FF)
	}
	return низ
}
func Низtounsignedinteger16(низ [2]byte) uint16 {
	var број uint16
	var i uint
	for i = 0; i < 2; i++ {
		број = број | (uint16(низ[1-i]) << (8 * i))
	}
	return број
}
func Низtounsignedinteger32(низ [4]byte) uint32 {
	var број uint32
	var i uint
	for i = 0; i < 4; i++ {
		број = број | (uint32(низ[3-i]) << (8 * i))
	}
	return број
}
func Низtounsignedinteger48(низ [6]byte) uint64 {
	var број uint64
	var i uint
	for i = 0; i < 6; i++ {
		број = број | (uint64(низ[5-i]) << (8 * i))
	}
	return број

}
func Низtounsignedinteger48be(низ [6]byte) uint64 {
	var број uint64
	var i uint
	for i = 0; i < 6; i++ {
		број = број | (uint64(низ[i]) << (8 * i))
	}
	return број
}
func Низtounsignedinteger64(низ [8]byte) uint64 {
	var број uint64
	var i uint
	for i = 0; i < 8; i++ {
		број = број | (uint64(низ[7-i]) << (8 * i))
	}
	return број
}
func Unsignedinteger64r(број uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(број>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(број uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(број>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(број uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(број>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(број uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(број>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ШтампајБајтова(dataПоказивач uintptr, величина int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataПоказивач))
	var i int
	utilКонзола.MШтампај([]byte("util["))
	for i = 0; i < величина; i++ {
		utilКонзола.MHexadecimalШтампај(buffer_2[i])
	}
	utilКонзола.MШтампај([]byte("]"))
}

func ШтампајТест(параметри_2 ...interface{}) {
	for _, param := range параметри_2 {
		utilКонзола.MШтампај([]byte(TypeOf(param).Name()))

	}
}
func ИстаБајтова(a, b []byte) bool {
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
func Бајтоваtoниска(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerПоказивачНизсаПоказивач(показивач_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показивач_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32НизсаПоказивач(показивач_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показивач_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБајтовасаПоказивач(показивач_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{показивач_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncПоказивачсаПоказивач(показивач_2 uintptr) func() {
	code1Показивач_2 := uintptr(Pointer(&показивач_2))
	return *(*func())(Pointer(&code1Показивач_2))
}
