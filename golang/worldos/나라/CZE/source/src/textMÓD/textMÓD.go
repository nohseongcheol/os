/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textMÓDwriter struct {
}

func (e textMÓDwriter) Zápis(p []byte) (int, error) {
	textMÓDTisknoutBytů(p)
	return len(p), nil
}

type textMÓDChybawriter struct {
}

func (e textMÓDChybawriter) Zápis(p []byte) (int, error) {
	textMÓDTisknoutChybaBytů(p)
	return len(p), nil
}

const (
	fbŠířka			= 80
	fbVýška			= 25
	fbphysAdresa	uintptr	= 0xb8000
	kurzorVýška		= 1
	kurzorSpustit		= 11
)

var (
	fbSoučasnýŘádek	= 0
	fbSoučasnýcol	= 0
)

var fb []uint16

func textMÓDinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠířka * fbVýška,
		Cap:	fbŠířka * fbVýška,
		Data:	fbphysAdresa,
	}))

}

func textMÓDPovolitKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kurzorSpustit)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kurzorVýška+kurzorSpustit)
}

func textMÓDZakázatKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textMÓDAktualizovatKurzor(x int, y int) {
	umístění := y*fbŠířka + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(umístění&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((umístění>>8)&0xFF))
}

func textMÓDflushObrazovka() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textMÓDcheckfbPřesunout() {
	for fbSoučasnýŘádek >= fbVýška {
		copy(fb[:len(fb)-fbŠířka], fb[fbŠířka:])

		for i := 0; i < fbŠířka; i++ {
			fb[(fbVýška-1)*fbŠířka+i] = 0xf00
		}
		fbSoučasnýŘádek--
	}
}

func textMÓDTisknoutcol(s string, atribut uint8) {
	for _, b := range s {
		textMÓDTisknoutcharcol(uint8(b), atribut)
	}
}

func textMÓDprintlncol(s string, atribut uint8) {
	for _, b := range s {
		textMÓDTisknoutcharcol(uint8(b), atribut)
	}
	textMÓDTisknoutchar(0xa)
}

func textMÓDTisknout(s string) {
	for _, b := range s {
		textMÓDTisknoutchar(uint8(b))
	}
}

func textMÓDTisknoutBytů(a []byte) {
	for _, b := range a {
		textMÓDTisknoutchar(uint8(b))
	}
}

func textMÓDTisknoutChybaBytů(a []byte) {
	for _, b := range a {
		textMÓDTisknoutcharcol(uint8(b), 4<<4|0xf)
	}
}

func textMÓDprintln(s string) {
	for _, b := range s {
		textMÓDTisknoutchar(uint8(b))
	}
	textMÓDTisknoutchar(0xa)
}

func textMÓDTisknoutChyba(s string) {
	for _, b := range s {
		textMÓDTisknoutcharcol(uint8(b), 4<<4|0xf)
	}
}

func textMÓDTisknouterrorln(s string) {
	textMÓDTisknoutChyba(s)
	textMÓDTisknoutchar(0xa)
}

func textMÓDTisknoutchar(char uint8) {
	textMÓDTisknoutcharcol(char, 0<<4|0xf)
}

func textMÓDTisknoutcharcol(char uint8, atribut uint8) {
	textMÓDcheckfbPřesunout()
	if char == '\n' {
		fbSoučasnýŘádek++
		fbSoučasnýcol = 0
		textMÓDcheckfbPřesunout()
	} else if char == '\b' {
		fb[fbSoučasnýcol+fbSoučasnýŘádek*fbŠířka] = 0xf00
		fbSoučasnýcol = fbSoučasnýcol - 1
		if fbSoučasnýcol < 0 {
			fbSoučasnýcol = 0
		}
	} else if char == '\r' {
		fbSoučasnýcol = 0
	} else {
		if fbSoučasnýcol >= fbŠířka {
			return
		}
		fb[fbSoučasnýcol+fbSoučasnýŘádek*fbŠířka] = uint16(atribut)<<8 | uint16(char)
		fbSoučasnýcol++
	}

}

func textMÓDTisknoutŠestnáctkově64(číslo uint64) {
	textMÓDTisknoutŠestnáctkově32(uint32(číslo >> 32))
	textMÓDTisknoutŠestnáctkově32(uint32(číslo))
}

func textMÓDTisknoutŠestnáctkově32(číslo uint32) {
	textMÓDTisknoutŠestnáctkově16(uint16(číslo >> 16))
	textMÓDTisknoutŠestnáctkově16(uint16(číslo))
}

func textMÓDTisknoutŠestnáctkově16(číslo uint16) {
	textMÓDTisknoutŠestnáctkově(uint8(číslo >> 8))
	textMÓDTisknoutŠestnáctkově(uint8(číslo))
}

func textMÓDTisknoutŠestnáctkově(číslo uint8) {
	textMÓDTisknoutŠestnáctkověchar(číslo >> 4)
	textMÓDTisknoutŠestnáctkověchar(číslo)
}

func textMÓDTisknoutŠestnáctkověchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textMÓDTisknoutchar(0x30 + n)
	} else {
		textMÓDTisknoutchar(0x41 + n - 10)
	}
}
