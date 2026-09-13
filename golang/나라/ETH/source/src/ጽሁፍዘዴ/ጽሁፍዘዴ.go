package main

import (
	"reflect"
	"unsafe"
)

type ጽሁፍዘዴwriter struct {
}

func (e ጽሁፍዘዴwriter) Wመጻፊያ(p []byte) (int, error) {
	ጽሁፍዘዴማተሚያባይትስ(p)
	return len(p), nil
}

type ጽሁፍዘዴስህተትwriter struct {
}

func (e ጽሁፍዘዴስህተትwriter) Wመጻፊያ(p []byte) (int, error) {
	ጽሁፍዘዴማተሚያስህተትባይትስ(p)
	return len(p), nil
}

const (
	fbስፋት			= 80
	fbእርዝመት			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorእርዝመት		= 1
	cursorማስጀመሪያ		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func ጽሁፍዘዴinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbስፋት * fbእርዝመት,
		Cap:	fbስፋት * fbእርዝመት,
		Data:	fbphysaddress,
	}))

}

func ጽሁፍዘዴአስቻለcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorማስጀመሪያ)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorእርዝመት+cursorማስጀመሪያ)
}

func ጽሁፍዘዴአበላሽcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func ጽሁፍዘዴማሻሻያcursor(x int, y int) {
	አካባቢ_2 := y*fbስፋት + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(አካባቢ_2&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((አካባቢ_2>>8)&0xFF))
}

func ጽሁፍዘዴflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func ጽሁፍዘዴcheckfbመንቀሳቅስ() {
	for fbcurrentline >= fbእርዝመት {
		copy(fb[:len(fb)-fbስፋት], fb[fbስፋት:])

		for i := 0; i < fbስፋት; i++ {
			fb[(fbእርዝመት-1)*fbስፋት+i] = 0xf00
		}
		fbcurrentline--
	}
}

func ጽሁፍዘዴማተሚያcol(s string, መለያ uint8) {
	for _, b := range s {
		ጽሁፍዘዴማተሚያcharcol(uint8(b), መለያ)
	}
}

func ጽሁፍዘዴprintlncol(s string, መለያ uint8) {
	for _, b := range s {
		ጽሁፍዘዴማተሚያcharcol(uint8(b), መለያ)
	}
	ጽሁፍዘዴማተሚያchar(0xa)
}

func ጽሁፍዘዴማተሚያ(s string) {
	for _, b := range s {
		ጽሁፍዘዴማተሚያchar(uint8(b))
	}
}

func ጽሁፍዘዴማተሚያባይትስ(a []byte) {
	for _, b := range a {
		ጽሁፍዘዴማተሚያchar(uint8(b))
	}
}

func ጽሁፍዘዴማተሚያስህተትባይትስ(a []byte) {
	for _, b := range a {
		ጽሁፍዘዴማተሚያcharcol(uint8(b), 4<<4|0xf)
	}
}

func ጽሁፍዘዴprintln(s string) {
	for _, b := range s {
		ጽሁፍዘዴማተሚያchar(uint8(b))
	}
	ጽሁፍዘዴማተሚያchar(0xa)
}

func ጽሁፍዘዴማተሚያስህተት(s string) {
	for _, b := range s {
		ጽሁፍዘዴማተሚያcharcol(uint8(b), 4<<4|0xf)
	}
}

func ጽሁፍዘዴማተሚያerrorln(s string) {
	ጽሁፍዘዴማተሚያስህተት(s)
	ጽሁፍዘዴማተሚያchar(0xa)
}

func ጽሁፍዘዴማተሚያchar(char uint8) {
	ጽሁፍዘዴማተሚያcharcol(char, 0<<4|0xf)
}

func ጽሁፍዘዴማተሚያcharcol(char uint8, መለያ uint8) {
	ጽሁፍዘዴcheckfbመንቀሳቅስ()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		ጽሁፍዘዴcheckfbመንቀሳቅስ()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbስፋት] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbስፋት {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbስፋት] = uint16(መለያ)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func ጽሁፍዘዴማተሚያhex64(ቁጥር uint64) {
	ጽሁፍዘዴማተሚያhex32(uint32(ቁጥር >> 32))
	ጽሁፍዘዴማተሚያhex32(uint32(ቁጥር))
}

func ጽሁፍዘዴማተሚያhex32(ቁጥር uint32) {
	ጽሁፍዘዴማተሚያhex16(uint16(ቁጥር >> 16))
	ጽሁፍዘዴማተሚያhex16(uint16(ቁጥር))
}

func ጽሁፍዘዴማተሚያhex16(ቁጥር uint16) {
	ጽሁፍዘዴማተሚያhex(uint8(ቁጥር >> 8))
	ጽሁፍዘዴማተሚያhex(uint8(ቁጥር))
}

func ጽሁፍዘዴማተሚያhex(ቁጥር uint8) {
	ጽሁፍዘዴማተሚያhexchar(ቁጥር >> 4)
	ጽሁፍዘዴማተሚያhexchar(ቁጥር)
}

func ጽሁፍዘዴማተሚያhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		ጽሁፍዘዴማተሚያchar(0x30 + n)
	} else {
		ጽሁፍዘዴማተሚያchar(0x41 + n - 10)
	}
}
