/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textmodewriter struct {
}

func (e textmodewriter) Escriptura(p []byte) (int, error) {
	textmodeImprimeixbytes(p)
	return len(p), nil
}

type textmodeshaproduïtunerrorwriter struct {
}

func (e textmodeshaproduïtunerrorwriter) Escriptura(p []byte) (int, error) {
	textmodeImprimeixshaproduïtunerrorbytes(p)
	return len(p), nil
}

const (
	fbAmplada		= 80
	fbAlçada		= 25
	fbphysAdreça	uintptr	= 0xb8000
	cursorAlçada		= 1
	cursorInicia		= 11
)

var (
	fbActualLínia	= 0
	fbActualcol	= 0
)

var fb []uint16

func textmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbAmplada * fbAlçada,
		Cap:	fbAmplada * fbAlçada,
		Data:	fbphysAdreça,
	}))

}

func textmodeActivacursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorInicia)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorAlçada+cursorInicia)
}

func textmodeInhabilitacursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textmodeActualitzacursor(x int, y int) {
	posició := y*fbAmplada + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posició&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posició>>8)&0xFF))
}

func textmodeflushPantalla() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textmodecheckfbMou() {
	for fbActualLínia >= fbAlçada {
		copy(fb[:len(fb)-fbAmplada], fb[fbAmplada:])

		for i := 0; i < fbAmplada; i++ {
			fb[(fbAlçada-1)*fbAmplada+i] = 0xf00
		}
		fbActualLínia--
	}
}

func textmodeImprimeixcol(s string, atribut uint8) {
	for _, b := range s {
		textmodeImprimeixcharcol(uint8(b), atribut)
	}
}

func textmodeprintlncol(s string, atribut uint8) {
	for _, b := range s {
		textmodeImprimeixcharcol(uint8(b), atribut)
	}
	textmodeImprimeixchar(0xa)
}

func textmodeImprimeix(s string) {
	for _, b := range s {
		textmodeImprimeixchar(uint8(b))
	}
}

func textmodeImprimeixbytes(a []byte) {
	for _, b := range a {
		textmodeImprimeixchar(uint8(b))
	}
}

func textmodeImprimeixshaproduïtunerrorbytes(a []byte) {
	for _, b := range a {
		textmodeImprimeixcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeprintln(s string) {
	for _, b := range s {
		textmodeImprimeixchar(uint8(b))
	}
	textmodeImprimeixchar(0xa)
}

func textmodeImprimeixshaproduïtunerror(s string) {
	for _, b := range s {
		textmodeImprimeixcharcol(uint8(b), 4<<4|0xf)
	}
}

func textmodeImprimeixerrorln(s string) {
	textmodeImprimeixshaproduïtunerror(s)
	textmodeImprimeixchar(0xa)
}

func textmodeImprimeixchar(char uint8) {
	textmodeImprimeixcharcol(char, 0<<4|0xf)
}

func textmodeImprimeixcharcol(char uint8, atribut uint8) {
	textmodecheckfbMou()
	if char == '\n' {
		fbActualLínia++
		fbActualcol = 0
		textmodecheckfbMou()
	} else if char == '\b' {
		fb[fbActualcol+fbActualLínia*fbAmplada] = 0xf00
		fbActualcol = fbActualcol - 1
		if fbActualcol < 0 {
			fbActualcol = 0
		}
	} else if char == '\r' {
		fbActualcol = 0
	} else {
		if fbActualcol >= fbAmplada {
			return
		}
		fb[fbActualcol+fbActualLínia*fbAmplada] = uint16(atribut)<<8 | uint16(char)
		fbActualcol++
	}

}

func textmodeImprimeixHexadecimal64(nombre uint64) {
	textmodeImprimeixHexadecimal32(uint32(nombre >> 32))
	textmodeImprimeixHexadecimal32(uint32(nombre))
}

func textmodeImprimeixHexadecimal32(nombre uint32) {
	textmodeImprimeixHexadecimal16(uint16(nombre >> 16))
	textmodeImprimeixHexadecimal16(uint16(nombre))
}

func textmodeImprimeixHexadecimal16(nombre uint16) {
	textmodeImprimeixHexadecimal(uint8(nombre >> 8))
	textmodeImprimeixHexadecimal(uint8(nombre))
}

func textmodeImprimeixHexadecimal(nombre uint8) {
	textmodeImprimeixHexadecimalchar(nombre >> 4)
	textmodeImprimeixHexadecimalchar(nombre)
}

func textmodeImprimeixHexadecimalchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textmodeImprimeixchar(0x30 + n)
	} else {
		textmodeImprimeixchar(0x41 + n - 10)
	}
}
