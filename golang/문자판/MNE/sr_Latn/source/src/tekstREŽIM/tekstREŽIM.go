/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstREŽIMwriter struct {
}

func (e tekstREŽIMwriter) Piše(p []byte) (int, error) {
	tekstREŽIMŠtampajBajtova(p)
	return len(p), nil
}

type tekstREŽIMGreškawriter struct {
}

func (e tekstREŽIMGreškawriter) Piše(p []byte) (int, error) {
	tekstREŽIMŠtampajGreškaBajtova(p)
	return len(p), nil
}

const (
	fbŠirina			= 80
	fbVisina			= 25
	fbphysaddress		uintptr	= 0xb8000
	pokazivačVisina			= 1
	pokazivačPokreni		= 11
)

var (
	fbTrenutnored	= 0
	fbTrenutnocol	= 0
)

var fb []uint16

func tekstREŽIMinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠirina * fbVisina,
		Cap:	fbŠirina * fbVisina,
		Data:	fbphysaddress,
	}))

}

func tekstREŽIMuključenoPokazivač() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|pokazivačPokreni)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|pokazivačVisina+pokazivačPokreni)
}

func tekstREŽIMIsključiPokazivač() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstREŽIMOsvežiPokazivač(x int, y int) {
	položaj := y*fbŠirina + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(položaj&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((položaj>>8)&0xFF))
}

func tekstREŽIMflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstREŽIMcheckfbPremesti() {
	for fbTrenutnored >= fbVisina {
		copy(fb[:len(fb)-fbŠirina], fb[fbŠirina:])

		for i := 0; i < fbŠirina; i++ {
			fb[(fbVisina-1)*fbŠirina+i] = 0xf00
		}
		fbTrenutnored--
	}
}

func tekstREŽIMŠtampajcol(s string, atribut uint8) {
	for _, b := range s {
		tekstREŽIMŠtampajcharcol(uint8(b), atribut)
	}
}

func tekstREŽIMprintlncol(s string, atribut uint8) {
	for _, b := range s {
		tekstREŽIMŠtampajcharcol(uint8(b), atribut)
	}
	tekstREŽIMŠtampajchar(0xa)
}

func tekstREŽIMŠtampaj(s string) {
	for _, b := range s {
		tekstREŽIMŠtampajchar(uint8(b))
	}
}

func tekstREŽIMŠtampajBajtova(a []byte) {
	for _, b := range a {
		tekstREŽIMŠtampajchar(uint8(b))
	}
}

func tekstREŽIMŠtampajGreškaBajtova(a []byte) {
	for _, b := range a {
		tekstREŽIMŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstREŽIMprintln(s string) {
	for _, b := range s {
		tekstREŽIMŠtampajchar(uint8(b))
	}
	tekstREŽIMŠtampajchar(0xa)
}

func tekstREŽIMŠtampajGreška(s string) {
	for _, b := range s {
		tekstREŽIMŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstREŽIMŠtampajerrorln(s string) {
	tekstREŽIMŠtampajGreška(s)
	tekstREŽIMŠtampajchar(0xa)
}

func tekstREŽIMŠtampajchar(char uint8) {
	tekstREŽIMŠtampajcharcol(char, 0<<4|0xf)
}

func tekstREŽIMŠtampajcharcol(char uint8, atribut uint8) {
	tekstREŽIMcheckfbPremesti()
	if char == '\n' {
		fbTrenutnored++
		fbTrenutnocol = 0
		tekstREŽIMcheckfbPremesti()
	} else if char == '\b' {
		fb[fbTrenutnocol+fbTrenutnored*fbŠirina] = 0xf00
		fbTrenutnocol = fbTrenutnocol - 1
		if fbTrenutnocol < 0 {
			fbTrenutnocol = 0
		}
	} else if char == '\r' {
		fbTrenutnocol = 0
	} else {
		if fbTrenutnocol >= fbŠirina {
			return
		}
		fb[fbTrenutnocol+fbTrenutnored*fbŠirina] = uint16(atribut)<<8 | uint16(char)
		fbTrenutnocol++
	}

}

func tekstREŽIMŠtampajHeksadecimalno64(broj uint64) {
	tekstREŽIMŠtampajHeksadecimalno32(uint32(broj >> 32))
	tekstREŽIMŠtampajHeksadecimalno32(uint32(broj))
}

func tekstREŽIMŠtampajHeksadecimalno32(broj uint32) {
	tekstREŽIMŠtampajHeksadecimalno16(uint16(broj >> 16))
	tekstREŽIMŠtampajHeksadecimalno16(uint16(broj))
}

func tekstREŽIMŠtampajHeksadecimalno16(broj uint16) {
	tekstREŽIMŠtampajHeksadecimalno(uint8(broj >> 8))
	tekstREŽIMŠtampajHeksadecimalno(uint8(broj))
}

func tekstREŽIMŠtampajHeksadecimalno(broj uint8) {
	tekstREŽIMŠtampajHeksadecimalnochar(broj >> 4)
	tekstREŽIMŠtampajHeksadecimalnochar(broj)
}

func tekstREŽIMŠtampajHeksadecimalnochar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstREŽIMŠtampajchar(0x30 + n)
	} else {
		tekstREŽIMŠtampajchar(0x41 + n - 10)
	}
}
