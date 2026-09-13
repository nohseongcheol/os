package main

import (
	"reflect"
	"unsafe"
)

type 문자화면출력기 struct {
}

func (e 문자화면출력기) M쓰기(p []byte) (int, error) {
	문자화면출력바이트(p)
	return len(p), nil
}

type 문자화면오류출력기 struct {
}

func (e 문자화면오류출력기) M쓰기(p []byte) (int, error) {
	문자화면출력오류바이트(p)
	return len(p), nil
}

const (
	화면너비			= 80
	화면높이			= 25
	화면물리주소	uintptr	= 0xb8000
	입력표시높이			= 1
	입력표시시작			= 11
)

var (
	화면현재줄	= 0
	화면현재열	= 0
)

var 화면기억공간 []uint16

func 문자화면초기화() {
	화면기억공간 = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	화면너비 * 화면높이,
		Cap:	화면너비 * 화면높이,
		Data:	화면물리주소,
	}))

}

func 문자화면입력표시활성화() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|입력표시시작)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|입력표시높이+입력표시시작)
}

func 문자화면입력표시비활성화() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func 문자화면입력위치갱신(x int, y int) {
	위치 := y*화면너비 + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(위치&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((위치>>8)&0xFF))
}

func 문자화면지우기() {
	for i := range 화면기억공간 {
		화면기억공간[i] = 0xf00
	}
}

func 문자화면넘침처리() {
	for 화면현재줄 >= 화면높이 {
		copy(화면기억공간[:len(화면기억공간)-화면너비], 화면기억공간[화면너비:])

		for i := 0; i < 화면너비; i++ {
			화면기억공간[(화면높이-1)*화면너비+i] = 0xf00
		}
		화면현재줄--
	}
}

func 문자화면색상지정출력(s string, 속성 uint8) {
	for _, b := range s {
		문자화면색상지정문자출력(uint8(b), 속성)
	}
}

func 문자화면색상지정줄출력(s string, 속성 uint8) {
	for _, b := range s {
		문자화면색상지정문자출력(uint8(b), 속성)
	}
	문자화면출력문자(0xa)
}

func 문자화면출력(s string) {
	for _, b := range s {
		문자화면출력문자(uint8(b))
	}
}

func 문자화면출력바이트(a []byte) {
	for _, b := range a {
		문자화면출력문자(uint8(b))
	}
}

func 문자화면출력오류바이트(a []byte) {
	for _, b := range a {
		문자화면색상지정문자출력(uint8(b), 4<<4|0xf)
	}
}

func 문자화면줄출력(s string) {
	for _, b := range s {
		문자화면출력문자(uint8(b))
	}
	문자화면출력문자(0xa)
}

func 문자화면출력오류(s string) {
	for _, b := range s {
		문자화면색상지정문자출력(uint8(b), 4<<4|0xf)
	}
}

func 문자화면오류줄출력(s string) {
	문자화면출력오류(s)
	문자화면출력문자(0xa)
}

func 문자화면출력문자(문자 uint8) {
	문자화면색상지정문자출력(문자, 0<<4|0xf)
}

func 문자화면색상지정문자출력(문자 uint8, 속성 uint8) {
	문자화면넘침처리()
	if 문자 == '\n' {
		화면현재줄++
		화면현재열 = 0
		문자화면넘침처리()
	} else if 문자 == '\b' {
		화면기억공간[화면현재열+화면현재줄*화면너비] = 0xf00
		화면현재열 = 화면현재열 - 1
		if 화면현재열 < 0 {
			화면현재열 = 0
		}
	} else if 문자 == '\r' {
		화면현재열 = 0
	} else {
		if 화면현재열 >= 화면너비 {
			return
		}
		화면기억공간[화면현재열+화면현재줄*화면너비] = uint16(속성)<<8 | uint16(문자)
		화면현재열++
	}

}

func 문자화면출력16진수64(번호 uint64) {
	문자화면출력16진수32(uint32(번호 >> 32))
	문자화면출력16진수32(uint32(번호))
}

func 문자화면출력16진수32(번호 uint32) {
	문자화면출력16진수16(uint16(번호 >> 16))
	문자화면출력16진수16(uint16(번호))
}

func 문자화면출력16진수16(번호 uint16) {
	문자화면출력16진수(uint8(번호 >> 8))
	문자화면출력16진수(uint8(번호))
}

func 문자화면출력16진수(번호 uint8) {
	문자화면출력16진수문자(번호 >> 4)
	문자화면출력16진수문자(번호)
}

func 문자화면출력16진수문자(반바이트 uint8) {
	n := 반바이트 & 0xf
	if n < 10 {
		문자화면출력문자(0x30 + n)
	} else {
		문자화면출력문자(0x41 + n - 10)
	}
}
