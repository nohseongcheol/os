package main

import (
	"reflect"
	"unsafe"
)

type tekstimënyrëwriter struct {
}

func (e tekstimënyrëwriter) Shkrimi(p []byte) (int, error) {
	tekstimënyrëPrintobytes(p)
	return len(p), nil
}

type tekstimënyrëGabimwriter struct {
}

func (e tekstimënyrëGabimwriter) Shkrimi(p []byte) (int, error) {
	tekstimënyrëPrintoGabimbytes(p)
	return len(p), nil
}

const (
	fbGjerësia		= 80
	fbLartësia		= 25
	fbphysaddress	uintptr	= 0xb8000
	kursorLartësia		= 1
	kursorFillo		= 11
)

var (
	fbEtanishmeline	= 0
	fbEtanishmecol	= 0
)

var fb []uint16

func tekstimënyrëinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbGjerësia * fbLartësia,
		Cap:	fbGjerësia * fbLartësia,
		Data:	fbphysaddress,
	}))

}

func tekstimënyrëenableKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kursorFillo)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kursorLartësia+kursorFillo)
}

func tekstimënyrëdisableKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstimënyrëPërditësoKursor(x int, y int) {
	pozicion := y*fbGjerësia + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozicion&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozicion>>8)&0xFF))
}

func tekstimënyrëflushRojeEkrani() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstimënyrëcheckfbLëviz() {
	for fbEtanishmeline >= fbLartësia {
		copy(fb[:len(fb)-fbGjerësia], fb[fbGjerësia:])

		for i := 0; i < fbGjerësia; i++ {
			fb[(fbLartësia-1)*fbGjerësia+i] = 0xf00
		}
		fbEtanishmeline--
	}
}

func tekstimënyrëPrintocol(s string, karakteristika uint8) {
	for _, b := range s {
		tekstimënyrëPrintocharcol(uint8(b), karakteristika)
	}
}

func tekstimënyrëprintlncol(s string, karakteristika uint8) {
	for _, b := range s {
		tekstimënyrëPrintocharcol(uint8(b), karakteristika)
	}
	tekstimënyrëPrintochar(0xa)
}

func tekstimënyrëPrinto(s string) {
	for _, b := range s {
		tekstimënyrëPrintochar(uint8(b))
	}
}

func tekstimënyrëPrintobytes(a []byte) {
	for _, b := range a {
		tekstimënyrëPrintochar(uint8(b))
	}
}

func tekstimënyrëPrintoGabimbytes(a []byte) {
	for _, b := range a {
		tekstimënyrëPrintocharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstimënyrëprintln(s string) {
	for _, b := range s {
		tekstimënyrëPrintochar(uint8(b))
	}
	tekstimënyrëPrintochar(0xa)
}

func tekstimënyrëPrintoGabim(s string) {
	for _, b := range s {
		tekstimënyrëPrintocharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstimënyrëPrintoerrorln(s string) {
	tekstimënyrëPrintoGabim(s)
	tekstimënyrëPrintochar(0xa)
}

func tekstimënyrëPrintochar(char uint8) {
	tekstimënyrëPrintocharcol(char, 0<<4|0xf)
}

func tekstimënyrëPrintocharcol(char uint8, karakteristika uint8) {
	tekstimënyrëcheckfbLëviz()
	if char == '\n' {
		fbEtanishmeline++
		fbEtanishmecol = 0
		tekstimënyrëcheckfbLëviz()
	} else if char == '\b' {
		fb[fbEtanishmecol+fbEtanishmeline*fbGjerësia] = 0xf00
		fbEtanishmecol = fbEtanishmecol - 1
		if fbEtanishmecol < 0 {
			fbEtanishmecol = 0
		}
	} else if char == '\r' {
		fbEtanishmecol = 0
	} else {
		if fbEtanishmecol >= fbGjerësia {
			return
		}
		fb[fbEtanishmecol+fbEtanishmeline*fbGjerësia] = uint16(karakteristika)<<8 | uint16(char)
		fbEtanishmecol++
	}

}

func tekstimënyrëPrintohex64(number uint64) {
	tekstimënyrëPrintohex32(uint32(number >> 32))
	tekstimënyrëPrintohex32(uint32(number))
}

func tekstimënyrëPrintohex32(number uint32) {
	tekstimënyrëPrintohex16(uint16(number >> 16))
	tekstimënyrëPrintohex16(uint16(number))
}

func tekstimënyrëPrintohex16(number uint16) {
	tekstimënyrëPrintohex(uint8(number >> 8))
	tekstimënyrëPrintohex(uint8(number))
}

func tekstimënyrëPrintohex(number uint8) {
	tekstimënyrëPrintohexchar(number >> 4)
	tekstimënyrëPrintohexchar(number)
}

func tekstimënyrëPrintohexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstimënyrëPrintochar(0x30 + n)
	} else {
		tekstimënyrëPrintochar(0x41 + n - 10)
	}
}
