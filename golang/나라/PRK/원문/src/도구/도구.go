package 도구

import . "단말"
import . "unsafe"
import . "reflect"

var 도구단말 T단말 = T단말{}

func F정수16을낮은바이트우선배열로변환(번호 uint16) [2]byte {
	var 배열 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		배열[i] = byte(번호 >> (8 * i) & 0x00FF)
	}
	return 배열
}
func F정수16을높은바이트우선배열로변환(번호 uint16) [2]byte {
	var 배열 [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		배열[2-i] = byte(번호 >> (8 * i) & 0x00FF)
	}
	return 배열
}

func F정수32를낮은바이트우선배열로변환(번호 uint32) [4]byte {
	var 배열 [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		배열[i] = byte(번호 >> (8 * i) & 0x000000FF)
	}
	return 배열
}
func F정수48을낮은바이트우선배열로변환(번호 uint64) [6]byte {
	var 배열 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		배열[i] = byte(번호 >> (8 * i) & 0x00000000FF)
	}
	return 배열
}
func F정수48을높은바이트우선배열로변환(번호 uint64) [6]byte {
	var 배열 [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		배열[5-i] = byte(번호 >> (8 * i) & 0x00000000FF)
	}
	return 배열
}
func F정수64를바이트배열로변환(번호 uint64) [8]byte {
	var 배열 [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		배열[1-i] = byte(번호 >> (8 * i) & 0x00000000000000FF)
	}
	return 배열
}
func F높은바이트우선배열을정수16으로변환(배열 [2]byte) uint16 {
	var 번호 uint16
	var i uint
	for i = 0; i < 2; i++ {
		번호 = 번호 | (uint16(배열[1-i]) << (8 * i))
	}
	return 번호
}
func F높은바이트우선배열을정수32로변환(배열 [4]byte) uint32 {
	var 번호 uint32
	var i uint
	for i = 0; i < 4; i++ {
		번호 = 번호 | (uint32(배열[3-i]) << (8 * i))
	}
	return 번호
}
func F높은바이트우선배열을정수48로변환(배열 [6]byte) uint64 {
	var 번호 uint64
	var i uint
	for i = 0; i < 6; i++ {
		번호 = 번호 | (uint64(배열[5-i]) << (8 * i))
	}
	return 번호

}
func F낮은바이트우선배열을정수48로변환(배열 [6]byte) uint64 {
	var 번호 uint64
	var i uint
	for i = 0; i < 6; i++ {
		번호 = 번호 | (uint64(배열[i]) << (8 * i))
	}
	return 번호
}
func F높은바이트우선배열을정수64로변환(배열 [8]byte) uint64 {
	var 번호 uint64
	var i uint
	for i = 0; i < 8; i++ {
		번호 = 번호 | (uint64(배열[7-i]) << (8 * i))
	}
	return 번호
}
func F정수64바이트순서뒤집기(번호 uint64) uint64 {
	var 임시 uint64
	var i uint
	for i = 0; i < 8; i++ {
		임시 = 임시 | (uint64(번호>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return 임시
}
func F정수48바이트순서뒤집기(번호 uint64) uint64 {
	var 임시 uint64
	var i uint
	for i = 0; i < 6; i++ {
		임시 = 임시 | (uint64(번호>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return 임시
}
func F정수32바이트순서뒤집기(번호 uint32) uint32 {
	var 임시 uint32
	var i uint
	for i = 0; i < 4; i++ {
		임시 = 임시 | (uint32(번호>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return 임시
}
func F정수16바이트순서뒤집기(번호 uint16) uint16 {
	var 임시 uint16
	var i uint
	for i = 0; i < 2; i++ {
		임시 = 임시 | (uint16(번호>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return 임시
}
func F주소의바이트출력(자료주소참조 uintptr, 크기 int) {
	var 임시공간_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(자료주소참조))
	var i int
	도구단말.M출력([]byte("util["))
	for i = 0; i < 크기; i++ {
		도구단말.M16진수출력(임시공간_2[i])
	}
	도구단말.M출력([]byte("]"))
}

func F자료형이름출력(인자_2 ...interface{}) {
	for _, 매개값 := range 인자_2 {
		도구단말.M출력([]byte(TypeOf(매개값).Name()))

	}
}
func F바이트열같은지확인(a, b []byte) bool {
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
func F바이트열을문자열로변환(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func F주소에서주소배열참조(주소참조_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		주소	uintptr
		len	int
		cap	int
	}{주소참조_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func F주소에서정수32배열참조(주소참조_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		주소	uintptr
		len	int
		cap	int
	}{주소참조_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func F주소에서바이트열참조(주소참조_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		주소	uintptr
		len	int
		cap	int
	}{주소참조_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func F주소에서함수참조(주소참조_2 uintptr) func() {
	코드1주소참조_2 := uintptr(Pointer(&주소참조_2))
	return *(*func())(Pointer(&코드1주소참조_2))
}
