package main

import (
	"reflect"
	"unsafe"
)

type soratraFombawriter struct {
}

func (e soratraFombawriter) Manoratra(p []byte) (int, error) {
	soratraFombaAtontayOctet(p)
	return len(p), nil
}

type soratraFombaDisowriter struct {
}

func (e soratraFombaDisowriter) Manoratra(p []byte) (int, error) {
	soratraFombaAtontayDisoOctet(p)
	return len(p), nil
}

const (
	fbIndra			= 80
	fbHaavo			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorHaavo		= 1
	cursorAtomboy		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func soratraFombainit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbIndra * fbHaavo,
		Cap:	fbIndra * fbHaavo,
		Data:	fbphysaddress,
	}))

}

func soratraFombaenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorAtomboy)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorHaavo+cursorAtomboy)
}

func soratraFombadisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func soratraFombaAvaozycursor(x int, y int) {
	position := y*fbIndra + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func soratraFombaflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func soratraFombacheckfbAfindrao() {
	for fbcurrentline >= fbHaavo {
		copy(fb[:len(fb)-fbIndra], fb[fbIndra:])

		for i := 0; i < fbIndra; i++ {
			fb[(fbHaavo-1)*fbIndra+i] = 0xf00
		}
		fbcurrentline--
	}
}

func soratraFombaAtontaycol(s string, marikamanokana uint8) {
	for _, b := range s {
		soratraFombaAtontaycharcol(uint8(b), marikamanokana)
	}
}

func soratraFombaprintlncol(s string, marikamanokana uint8) {
	for _, b := range s {
		soratraFombaAtontaycharcol(uint8(b), marikamanokana)
	}
	soratraFombaAtontaychar(0xa)
}

func soratraFombaAtontay(s string) {
	for _, b := range s {
		soratraFombaAtontaychar(uint8(b))
	}
}

func soratraFombaAtontayOctet(a []byte) {
	for _, b := range a {
		soratraFombaAtontaychar(uint8(b))
	}
}

func soratraFombaAtontayDisoOctet(a []byte) {
	for _, b := range a {
		soratraFombaAtontaycharcol(uint8(b), 4<<4|0xf)
	}
}

func soratraFombaprintln(s string) {
	for _, b := range s {
		soratraFombaAtontaychar(uint8(b))
	}
	soratraFombaAtontaychar(0xa)
}

func soratraFombaAtontayDiso(s string) {
	for _, b := range s {
		soratraFombaAtontaycharcol(uint8(b), 4<<4|0xf)
	}
}

func soratraFombaAtontayerrorln(s string) {
	soratraFombaAtontayDiso(s)
	soratraFombaAtontaychar(0xa)
}

func soratraFombaAtontaychar(char uint8) {
	soratraFombaAtontaycharcol(char, 0<<4|0xf)
}

func soratraFombaAtontaycharcol(char uint8, marikamanokana uint8) {
	soratraFombacheckfbAfindrao()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		soratraFombacheckfbAfindrao()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbIndra] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbIndra {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbIndra] = uint16(marikamanokana)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func soratraFombaAtontayhex64(number uint64) {
	soratraFombaAtontayhex32(uint32(number >> 32))
	soratraFombaAtontayhex32(uint32(number))
}

func soratraFombaAtontayhex32(number uint32) {
	soratraFombaAtontayhex16(uint16(number >> 16))
	soratraFombaAtontayhex16(uint16(number))
}

func soratraFombaAtontayhex16(number uint16) {
	soratraFombaAtontayhex(uint8(number >> 8))
	soratraFombaAtontayhex(uint8(number))
}

func soratraFombaAtontayhex(number uint8) {
	soratraFombaAtontayhexchar(number >> 4)
	soratraFombaAtontayhexchar(number)
}

func soratraFombaAtontayhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		soratraFombaAtontaychar(0x30 + n)
	} else {
		soratraFombaAtontaychar(0x41 + n - 10)
	}
}
