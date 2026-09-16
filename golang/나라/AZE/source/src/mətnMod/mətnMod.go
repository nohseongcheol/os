/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type mətnModwriter struct {
}

func (e mətnModwriter) Yazma(p []byte) (int, error) {
	mətnModÇapEtBayt(p)
	return len(p), nil
}

type mətnModXətawriter struct {
}

func (e mətnModXətawriter) Yazma(p []byte) (int, error) {
	mətnModÇapEtXətaBayt(p)
	return len(p), nil
}

const (
	fbEn			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorheight		= 1
	cursorstart		= 11
)

var (
	fbcurrentGiriş	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func mətnModinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbEn * fbheight,
		Cap:	fbEn * fbheight,
		Data:	fbphysaddress,
	}))

}

func mətnModFəallaşdırcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorstart)
}

func mətnModdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func mətnModYeniləcursor(x int, y int) {
	position := y*fbEn + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func mətnModflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func mətnModcheckfbDaşı() {
	for fbcurrentGiriş >= fbheight {
		copy(fb[:len(fb)-fbEn], fb[fbEn:])

		for i := 0; i < fbEn; i++ {
			fb[(fbheight-1)*fbEn+i] = 0xf00
		}
		fbcurrentGiriş--
	}
}

func mətnModÇapEtcol(s string, attribute uint8) {
	for _, b := range s {
		mətnModÇapEtcharcol(uint8(b), attribute)
	}
}

func mətnModprintlncol(s string, attribute uint8) {
	for _, b := range s {
		mətnModÇapEtcharcol(uint8(b), attribute)
	}
	mətnModÇapEtchar(0xa)
}

func mətnModÇapEt(s string) {
	for _, b := range s {
		mətnModÇapEtchar(uint8(b))
	}
}

func mətnModÇapEtBayt(a []byte) {
	for _, b := range a {
		mətnModÇapEtchar(uint8(b))
	}
}

func mətnModÇapEtXətaBayt(a []byte) {
	for _, b := range a {
		mətnModÇapEtcharcol(uint8(b), 4<<4|0xf)
	}
}

func mətnModprintln(s string) {
	for _, b := range s {
		mətnModÇapEtchar(uint8(b))
	}
	mətnModÇapEtchar(0xa)
}

func mətnModÇapEtXəta(s string) {
	for _, b := range s {
		mətnModÇapEtcharcol(uint8(b), 4<<4|0xf)
	}
}

func mətnModÇapEterrorln(s string) {
	mətnModÇapEtXəta(s)
	mətnModÇapEtchar(0xa)
}

func mətnModÇapEtchar(char uint8) {
	mətnModÇapEtcharcol(char, 0<<4|0xf)
}

func mətnModÇapEtcharcol(char uint8, attribute uint8) {
	mətnModcheckfbDaşı()
	if char == '\n' {
		fbcurrentGiriş++
		fbcurrentcol = 0
		mətnModcheckfbDaşı()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentGiriş*fbEn] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbEn {
			return
		}
		fb[fbcurrentcol+fbcurrentGiriş*fbEn] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func mətnModÇapEtOnaltılıq64(number uint64) {
	mətnModÇapEtOnaltılıq32(uint32(number >> 32))
	mətnModÇapEtOnaltılıq32(uint32(number))
}

func mətnModÇapEtOnaltılıq32(number uint32) {
	mətnModÇapEtOnaltılıq16(uint16(number >> 16))
	mətnModÇapEtOnaltılıq16(uint16(number))
}

func mətnModÇapEtOnaltılıq16(number uint16) {
	mətnModÇapEtOnaltılıq(uint8(number >> 8))
	mətnModÇapEtOnaltılıq(uint8(number))
}

func mətnModÇapEtOnaltılıq(number uint8) {
	mətnModÇapEtOnaltılıqchar(number >> 4)
	mətnModÇapEtOnaltılıqchar(number)
}

func mətnModÇapEtOnaltılıqchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		mətnModÇapEtchar(0x30 + n)
	} else {
		mətnModÇapEtchar(0x41 + n - 10)
	}
}
