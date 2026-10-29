/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package util

import . "console"
import . "unsafe"
import . "reflect"

var utilconsole TConsole = TConsole{}

func Unsignedinteger16toԶանգված(հԱՄԱՐ uint16) [2]byte {
	var զանգված [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		զանգված[i] = byte(հԱՄԱՐ >> (8 * i) & 0x00FF)
	}
	return զանգված
}
func Unsignedinteger16toԶանգվածbe(հԱՄԱՐ uint16) [2]byte {
	var զանգված [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		զանգված[2-i] = byte(հԱՄԱՐ >> (8 * i) & 0x00FF)
	}
	return զանգված
}

func Unsignedinteger32toԶանգված(հԱՄԱՐ uint32) [4]byte {
	var զանգված [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		զանգված[i] = byte(հԱՄԱՐ >> (8 * i) & 0x000000FF)
	}
	return զանգված
}
func Unsignedinteger48toԶանգված(հԱՄԱՐ uint64) [6]byte {
	var զանգված [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		զանգված[i] = byte(հԱՄԱՐ >> (8 * i) & 0x00000000FF)
	}
	return զանգված
}
func Unsignedinteger48toԶանգվածbe(հԱՄԱՐ uint64) [6]byte {
	var զանգված [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		զանգված[5-i] = byte(հԱՄԱՐ >> (8 * i) & 0x00000000FF)
	}
	return զանգված
}
func Unsignedinteger64toԶանգված(հԱՄԱՐ uint64) [8]byte {
	var զանգված [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		զանգված[1-i] = byte(հԱՄԱՐ >> (8 * i) & 0x00000000000000FF)
	}
	return զանգված
}
func Զանգվածtounsignedinteger16(զանգված [2]byte) uint16 {
	var հԱՄԱՐ uint16
	var i uint
	for i = 0; i < 2; i++ {
		հԱՄԱՐ = հԱՄԱՐ | (uint16(զանգված[1-i]) << (8 * i))
	}
	return հԱՄԱՐ
}
func Զանգվածtounsignedinteger32(զանգված [4]byte) uint32 {
	var հԱՄԱՐ uint32
	var i uint
	for i = 0; i < 4; i++ {
		հԱՄԱՐ = հԱՄԱՐ | (uint32(զանգված[3-i]) << (8 * i))
	}
	return հԱՄԱՐ
}
func Զանգվածtounsignedinteger48(զանգված [6]byte) uint64 {
	var հԱՄԱՐ uint64
	var i uint
	for i = 0; i < 6; i++ {
		հԱՄԱՐ = հԱՄԱՐ | (uint64(զանգված[5-i]) << (8 * i))
	}
	return հԱՄԱՐ

}
func Զանգվածtounsignedinteger48be(զանգված [6]byte) uint64 {
	var հԱՄԱՐ uint64
	var i uint
	for i = 0; i < 6; i++ {
		հԱՄԱՐ = հԱՄԱՐ | (uint64(զանգված[i]) << (8 * i))
	}
	return հԱՄԱՐ
}
func Զանգվածtounsignedinteger64(զանգված [8]byte) uint64 {
	var հԱՄԱՐ uint64
	var i uint
	for i = 0; i < 8; i++ {
		հԱՄԱՐ = հԱՄԱՐ | (uint64(զանգված[7-i]) << (8 * i))
	}
	return հԱՄԱՐ
}
func Unsignedinteger64r(հԱՄԱՐ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(հԱՄԱՐ>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(հԱՄԱՐ uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(հԱՄԱՐ>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(հԱՄԱՐ uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(հԱՄԱՐ>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(հԱՄԱՐ uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(հԱՄԱՐ>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ՏպելԲայթեր(dataՑուցիչ uintptr, չափս int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(dataՑուցիչ))
	var i int
	utilconsole.MՏպել([]byte("util["))
	for i = 0; i < չափս; i++ {
		utilconsole.MHexadecimalՏպել(buffer_2[i])
	}
	utilconsole.MՏպել([]byte("]"))
}

func ՏպելԹեստ(params ...interface{}) {
	for _, param := range params {
		utilconsole.MՏպել([]byte(TypeOf(param).Name()))

	}
}
func EqualԲայթեր(a, b []byte) bool {
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
func ԲայթերtoՏՈՂ(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerՑուցիչԶանգվածիցՑուցիչ(ցուցիչ_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ցուցիչ_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32ԶանգվածիցՑուցիչ(ցուցիչ_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ցուցիչ_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetԲայթերիցՑուցիչ(ցուցիչ_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{ցուցիչ_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncՑուցիչիցՑուցիչ(ցուցիչ_2 uintptr) func() {
	code1Ցուցիչ_2 := uintptr(Pointer(&ցուցիչ_2))
	return *(*func())(Pointer(&code1Ցուցիչ_2))
}
