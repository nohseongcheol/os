package main

import (
	"reflect"
	"unsafe"
)

type متنحالتwriter struct {
}

func (e متنحالتwriter) Wنوشتن(p []byte) (int, error) {
	متنحالتچاپبایت(p)
	return len(p), nil
}

type متنحالتخطاwriter struct {
}

func (e متنحالتخطاwriter) Wنوشتن(p []byte) (int, error) {
	متنحالتچاپخطابایت(p)
	return len(p), nil
}

const (
	fbعرض			= 80
	fbارتفاع		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorارتفاع		= 1
	cursorstart		= 11
)

var (
	fbcurrentخط	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func متنحالتinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbعرض * fbارتفاع,
		Cap:	fbعرض * fbارتفاع,
		Data:	fbphysaddress,
	}))

}

func متنحالتenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorارتفاع+cursorstart)
}

func متنحالتغیرفعالکردنcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func متنحالتupdatecursor(x int, y int) {
	position := y*fbعرض + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func متنحالتflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func متنحالتcheckfbانتقال() {
	for fbcurrentخط >= fbارتفاع {
		copy(fb[:len(fb)-fbعرض], fb[fbعرض:])

		for i := 0; i < fbعرض; i++ {
			fb[(fbارتفاع-1)*fbعرض+i] = 0xf00
		}
		fbcurrentخط--
	}
}

func متنحالتچاپcol(s string, مشخصه uint8) {
	for _, b := range s {
		متنحالتچاپcharcol(uint8(b), مشخصه)
	}
}

func متنحالتprintlncol(s string, مشخصه uint8) {
	for _, b := range s {
		متنحالتچاپcharcol(uint8(b), مشخصه)
	}
	متنحالتچاپchar(0xa)
}

func متنحالتچاپ(s string) {
	for _, b := range s {
		متنحالتچاپchar(uint8(b))
	}
}

func متنحالتچاپبایت(a []byte) {
	for _, b := range a {
		متنحالتچاپchar(uint8(b))
	}
}

func متنحالتچاپخطابایت(a []byte) {
	for _, b := range a {
		متنحالتچاپcharcol(uint8(b), 4<<4|0xf)
	}
}

func متنحالتprintln(s string) {
	for _, b := range s {
		متنحالتچاپchar(uint8(b))
	}
	متنحالتچاپchar(0xa)
}

func متنحالتچاپخطا(s string) {
	for _, b := range s {
		متنحالتچاپcharcol(uint8(b), 4<<4|0xf)
	}
}

func متنحالتچاپerrorln(s string) {
	متنحالتچاپخطا(s)
	متنحالتچاپchar(0xa)
}

func متنحالتچاپchar(char uint8) {
	متنحالتچاپcharcol(char, 0<<4|0xf)
}

func متنحالتچاپcharcol(char uint8, مشخصه uint8) {
	متنحالتcheckfbانتقال()
	if char == '\n' {
		fbcurrentخط++
		fbcurrentcol = 0
		متنحالتcheckfbانتقال()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentخط*fbعرض] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbعرض {
			return
		}
		fb[fbcurrentcol+fbcurrentخط*fbعرض] = uint16(مشخصه)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func متنحالتچاپhex64(number uint64) {
	متنحالتچاپhex32(uint32(number >> 32))
	متنحالتچاپhex32(uint32(number))
}

func متنحالتچاپhex32(number uint32) {
	متنحالتچاپhex16(uint16(number >> 16))
	متنحالتچاپhex16(uint16(number))
}

func متنحالتچاپhex16(number uint16) {
	متنحالتچاپhex(uint8(number >> 8))
	متنحالتچاپhex(uint8(number))
}

func متنحالتچاپhex(number uint8) {
	متنحالتچاپhexchar(number >> 4)
	متنحالتچاپhexchar(number)
}

func متنحالتچاپhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		متنحالتچاپchar(0x30 + n)
	} else {
		متنحالتچاپchar(0x41 + n - 10)
	}
}
