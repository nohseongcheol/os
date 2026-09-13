package main

import (
	"reflect"
	"unsafe"
)

type نصوضعwriter struct {
}

func (e نصوضعwriter) Wكتابة(p []byte) (int, error) {
	نصوضعاطبعبايت(p)
	return len(p), nil
}

type نصوضعخطأwriter struct {
}

func (e نصوضعخطأwriter) Wكتابة(p []byte) (int, error) {
	نصوضعاطبعخطأبايت(p)
	return len(p), nil
}

const (
	fbالعرض			= 80
	fbالارتفاع		= 25
	fbphysaddress	uintptr	= 0xb8000
	مؤشرالارتفاع		= 1
	مؤشرابدأ		= 11
)

var (
	fbالحاليline	= 0
	fbالحاليcol	= 0
)

var fb []uint16

func نصوضعinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbالعرض * fbالارتفاع,
		Cap:	fbالعرض * fbالارتفاع,
		Data:	fbphysaddress,
	}))

}

func نصوضعenableمؤشر() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|مؤشرابدأ)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|مؤشرالارتفاع+مؤشرابدأ)
}

func نصوضعdisableمؤشر() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func نصوضعupdateمؤشر(x int, y int) {
	الموضع := y*fbالعرض + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(الموضع&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((الموضع>>8)&0xFF))
}

func نصوضعflushشاشة() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func نصوضعcheckfbانقل() {
	for fbالحاليline >= fbالارتفاع {
		copy(fb[:len(fb)-fbالعرض], fb[fbالعرض:])

		for i := 0; i < fbالعرض; i++ {
			fb[(fbالارتفاع-1)*fbالعرض+i] = 0xf00
		}
		fbالحاليline--
	}
}

func نصوضعاطبعcol(s string, خاصية uint8) {
	for _, b := range s {
		نصوضعاطبعcharcol(uint8(b), خاصية)
	}
}

func نصوضعprintlncol(s string, خاصية uint8) {
	for _, b := range s {
		نصوضعاطبعcharcol(uint8(b), خاصية)
	}
	نصوضعاطبعchar(0xa)
}

func نصوضعاطبع(s string) {
	for _, b := range s {
		نصوضعاطبعchar(uint8(b))
	}
}

func نصوضعاطبعبايت(a []byte) {
	for _, b := range a {
		نصوضعاطبعchar(uint8(b))
	}
}

func نصوضعاطبعخطأبايت(a []byte) {
	for _, b := range a {
		نصوضعاطبعcharcol(uint8(b), 4<<4|0xf)
	}
}

func نصوضعprintln(s string) {
	for _, b := range s {
		نصوضعاطبعchar(uint8(b))
	}
	نصوضعاطبعchar(0xa)
}

func نصوضعاطبعخطأ(s string) {
	for _, b := range s {
		نصوضعاطبعcharcol(uint8(b), 4<<4|0xf)
	}
}

func نصوضعاطبعerrorln(s string) {
	نصوضعاطبعخطأ(s)
	نصوضعاطبعchar(0xa)
}

func نصوضعاطبعchar(char uint8) {
	نصوضعاطبعcharcol(char, 0<<4|0xf)
}

func نصوضعاطبعcharcol(char uint8, خاصية uint8) {
	نصوضعcheckfbانقل()
	if char == '\n' {
		fbالحاليline++
		fbالحاليcol = 0
		نصوضعcheckfbانقل()
	} else if char == '\b' {
		fb[fbالحاليcol+fbالحاليline*fbالعرض] = 0xf00
		fbالحاليcol = fbالحاليcol - 1
		if fbالحاليcol < 0 {
			fbالحاليcol = 0
		}
	} else if char == '\r' {
		fbالحاليcol = 0
	} else {
		if fbالحاليcol >= fbالعرض {
			return
		}
		fb[fbالحاليcol+fbالحاليline*fbالعرض] = uint16(خاصية)<<8 | uint16(char)
		fbالحاليcol++
	}

}

func نصوضعاطبعhex64(الأرقام uint64) {
	نصوضعاطبعhex32(uint32(الأرقام >> 32))
	نصوضعاطبعhex32(uint32(الأرقام))
}

func نصوضعاطبعhex32(الأرقام uint32) {
	نصوضعاطبعhex16(uint16(الأرقام >> 16))
	نصوضعاطبعhex16(uint16(الأرقام))
}

func نصوضعاطبعhex16(الأرقام uint16) {
	نصوضعاطبعhex(uint8(الأرقام >> 8))
	نصوضعاطبعhex(uint8(الأرقام))
}

func نصوضعاطبعhex(الأرقام uint8) {
	نصوضعاطبعhexchar(الأرقام >> 4)
	نصوضعاطبعhexchar(الأرقام)
}

func نصوضعاطبعhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		نصوضعاطبعchar(0x30 + n)
	} else {
		نصوضعاطبعchar(0x41 + n - 10)
	}
}
