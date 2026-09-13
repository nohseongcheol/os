package main

import (
	"reflect"
	"unsafe"
)

type spracovanietexturežimwriter struct {
}

func (e spracovanietexturežimwriter) Zápis(p []byte) (int, error) {
	spracovanietexturežimTlačiťBajty(p)
	return len(p), nil
}

type spracovanietexturežimChybawriter struct {
}

func (e spracovanietexturežimChybawriter) Zápis(p []byte) (int, error) {
	spracovanietexturežimTlačiťChybaBajty(p)
	return len(p), nil
}

const (
	fbŠírka			= 80
	fbVýška			= 25
	fbphysaddress	uintptr	= 0xb8000
	kurzorVýška		= 1
	kurzorSpustiť		= 11
)

var (
	fbAktuálnyRiadok	= 0
	fbAktuálnycol		= 0
)

var fb []uint16

func spracovanietexturežiminit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠírka * fbVýška,
		Cap:	fbŠírka * fbVýška,
		Data:	fbphysaddress,
	}))

}

func spracovanietexturežimPovoliťKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kurzorSpustiť)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kurzorVýška+kurzorSpustiť)
}

func spracovanietexturežimZakázaťKurzor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func spracovanietexturežimAktualizovaťKurzor(x int, y int) {
	pozícia := y*fbŠírka + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozícia&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozícia>>8)&0xFF))
}

func spracovanietexturežimflushObrazovka() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func spracovanietexturežimcheckfbPresunúť() {
	for fbAktuálnyRiadok >= fbVýška {
		copy(fb[:len(fb)-fbŠírka], fb[fbŠírka:])

		for i := 0; i < fbŠírka; i++ {
			fb[(fbVýška-1)*fbŠírka+i] = 0xf00
		}
		fbAktuálnyRiadok--
	}
}

func spracovanietexturežimTlačiťcol(s string, vlastnosť uint8) {
	for _, b := range s {
		spracovanietexturežimTlačiťcharcol(uint8(b), vlastnosť)
	}
}

func spracovanietexturežimprintlncol(s string, vlastnosť uint8) {
	for _, b := range s {
		spracovanietexturežimTlačiťcharcol(uint8(b), vlastnosť)
	}
	spracovanietexturežimTlačiťchar(0xa)
}

func spracovanietexturežimTlačiť(s string) {
	for _, b := range s {
		spracovanietexturežimTlačiťchar(uint8(b))
	}
}

func spracovanietexturežimTlačiťBajty(a []byte) {
	for _, b := range a {
		spracovanietexturežimTlačiťchar(uint8(b))
	}
}

func spracovanietexturežimTlačiťChybaBajty(a []byte) {
	for _, b := range a {
		spracovanietexturežimTlačiťcharcol(uint8(b), 4<<4|0xf)
	}
}

func spracovanietexturežimprintln(s string) {
	for _, b := range s {
		spracovanietexturežimTlačiťchar(uint8(b))
	}
	spracovanietexturežimTlačiťchar(0xa)
}

func spracovanietexturežimTlačiťChyba(s string) {
	for _, b := range s {
		spracovanietexturežimTlačiťcharcol(uint8(b), 4<<4|0xf)
	}
}

func spracovanietexturežimTlačiťerrorln(s string) {
	spracovanietexturežimTlačiťChyba(s)
	spracovanietexturežimTlačiťchar(0xa)
}

func spracovanietexturežimTlačiťchar(char uint8) {
	spracovanietexturežimTlačiťcharcol(char, 0<<4|0xf)
}

func spracovanietexturežimTlačiťcharcol(char uint8, vlastnosť uint8) {
	spracovanietexturežimcheckfbPresunúť()
	if char == '\n' {
		fbAktuálnyRiadok++
		fbAktuálnycol = 0
		spracovanietexturežimcheckfbPresunúť()
	} else if char == '\b' {
		fb[fbAktuálnycol+fbAktuálnyRiadok*fbŠírka] = 0xf00
		fbAktuálnycol = fbAktuálnycol - 1
		if fbAktuálnycol < 0 {
			fbAktuálnycol = 0
		}
	} else if char == '\r' {
		fbAktuálnycol = 0
	} else {
		if fbAktuálnycol >= fbŠírka {
			return
		}
		fb[fbAktuálnycol+fbAktuálnyRiadok*fbŠírka] = uint16(vlastnosť)<<8 | uint16(char)
		fbAktuálnycol++
	}

}

func spracovanietexturežimTlačiťŠestnástkové64(číslo uint64) {
	spracovanietexturežimTlačiťŠestnástkové32(uint32(číslo >> 32))
	spracovanietexturežimTlačiťŠestnástkové32(uint32(číslo))
}

func spracovanietexturežimTlačiťŠestnástkové32(číslo uint32) {
	spracovanietexturežimTlačiťŠestnástkové16(uint16(číslo >> 16))
	spracovanietexturežimTlačiťŠestnástkové16(uint16(číslo))
}

func spracovanietexturežimTlačiťŠestnástkové16(číslo uint16) {
	spracovanietexturežimTlačiťŠestnástkové(uint8(číslo >> 8))
	spracovanietexturežimTlačiťŠestnástkové(uint8(číslo))
}

func spracovanietexturežimTlačiťŠestnástkové(číslo uint8) {
	spracovanietexturežimTlačiťŠestnástkovéchar(číslo >> 4)
	spracovanietexturežimTlačiťŠestnástkovéchar(číslo)
}

func spracovanietexturežimTlačiťŠestnástkovéchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		spracovanietexturežimTlačiťchar(0x30 + n)
	} else {
		spracovanietexturežimTlačiťchar(0x41 + n - 10)
	}
}
