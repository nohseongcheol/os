package main

import (
	"reflect"
	"unsafe"
)

type textmodewriter struct {
}

func (e textmodewriter) Livima(p []byte) (int, error) {
	textmodeprintbytes(p)
	return len(p), nil
}

type textmodeerrorwriter struct {
}

func (e textmodeerrorwriter) Livima(p []byte) (int, error) {
	textmodeprinterrorbytes(p)
	return len(p), nil
}

const (
	fbපළල			= 80
	fbඋස			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorඋස		= 1
	cursorstart		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func textmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbපළල * fbඋස,
		Cap:	fbපළල * fbඋස,
		Data:	fbphysaddress,
	}))

}

func textmodeenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorඋස+cursorstart)
}

func textmodedisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textmodeupdatecursor(x int, y int) {
	position := y*fbපළල + x
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

func textmodecheckfbmove() {
	for fbcurrentline >= fbඋස {
		copy(fb[:len(fb)-fbපළල], fb[fbපළල:])

		for i := 0; i < fbපළල; i++ {
			fb[(fbඋස-1)*fbපළල+i] = 0xf00
		}
		fbcurrentline--
	}
}

func textmodeprintcol(s string, attribute uint8) {
	for _, b := range s {
		textmodeprintcharcol(uint8(b), attribute)
	}
}

func textmodeprintlncol(s string, attribute uint8) {
	for _, b := range s {
		textmodeprintcharcol(uint8(b), attribute)
	}
	textmodeprintchar(0xa)
}

func textmodeprint(s string) {
	for _, b := range s {
		textmodeprintchar(uint8(b))
	}
}

func textmodeprintbytes(a []byte) {
	for _, b := range a {
		textmodeprintchar(uint8(b))
	}
}

func textmodeprinterrorbytes(a []byte) {
	for _, b := range a {
		textmodeprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeprintln(s string) {
	for _, b := range s {
		textmodeprintchar(uint8(b))
	}
	textmodeprintchar(0xa)
}

func textmodeprinterror(s string) {
	for _, b := range s {
		textmodeprintcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeprinterrorln(s string) {
	textmodeprinterror(s)
	textmodeprintchar(0xa)
}

func textmodeprintchar(char uint8) {
	textmodeprintcharcol(char, 0<<4|0xf)
}

func textmodeprintcharcol(char uint8, attribute uint8) {
	textmodecheckfbmove()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		textmodecheckfbmove()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbපළල] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbපළල {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbපළල] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func textmodeprinthex64(number uint64) {
	textmodeprinthex32(uint32(number >> 32))
	textmodeprinthex32(uint32(number))
}

func textmodeprinthex32(number uint32) {
	textmodeprinthex16(uint16(number >> 16))
	textmodeprinthex16(uint16(number))
}

func textmodeprinthex16(number uint16) {
	textmodeprinthex(uint8(number >> 8))
	textmodeprinthex(uint8(number))
}

func textmodeprinthex(number uint8) {
	textmodeprinthexchar(number >> 4)
	textmodeprinthexchar(number)
}

func textmodeprinthexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textmodeprintchar(0x30 + n)
	} else {
		textmodeprintchar(0x41 + n - 10)
	}
}
