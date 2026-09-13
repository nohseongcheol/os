package main

import (
	"reflect"
	"unsafe"
)

type textmodewriter struct {
}

func (e textmodewriter) Навиштан(p []byte) (int, error) {
	textmodeЧопкарданbytes(p)
	return len(p), nil
}

type textmodeХатоwriter struct {
}

func (e textmodeХатоwriter) Навиштан(p []byte) (int, error) {
	textmodeЧопкарданХатоbytes(p)
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

func textmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbheight,
		Cap:	fbwidth * fbheight,
		Data:	fbphysaddress,
	}))

}

func textmodeenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorheight+cursorstart)
}

func textmodedisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textmodeНавсозӣcursor(x int, y int) {
	position := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func textmodeflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textmodecheckfbТаҳвил() {
	for fbcurrentline >= fbheight {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbheight-1)*fbwidth+i] = 0xf00
		}
		fbcurrentline--
	}
}

func textmodeЧопкарданcol(s string, attribute uint8) {
	for _, b := range s {
		textmodeЧопкарданcharcol(uint8(b), attribute)
	}
}

func textmodeprintlncol(s string, attribute uint8) {
	for _, b := range s {
		textmodeЧопкарданcharcol(uint8(b), attribute)
	}
	textmodeЧопкарданchar(0xa)
}

func textmodeЧопкардан(s string) {
	for _, b := range s {
		textmodeЧопкарданchar(uint8(b))
	}
}

func textmodeЧопкарданbytes(a []byte) {
	for _, b := range a {
		textmodeЧопкарданchar(uint8(b))
	}
}

func textmodeЧопкарданХатоbytes(a []byte) {
	for _, b := range a {
		textmodeЧопкарданcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeprintln(s string) {
	for _, b := range s {
		textmodeЧопкарданchar(uint8(b))
	}
	textmodeЧопкарданchar(0xa)
}

func textmodeЧопкарданХато(s string) {
	for _, b := range s {
		textmodeЧопкарданcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeЧопкарданerrorln(s string) {
	textmodeЧопкарданХато(s)
	textmodeЧопкарданchar(0xa)
}

func textmodeЧопкарданchar(char uint8) {
	textmodeЧопкарданcharcol(char, 0<<4|0xf)
}

func textmodeЧопкарданcharcol(char uint8, attribute uint8) {
	textmodecheckfbТаҳвил()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		textmodecheckfbТаҳвил()
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

func textmodeЧопкарданhex64(number uint64) {
	textmodeЧопкарданhex32(uint32(number >> 32))
	textmodeЧопкарданhex32(uint32(number))
}

func textmodeЧопкарданhex32(number uint32) {
	textmodeЧопкарданhex16(uint16(number >> 16))
	textmodeЧопкарданhex16(uint16(number))
}

func textmodeЧопкарданhex16(number uint16) {
	textmodeЧопкарданhex(uint8(number >> 8))
	textmodeЧопкарданhex(uint8(number))
}

func textmodeЧопкарданhex(number uint8) {
	textmodeЧопкарданhexchar(number >> 4)
	textmodeЧопкарданhexchar(number)
}

func textmodeЧопкарданhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textmodeЧопкарданchar(0x30 + n)
	} else {
		textmodeЧопкарданchar(0x41 + n - 10)
	}
}
