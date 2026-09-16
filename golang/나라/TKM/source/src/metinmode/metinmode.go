/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type metinmodewriter struct {
}

func (e metinmodewriter) Ýaz(p []byte) (int, error) {
	metinmodeÇapBaýtlar(p)
	return len(p), nil
}

type metinmodeHatawriter struct {
}

func (e metinmodeHatawriter) Ýaz(p []byte) (int, error) {
	metinmodeÇapHataBaýtlar(p)
	return len(p), nil
}

const (
	fbwidth			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorheight		= 1
	cursorstart		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func metinmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbheight,
		Cap:	fbwidth * fbheight,
		Data:	fbphysaddress,
	}))

}

func metinmodeenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorstart)
}

func metinmodedisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func metinmodeTäzelecursor(x int, y int) {
	position := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func metinmodeflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func metinmodecheckfbGöçir() {
	for fbcurrentline >= fbheight {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbheight-1)*fbwidth+i] = 0xf00
		}
		fbcurrentline--
	}
}

func metinmodeÇapcol(s string, attribute uint8) {
	for _, b := range s {
		metinmodeÇapcharcol(uint8(b), attribute)
	}
}

func metinmodeprintlncol(s string, attribute uint8) {
	for _, b := range s {
		metinmodeÇapcharcol(uint8(b), attribute)
	}
	metinmodeÇapchar(0xa)
}

func metinmodeÇap(s string) {
	for _, b := range s {
		metinmodeÇapchar(uint8(b))
	}
}

func metinmodeÇapBaýtlar(a []byte) {
	for _, b := range a {
		metinmodeÇapchar(uint8(b))
	}
}

func metinmodeÇapHataBaýtlar(a []byte) {
	for _, b := range a {
		metinmodeÇapcharcol(uint8(b), 4<<4|0xf)
	}
}

func metinmodeprintln(s string) {
	for _, b := range s {
		metinmodeÇapchar(uint8(b))
	}
	metinmodeÇapchar(0xa)
}

func metinmodeÇapHata(s string) {
	for _, b := range s {
		metinmodeÇapcharcol(uint8(b), 4<<4|0xf)
	}
}

func metinmodeÇaperrorln(s string) {
	metinmodeÇapHata(s)
	metinmodeÇapchar(0xa)
}

func metinmodeÇapchar(char uint8) {
	metinmodeÇapcharcol(char, 0<<4|0xf)
}

func metinmodeÇapcharcol(char uint8, attribute uint8) {
	metinmodecheckfbGöçir()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		metinmodecheckfbGöçir()
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

func metinmodeÇaphex64(number uint64) {
	metinmodeÇaphex32(uint32(number >> 32))
	metinmodeÇaphex32(uint32(number))
}

func metinmodeÇaphex32(number uint32) {
	metinmodeÇaphex16(uint16(number >> 16))
	metinmodeÇaphex16(uint16(number))
}

func metinmodeÇaphex16(number uint16) {
	metinmodeÇaphex(uint8(number >> 8))
	metinmodeÇaphex(uint8(number))
}

func metinmodeÇaphex(number uint8) {
	metinmodeÇaphexchar(number >> 4)
	metinmodeÇaphexchar(number)
}

func metinmodeÇaphexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		metinmodeÇapchar(0x30 + n)
	} else {
		metinmodeÇapchar(0x41 + n - 10)
	}
}
