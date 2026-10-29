/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package утилита

import . "консоль"
import . "unsafe"
import . "reflect"

var утилитаконсоль TКонсоль = TКонсоль{}

func Unsignedinteger16кмассив(число uint16) [2]byte {
	var массив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		массив[i] = byte(число >> (8 * i) & 0x00FF)
	}
	return массив
}
func Unsignedinteger16кмассивbe(число uint16) [2]byte {
	var массив [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		массив[2-i] = byte(число >> (8 * i) & 0x00FF)
	}
	return массив
}

func Unsignedinteger32кмассив(число uint32) [4]byte {
	var массив [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		массив[i] = byte(число >> (8 * i) & 0x000000FF)
	}
	return массив
}
func Unsignedinteger48кмассив(число uint64) [6]byte {
	var массив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		массив[i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return массив
}
func Unsignedinteger48кмассивbe(число uint64) [6]byte {
	var массив [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		массив[5-i] = byte(число >> (8 * i) & 0x00000000FF)
	}
	return массив
}
func Unsignedinteger64кмассив(число uint64) [8]byte {
	var массив [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		массив[1-i] = byte(число >> (8 * i) & 0x00000000000000FF)
	}
	return массив
}
func Массивкunsignedinteger16(массив [2]byte) uint16 {
	var число uint16
	var i uint
	for i = 0; i < 2; i++ {
		число = число | (uint16(массив[1-i]) << (8 * i))
	}
	return число
}
func Массивкunsignedinteger32(массив [4]byte) uint32 {
	var число uint32
	var i uint
	for i = 0; i < 4; i++ {
		число = число | (uint32(массив[3-i]) << (8 * i))
	}
	return число
}
func Массивкunsignedinteger48(массив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(массив[5-i]) << (8 * i))
	}
	return число

}
func Массивкunsignedinteger48be(массив [6]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 6; i++ {
		число = число | (uint64(массив[i]) << (8 * i))
	}
	return число
}
func Массивкunsignedinteger64(массив [8]byte) uint64 {
	var число uint64
	var i uint
	for i = 0; i < 8; i++ {
		число = число | (uint64(массив[7-i]) << (8 * i))
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
func ПечатьБайт(данныеУказатели uintptr, размер int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(данныеУказатели))
	var i int
	утилитаконсоль.MПечать([]byte("util["))
	for i = 0; i < размер; i++ {
		утилитаконсоль.MHexadecimalПечать(buffer_2[i])
	}
	утилитаконсоль.MПечать([]byte("]"))
}

func ПечатьПроверить(аргументы_3 ...interface{}) {
	for _, param := range аргументы_3 {
		утилитаконсоль.MПечать([]byte(TypeOf(param).Name()))

	}
}
func РавныйБайт(a, b []byte) bool {
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
func БайткСтрока(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerУказателимассивfromУказатели(ссылка_на_адрес_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ссылка_на_адрес_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32массивfromУказатели(ссылка_на_адрес_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ссылка_на_адрес_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetБайтfromУказатели(ссылка_на_адрес_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ссылка_на_адрес_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncУказателиfromУказатели(ссылка_на_адрес_2 uintptr) func() {
	code1Указатели_2 := uintptr(Pointer(&ссылка_на_адрес_2))
	return *(*func())(Pointer(&code1Указатели_2))
}
