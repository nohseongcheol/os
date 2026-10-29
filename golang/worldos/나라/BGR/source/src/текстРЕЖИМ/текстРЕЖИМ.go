/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type текстРЕЖИМwriter struct {
}

func (e текстРЕЖИМwriter) Писане(p []byte) (int, error) {
	текстРЕЖИМПечатБайтове(p)
	return len(p), nil
}

type текстРЕЖИМГрешкаwriter struct {
}

func (e текстРЕЖИМГрешкаwriter) Писане(p []byte) (int, error) {
	текстРЕЖИМПечатГрешкаБайтове(p)
	return len(p), nil
}

const (
	fbШирочина			= 80
	fbВисочина			= 25
	fbphysaddress		uintptr	= 0xb8000
	курсорВисочина			= 1
	курсорСтартиране		= 11
)

var (
	fbТекущадатаline	= 0
	fbТекущадатаcol		= 0
)

var fb []uint16

func текстРЕЖИМinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШирочина * fbВисочина,
		Cap:	fbШирочина * fbВисочина,
		Data:	fbphysaddress,
	}))

}

func текстРЕЖИМВключванеКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|курсорСтартиране)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|курсорВисочина+курсорСтартиране)
}

func текстРЕЖИМИзключванеКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстРЕЖИМОбновяванеКурсор(x int, y int) {
	позиция := y*fbШирочина + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(позиция&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((позиция>>8)&0xFF))
}

func текстРЕЖИМflushЕкран() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстРЕЖИМcheckfbПреместване() {
	for fbТекущадатаline >= fbВисочина {
		copy(fb[:len(fb)-fbШирочина], fb[fbШирочина:])

		for i := 0; i < fbШирочина; i++ {
			fb[(fbВисочина-1)*fbШирочина+i] = 0xf00
		}
		fbТекущадатаline--
	}
}

func текстРЕЖИМПечатcol(s string, атрибут uint8) {
	for _, b := range s {
		текстРЕЖИМПечатcharcol(uint8(b), атрибут)
	}
}

func текстРЕЖИМprintlncol(s string, атрибут uint8) {
	for _, b := range s {
		текстРЕЖИМПечатcharcol(uint8(b), атрибут)
	}
	текстРЕЖИМПечатchar(0xa)
}

func текстРЕЖИМПечат(s string) {
	for _, b := range s {
		текстРЕЖИМПечатchar(uint8(b))
	}
}

func текстРЕЖИМПечатБайтове(a []byte) {
	for _, b := range a {
		текстРЕЖИМПечатchar(uint8(b))
	}
}

func текстРЕЖИМПечатГрешкаБайтове(a []byte) {
	for _, b := range a {
		текстРЕЖИМПечатcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМprintln(s string) {
	for _, b := range s {
		текстРЕЖИМПечатchar(uint8(b))
	}
	текстРЕЖИМПечатchar(0xa)
}

func текстРЕЖИМПечатГрешка(s string) {
	for _, b := range s {
		текстРЕЖИМПечатcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМПечатerrorln(s string) {
	текстРЕЖИМПечатГрешка(s)
	текстРЕЖИМПечатchar(0xa)
}

func текстРЕЖИМПечатchar(char uint8) {
	текстРЕЖИМПечатcharcol(char, 0<<4|0xf)
}

func текстРЕЖИМПечатcharcol(char uint8, атрибут uint8) {
	текстРЕЖИМcheckfbПреместване()
	if char == '\n' {
		fbТекущадатаline++
		fbТекущадатаcol = 0
		текстРЕЖИМcheckfbПреместване()
	} else if char == '\b' {
		fb[fbТекущадатаcol+fbТекущадатаline*fbШирочина] = 0xf00
		fbТекущадатаcol = fbТекущадатаcol - 1
		if fbТекущадатаcol < 0 {
			fbТекущадатаcol = 0
		}
	} else if char == '\r' {
		fbТекущадатаcol = 0
	} else {
		if fbТекущадатаcol >= fbШирочина {
			return
		}
		fb[fbТекущадатаcol+fbТекущадатаline*fbШирочина] = uint16(атрибут)<<8 | uint16(char)
		fbТекущадатаcol++
	}

}

func текстРЕЖИМПечатhex64(число uint64) {
	текстРЕЖИМПечатhex32(uint32(число >> 32))
	текстРЕЖИМПечатhex32(uint32(число))
}

func текстРЕЖИМПечатhex32(число uint32) {
	текстРЕЖИМПечатhex16(uint16(число >> 16))
	текстРЕЖИМПечатhex16(uint16(число))
}

func текстРЕЖИМПечатhex16(число uint16) {
	текстРЕЖИМПечатhex(uint8(число >> 8))
	текстРЕЖИМПечатhex(uint8(число))
}

func текстРЕЖИМПечатhex(число uint8) {
	текстРЕЖИМПечатhexchar(число >> 4)
	текстРЕЖИМПечатhexchar(число)
}

func текстРЕЖИМПечатhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстРЕЖИМПечатchar(0x30 + n)
	} else {
		текстРЕЖИМПечатchar(0x41 + n - 10)
	}
}
