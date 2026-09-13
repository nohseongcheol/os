package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16naarReeks(getal uint16) [2]byte {
	var reeks [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		reeks[i] = byte(getal >> (8 * i) & 0x00FF)
	}
	return reeks
}
func Unsignedinteger16naarReeksbe(getal uint16) [2]byte {
	var reeks [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		reeks[2-i] = byte(getal >> (8 * i) & 0x00FF)
	}
	return reeks
}

func Unsignedinteger32naarReeks(getal uint32) [4]byte {
	var reeks [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		reeks[i] = byte(getal >> (8 * i) & 0x000000FF)
	}
	return reeks
}
func Unsignedinteger48naarReeks(getal uint64) [6]byte {
	var reeks [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		reeks[i] = byte(getal >> (8 * i) & 0x00000000FF)
	}
	return reeks
}
func Unsignedinteger48naarReeksbe(getal uint64) [6]byte {
	var reeks [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		reeks[5-i] = byte(getal >> (8 * i) & 0x00000000FF)
	}
	return reeks
}
func Unsignedinteger64naarReeks(getal uint64) [8]byte {
	var reeks [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		reeks[1-i] = byte(getal >> (8 * i) & 0x00000000000000FF)
	}
	return reeks
}
func Reeksnaarunsignedinteger16(reeks [2]byte) uint16 {
	var getal uint16
	var i uint
	for i = 0; i < 2; i++ {
		getal = getal | (uint16(reeks[1-i]) << (8 * i))
	}
	return getal
}
func Reeksnaarunsignedinteger32(reeks [4]byte) uint32 {
	var getal uint32
	var i uint
	for i = 0; i < 4; i++ {
		getal = getal | (uint32(reeks[3-i]) << (8 * i))
	}
	return getal
}
func Reeksnaarunsignedinteger48(reeks [6]byte) uint64 {
	var getal uint64
	var i uint
	for i = 0; i < 6; i++ {
		getal = getal | (uint64(reeks[5-i]) << (8 * i))
	}
	return getal

}
func Reeksnaarunsignedinteger48be(reeks [6]byte) uint64 {
	var getal uint64
	var i uint
	for i = 0; i < 6; i++ {
		getal = getal | (uint64(reeks[i]) << (8 * i))
	}
	return getal
}
func Reeksnaarunsignedinteger64(reeks [8]byte) uint64 {
	var getal uint64
	var i uint
	for i = 0; i < 8; i++ {
		getal = getal | (uint64(reeks[7-i]) << (8 * i))
	}
	return getal
}
func Unsignedinteger64r(getal uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(getal>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(getal uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(getal>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(getal uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(getal>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(getal uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(getal>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Afdrukkenbytes(dataMuisaanwijzer uintptr, grootte int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataMuisaanwijzer))
	var i int
	utilconsole.MAfdrukken([]byte("util["))
	for i = 0; i < grootte; i++ {
		utilconsole.MHexadecimalAfdrukken(buffer_2[i])
	}
	utilconsole.MAfdrukken([]byte("]"))
}

func AfdrukkenProef(params ...interface{}) {
	for _, param := range params {
		utilconsole.MAfdrukken([]byte(TypeOf(param).Name()))

	}
}
func Gelijkebytes(a, b []byte) bool {
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
func BytesnaarTekstsnoer(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerMuisaanwijzerReeksvanMuisaanwijzer(adresverwijzing_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adresverwijzing_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ReeksvanMuisaanwijzer(adresverwijzing_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adresverwijzing_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetbytesvanMuisaanwijzer(adresverwijzing_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adresverwijzing_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncMuisaanwijzervanMuisaanwijzer(adresverwijzing_2 uintptr) func() {
	code1Muisaanwijzer_2 := uintptr(Pointer(&adresverwijzing_2))
	return *(*func())(Pointer(&code1Muisaanwijzer_2))
}
