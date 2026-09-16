/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstmodewriter struct {
}

func (e tekstmodewriter) Bind_2(p []byte) (int, error) {
	tekstmodeprintbytes(p)
	return len(p), nil
}

type tekstmodeerrorwriter struct {
}

func (e tekstmodeerrorwriter) Bind_2(p []byte) (int, error) {
	tekstmodeprinterrorbytes(p)
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

func tekstmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbheight,
		Cap:	fbwidth * fbheight,
		Data:	fbphysaddress,
	}))

}

func tekstmodeenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorstart)
}

func tekstmodedisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstmodeupdatecursor(x int, y int) {
	position := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func tekstmodeflushEkraŋ() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstmodecheckfbmove() {
	for fbcurrentline >= fbheight {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbheight-1)*fbwidth+i] = 0xf00
		}
		fbcurrentline--
	}
}

func tekstmodeprintcol(s string, attribute uint8) {
	for _, b := range s {
		tekstmodeprintcharcol(uint8(b), attribute)
	}
}

func tekstmodeprintlncol(s string, attribute uint8) {
	for _, b := range s {
		tekstmodeprintcharcol(uint8(b), attribute)
	}
	tekstmodeprintchar(0xa)
}

func tekstmodeprint(s string) {
	for _, b := range s {
		tekstmodeprintchar(uint8(b))
	}
}

func tekstmodeprintbytes(a []byte) {
	for _, b := range a {
		tekstmodeprintchar(uint8(b))
	}
}

func tekstmodeprinterrorbytes(a []byte) {
	for _, b := range a {
		tekstmodeprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodeprintln(s string) {
	for _, b := range s {
		tekstmodeprintchar(uint8(b))
	}
	tekstmodeprintchar(0xa)
}

func tekstmodeprinterror(s string) {
	for _, b := range s {
		tekstmodeprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodeprinterrorln(s string) {
	tekstmodeprinterror(s)
	tekstmodeprintchar(0xa)
}

func tekstmodeprintchar(char uint8) {
	tekstmodeprintcharcol(char, 0<<4|0xf)
}

func tekstmodeprintcharcol(char uint8, attribute uint8) {
	tekstmodecheckfbmove()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		tekstmodecheckfbmove()
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

func tekstmodeprinthex64(number uint64) {
	tekstmodeprinthex32(uint32(number >> 32))
	tekstmodeprinthex32(uint32(number))
}

func tekstmodeprinthex32(number uint32) {
	tekstmodeprinthex16(uint16(number >> 16))
	tekstmodeprinthex16(uint16(number))
}

func tekstmodeprinthex16(number uint16) {
	tekstmodeprinthex(uint8(number >> 8))
	tekstmodeprinthex(uint8(number))
}

func tekstmodeprinthex(number uint8) {
	tekstmodeprinthexchar(number >> 4)
	tekstmodeprinthexchar(number)
}

func tekstmodeprinthexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstmodeprintchar(0x30 + n)
	} else {
		tekstmodeprintchar(0x41 + n - 10)
	}
}
