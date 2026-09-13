package main

import (
	"reflect"
	"unsafe"
)

type текстРежимwriter struct {
}

func (e текстРежимwriter) Жазуу(p []byte) (int, error) {
	текстРежимБасмаБайт(p)
	return len(p), nil
}

type текстРежимКатаwriter struct {
}

func (e текстРежимКатаwriter) Жазуу(p []byte) (int, error) {
	текстРежимБасмаКатаБайт(p)
	return len(p), nil
}

const (
	fbТуурасы		= 80
	fbБийиктик		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorБийиктик		= 1
	cursorЖүргүзүү		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func текстРежимinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbТуурасы * fbБийиктик,
		Cap:	fbТуурасы * fbБийиктик,
		Data:	fbphysaddress,
	}))

}

func текстРежимenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorЖүргүзүү)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorБийиктик+cursorЖүргүзүү)
}

func текстРежимdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстРежимЖаңылооcursor(x int, y int) {
	турганжери := y*fbТуурасы + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(турганжери&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((турганжери>>8)&0xFF))
}

func текстРежимflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстРежимcheckfbТашуу() {
	for fbcurrentline >= fbБийиктик {
		copy(fb[:len(fb)-fbТуурасы], fb[fbТуурасы:])

		for i := 0; i < fbТуурасы; i++ {
			fb[(fbБийиктик-1)*fbТуурасы+i] = 0xf00
		}
		fbcurrentline--
	}
}

func текстРежимБасмаcol(s string, атрибут uint8) {
	for _, b := range s {
		текстРежимБасмаcharcol(uint8(b), атрибут)
	}
}

func текстРежимprintlncol(s string, атрибут uint8) {
	for _, b := range s {
		текстРежимБасмаcharcol(uint8(b), атрибут)
	}
	текстРежимБасмаchar(0xa)
}

func текстРежимБасма(s string) {
	for _, b := range s {
		текстРежимБасмаchar(uint8(b))
	}
}

func текстРежимБасмаБайт(a []byte) {
	for _, b := range a {
		текстРежимБасмаchar(uint8(b))
	}
}

func текстРежимБасмаКатаБайт(a []byte) {
	for _, b := range a {
		текстРежимБасмаcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРежимprintln(s string) {
	for _, b := range s {
		текстРежимБасмаchar(uint8(b))
	}
	текстРежимБасмаchar(0xa)
}

func текстРежимБасмаКата(s string) {
	for _, b := range s {
		текстРежимБасмаcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРежимБасмаerrorln(s string) {
	текстРежимБасмаКата(s)
	текстРежимБасмаchar(0xa)
}

func текстРежимБасмаchar(char uint8) {
	текстРежимБасмаcharcol(char, 0<<4|0xf)
}

func текстРежимБасмаcharcol(char uint8, атрибут uint8) {
	текстРежимcheckfbТашуу()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		текстРежимcheckfbТашуу()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbТуурасы] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbТуурасы {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbТуурасы] = uint16(атрибут)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func текстРежимБасмаhex64(нОМЕР uint64) {
	текстРежимБасмаhex32(uint32(нОМЕР >> 32))
	текстРежимБасмаhex32(uint32(нОМЕР))
}

func текстРежимБасмаhex32(нОМЕР uint32) {
	текстРежимБасмаhex16(uint16(нОМЕР >> 16))
	текстРежимБасмаhex16(uint16(нОМЕР))
}

func текстРежимБасмаhex16(нОМЕР uint16) {
	текстРежимБасмаhex(uint8(нОМЕР >> 8))
	текстРежимБасмаhex(uint8(нОМЕР))
}

func текстРежимБасмаhex(нОМЕР uint8) {
	текстРежимБасмаhexchar(нОМЕР >> 4)
	текстРежимБасмаhexchar(нОМЕР)
}

func текстРежимБасмаhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстРежимБасмаchar(0x30 + n)
	} else {
		текстРежимБасмаchar(0x41 + n - 10)
	}
}
