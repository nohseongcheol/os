package main

import (
	"reflect"
	"unsafe"
)

type textMODwriter struct {
}

func (e textMODwriter) Scriere(p []byte) (int, error) {
	textMODTipăreșteOcteți(p)
	return len(p), nil
}

type textMODEroarewriter struct {
}

func (e textMODEroarewriter) Scriere(p []byte) (int, error) {
	textMODTipăreșteEroareOcteți(p)
	return len(p), nil
}

const (
	fbLățime		= 80
	fbÎnălțime		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorÎnălțime		= 1
	cursorPornește		= 11
)

var (
	fbCurentăLinie	= 0
	fbCurentăcol	= 0
)

var fb []uint16

func textMODinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLățime * fbÎnălțime,
		Cap:	fbLățime * fbÎnălțime,
		Data:	fbphysaddress,
	}))

}

func textMODActiveazăcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorPornește)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorÎnălțime+cursorPornește)
}

func textMODDezactiveazăcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textMODActualizeazăcursor(x int, y int) {
	poziție := y*fbLățime + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(poziție&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((poziție>>8)&0xFF))
}

func textMODflushEcran() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textMODcheckfbMutare() {
	for fbCurentăLinie >= fbÎnălțime {
		copy(fb[:len(fb)-fbLățime], fb[fbLățime:])

		for i := 0; i < fbLățime; i++ {
			fb[(fbÎnălțime-1)*fbLățime+i] = 0xf00
		}
		fbCurentăLinie--
	}
}

func textMODTipăreștecol(s string, atribut uint8) {
	for _, b := range s {
		textMODTipăreștecharcol(uint8(b), atribut)
	}
}

func textMODprintlncol(s string, atribut uint8) {
	for _, b := range s {
		textMODTipăreștecharcol(uint8(b), atribut)
	}
	textMODTipăreștechar(0xa)
}

func textMODTipărește(s string) {
	for _, b := range s {
		textMODTipăreștechar(uint8(b))
	}
}

func textMODTipăreșteOcteți(a []byte) {
	for _, b := range a {
		textMODTipăreștechar(uint8(b))
	}
}

func textMODTipăreșteEroareOcteți(a []byte) {
	for _, b := range a {
		textMODTipăreștecharcol(uint8(b), 4<<4|0xf)
	}
}

func textMODprintln(s string) {
	for _, b := range s {
		textMODTipăreștechar(uint8(b))
	}
	textMODTipăreștechar(0xa)
}

func textMODTipăreșteEroare(s string) {
	for _, b := range s {
		textMODTipăreștecharcol(uint8(b), 4<<4|0xf)
	}
}

func textMODTipăreșteerrorln(s string) {
	textMODTipăreșteEroare(s)
	textMODTipăreștechar(0xa)
}

func textMODTipăreștechar(char uint8) {
	textMODTipăreștecharcol(char, 0<<4|0xf)
}

func textMODTipăreștecharcol(char uint8, atribut uint8) {
	textMODcheckfbMutare()
	if char == '\n' {
		fbCurentăLinie++
		fbCurentăcol = 0
		textMODcheckfbMutare()
	} else if char == '\b' {
		fb[fbCurentăcol+fbCurentăLinie*fbLățime] = 0xf00
		fbCurentăcol = fbCurentăcol - 1
		if fbCurentăcol < 0 {
			fbCurentăcol = 0
		}
	} else if char == '\r' {
		fbCurentăcol = 0
	} else {
		if fbCurentăcol >= fbLățime {
			return
		}
		fb[fbCurentăcol+fbCurentăLinie*fbLățime] = uint16(atribut)<<8 | uint16(char)
		fbCurentăcol++
	}

}

func textMODTipăreștehex64(număr uint64) {
	textMODTipăreștehex32(uint32(număr >> 32))
	textMODTipăreștehex32(uint32(număr))
}

func textMODTipăreștehex32(număr uint32) {
	textMODTipăreștehex16(uint16(număr >> 16))
	textMODTipăreștehex16(uint16(număr))
}

func textMODTipăreștehex16(număr uint16) {
	textMODTipăreștehex(uint8(număr >> 8))
	textMODTipăreștehex(uint8(număr))
}

func textMODTipăreștehex(număr uint8) {
	textMODTipăreștehexchar(număr >> 4)
	textMODTipăreștehexchar(număr)
}

func textMODTipăreștehexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textMODTipăreștechar(0x30 + n)
	} else {
		textMODTipăreștechar(0x41 + n - 10)
	}
}
