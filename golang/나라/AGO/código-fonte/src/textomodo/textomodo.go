package main

import (
	"reflect"
	"unsafe"
)

type textomodowriter struct {
}

func (e textomodowriter) Escrever(p []byte) (int, error) {
	textomodoImprimirbytes(p)
	return len(p), nil
}

type textomodoErrowriter struct {
}

func (e textomodoErrowriter) Escrever(p []byte) (int, error) {
	textomodoImprimirErrobytes(p)
	return len(p), nil
}

const (
	fbLargura		= 80
	fbAltura		= 25
	fbphysEndereço	uintptr	= 0xb8000
	cursorAltura		= 1
	cursorIniciar		= 11
)

var (
	fbAtualLinha	= 0
	fbAtualcol	= 0
)

var fb []uint16

func textomodoinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLargura * fbAltura,
		Cap:	fbLargura * fbAltura,
		Data:	fbphysEndereço,
	}))

}

func textomodoActivarcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorIniciar)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorAltura+cursorIniciar)
}

func textomodoDesativarcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textomodoAtualizarcursor(x int, y int) {
	posição := y*fbLargura + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posição&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posição>>8)&0xFF))
}

func textomodoflushEcrã() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textomodocheckfbMover() {
	for fbAtualLinha >= fbAltura {
		copy(fb[:len(fb)-fbLargura], fb[fbLargura:])

		for i := 0; i < fbLargura; i++ {
			fb[(fbAltura-1)*fbLargura+i] = 0xf00
		}
		fbAtualLinha--
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

func textomodoImprimirErrobytes(a []byte) {
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

func textomodoImprimirErro(s string) {
	for _, b := range s {
		textomodoImprimircharcol(uint8(b), 4<<4|0xf)
	}
}

func textomodoImprimirerrorln(s string) {
	textomodoImprimirErro(s)
	textomodoImprimirchar(0xa)
}

func textomodoImprimirchar(char uint8) {
	textomodoImprimircharcol(char, 0<<4|0xf)
}

func textomodoImprimircharcol(char uint8, atributo uint8) {
	textomodocheckfbMover()
	if char == '\n' {
		fbAtualLinha++
		fbAtualcol = 0
		textomodocheckfbMover()
	} else if char == '\b' {
		fb[fbAtualcol+fbAtualLinha*fbLargura] = 0xf00
		fbAtualcol = fbAtualcol - 1
		if fbAtualcol < 0 {
			fbAtualcol = 0
		}
	} else if char == '\r' {
		fbAtualcol = 0
	} else {
		if fbAtualcol >= fbLargura {
			return
		}
		fb[fbAtualcol+fbAtualLinha*fbLargura] = uint16(atributo)<<8 | uint16(char)
		fbAtualcol++
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
