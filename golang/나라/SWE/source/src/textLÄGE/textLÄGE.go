package main

import (
	"reflect"
	"unsafe"
)

type textLÄGEwriter struct {
}

func (e textLÄGEwriter) Skriv(p []byte) (int, error) {
	textLÄGESkrivutByte(p)
	return len(p), nil
}

type textLÄGEFelwriter struct {
}

func (e textLÄGEFelwriter) Skriv(p []byte) (int, error) {
	textLÄGESkrivutFelByte(p)
	return len(p), nil
}

const (
	fbBredd			= 80
	fbHöjd			= 25
	fbphysAdress	uintptr	= 0xb8000
	markörHöjd		= 1
	markörStarta		= 11
)

var (
	fbAktuellRad	= 0
	fbAktuellcol	= 0
)

var fb []uint16

func textLÄGEinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBredd * fbHöjd,
		Cap:	fbBredd * fbHöjd,
		Data:	fbphysAdress,
	}))

}

func textLÄGEAktiveraMarkör() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|markörStarta)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|markörHöjd+markörStarta)
}

func textLÄGEAvaktiveraMarkör() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textLÄGEUppdateraMarkör(x int, y int) {
	position := y*fbBredd + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func textLÄGEflushSkärm() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textLÄGEcheckfbFlytta() {
	for fbAktuellRad >= fbHöjd {
		copy(fb[:len(fb)-fbBredd], fb[fbBredd:])

		for i := 0; i < fbBredd; i++ {
			fb[(fbHöjd-1)*fbBredd+i] = 0xf00
		}
		fbAktuellRad--
	}
}

func textLÄGESkrivutcol(s string, attribut uint8) {
	for _, b := range s {
		textLÄGESkrivutcharcol(uint8(b), attribut)
	}
}

func textLÄGEprintlncol(s string, attribut uint8) {
	for _, b := range s {
		textLÄGESkrivutcharcol(uint8(b), attribut)
	}
	textLÄGESkrivutchar(0xa)
}

func textLÄGESkrivut(s string) {
	for _, b := range s {
		textLÄGESkrivutchar(uint8(b))
	}
}

func textLÄGESkrivutByte(a []byte) {
	for _, b := range a {
		textLÄGESkrivutchar(uint8(b))
	}
}

func textLÄGESkrivutFelByte(a []byte) {
	for _, b := range a {
		textLÄGESkrivutcharcol(uint8(b), 4<<4|0xf)
	}
}

func textLÄGEprintln(s string) {
	for _, b := range s {
		textLÄGESkrivutchar(uint8(b))
	}
	textLÄGESkrivutchar(0xa)
}

func textLÄGESkrivutFel(s string) {
	for _, b := range s {
		textLÄGESkrivutcharcol(uint8(b), 4<<4|0xf)
	}
}

func textLÄGESkrivuterrorln(s string) {
	textLÄGESkrivutFel(s)
	textLÄGESkrivutchar(0xa)
}

func textLÄGESkrivutchar(char uint8) {
	textLÄGESkrivutcharcol(char, 0<<4|0xf)
}

func textLÄGESkrivutcharcol(char uint8, attribut uint8) {
	textLÄGEcheckfbFlytta()
	if char == '\n' {
		fbAktuellRad++
		fbAktuellcol = 0
		textLÄGEcheckfbFlytta()
	} else if char == '\b' {
		fb[fbAktuellcol+fbAktuellRad*fbBredd] = 0xf00
		fbAktuellcol = fbAktuellcol - 1
		if fbAktuellcol < 0 {
			fbAktuellcol = 0
		}
	} else if char == '\r' {
		fbAktuellcol = 0
	} else {
		if fbAktuellcol >= fbBredd {
			return
		}
		fb[fbAktuellcol+fbAktuellRad*fbBredd] = uint16(attribut)<<8 | uint16(char)
		fbAktuellcol++
	}

}

func textLÄGESkrivutHexadecimalt64(nummer uint64) {
	textLÄGESkrivutHexadecimalt32(uint32(nummer >> 32))
	textLÄGESkrivutHexadecimalt32(uint32(nummer))
}

func textLÄGESkrivutHexadecimalt32(nummer uint32) {
	textLÄGESkrivutHexadecimalt16(uint16(nummer >> 16))
	textLÄGESkrivutHexadecimalt16(uint16(nummer))
}

func textLÄGESkrivutHexadecimalt16(nummer uint16) {
	textLÄGESkrivutHexadecimalt(uint8(nummer >> 8))
	textLÄGESkrivutHexadecimalt(uint8(nummer))
}

func textLÄGESkrivutHexadecimalt(nummer uint8) {
	textLÄGESkrivutHexadecimaltchar(nummer >> 4)
	textLÄGESkrivutHexadecimaltchar(nummer)
}

func textLÄGESkrivutHexadecimaltchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textLÄGESkrivutchar(0x30 + n)
	} else {
		textLÄGESkrivutchar(0x41 + n - 10)
	}
}
