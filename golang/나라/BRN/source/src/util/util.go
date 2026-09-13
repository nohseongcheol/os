package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toTatasusunan(nOMBOR uint16) [2]byte {
	var tatasusunan [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tatasusunan[i] = byte(nOMBOR >> (8 * i) & 0x00FF)
	}
	return tatasusunan
}
func Unsignedinteger16toTatasusunanbe(nOMBOR uint16) [2]byte {
	var tatasusunan [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tatasusunan[2-i] = byte(nOMBOR >> (8 * i) & 0x00FF)
	}
	return tatasusunan
}

func Unsignedinteger32toTatasusunan(nOMBOR uint32) [4]byte {
	var tatasusunan [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		tatasusunan[i] = byte(nOMBOR >> (8 * i) & 0x000000FF)
	}
	return tatasusunan
}
func Unsignedinteger48toTatasusunan(nOMBOR uint64) [6]byte {
	var tatasusunan [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tatasusunan[i] = byte(nOMBOR >> (8 * i) & 0x00000000FF)
	}
	return tatasusunan
}
func Unsignedinteger48toTatasusunanbe(nOMBOR uint64) [6]byte {
	var tatasusunan [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tatasusunan[5-i] = byte(nOMBOR >> (8 * i) & 0x00000000FF)
	}
	return tatasusunan
}
func Unsignedinteger64toTatasusunan(nOMBOR uint64) [8]byte {
	var tatasusunan [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		tatasusunan[1-i] = byte(nOMBOR >> (8 * i) & 0x00000000000000FF)
	}
	return tatasusunan
}
func Tatasusunantounsignedinteger16(tatasusunan [2]byte) uint16 {
	var nOMBOR uint16
	var i uint
	for i = 0; i < 2; i++ {
		nOMBOR = nOMBOR | (uint16(tatasusunan[1-i]) << (8 * i))
	}
	return nOMBOR
}
func Tatasusunantounsignedinteger32(tatasusunan [4]byte) uint32 {
	var nOMBOR uint32
	var i uint
	for i = 0; i < 4; i++ {
		nOMBOR = nOMBOR | (uint32(tatasusunan[3-i]) << (8 * i))
	}
	return nOMBOR
}
func Tatasusunantounsignedinteger48(tatasusunan [6]byte) uint64 {
	var nOMBOR uint64
	var i uint
	for i = 0; i < 6; i++ {
		nOMBOR = nOMBOR | (uint64(tatasusunan[5-i]) << (8 * i))
	}
	return nOMBOR

}
func Tatasusunantounsignedinteger48be(tatasusunan [6]byte) uint64 {
	var nOMBOR uint64
	var i uint
	for i = 0; i < 6; i++ {
		nOMBOR = nOMBOR | (uint64(tatasusunan[i]) << (8 * i))
	}
	return nOMBOR
}
func Tatasusunantounsignedinteger64(tatasusunan [8]byte) uint64 {
	var nOMBOR uint64
	var i uint
	for i = 0; i < 8; i++ {
		nOMBOR = nOMBOR | (uint64(tatasusunan[7-i]) << (8 * i))
	}
	return nOMBOR
}
func Unsignedinteger64r(nOMBOR uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nOMBOR>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nOMBOR uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nOMBOR>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nOMBOR uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nOMBOR>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nOMBOR uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nOMBOR>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func CetakBait(dataPenuding uintptr, saiz int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataPenuding))
	var i int
	utilconsole.MCetak([]byte("util["))
	for i = 0; i < saiz; i++ {
		utilconsole.MHexadecimalCetak(buffer_2[i])
	}
	utilconsole.MCetak([]byte("]"))
}

func CetakUji(params ...interface{}) {
	for _, param := range params {
		utilconsole.MCetak([]byte(TypeOf(param).Name()))

	}
}
func SamaBait(a, b []byte) bool {
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
func BaittoRentetan(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPenudingTatasusunanfromPenuding(rujukan_alamat_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rujukan_alamat_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32TatasusunanfromPenuding(rujukan_alamat_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rujukan_alamat_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBaitfromPenuding(rujukan_alamat_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{rujukan_alamat_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPenudingfromPenuding(rujukan_alamat_2 uintptr) func() {
	code1Penuding_2 := uintptr(Pointer(&rujukan_alamat_2))
	return *(*func())(Pointer(&code1Penuding_2))
}
