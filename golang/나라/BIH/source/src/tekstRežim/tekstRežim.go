/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstRežimwriter struct {
}

func (e tekstRežimwriter) Piši(p []byte) (int, error) {
	tekstRežimŠtampajBajtova(p)
	return len(p), nil
}

type tekstRežimGreškawriter struct {
}

func (e tekstRežimGreškawriter) Piši(p []byte) (int, error) {
	tekstRežimŠtampajGreškaBajtova(p)
	return len(p), nil
}

const (
	fbŠirina		= 80
	fbVisina		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorVisina		= 1
	cursorstart		= 11
)

var (
	fbcurrentLinija	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func tekstRežiminit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠirina * fbVisina,
		Cap:	fbŠirina * fbVisina,
		Data:	fbphysaddress,
	}))

}

func tekstRežimenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorVisina+cursorstart)
}

func tekstRežimdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstRežimAžurirajcursor(x int, y int) {
	položaj := y*fbŠirina + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(položaj&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((položaj>>8)&0xFF))
}

func tekstRežimflushEkran() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstRežimcheckfbPremjesti() {
	for fbcurrentLinija >= fbVisina {
		copy(fb[:len(fb)-fbŠirina], fb[fbŠirina:])

		for i := 0; i < fbŠirina; i++ {
			fb[(fbVisina-1)*fbŠirina+i] = 0xf00
		}
		fbcurrentLinija--
	}
}

func tekstRežimŠtampajcol(s string, attribute uint8) {
	for _, b := range s {
		tekstRežimŠtampajcharcol(uint8(b), attribute)
	}
}

func tekstRežimprintlncol(s string, attribute uint8) {
	for _, b := range s {
		tekstRežimŠtampajcharcol(uint8(b), attribute)
	}
	tekstRežimŠtampajchar(0xa)
}

func tekstRežimŠtampaj(s string) {
	for _, b := range s {
		tekstRežimŠtampajchar(uint8(b))
	}
}

func tekstRežimŠtampajBajtova(a []byte) {
	for _, b := range a {
		tekstRežimŠtampajchar(uint8(b))
	}
}

func tekstRežimŠtampajGreškaBajtova(a []byte) {
	for _, b := range a {
		tekstRežimŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstRežimprintln(s string) {
	for _, b := range s {
		tekstRežimŠtampajchar(uint8(b))
	}
	tekstRežimŠtampajchar(0xa)
}

func tekstRežimŠtampajGreška(s string) {
	for _, b := range s {
		tekstRežimŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstRežimŠtampajerrorln(s string) {
	tekstRežimŠtampajGreška(s)
	tekstRežimŠtampajchar(0xa)
}

func tekstRežimŠtampajchar(char uint8) {
	tekstRežimŠtampajcharcol(char, 0<<4|0xf)
}

func tekstRežimŠtampajcharcol(char uint8, attribute uint8) {
	tekstRežimcheckfbPremjesti()
	if char == '\n' {
		fbcurrentLinija++
		fbcurrentcol = 0
		tekstRežimcheckfbPremjesti()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentLinija*fbŠirina] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbŠirina {
			return
		}
		fb[fbcurrentcol+fbcurrentLinija*fbŠirina] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func tekstRežimŠtampajhex64(broj uint64) {
	tekstRežimŠtampajhex32(uint32(broj >> 32))
	tekstRežimŠtampajhex32(uint32(broj))
}

func tekstRežimŠtampajhex32(broj uint32) {
	tekstRežimŠtampajhex16(uint16(broj >> 16))
	tekstRežimŠtampajhex16(uint16(broj))
}

func tekstRežimŠtampajhex16(broj uint16) {
	tekstRežimŠtampajhex(uint8(broj >> 8))
	tekstRežimŠtampajhex(uint8(broj))
}

func tekstRežimŠtampajhex(broj uint8) {
	tekstRežimŠtampajhexchar(broj >> 4)
	tekstRežimŠtampajhexchar(broj)
}

func tekstRežimŠtampajhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstRežimŠtampajchar(0x30 + n)
	} else {
		tekstRežimŠtampajchar(0x41 + n - 10)
	}
}
