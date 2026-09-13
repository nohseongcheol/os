package main

import (
	"reflect"
	"unsafe"
)

type teksttilstandwriter struct {
}

func (e teksttilstandwriter) Skrive(p []byte) (int, error) {
	teksttilstandUdskrivByte(p)
	return len(p), nil
}

type teksttilstandFejlwriter struct {
}

func (e teksttilstandFejlwriter) Skrive(p []byte) (int, error) {
	teksttilstandUdskrivFejlByte(p)
	return len(p), nil
}

const (
	fbBredde		= 80
	fbHøjde			= 25
	fbphysaddress	uintptr	= 0xb8000
	markørHøjde		= 1
	markørBegynd		= 11
)

var (
	fbAktiveLinje	= 0
	fbAktivecol	= 0
)

var fb []uint16

func teksttilstandinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBredde * fbHøjde,
		Cap:	fbBredde * fbHøjde,
		Data:	fbphysaddress,
	}))

}

func teksttilstandAktiverMarkør() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|markørBegynd)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|markørHøjde+markørBegynd)
}

func teksttilstandSlåfraMarkør() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func teksttilstandOpdatérMarkør(x int, y int) {
	placering := y*fbBredde + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(placering&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((placering>>8)&0xFF))
}

func teksttilstandflushSkærm() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func teksttilstandcheckfbFlyt() {
	for fbAktiveLinje >= fbHøjde {
		copy(fb[:len(fb)-fbBredde], fb[fbBredde:])

		for i := 0; i < fbBredde; i++ {
			fb[(fbHøjde-1)*fbBredde+i] = 0xf00
		}
		fbAktiveLinje--
	}
}

func teksttilstandUdskrivcol(s string, egenskab uint8) {
	for _, b := range s {
		teksttilstandUdskrivcharcol(uint8(b), egenskab)
	}
}

func teksttilstandprintlncol(s string, egenskab uint8) {
	for _, b := range s {
		teksttilstandUdskrivcharcol(uint8(b), egenskab)
	}
	teksttilstandUdskrivchar(0xa)
}

func teksttilstandUdskriv(s string) {
	for _, b := range s {
		teksttilstandUdskrivchar(uint8(b))
	}
}

func teksttilstandUdskrivByte(a []byte) {
	for _, b := range a {
		teksttilstandUdskrivchar(uint8(b))
	}
}

func teksttilstandUdskrivFejlByte(a []byte) {
	for _, b := range a {
		teksttilstandUdskrivcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksttilstandprintln(s string) {
	for _, b := range s {
		teksttilstandUdskrivchar(uint8(b))
	}
	teksttilstandUdskrivchar(0xa)
}

func teksttilstandUdskrivFejl(s string) {
	for _, b := range s {
		teksttilstandUdskrivcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksttilstandUdskriverrorln(s string) {
	teksttilstandUdskrivFejl(s)
	teksttilstandUdskrivchar(0xa)
}

func teksttilstandUdskrivchar(char uint8) {
	teksttilstandUdskrivcharcol(char, 0<<4|0xf)
}

func teksttilstandUdskrivcharcol(char uint8, egenskab uint8) {
	teksttilstandcheckfbFlyt()
	if char == '\n' {
		fbAktiveLinje++
		fbAktivecol = 0
		teksttilstandcheckfbFlyt()
	} else if char == '\b' {
		fb[fbAktivecol+fbAktiveLinje*fbBredde] = 0xf00
		fbAktivecol = fbAktivecol - 1
		if fbAktivecol < 0 {
			fbAktivecol = 0
		}
	} else if char == '\r' {
		fbAktivecol = 0
	} else {
		if fbAktivecol >= fbBredde {
			return
		}
		fb[fbAktivecol+fbAktiveLinje*fbBredde] = uint16(egenskab)<<8 | uint16(char)
		fbAktivecol++
	}

}

func teksttilstandUdskrivhex64(tal uint64) {
	teksttilstandUdskrivhex32(uint32(tal >> 32))
	teksttilstandUdskrivhex32(uint32(tal))
}

func teksttilstandUdskrivhex32(tal uint32) {
	teksttilstandUdskrivhex16(uint16(tal >> 16))
	teksttilstandUdskrivhex16(uint16(tal))
}

func teksttilstandUdskrivhex16(tal uint16) {
	teksttilstandUdskrivhex(uint8(tal >> 8))
	teksttilstandUdskrivhex(uint8(tal))
}

func teksttilstandUdskrivhex(tal uint8) {
	teksttilstandUdskrivhexchar(tal >> 4)
	teksttilstandUdskrivhexchar(tal)
}

func teksttilstandUdskrivhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		teksttilstandUdskrivchar(0x30 + n)
	} else {
		teksttilstandUdskrivchar(0x41 + n - 10)
	}
}
