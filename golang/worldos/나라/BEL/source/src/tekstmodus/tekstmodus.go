/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstmoduswriter struct {
}

func (e tekstmoduswriter) Schrijven(p []byte) (int, error) {
	tekstmodusAfdrukkenbytes(p)
	return len(p), nil
}

type tekstmodusFoutwriter struct {
}

func (e tekstmodusFoutwriter) Schrijven(p []byte) (int, error) {
	tekstmodusAfdrukkenFoutbytes(p)
	return len(p), nil
}

const (
	fbBreedte			= 80
	fbHoogte			= 25
	fbphysaddress		uintptr	= 0xb8000
	aanwijzerHoogte			= 1
	aanwijzerStarten		= 11
)

var (
	fbHuidigRegel	= 0
	fbHuidigcol	= 0
)

var fb []uint16

func tekstmodusinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBreedte * fbHoogte,
		Cap:	fbBreedte * fbHoogte,
		Data:	fbphysaddress,
	}))

}

func tekstmodusInschakelenAanwijzer() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|aanwijzerStarten)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|aanwijzerHoogte+aanwijzerStarten)
}

func tekstmodusUitschakelenAanwijzer() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstmodusBijwerkenAanwijzer(x int, y int) {
	positie := y*fbBreedte + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(positie&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((positie>>8)&0xFF))
}

func tekstmodusflushScherm() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstmoduscheckfbVerplaatsen() {
	for fbHuidigRegel >= fbHoogte {
		copy(fb[:len(fb)-fbBreedte], fb[fbBreedte:])

		for i := 0; i < fbBreedte; i++ {
			fb[(fbHoogte-1)*fbBreedte+i] = 0xf00
		}
		fbHuidigRegel--
	}
}

func tekstmodusAfdrukkencol(s string, attribuut uint8) {
	for _, b := range s {
		tekstmodusAfdrukkencharcol(uint8(b), attribuut)
	}
}

func tekstmodusprintlncol(s string, attribuut uint8) {
	for _, b := range s {
		tekstmodusAfdrukkencharcol(uint8(b), attribuut)
	}
	tekstmodusAfdrukkenchar(0xa)
}

func tekstmodusAfdrukken(s string) {
	for _, b := range s {
		tekstmodusAfdrukkenchar(uint8(b))
	}
}

func tekstmodusAfdrukkenbytes(a []byte) {
	for _, b := range a {
		tekstmodusAfdrukkenchar(uint8(b))
	}
}

func tekstmodusAfdrukkenFoutbytes(a []byte) {
	for _, b := range a {
		tekstmodusAfdrukkencharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodusprintln(s string) {
	for _, b := range s {
		tekstmodusAfdrukkenchar(uint8(b))
	}
	tekstmodusAfdrukkenchar(0xa)
}

func tekstmodusAfdrukkenFout(s string) {
	for _, b := range s {
		tekstmodusAfdrukkencharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodusAfdrukkenerrorln(s string) {
	tekstmodusAfdrukkenFout(s)
	tekstmodusAfdrukkenchar(0xa)
}

func tekstmodusAfdrukkenchar(char uint8) {
	tekstmodusAfdrukkencharcol(char, 0<<4|0xf)
}

func tekstmodusAfdrukkencharcol(char uint8, attribuut uint8) {
	tekstmoduscheckfbVerplaatsen()
	if char == '\n' {
		fbHuidigRegel++
		fbHuidigcol = 0
		tekstmoduscheckfbVerplaatsen()
	} else if char == '\b' {
		fb[fbHuidigcol+fbHuidigRegel*fbBreedte] = 0xf00
		fbHuidigcol = fbHuidigcol - 1
		if fbHuidigcol < 0 {
			fbHuidigcol = 0
		}
	} else if char == '\r' {
		fbHuidigcol = 0
	} else {
		if fbHuidigcol >= fbBreedte {
			return
		}
		fb[fbHuidigcol+fbHuidigRegel*fbBreedte] = uint16(attribuut)<<8 | uint16(char)
		fbHuidigcol++
	}

}

func tekstmodusAfdrukkenhex64(getal uint64) {
	tekstmodusAfdrukkenhex32(uint32(getal >> 32))
	tekstmodusAfdrukkenhex32(uint32(getal))
}

func tekstmodusAfdrukkenhex32(getal uint32) {
	tekstmodusAfdrukkenhex16(uint16(getal >> 16))
	tekstmodusAfdrukkenhex16(uint16(getal))
}

func tekstmodusAfdrukkenhex16(getal uint16) {
	tekstmodusAfdrukkenhex(uint8(getal >> 8))
	tekstmodusAfdrukkenhex(uint8(getal))
}

func tekstmodusAfdrukkenhex(getal uint8) {
	tekstmodusAfdrukkenhexchar(getal >> 4)
	tekstmodusAfdrukkenhexchar(getal)
}

func tekstmodusAfdrukkenhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstmodusAfdrukkenchar(0x30 + n)
	} else {
		tekstmodusAfdrukkenchar(0x41 + n - 10)
	}
}
