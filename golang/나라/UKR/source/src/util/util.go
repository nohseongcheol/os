package util

import . "консоль"
import . "unsafe"
import . "reflect"

var utilКонсоль TКонсоль = TКонсоль{}

func Unsignedinteger16тоМасив(число uint16) [2]byte {
	var масив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масив[i] = byte(число >> (8 * i) & 0x00FF)
	}
	return масив
}
func Unsignedinteger16тоМасивbe(число uint16) [2]byte {
	var масив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		масив[2-i] = byte(число >> (8 * i) & 0x00FF)
	}
	return масив
}

func Unsignedinteger32тоМасив(число uint32) [4]byte {
	var масив [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		масив[i] = byte(число >> (8 * i) & 0x000000FF)
	}
	return масив
}
func Unsignedinteger48тоМасив(число uint64) [6]byte {
	var масив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масив[i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return масив
}
func Unsignedinteger48тоМасивbe(число uint64) [6]byte {
	var масив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		масив[5-i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return масив
}
func Unsignedinteger64тоМасив(число uint64) [8]byte {
	var масив [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		масив[1-i] = byte(число >> (8 * i) & 0x00000000000000FF)
	}
	return масив
}
func Масивтоunsignedinteger16(масив [2]byte) uint16 {
	var число uint16
	var i uint
	for i = 0; i < 2; i++ {
		число = число | (uint16(масив[1-i]) << (8 * i))
	}
	return число
}
func Масивтоunsignedinteger32(масив [4]byte) uint32 {
	var число uint32
	var i uint
	for i = 0; i < 4; i++ {
		число = число | (uint32(масив[3-i]) << (8 * i))
	}
	return число
}
func Масивтоunsignedinteger48(масив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(масив[5-i]) << (8 * i))
	}
	return число

}
func Масивтоunsignedinteger48be(масив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(масив[i]) << (8 * i))
	}
	return число
}
func Масивтоunsignedinteger64(масив [8]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 8; i++ {
		число = число | (uint64(масив[7-i]) << (8 * i))
	}
	return число
}
func Unsignedinteger64r(число uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(число>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(число uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(число>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(число uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(число>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(число uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(число>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ДрукБайт(dataВказівник uintptr, розмір int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataВказівник))
	var i int
	utilКонсоль.MДрук([]byte("util["))
	for i = 0; i < розмір; i++ {
		utilКонсоль.MHexadecimalДрук(buffer_2[i])
	}
	utilКонсоль.MДрук([]byte("]"))
}

func ДрукТест(параметри_2 ...interface{}) {
	for _, param := range параметри_2 {
		utilКонсоль.MДрук([]byte(TypeOf(param).Name()))

	}
}
func РівноБайт(a, b []byte) bool {
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
func БайттоРядок(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerВказівникМасивзВказівник(посилання_на_адресу_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		адреса	uintptr
		len	int
		cap	int
	}{посилання_на_адресу_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32МасивзВказівник(посилання_на_адресу_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		адреса	uintptr
		len	int
		cap	int
	}{посилання_на_адресу_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБайтзВказівник(посилання_на_адресу_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		адреса	uintptr
		len	int
		cap	int
	}{посилання_на_адресу_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncВказівникзВказівник(посилання_на_адресу_2 uintptr) func() {
	code1Вказівник_2 := uintptr(Pointer(&посилання_на_адресу_2))
	return *(*func())(Pointer(&code1Вказівник_2))
}
