/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "konzol"
import . "unsafe"
import . "reflect"

var utilKonzol TKonzol = TKonzol{}

func Unsignedinteger16toTömb(szám uint16) [2]byte {
	var tömb [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tömb[i] = byte(szám >> (8 * i) & 0x00FF)
	}
	return tömb
}
func Unsignedinteger16toTömbbe(szám uint16) [2]byte {
	var tömb [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tömb[2-i] = byte(szám >> (8 * i) & 0x00FF)
	}
	return tömb
}

func Unsignedinteger32toTömb(szám uint32) [4]byte {
	var tömb [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		tömb[i] = byte(szám >> (8 * i) & 0x000000FF)
	}
	return tömb
}
func Unsignedinteger48toTömb(szám uint64) [6]byte {
	var tömb [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tömb[i] = byte(szám >> (8 * i) & 0x00000000FF)
	}
	return tömb
}
func Unsignedinteger48toTömbbe(szám uint64) [6]byte {
	var tömb [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tömb[5-i] = byte(szám >> (8 * i) & 0x00000000FF)
	}
	return tömb
}
func Unsignedinteger64toTömb(szám uint64) [8]byte {
	var tömb [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		tömb[1-i] = byte(szám >> (8 * i) & 0x00000000000000FF)
	}
	return tömb
}
func Tömbtounsignedinteger16(tömb [2]byte) uint16 {
	var szám uint16
	var i uint
	for i = 0; i < 2; i++ {
		szám = szám | (uint16(tömb[1-i]) << (8 * i))
	}
	return szám
}
func Tömbtounsignedinteger32(tömb [4]byte) uint32 {
	var szám uint32
	var i uint
	for i = 0; i < 4; i++ {
		szám = szám | (uint32(tömb[3-i]) << (8 * i))
	}
	return szám
}
func Tömbtounsignedinteger48(tömb [6]byte) uint64 {
	var szám uint64
	var i uint
	for i = 0; i < 6; i++ {
		szám = szám | (uint64(tömb[5-i]) << (8 * i))
	}
	return szám

}
func Tömbtounsignedinteger48be(tömb [6]byte) uint64 {
	var szám uint64
	var i uint
	for i = 0; i < 6; i++ {
		szám = szám | (uint64(tömb[i]) << (8 * i))
	}
	return szám
}
func Tömbtounsignedinteger64(tömb [8]byte) uint64 {
	var szám uint64
	var i uint
	for i = 0; i < 8; i++ {
		szám = szám | (uint64(tömb[7-i]) << (8 * i))
	}
	return szám
}
func Unsignedinteger64r(szám uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(szám>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(szám uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(szám>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(szám uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(szám>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(szám uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(szám>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func NyomtatásBájt(dataMutató uintptr, méret int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataMutató))
	var i int
	utilKonzol.MNyomtatás([]byte("util["))
	for i = 0; i < méret; i++ {
		utilKonzol.MHexadecimalNyomtatás(buffer_2[i])
	}
	utilKonzol.MNyomtatás([]byte("]"))
}

func NyomtatásTeszt(paraméterek ...interface{}) {
	for _, param := range paraméterek {
		utilKonzol.MNyomtatás([]byte(TypeOf(param).Name()))

	}
}
func EgyenlőBájt(a, b []byte) bool {
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
func BájttoKarakterlánc(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerMutatóTömbfromMutató(mutató_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{mutató_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32TömbfromMutató(mutató_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{mutató_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBájtfromMutató(mutató_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{mutató_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncMutatófromMutató(mutató_2 uintptr) func() {
	code1Mutató_2 := uintptr(Pointer(&mutató_2))
	return *(*func())(Pointer(&code1Mutató_2))
}
