/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type 文本模式writer struct {
}

func (e 文本模式writer) W写入(p []byte) (int, error) {
	文本模式打印字节(p)
	return len(p), nil
}

type 文本模式错误writer struct {
}

func (e 文本模式错误writer) W写入(p []byte) (int, error) {
	文本模式打印错误字节(p)
	return len(p), nil
}

const (
	fb宽度			= 80
	fb高度			= 25
	fbphysaddress	uintptr	= 0xb8000
	光标高度			= 1
	光标开始			= 11
)

var (
	fb当前行	= 0
	fb当前col	= 0
)

var fb []uint16

func 文本模式init() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fb宽度 * fb高度,
		Cap:	fb宽度 * fb高度,
		Data:	fbphysaddress,
	}))

}

func 文本模式启用光标() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|光标开始)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|光标高度+光标开始)
}

func 文本模式禁用光标() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func 文本模式更新光标(x int, y int) {
	位置 := y*fb宽度 + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(位置&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((位置>>8)&0xFF))
}

func 文本模式flush屏幕() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func 文本模式checkfb移动() {
	for fb当前行 >= fb高度 {
		copy(fb[:len(fb)-fb宽度], fb[fb宽度:])

		for i := 0; i < fb宽度; i++ {
			fb[(fb高度-1)*fb宽度+i] = 0xf00
		}
		fb当前行--
	}
}

func 文本模式打印col(s string, 属性 uint8) {
	for _, b := range s {
		文本模式打印charcol(uint8(b), 属性)
	}
}

func 文本模式printlncol(s string, 属性 uint8) {
	for _, b := range s {
		文本模式打印charcol(uint8(b), 属性)
	}
	文本模式打印char(0xa)
}

func 文本模式打印(s string) {
	for _, b := range s {
		文本模式打印char(uint8(b))
	}
}

func 文本模式打印字节(a []byte) {
	for _, b := range a {
		文本模式打印char(uint8(b))
	}
}

func 文本模式打印错误字节(a []byte) {
	for _, b := range a {
		文本模式打印charcol(uint8(b), 4<<4|0xf)
	}
}

func 文本模式println(s string) {
	for _, b := range s {
		文本模式打印char(uint8(b))
	}
	文本模式打印char(0xa)
}

func 文本模式打印错误(s string) {
	for _, b := range s {
		文本模式打印charcol(uint8(b), 4<<4|0xf)
	}
}

func 文本模式打印errorln(s string) {
	文本模式打印错误(s)
	文本模式打印char(0xa)
}

func 文本模式打印char(char uint8) {
	文本模式打印charcol(char, 0<<4|0xf)
}

func 文本模式打印charcol(char uint8, 属性 uint8) {
	文本模式checkfb移动()
	if char == '\n' {
		fb当前行++
		fb当前col = 0
		文本模式checkfb移动()
	} else if char == '\b' {
		fb[fb当前col+fb当前行*fb宽度] = 0xf00
		fb当前col = fb当前col - 1
		if fb当前col < 0 {
			fb当前col = 0
		}
	} else if char == '\r' {
		fb当前col = 0
	} else {
		if fb当前col >= fb宽度 {
			return
		}
		fb[fb当前col+fb当前行*fb宽度] = uint16(属性)<<8 | uint16(char)
		fb当前col++
	}

}

func 文本模式打印十六进制64(数字 uint64) {
	文本模式打印十六进制32(uint32(数字 >> 32))
	文本模式打印十六进制32(uint32(数字))
}

func 文本模式打印十六进制32(数字 uint32) {
	文本模式打印十六进制16(uint16(数字 >> 16))
	文本模式打印十六进制16(uint16(数字))
}

func 文本模式打印十六进制16(数字 uint16) {
	文本模式打印十六进制(uint8(数字 >> 8))
	文本模式打印十六进制(uint8(数字))
}

func 文本模式打印十六进制(数字 uint8) {
	文本模式打印十六进制char(数字 >> 4)
	文本模式打印十六进制char(数字)
}

func 文本模式打印十六进制char(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		文本模式打印char(0x30 + n)
	} else {
		文本模式打印char(0x41 + n - 10)
	}
}
