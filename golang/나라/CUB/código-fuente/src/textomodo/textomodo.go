/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textomodowriter struct {
}

func (e textomodowriter) Escribir(p []byte) (int, error) {
	textomodoImprimirbytes(p)
	return len(p), nil
}

type textomodoerrorwriter struct {
}

func (e textomodoerrorwriter) Escribir(p []byte) (int, error) {
	textomodoImprimirerrorbytes(p)
	return len(p), nil
}

const (
	fbAncho			= 80
	fbAltura		= 25
	fbphysDirección	uintptr	= 0xb8000
	cursorAltura		= 1
	cursorIniciar		= 11
)

var (
	fbActualLínea	= 0
	fbActualcol	= 0
)

var fb []uint16

func textomodoinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbAncho * fbAltura,
		Cap:	fbAncho * fbAltura,
		Data:	fbphysDirección,
	}))

}

func textomodoActivarcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorIniciar)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorAltura+cursorIniciar)
}

func textomodoDesactivarcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textomodoActualizarcursor(x int, y int) {
	posición := y*fbAncho + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posición&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posición>>8)&0xFF))
}

func textomodoflushPantalla() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textomodocheckfbMover() {
	for fbActualLínea >= fbAltura {
		copy(fb[:len(fb)-fbAncho], fb[fbAncho:])

		for i := 0; i < fbAncho; i++ {
			fb[(fbAltura-1)*fbAncho+i] = 0xf00
		}
		fbActualLínea--
	}
}

func textomodoImprimircol(s string, atributo uint8) {
	for _, b := range s {
		textomodoImprimircharcol(uint8(b), atributo)
	}
}

func textomodoprintlncol(s string, atributo uint8) {
	for _, b := range s {
		textomodoImprimircharcol(uint8(b), atributo)
	}
	textomodoImprimirchar(0xa)
}

func textomodoImprimir(s string) {
	for _, b := range s {
		textomodoImprimirchar(uint8(b))
	}
}

func textomodoImprimirbytes(a []byte) {
	for _, b := range a {
		textomodoImprimirchar(uint8(b))
	}
}

func textomodoImprimirerrorbytes(a []byte) {
	for _, b := range a {
		textomodoImprimircharcol(uint8(b), 4<<4|0xf)
	}
}

func textomodoprintln(s string) {
	for _, b := range s {
		textomodoImprimirchar(uint8(b))
	}
	textomodoImprimirchar(0xa)
}

func textomodoImprimirerror(s string) {
	for _, b := range s {
		textomodoImprimircharcol(uint8(b), 4<<4|0xf)
	}
}

func textomodoImprimirerrorln(s string) {
	textomodoImprimirerror(s)
	textomodoImprimirchar(0xa)
}

func textomodoImprimirchar(char uint8) {
	textomodoImprimircharcol(char, 0<<4|0xf)
}

func textomodoImprimircharcol(char uint8, atributo uint8) {
	textomodocheckfbMover()
	if char == '\n' {
		fbActualLínea++
		fbActualcol = 0
		textomodocheckfbMover()
	} else if char == '\b' {
		fb[fbActualcol+fbActualLínea*fbAncho] = 0xf00
		fbActualcol = fbActualcol - 1
		if fbActualcol < 0 {
			fbActualcol = 0
		}
	} else if char == '\r' {
		fbActualcol = 0
	} else {
		if fbActualcol >= fbAncho {
			return
		}
		fb[fbActualcol+fbActualLínea*fbAncho] = uint16(atributo)<<8 | uint16(char)
		fbActualcol++
	}

}

func textomodoImprimirHexadecimal64(número uint64) {
	textomodoImprimirHexadecimal32(uint32(número >> 32))
	textomodoImprimirHexadecimal32(uint32(número))
}

func textomodoImprimirHexadecimal32(número uint32) {
	textomodoImprimirHexadecimal16(uint16(número >> 16))
	textomodoImprimirHexadecimal16(uint16(número))
}

func textomodoImprimirHexadecimal16(número uint16) {
	textomodoImprimirHexadecimal(uint8(número >> 8))
	textomodoImprimirHexadecimal(uint8(número))
}

func textomodoImprimirHexadecimal(número uint8) {
	textomodoImprimirHexadecimalchar(número >> 4)
	textomodoImprimirHexadecimalchar(número)
}

func textomodoImprimirHexadecimalchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textomodoImprimirchar(0x30 + n)
	} else {
		textomodoImprimirchar(0x41 + n - 10)
	}
}
