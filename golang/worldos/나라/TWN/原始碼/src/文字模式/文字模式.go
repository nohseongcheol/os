/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type 文字模式writer struct {
}

func (e 文字模式writer) W寫入(p []byte) (int, error) {
	文字模式列印位元組(p)
	return len(p), nil
}

type 文字模式錯誤writer struct {
}

func (e 文字模式錯誤writer) W寫入(p []byte) (int, error) {
	文字模式列印錯誤位元組(p)
	return len(p), nil
}

const (
	fb寬度			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	游標height		= 1
	游標啟動			= 11
)

var (
	fb目前行	= 0
	fb目前col	= 0
)

var fb []uint16

func 文字模式init() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fb寬度 * fbheight,
		Cap:	fb寬度 * fbheight,
		Data:	fbphysaddress,
	}))

}

func 文字模式啟用游標() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|游標啟動)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|游標height+游標啟動)
}

func 文字模式停用游標() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func 文字模式更新游標(x int, y int) {
	位置 := y*fb寬度 + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(位置&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((位置>>8)&0xFF))
}

func 文字模式flush螢幕() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func 文字模式checkfb移動() {
	for fb目前行 >= fbheight {
		copy(fb[:len(fb)-fb寬度], fb[fb寬度:])

		for i := 0; i < fb寬度; i++ {
			fb[(fbheight-1)*fb寬度+i] = 0xf00
		}
		fb目前行--
	}
}

func 文字模式列印col(s string, 屬性 uint8) {
	for _, b := range s {
		文字模式列印charcol(uint8(b), 屬性)
	}
}

func 文字模式printlncol(s string, 屬性 uint8) {
	for _, b := range s {
		文字模式列印charcol(uint8(b), 屬性)
	}
	文字模式列印char(0xa)
}

func 文字模式列印(s string) {
	for _, b := range s {
		文字模式列印char(uint8(b))
	}
}

func 文字模式列印位元組(a []byte) {
	for _, b := range a {
		文字模式列印char(uint8(b))
	}
}

func 文字模式列印錯誤位元組(a []byte) {
	for _, b := range a {
		文字模式列印charcol(uint8(b), 4<<4|0xf)
	}
}

func 文字模式println(s string) {
	for _, b := range s {
		文字模式列印char(uint8(b))
	}
	文字模式列印char(0xa)
}

func 文字模式列印錯誤(s string) {
	for _, b := range s {
		文字模式列印charcol(uint8(b), 4<<4|0xf)
	}
}

func 文字模式列印errorln(s string) {
	文字模式列印錯誤(s)
	文字模式列印char(0xa)
}

func 文字模式列印char(char uint8) {
	文字模式列印charcol(char, 0<<4|0xf)
}

func 文字模式列印charcol(char uint8, 屬性 uint8) {
	文字模式checkfb移動()
	if char == '\n' {
		fb目前行++
		fb目前col = 0
		文字模式checkfb移動()
	} else if char == '\b' {
		fb[fb目前col+fb目前行*fb寬度] = 0xf00
		fb目前col = fb目前col - 1
		if fb目前col < 0 {
			fb目前col = 0
		}
	} else if char == '\r' {
		fb目前col = 0
	} else {
		if fb目前col >= fb寬度 {
			return
		}
		fb[fb目前col+fb目前行*fb寬度] = uint16(屬性)<<8 | uint16(char)
		fb目前col++
	}

}

func 文字模式列印十六進位64(數字 uint64) {
	文字模式列印十六進位32(uint32(數字 >> 32))
	文字模式列印十六進位32(uint32(數字))
}

func 文字模式列印十六進位32(數字 uint32) {
	文字模式列印十六進位16(uint16(數字 >> 16))
	文字模式列印十六進位16(uint16(數字))
}

func 文字模式列印十六進位16(數字 uint16) {
	文字模式列印十六進位(uint8(數字 >> 8))
	文字模式列印十六進位(uint8(數字))
}

func 文字模式列印十六進位(數字 uint8) {
	文字模式列印十六進位char(數字 >> 4)
	文字模式列印十六進位char(數字)
}

func 文字模式列印十六進位char(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		文字模式列印char(0x30 + n)
	} else {
		文字模式列印char(0x41 + n - 10)
	}
}
