package main

import (
	"reflect"
	"unsafe"
)

type текстРежимwriter struct {
}

func (e текстРежимwriter) Запиши(p []byte) (int, error) {
	текстРежимПечатибајти(p)
	return len(p), nil
}

type текстРежимГрешкаwriter struct {
}

func (e текстРежимГрешкаwriter) Запиши(p []byte) (int, error) {
	текстРежимПечатиГрешкабајти(p)
	return len(p), nil
}

const (
	fbШирина		= 80
	fbВисина		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorВисина		= 1
	cursorПушти		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func текстРежимinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШирина * fbВисина,
		Cap:	fbШирина * fbВисина,
		Data:	fbphysaddress,
	}))

}

func текстРежимenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorПушти)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorВисина+cursorПушти)
}

func текстРежимdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстРежимАжурирајcursor(x int, y int) {
	позиција := y*fbШирина + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(позиција&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((позиција>>8)&0xFF))
}

func текстРежимflushЕкран() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстРежимcheckfbПомести() {
	for fbcurrentline >= fbВисина {
		copy(fb[:len(fb)-fbШирина], fb[fbШирина:])

		for i := 0; i < fbШирина; i++ {
			fb[(fbВисина-1)*fbШирина+i] = 0xf00
		}
		fbcurrentline--
	}
}

func текстРежимПечатиcol(s string, атрибут uint8) {
	for _, b := range s {
		текстРежимПечатиcharcol(uint8(b), атрибут)
	}
}

func текстРежимprintlncol(s string, атрибут uint8) {
	for _, b := range s {
		текстРежимПечатиcharcol(uint8(b), атрибут)
	}
	текстРежимПечатиchar(0xa)
}

func текстРежимПечати(s string) {
	for _, b := range s {
		текстРежимПечатиchar(uint8(b))
	}
}

func текстРежимПечатибајти(a []byte) {
	for _, b := range a {
		текстРежимПечатиchar(uint8(b))
	}
}

func текстРежимПечатиГрешкабајти(a []byte) {
	for _, b := range a {
		текстРежимПечатиcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРежимprintln(s string) {
	for _, b := range s {
		текстРежимПечатиchar(uint8(b))
	}
	текстРежимПечатиchar(0xa)
}

func текстРежимПечатиГрешка(s string) {
	for _, b := range s {
		текстРежимПечатиcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРежимПечатиerrorln(s string) {
	текстРежимПечатиГрешка(s)
	текстРежимПечатиchar(0xa)
}

func текстРежимПечатиchar(char uint8) {
	текстРежимПечатиcharcol(char, 0<<4|0xf)
}

func текстРежимПечатиcharcol(char uint8, атрибут uint8) {
	текстРежимcheckfbПомести()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		текстРежимcheckfbПомести()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbШирина] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbШирина {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbШирина] = uint16(атрибут)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func текстРежимПечатиХекса64(number uint64) {
	текстРежимПечатиХекса32(uint32(number >> 32))
	текстРежимПечатиХекса32(uint32(number))
}

func текстРежимПечатиХекса32(number uint32) {
	текстРежимПечатиХекса16(uint16(number >> 16))
	текстРежимПечатиХекса16(uint16(number))
}

func текстРежимПечатиХекса16(number uint16) {
	текстРежимПечатиХекса(uint8(number >> 8))
	текстРежимПечатиХекса(uint8(number))
}

func текстРежимПечатиХекса(number uint8) {
	текстРежимПечатиХексаchar(number >> 4)
	текстРежимПечатиХексаchar(number)
}

func текстРежимПечатиХексаchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстРежимПечатиchar(0x30 + n)
	} else {
		текстРежимПечатиchar(0x41 + n - 10)
	}
}
