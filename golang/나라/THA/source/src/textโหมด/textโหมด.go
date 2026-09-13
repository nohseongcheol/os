package main

import (
	"reflect"
	"unsafe"
)

type textโหมดwriter struct {
}

func (e textโหมดwriter) Khian(p []byte) (int, error) {
	textโหมดprintbytes(p)
	return len(p), nil
}

type textโหมดerrorwriter struct {
}

func (e textโหมดerrorwriter) Khian(p []byte) (int, error) {
	textโหมดprinterrorbytes(p)
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

func textโหมดinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbheight,
		Cap:	fbwidth * fbheight,
		Data:	fbphysaddress,
	}))

}

func textโหมดenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorstart)
}

func textโหมดdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textโหมดupdatecursor(x int, y int) {
	position := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func textโหมดflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textโหมดcheckfbmove() {
	for fbcurrentline >= fbheight {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbheight-1)*fbwidth+i] = 0xf00
		}
		fbcurrentline--
	}
}

func textโหมดprintcol(s string, attribute uint8) {
	for _, b := range s {
		textโหมดprintcharcol(uint8(b), attribute)
	}
}

func textโหมดprintlncol(s string, attribute uint8) {
	for _, b := range s {
		textโหมดprintcharcol(uint8(b), attribute)
	}
	textโหมดprintchar(0xa)
}

func textโหมดprint(s string) {
	for _, b := range s {
		textโหมดprintchar(uint8(b))
	}
}

func textโหมดprintbytes(a []byte) {
	for _, b := range a {
		textโหมดprintchar(uint8(b))
	}
}

func textโหมดprinterrorbytes(a []byte) {
	for _, b := range a {
		textโหมดprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func textโหมดprintln(s string) {
	for _, b := range s {
		textโหมดprintchar(uint8(b))
	}
	textโหมดprintchar(0xa)
}

func textโหมดprinterror(s string) {
	for _, b := range s {
		textโหมดprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func textโหมดprinterrorln(s string) {
	textโหมดprinterror(s)
	textโหมดprintchar(0xa)
}

func textโหมดprintchar(char uint8) {
	textโหมดprintcharcol(char, 0<<4|0xf)
}

func textโหมดprintcharcol(char uint8, attribute uint8) {
	textโหมดcheckfbmove()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		textโหมดcheckfbmove()
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

func textโหมดprinthex64(number uint64) {
	textโหมดprinthex32(uint32(number >> 32))
	textโหมดprinthex32(uint32(number))
}

func textโหมดprinthex32(number uint32) {
	textโหมดprinthex16(uint16(number >> 16))
	textโหมดprinthex16(uint16(number))
}

func textโหมดprinthex16(number uint16) {
	textโหมดprinthex(uint8(number >> 8))
	textโหมดprinthex(uint8(number))
}

func textโหมดprinthex(number uint8) {
	textโหมดprinthexchar(number >> 4)
	textโหมดprinthexchar(number)
}

func textโหมดprinthexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textโหมดprintchar(0x30 + n)
	} else {
		textโหมดprintchar(0x41 + n - 10)
	}
}
