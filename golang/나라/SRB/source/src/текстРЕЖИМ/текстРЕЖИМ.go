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

func (e текстРЕЖИМwriter) Пише(p []byte) (int, error) {
	текстРЕЖИМШтампајБајтова(p)
	return len(p), nil
}

type текстРЕЖИМГрешкаwriter struct {
}

func (e текстРЕЖИМГрешкаwriter) Пише(p []byte) (int, error) {
	текстРЕЖИМШтампајГрешкаБајтова(p)
	return len(p), nil
}

const (
	fbШирина			= 80
	fbВисина			= 25
	fbphysaddress		uintptr	= 0xb8000
	показивачВисина			= 1
	показивачПокрени		= 11
)

var (
	fbТренутноред	= 0
	fbТренутноcol	= 0
)

var fb []uint16

func текстРЕЖИМinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШирина * fbВисина,
		Cap:	fbШирина * fbВисина,
		Data:	fbphysaddress,
	}))

}

func текстРЕЖИМукљученоПоказивач() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|показивачПокрени)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|показивачВисина+показивачПокрени)
}

func текстРЕЖИМИскључиПоказивач() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстРЕЖИМОсвежиПоказивач(x int, y int) {
	положај := y*fbШирина + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(положај&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((положај>>8)&0xFF))
}

func текстРЕЖИМflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстРЕЖИМcheckfbПремести() {
	for fbТренутноред >= fbВисина {
		copy(fb[:len(fb)-fbШирина], fb[fbШирина:])

		for i := 0; i < fbШирина; i++ {
			fb[(fbВисина-1)*fbШирина+i] = 0xf00
		}
		fbТренутноред--
	}
}

func текстРЕЖИМШтампајcol(s string, атрибут uint8) {
	for _, b := range s {
		текстРЕЖИМШтампајcharcol(uint8(b), атрибут)
	}
}

func текстРЕЖИМprintlncol(s string, атрибут uint8) {
	for _, b := range s {
		текстРЕЖИМШтампајcharcol(uint8(b), атрибут)
	}
	текстРЕЖИМШтампајchar(0xa)
}

func текстРЕЖИМШтампај(s string) {
	for _, b := range s {
		текстРЕЖИМШтампајchar(uint8(b))
	}
}

func текстРЕЖИМШтампајБајтова(a []byte) {
	for _, b := range a {
		текстРЕЖИМШтампајchar(uint8(b))
	}
}

func текстРЕЖИМШтампајГрешкаБајтова(a []byte) {
	for _, b := range a {
		текстРЕЖИМШтампајcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМprintln(s string) {
	for _, b := range s {
		текстРЕЖИМШтампајchar(uint8(b))
	}
	текстРЕЖИМШтампајchar(0xa)
}

func текстРЕЖИМШтампајГрешка(s string) {
	for _, b := range s {
		текстРЕЖИМШтампајcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМШтампајerrorln(s string) {
	текстРЕЖИМШтампајГрешка(s)
	текстРЕЖИМШтампајchar(0xa)
}

func текстРЕЖИМШтампајchar(char uint8) {
	текстРЕЖИМШтампајcharcol(char, 0<<4|0xf)
}

func текстРЕЖИМШтампајcharcol(char uint8, атрибут uint8) {
	текстРЕЖИМcheckfbПремести()
	if char == '\n' {
		fbТренутноред++
		fbТренутноcol = 0
		текстРЕЖИМcheckfbПремести()
	} else if char == '\b' {
		fb[fbТренутноcol+fbТренутноред*fbШирина] = 0xf00
		fbТренутноcol = fbТренутноcol - 1
		if fbТренутноcol < 0 {
			fbТренутноcol = 0
		}
	} else if char == '\r' {
		fbТренутноcol = 0
	} else {
		if fbТренутноcol >= fbШирина {
			return
		}
		fb[fbТренутноcol+fbТренутноред*fbШирина] = uint16(атрибут)<<8 | uint16(char)
		fbТренутноcol++
	}

}

func текстРЕЖИМШтампајХексадецимално64(број uint64) {
	текстРЕЖИМШтампајХексадецимално32(uint32(број >> 32))
	текстРЕЖИМШтампајХексадецимално32(uint32(број))
}

func текстРЕЖИМШтампајХексадецимално32(број uint32) {
	текстРЕЖИМШтампајХексадецимално16(uint16(број >> 16))
	текстРЕЖИМШтампајХексадецимално16(uint16(број))
}

func текстРЕЖИМШтампајХексадецимално16(број uint16) {
	текстРЕЖИМШтампајХексадецимално(uint8(број >> 8))
	текстРЕЖИМШтампајХексадецимално(uint8(број))
}

func текстРЕЖИМШтампајХексадецимално(број uint8) {
	текстРЕЖИМШтампајХексадецималноchar(број >> 4)
	текстРЕЖИМШтампајХексадецималноchar(број)
}

func текстРЕЖИМШтампајХексадецималноchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстРЕЖИМШтампајchar(0x30 + n)
	} else {
		текстРЕЖИМШтампајchar(0x41 + n - 10)
	}
}
