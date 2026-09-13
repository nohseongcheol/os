package hilfswerkzeug

import . "konsole"
import . "unsafe"
import . "reflect"

var hilfswerkzeugKonsole TKonsole = TKonsole{}

func Unsignedinteger16toFeld(nummer uint16) [2]byte {
	var feld [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		feld[i] = byte(nummer >> (8 * i) & 0x00FF)
	}
	return feld
}
func Unsignedinteger16toFeldbe(nummer uint16) [2]byte {
	var feld [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		feld[2-i] = byte(nummer >> (8 * i) & 0x00FF)
	}
	return feld
}

func Unsignedinteger32toFeld(nummer uint32) [4]byte {
	var feld [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		feld[i] = byte(nummer >> (8 * i) & 0x000000FF)
	}
	return feld
}
func Unsignedinteger48toFeld(nummer uint64) [6]byte {
	var feld [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		feld[i] = byte(nummer >> (8 * i) & 0x00000000FF)
	}
	return feld
}
func Unsignedinteger48toFeldbe(nummer uint64) [6]byte {
	var feld [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		feld[5-i] = byte(nummer >> (8 * i) & 0x00000000FF)
	}
	return feld
}
func Unsignedinteger64toFeld(nummer uint64) [8]byte {
	var feld [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		feld[1-i] = byte(nummer >> (8 * i) & 0x00000000000000FF)
	}
	return feld
}
func Feldtounsignedinteger16(feld [2]byte) uint16 {
	var nummer uint16
	var i uint
	for i = 0; i < 2; i++ {
		nummer = nummer | (uint16(feld[1-i]) << (8 * i))
	}
	return nummer
}
func Feldtounsignedinteger32(feld [4]byte) uint32 {
	var nummer uint32
	var i uint
	for i = 0; i < 4; i++ {
		nummer = nummer | (uint32(feld[3-i]) << (8 * i))
	}
	return nummer
}
func Feldtounsignedinteger48(feld [6]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 6; i++ {
		nummer = nummer | (uint64(feld[5-i]) << (8 * i))
	}
	return nummer

}
func Feldtounsignedinteger48be(feld [6]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 6; i++ {
		nummer = nummer | (uint64(feld[i]) << (8 * i))
	}
	return nummer
}
func Feldtounsignedinteger64(feld [8]byte) uint64 {
	var nummer uint64
	var i uint
	for i = 0; i < 8; i++ {
		nummer = nummer | (uint64(feld[7-i]) << (8 * i))
	}
	return nummer
}
func Unsignedinteger64r(nummer uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nummer>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nummer uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nummer>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nummer uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nummer>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nummer uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nummer>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func DruckenByte(datenZeiger uintptr, größe int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(datenZeiger))
	var i int
	hilfswerkzeugKonsole.MDrucken([]byte("util["))
	for i = 0; i < größe; i++ {
		hilfswerkzeugKonsole.MHexadecimalDrucken(buffer_2[i])
	}
	hilfswerkzeugKonsole.MDrucken([]byte("]"))
}

func DruckenTesten(parameter ...interface{}) {
	for _, param := range parameter {
		hilfswerkzeugKonsole.MDrucken([]byte(TypeOf(param).Name()))

	}
}
func EntsprechendByte(a, b []byte) bool {
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
func BytetoZeichenkette(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerZeigerFeldvonZeiger(adressverweis_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adressverweis_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32FeldvonZeiger(adressverweis_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adressverweis_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetBytevonZeiger(adressverweis_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{adressverweis_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncZeigervonZeiger(adressverweis_2 uintptr) func() {
	code1Zeiger_2 := uintptr(Pointer(&adressverweis_2))
	return *(*func())(Pointer(&code1Zeiger_2))
}
