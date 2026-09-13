package main

import (
	"reflect"
	"unsafe"
)

type tekstTRYBwriter struct {
}

func (e tekstTRYBwriter) Zapis(p []byte) (int, error) {
	tekstTRYBWydrukujBajty(p)
	return len(p), nil
}

type tekstTRYBBłądwriter struct {
}

func (e tekstTRYBBłądwriter) Zapis(p []byte) (int, error) {
	tekstTRYBWydrukujBłądBajty(p)
	return len(p), nil
}

const (
	fbSzerokość		= 80
	fbWysokość		= 25
	fbphysAdres	uintptr	= 0xb8000
	kursorWysokość		= 1
	kursorUruchom		= 11
)

var (
	fbBieżącyWiersz	= 0
	fbBieżącycol	= 0
)

var fb []uint16

func tekstTRYBinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbSzerokość * fbWysokość,
		Cap:	fbSzerokość * fbWysokość,
		Data:	fbphysAdres,
	}))

}

func tekstTRYBWłączKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kursorUruchom)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kursorWysokość+kursorUruchom)
}

func tekstTRYBWyłączKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstTRYBUaktualnijKursor(x int, y int) {
	pozycja := y*fbSzerokość + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozycja&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozycja>>8)&0xFF))
}

func tekstTRYBflushEkran() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstTRYBcheckfbPrzenoszenie() {
	for fbBieżącyWiersz >= fbWysokość {
		copy(fb[:len(fb)-fbSzerokość], fb[fbSzerokość:])

		for i := 0; i < fbSzerokość; i++ {
			fb[(fbWysokość-1)*fbSzerokość+i] = 0xf00
		}
		fbBieżącyWiersz--
	}
}

func tekstTRYBWydrukujcol(s string, atrybut uint8) {
	for _, b := range s {
		tekstTRYBWydrukujcharcol(uint8(b), atrybut)
	}
}

func tekstTRYBprintlncol(s string, atrybut uint8) {
	for _, b := range s {
		tekstTRYBWydrukujcharcol(uint8(b), atrybut)
	}
	tekstTRYBWydrukujchar(0xa)
}

func tekstTRYBWydrukuj(s string) {
	for _, b := range s {
		tekstTRYBWydrukujchar(uint8(b))
	}
}

func tekstTRYBWydrukujBajty(a []byte) {
	for _, b := range a {
		tekstTRYBWydrukujchar(uint8(b))
	}
}

func tekstTRYBWydrukujBłądBajty(a []byte) {
	for _, b := range a {
		tekstTRYBWydrukujcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstTRYBprintln(s string) {
	for _, b := range s {
		tekstTRYBWydrukujchar(uint8(b))
	}
	tekstTRYBWydrukujchar(0xa)
}

func tekstTRYBWydrukujBłąd(s string) {
	for _, b := range s {
		tekstTRYBWydrukujcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstTRYBWydrukujerrorln(s string) {
	tekstTRYBWydrukujBłąd(s)
	tekstTRYBWydrukujchar(0xa)
}

func tekstTRYBWydrukujchar(char uint8) {
	tekstTRYBWydrukujcharcol(char, 0<<4|0xf)
}

func tekstTRYBWydrukujcharcol(char uint8, atrybut uint8) {
	tekstTRYBcheckfbPrzenoszenie()
	if char == '\n' {
		fbBieżącyWiersz++
		fbBieżącycol = 0
		tekstTRYBcheckfbPrzenoszenie()
	} else if char == '\b' {
		fb[fbBieżącycol+fbBieżącyWiersz*fbSzerokość] = 0xf00
		fbBieżącycol = fbBieżącycol - 1
		if fbBieżącycol < 0 {
			fbBieżącycol = 0
		}
	} else if char == '\r' {
		fbBieżącycol = 0
	} else {
		if fbBieżącycol >= fbSzerokość {
			return
		}
		fb[fbBieżącycol+fbBieżącyWiersz*fbSzerokość] = uint16(atrybut)<<8 | uint16(char)
		fbBieżącycol++
	}

}

func tekstTRYBWydrukujSzesnastkowo64(liczba_2 uint64) {
	tekstTRYBWydrukujSzesnastkowo32(uint32(liczba_2 >> 32))
	tekstTRYBWydrukujSzesnastkowo32(uint32(liczba_2))
}

func tekstTRYBWydrukujSzesnastkowo32(liczba_2 uint32) {
	tekstTRYBWydrukujSzesnastkowo16(uint16(liczba_2 >> 16))
	tekstTRYBWydrukujSzesnastkowo16(uint16(liczba_2))
}

func tekstTRYBWydrukujSzesnastkowo16(liczba_2 uint16) {
	tekstTRYBWydrukujSzesnastkowo(uint8(liczba_2 >> 8))
	tekstTRYBWydrukujSzesnastkowo(uint8(liczba_2))
}

func tekstTRYBWydrukujSzesnastkowo(liczba_2 uint8) {
	tekstTRYBWydrukujSzesnastkowochar(liczba_2 >> 4)
	tekstTRYBWydrukujSzesnastkowochar(liczba_2)
}

func tekstTRYBWydrukujSzesnastkowochar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstTRYBWydrukujchar(0x30 + n)
	} else {
		tekstTRYBWydrukujchar(0x41 + n - 10)
	}
}
