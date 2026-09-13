package main

import (
	"reflect"
	"unsafe"
)

type текстГоримwriter struct {
}

func (e текстГоримwriter) Бичих(p []byte) (int, error) {
	текстГоримХэвлэхБайт(p)
	return len(p), nil
}

type текстГоримАлдааwriter struct {
}

func (e текстГоримАлдааwriter) Бичих(p []byte) (int, error) {
	текстГоримХэвлэхАлдааБайт(p)
	return len(p), nil
}

const (
	fbӨргөн			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorheight		= 1
	cursorЭхлэл		= 11
)

var (
	fbcurrentШугам	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func текстГоримinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbӨргөн * fbheight,
		Cap:	fbӨргөн * fbheight,
		Data:	fbphysaddress,
	}))

}

func текстГоримenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorЭхлэл)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorЭхлэл)
}

func текстГоримdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстГоримШинэчлэхcursor(x int, y int) {
	position := y*fbӨргөн + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func текстГоримflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстГоримcheckfbЗөөх() {
	for fbcurrentШугам >= fbheight {
		copy(fb[:len(fb)-fbӨргөн], fb[fbӨргөн:])

		for i := 0; i < fbӨргөн; i++ {
			fb[(fbheight-1)*fbӨргөн+i] = 0xf00
		}
		fbcurrentШугам--
	}
}

func текстГоримХэвлэхcol(s string, attribute uint8) {
	for _, b := range s {
		текстГоримХэвлэхcharcol(uint8(b), attribute)
	}
}

func текстГоримprintlncol(s string, attribute uint8) {
	for _, b := range s {
		текстГоримХэвлэхcharcol(uint8(b), attribute)
	}
	текстГоримХэвлэхchar(0xa)
}

func текстГоримХэвлэх(s string) {
	for _, b := range s {
		текстГоримХэвлэхchar(uint8(b))
	}
}

func текстГоримХэвлэхБайт(a []byte) {
	for _, b := range a {
		текстГоримХэвлэхchar(uint8(b))
	}
}

func текстГоримХэвлэхАлдааБайт(a []byte) {
	for _, b := range a {
		текстГоримХэвлэхcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстГоримprintln(s string) {
	for _, b := range s {
		текстГоримХэвлэхchar(uint8(b))
	}
	текстГоримХэвлэхchar(0xa)
}

func текстГоримХэвлэхАлдаа(s string) {
	for _, b := range s {
		текстГоримХэвлэхcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстГоримХэвлэхerrorln(s string) {
	текстГоримХэвлэхАлдаа(s)
	текстГоримХэвлэхchar(0xa)
}

func текстГоримХэвлэхchar(char uint8) {
	текстГоримХэвлэхcharcol(char, 0<<4|0xf)
}

func текстГоримХэвлэхcharcol(char uint8, attribute uint8) {
	текстГоримcheckfbЗөөх()
	if char == '\n' {
		fbcurrentШугам++
		fbcurrentcol = 0
		текстГоримcheckfbЗөөх()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentШугам*fbӨргөн] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbӨргөн {
			return
		}
		fb[fbcurrentcol+fbcurrentШугам*fbӨргөн] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func текстГоримХэвлэхhex64(number uint64) {
	текстГоримХэвлэхhex32(uint32(number >> 32))
	текстГоримХэвлэхhex32(uint32(number))
}

func текстГоримХэвлэхhex32(number uint32) {
	текстГоримХэвлэхhex16(uint16(number >> 16))
	текстГоримХэвлэхhex16(uint16(number))
}

func текстГоримХэвлэхhex16(number uint16) {
	текстГоримХэвлэхhex(uint8(number >> 8))
	текстГоримХэвлэхhex(uint8(number))
}

func текстГоримХэвлэхhex(number uint8) {
	текстГоримХэвлэхhexchar(number >> 4)
	текстГоримХэвлэхhexchar(number)
}

func текстГоримХэвлэхhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстГоримХэвлэхchar(0x30 + n)
	} else {
		текстГоримХэвлэхchar(0x41 + n - 10)
	}
}
