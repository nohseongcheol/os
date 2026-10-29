/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type matnRejimwriter struct {
}

func (e matnRejimwriter) Yozish(p []byte) (int, error) {
	matnRejimChopetishBaytlar(p)
	return len(p), nil
}

type matnRejimXatowriter struct {
}

func (e matnRejimXatowriter) Yozish(p []byte) (int, error) {
	matnRejimChopetishXatoBaytlar(p)
	return len(p), nil
}

const (
	fbwidth			= 80
	fbBoyi			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorBoyi		= 1
	cursorBoshlash		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func matnRejiminit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbBoyi,
		Cap:	fbwidth * fbBoyi,
		Data:	fbphysaddress,
	}))

}

func matnRejimenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorBoshlash)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorBoyi+cursorBoshlash)
}

func matnRejimdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func matnRejimYangilashcursor(x int, y int) {
	holati := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(holati&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((holati>>8)&0xFF))
}

func matnRejimflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func matnRejimcheckfbKoʻchirish() {
	for fbcurrentline >= fbBoyi {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbBoyi-1)*fbwidth+i] = 0xf00
		}
		fbcurrentline--
	}
}

func matnRejimChopetishcol(s string, attribute uint8) {
	for _, b := range s {
		matnRejimChopetishcharcol(uint8(b), attribute)
	}
}

func matnRejimprintlncol(s string, attribute uint8) {
	for _, b := range s {
		matnRejimChopetishcharcol(uint8(b), attribute)
	}
	matnRejimChopetishchar(0xa)
}

func matnRejimChopetish(s string) {
	for _, b := range s {
		matnRejimChopetishchar(uint8(b))
	}
}

func matnRejimChopetishBaytlar(a []byte) {
	for _, b := range a {
		matnRejimChopetishchar(uint8(b))
	}
}

func matnRejimChopetishXatoBaytlar(a []byte) {
	for _, b := range a {
		matnRejimChopetishcharcol(uint8(b), 4<<4|0xf)
	}
}

func matnRejimprintln(s string) {
	for _, b := range s {
		matnRejimChopetishchar(uint8(b))
	}
	matnRejimChopetishchar(0xa)
}

func matnRejimChopetishXato(s string) {
	for _, b := range s {
		matnRejimChopetishcharcol(uint8(b), 4<<4|0xf)
	}
}

func matnRejimChopetisherrorln(s string) {
	matnRejimChopetishXato(s)
	matnRejimChopetishchar(0xa)
}

func matnRejimChopetishchar(char uint8) {
	matnRejimChopetishcharcol(char, 0<<4|0xf)
}

func matnRejimChopetishcharcol(char uint8, attribute uint8) {
	matnRejimcheckfbKoʻchirish()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		matnRejimcheckfbKoʻchirish()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbwidth] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbwidth {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbwidth] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func matnRejimChopetishhex64(rAQAM uint64) {
	matnRejimChopetishhex32(uint32(rAQAM >> 32))
	matnRejimChopetishhex32(uint32(rAQAM))
}

func matnRejimChopetishhex32(rAQAM uint32) {
	matnRejimChopetishhex16(uint16(rAQAM >> 16))
	matnRejimChopetishhex16(uint16(rAQAM))
}

func matnRejimChopetishhex16(rAQAM uint16) {
	matnRejimChopetishhex(uint8(rAQAM >> 8))
	matnRejimChopetishhex(uint8(rAQAM))
}

func matnRejimChopetishhex(rAQAM uint8) {
	matnRejimChopetishhexchar(rAQAM >> 4)
	matnRejimChopetishhexchar(rAQAM)
}

func matnRejimChopetishhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		matnRejimChopetishchar(0x30 + n)
	} else {
		matnRejimChopetishchar(0x41 + n - 10)
	}
}
