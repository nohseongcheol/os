package main

import (
	"reflect"
	"unsafe"
)

type текстрежимwriter struct {
}

func (e текстрежимwriter) Писать(p []byte) (int, error) {
	текстрежимПечатьБайт(p)
	return len(p), nil
}

type текстрежимОшибкаwriter struct {
}

func (e текстрежимОшибкаwriter) Писать(p []byte) (int, error) {
	текстрежимПечатьОшибкаБайт(p)
	return len(p), nil
}

const (
	fbШирина		= 80
	fbВысота		= 25
	fbphysaddress	uintptr	= 0xb8000
	курсорВысота		= 1
	курсорПуск		= 11
)

var (
	fbТекущаядатаСтрока	= 0
	fbТекущаядатаcol	= 0
)

var fb []uint16

func текстрежимinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШирина * fbВысота,
		Cap:	fbШирина * fbВысота,
		Data:	fbphysaddress,
	}))

}

func текстрежимВключитьКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|курсорПуск)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|курсорВысота+курсорПуск)
}

func текстрежимОтключитьКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстрежимОбновитьКурсор(x int, y int) {
	позиция := y*fbШирина + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(позиция&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((позиция>>8)&0xFF))
}

func текстрежимflushЭкран() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстрежимcheckfbПереместить() {
	for fbТекущаядатаСтрока >= fbВысота {
		copy(fb[:len(fb)-fbШирина], fb[fbШирина:])

		for i := 0; i < fbШирина; i++ {
			fb[(fbВысота-1)*fbШирина+i] = 0xf00
		}
		fbТекущаядатаСтрока--
	}
}

func текстрежимПечатьcol(s string, атрибут uint8) {
	for _, b := range s {
		текстрежимПечатьcharcol(uint8(b), атрибут)
	}
}

func текстрежимprintlncol(s string, атрибут uint8) {
	for _, b := range s {
		текстрежимПечатьcharcol(uint8(b), атрибут)
	}
	текстрежимПечатьchar(0xa)
}

func текстрежимПечать(s string) {
	for _, b := range s {
		текстрежимПечатьchar(uint8(b))
	}
}

func текстрежимПечатьБайт(a []byte) {
	for _, b := range a {
		текстрежимПечатьchar(uint8(b))
	}
}

func текстрежимПечатьОшибкаБайт(a []byte) {
	for _, b := range a {
		текстрежимПечатьcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстрежимprintln(s string) {
	for _, b := range s {
		текстрежимПечатьchar(uint8(b))
	}
	текстрежимПечатьchar(0xa)
}

func текстрежимПечатьОшибка(s string) {
	for _, b := range s {
		текстрежимПечатьcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстрежимПечатьerrorln(s string) {
	текстрежимПечатьОшибка(s)
	текстрежимПечатьchar(0xa)
}

func текстрежимПечатьchar(char uint8) {
	текстрежимПечатьcharcol(char, 0<<4|0xf)
}

func текстрежимПечатьcharcol(char uint8, атрибут uint8) {
	текстрежимcheckfbПереместить()
	if char == '\n' {
		fbТекущаядатаСтрока++
		fbТекущаядатаcol = 0
		текстрежимcheckfbПереместить()
	} else if char == '\b' {
		fb[fbТекущаядатаcol+fbТекущаядатаСтрока*fbШирина] = 0xf00
		fbТекущаядатаcol = fbТекущаядатаcol - 1
		if fbТекущаядатаcol < 0 {
			fbТекущаядатаcol = 0
		}
	} else if char == '\r' {
		fbТекущаядатаcol = 0
	} else {
		if fbТекущаядатаcol >= fbШирина {
			return
		}
		fb[fbТекущаядатаcol+fbТекущаядатаСтрока*fbШирина] = uint16(атрибут)<<8 | uint16(char)
		fbТекущаядатаcol++
	}

}

func текстрежимПечатьhex64(число uint64) {
	текстрежимПечатьhex32(uint32(число >> 32))
	текстрежимПечатьhex32(uint32(число))
}

func текстрежимПечатьhex32(число uint32) {
	текстрежимПечатьhex16(uint16(число >> 16))
	текстрежимПечатьhex16(uint16(число))
}

func текстрежимПечатьhex16(число uint16) {
	текстрежимПечатьhex(uint8(число >> 8))
	текстрежимПечатьhex(uint8(число))
}

func текстрежимПечатьhex(число uint8) {
	текстрежимПечатьhexchar(число >> 4)
	текстрежимПечатьhexchar(число)
}

func текстрежимПечатьhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстрежимПечатьchar(0x30 + n)
	} else {
		текстрежимПечатьchar(0x41 + n - 10)
	}
}
