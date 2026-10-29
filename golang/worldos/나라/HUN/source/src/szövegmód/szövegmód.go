/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type szövegmódwriter struct {
}

func (e szövegmódwriter) Írás(p []byte) (int, error) {
	szövegmódNyomtatásBájt(p)
	return len(p), nil
}

type szövegmódHibawriter struct {
}

func (e szövegmódHibawriter) Írás(p []byte) (int, error) {
	szövegmódNyomtatásHibaBájt(p)
	return len(p), nil
}

const (
	fbSzélesség		= 80
	fbMagasság		= 25
	fbphysaddress	uintptr	= 0xb8000
	kurzorMagasság		= 1
	kurzorIndítás		= 11
)

var (
	fbJelenlegiSor	= 0
	fbJelenlegicol	= 0
)

var fb []uint16

func szövegmódinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbSzélesség * fbMagasság,
		Cap:	fbSzélesség * fbMagasság,
		Data:	fbphysaddress,
	}))

}

func szövegmódEngedélyezveKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kurzorIndítás)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kurzorMagasság+kurzorIndítás)
}

func szövegmódLetiltvaKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func szövegmódFrissítésKurzor(x int, y int) {
	pozíció := y*fbSzélesség + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozíció&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozíció>>8)&0xFF))
}

func szövegmódflushKépernyő() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func szövegmódcheckfbÁthelyezés() {
	for fbJelenlegiSor >= fbMagasság {
		copy(fb[:len(fb)-fbSzélesség], fb[fbSzélesség:])

		for i := 0; i < fbSzélesség; i++ {
			fb[(fbMagasság-1)*fbSzélesség+i] = 0xf00
		}
		fbJelenlegiSor--
	}
}

func szövegmódNyomtatáscol(s string, attribútum uint8) {
	for _, b := range s {
		szövegmódNyomtatáscharcol(uint8(b), attribútum)
	}
}

func szövegmódprintlncol(s string, attribútum uint8) {
	for _, b := range s {
		szövegmódNyomtatáscharcol(uint8(b), attribútum)
	}
	szövegmódNyomtatáschar(0xa)
}

func szövegmódNyomtatás(s string) {
	for _, b := range s {
		szövegmódNyomtatáschar(uint8(b))
	}
}

func szövegmódNyomtatásBájt(a []byte) {
	for _, b := range a {
		szövegmódNyomtatáschar(uint8(b))
	}
}

func szövegmódNyomtatásHibaBájt(a []byte) {
	for _, b := range a {
		szövegmódNyomtatáscharcol(uint8(b), 4<<4|0xf)
	}
}

func szövegmódprintln(s string) {
	for _, b := range s {
		szövegmódNyomtatáschar(uint8(b))
	}
	szövegmódNyomtatáschar(0xa)
}

func szövegmódNyomtatásHiba(s string) {
	for _, b := range s {
		szövegmódNyomtatáscharcol(uint8(b), 4<<4|0xf)
	}
}

func szövegmódNyomtatáserrorln(s string) {
	szövegmódNyomtatásHiba(s)
	szövegmódNyomtatáschar(0xa)
}

func szövegmódNyomtatáschar(char uint8) {
	szövegmódNyomtatáscharcol(char, 0<<4|0xf)
}

func szövegmódNyomtatáscharcol(char uint8, attribútum uint8) {
	szövegmódcheckfbÁthelyezés()
	if char == '\n' {
		fbJelenlegiSor++
		fbJelenlegicol = 0
		szövegmódcheckfbÁthelyezés()
	} else if char == '\b' {
		fb[fbJelenlegicol+fbJelenlegiSor*fbSzélesség] = 0xf00
		fbJelenlegicol = fbJelenlegicol - 1
		if fbJelenlegicol < 0 {
			fbJelenlegicol = 0
		}
	} else if char == '\r' {
		fbJelenlegicol = 0
	} else {
		if fbJelenlegicol >= fbSzélesség {
			return
		}
		fb[fbJelenlegicol+fbJelenlegiSor*fbSzélesség] = uint16(attribútum)<<8 | uint16(char)
		fbJelenlegicol++
	}

}

func szövegmódNyomtatásHexadecimális64(szám uint64) {
	szövegmódNyomtatásHexadecimális32(uint32(szám >> 32))
	szövegmódNyomtatásHexadecimális32(uint32(szám))
}

func szövegmódNyomtatásHexadecimális32(szám uint32) {
	szövegmódNyomtatásHexadecimális16(uint16(szám >> 16))
	szövegmódNyomtatásHexadecimális16(uint16(szám))
}

func szövegmódNyomtatásHexadecimális16(szám uint16) {
	szövegmódNyomtatásHexadecimális(uint8(szám >> 8))
	szövegmódNyomtatásHexadecimális(uint8(szám))
}

func szövegmódNyomtatásHexadecimális(szám uint8) {
	szövegmódNyomtatásHexadecimálischar(szám >> 4)
	szövegmódNyomtatásHexadecimálischar(szám)
}

func szövegmódNyomtatásHexadecimálischar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		szövegmódNyomtatáschar(0x30 + n)
	} else {
		szövegmódNyomtatáschar(0x41 + n - 10)
	}
}
