/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type տեքստՌեժիմwriter struct {
}

func (e տեքստՌեժիմwriter) Գրել(p []byte) (int, error) {
	տեքստՌեժիմՏպելԲայթեր(p)
	return len(p), nil
}

type տեքստՌեժիմՍխալwriter struct {
}

func (e տեքստՌեժիմՍխալwriter) Գրել(p []byte) (int, error) {
	տեքստՌեժիմՏպելՍխալԲայթեր(p)
	return len(p), nil
}

const (
	fbԼայնություն			= 80
	fbԲարձրություն			= 25
	fbphysaddress		uintptr	= 0xb8000
	cursorԲարձրություն		= 1
	cursorՍկիզբ			= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func տեքստՌեժիմinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbԼայնություն * fbԲարձրություն,
		Cap:	fbԼայնություն * fbԲարձրություն,
		Data:	fbphysaddress,
	}))

}

func տեքստՌեժիմenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorՍկիզբ)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorԲարձրություն+cursorՍկիզբ)
}

func տեքստՌեժիմdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func տեքստՌեժիմՆորացնելcursor(x int, y int) {
	դիրք := y*fbԼայնություն + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(դիրք&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((դիրք>>8)&0xFF))
}

func տեքստՌեժիմflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func տեքստՌեժիմcheckfbՏեղաշարժել() {
	for fbcurrentline >= fbԲարձրություն {
		copy(fb[:len(fb)-fbԼայնություն], fb[fbԼայնություն:])

		for i := 0; i < fbԼայնություն; i++ {
			fb[(fbԲարձրություն-1)*fbԼայնություն+i] = 0xf00
		}
		fbcurrentline--
	}
}

func տեքստՌեժիմՏպելcol(s string, ատրիբուտ uint8) {
	for _, b := range s {
		տեքստՌեժիմՏպելcharcol(uint8(b), ատրիբուտ)
	}
}

func տեքստՌեժիմprintlncol(s string, ատրիբուտ uint8) {
	for _, b := range s {
		տեքստՌեժիմՏպելcharcol(uint8(b), ատրիբուտ)
	}
	տեքստՌեժիմՏպելchar(0xa)
}

func տեքստՌեժիմՏպել(s string) {
	for _, b := range s {
		տեքստՌեժիմՏպելchar(uint8(b))
	}
}

func տեքստՌեժիմՏպելԲայթեր(a []byte) {
	for _, b := range a {
		տեքստՌեժիմՏպելchar(uint8(b))
	}
}

func տեքստՌեժիմՏպելՍխալԲայթեր(a []byte) {
	for _, b := range a {
		տեքստՌեժիմՏպելcharcol(uint8(b), 4<<4|0xf)
	}
}

func տեքստՌեժիմprintln(s string) {
	for _, b := range s {
		տեքստՌեժիմՏպելchar(uint8(b))
	}
	տեքստՌեժիմՏպելchar(0xa)
}

func տեքստՌեժիմՏպելՍխալ(s string) {
	for _, b := range s {
		տեքստՌեժիմՏպելcharcol(uint8(b), 4<<4|0xf)
	}
}

func տեքստՌեժիմՏպելerrorln(s string) {
	տեքստՌեժիմՏպելՍխալ(s)
	տեքստՌեժիմՏպելchar(0xa)
}

func տեքստՌեժիմՏպելchar(char uint8) {
	տեքստՌեժիմՏպելcharcol(char, 0<<4|0xf)
}

func տեքստՌեժիմՏպելcharcol(char uint8, ատրիբուտ uint8) {
	տեքստՌեժիմcheckfbՏեղաշարժել()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		տեքստՌեժիմcheckfbՏեղաշարժել()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbԼայնություն] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbԼայնություն {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbԼայնություն] = uint16(ատրիբուտ)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func տեքստՌեժիմՏպելhex64(հԱՄԱՐ uint64) {
	տեքստՌեժիմՏպելhex32(uint32(հԱՄԱՐ >> 32))
	տեքստՌեժիմՏպելhex32(uint32(հԱՄԱՐ))
}

func տեքստՌեժիմՏպելhex32(հԱՄԱՐ uint32) {
	տեքստՌեժիմՏպելhex16(uint16(հԱՄԱՐ >> 16))
	տեքստՌեժիմՏպելhex16(uint16(հԱՄԱՐ))
}

func տեքստՌեժիմՏպելhex16(հԱՄԱՐ uint16) {
	տեքստՌեժիմՏպելhex(uint8(հԱՄԱՐ >> 8))
	տեքստՌեժիմՏպելhex(uint8(հԱՄԱՐ))
}

func տեքստՌեժիմՏպելhex(հԱՄԱՐ uint8) {
	տեքստՌեժիմՏպելhexchar(հԱՄԱՐ >> 4)
	տեքստՌեժիմՏպելhexchar(հԱՄԱՐ)
}

func տեքստՌեժիմՏպելhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		տեքստՌեժիմՏպելchar(0x30 + n)
	} else {
		տեքստՌեժիմՏպելchar(0x41 + n - 10)
	}
}
