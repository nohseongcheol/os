package main

import (
	"reflect"
	"unsafe"
)

type tekstmoduswriter struct {
}

func (e tekstmoduswriter) Skriv(p []byte) (int, error) {
	tekstmodusSkrivutByte(p)
	return len(p), nil
}

type tekstmodusFeilwriter struct {
}

func (e tekstmodusFeilwriter) Skriv(p []byte) (int, error) {
	tekstmodusSkrivutFeilByte(p)
	return len(p), nil
}

const (
	fbBredde		= 80
	fbHøyde			= 25
	fbphysaddress	uintptr	= 0xb8000
	pekerHøyde		= 1
	pekerstart		= 11
)

var (
	fbGjeldendeLinje	= 0
	fbGjeldendecol		= 0
)

var fb []uint16

func tekstmodusinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBredde * fbHøyde,
		Cap:	fbBredde * fbHøyde,
		Data:	fbphysaddress,
	}))

}

func tekstmodusSlåpåPeker() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|pekerstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|pekerHøyde+pekerstart)
}

func tekstmodusSlåavPeker() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstmodusOppdaterPeker(x int, y int) {
	posisjon := y*fbBredde + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posisjon&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posisjon>>8)&0xFF))
}

func tekstmodusflushSkjerm() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstmoduscheckfbFlytt() {
	for fbGjeldendeLinje >= fbHøyde {
		copy(fb[:len(fb)-fbBredde], fb[fbBredde:])

		for i := 0; i < fbBredde; i++ {
			fb[(fbHøyde-1)*fbBredde+i] = 0xf00
		}
		fbGjeldendeLinje--
	}
}

func tekstmodusSkrivutcol(s string, egenskap uint8) {
	for _, b := range s {
		tekstmodusSkrivutcharcol(uint8(b), egenskap)
	}
}

func tekstmodusprintlncol(s string, egenskap uint8) {
	for _, b := range s {
		tekstmodusSkrivutcharcol(uint8(b), egenskap)
	}
	tekstmodusSkrivutchar(0xa)
}

func tekstmodusSkrivut(s string) {
	for _, b := range s {
		tekstmodusSkrivutchar(uint8(b))
	}
}

func tekstmodusSkrivutByte(a []byte) {
	for _, b := range a {
		tekstmodusSkrivutchar(uint8(b))
	}
}

func tekstmodusSkrivutFeilByte(a []byte) {
	for _, b := range a {
		tekstmodusSkrivutcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodusprintln(s string) {
	for _, b := range s {
		tekstmodusSkrivutchar(uint8(b))
	}
	tekstmodusSkrivutchar(0xa)
}

func tekstmodusSkrivutFeil(s string) {
	for _, b := range s {
		tekstmodusSkrivutcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstmodusSkrivuterrorln(s string) {
	tekstmodusSkrivutFeil(s)
	tekstmodusSkrivutchar(0xa)
}

func tekstmodusSkrivutchar(char uint8) {
	tekstmodusSkrivutcharcol(char, 0<<4|0xf)
}

func tekstmodusSkrivutcharcol(char uint8, egenskap uint8) {
	tekstmoduscheckfbFlytt()
	if char == '\n' {
		fbGjeldendeLinje++
		fbGjeldendecol = 0
		tekstmoduscheckfbFlytt()
	} else if char == '\b' {
		fb[fbGjeldendecol+fbGjeldendeLinje*fbBredde] = 0xf00
		fbGjeldendecol = fbGjeldendecol - 1
		if fbGjeldendecol < 0 {
			fbGjeldendecol = 0
		}
	} else if char == '\r' {
		fbGjeldendecol = 0
	} else {
		if fbGjeldendecol >= fbBredde {
			return
		}
		fb[fbGjeldendecol+fbGjeldendeLinje*fbBredde] = uint16(egenskap)<<8 | uint16(char)
		fbGjeldendecol++
	}

}

func tekstmodusSkrivutHeksadesimal64(tall uint64) {
	tekstmodusSkrivutHeksadesimal32(uint32(tall >> 32))
	tekstmodusSkrivutHeksadesimal32(uint32(tall))
}

func tekstmodusSkrivutHeksadesimal32(tall uint32) {
	tekstmodusSkrivutHeksadesimal16(uint16(tall >> 16))
	tekstmodusSkrivutHeksadesimal16(uint16(tall))
}

func tekstmodusSkrivutHeksadesimal16(tall uint16) {
	tekstmodusSkrivutHeksadesimal(uint8(tall >> 8))
	tekstmodusSkrivutHeksadesimal(uint8(tall))
}

func tekstmodusSkrivutHeksadesimal(tall uint8) {
	tekstmodusSkrivutHeksadesimalchar(tall >> 4)
	tekstmodusSkrivutHeksadesimalchar(tall)
}

func tekstmodusSkrivutHeksadesimalchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstmodusSkrivutchar(0x30 + n)
	} else {
		tekstmodusSkrivutchar(0x41 + n - 10)
	}
}
