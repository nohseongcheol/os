package main

import (
	"reflect"
	"unsafe"
)

type ტექსტირეჟიმიwriter struct {
}

func (e ტექსტირეჟიმიwriter) Wჩაწერა(p []byte) (int, error) {
	ტექსტირეჟიმიბეჭდვაბაიტი(p)
	return len(p), nil
}

type ტექსტირეჟიმიშეცდომაwriter struct {
}

func (e ტექსტირეჟიმიშეცდომაwriter) Wჩაწერა(p []byte) (int, error) {
	ტექსტირეჟიმიბეჭდვაშეცდომაბაიტი(p)
	return len(p), nil
}

const (
	fbსიგანე		= 80
	fbსიმაღლე		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorსიმაღლე		= 1
	cursorstart		= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func ტექსტირეჟიმიinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbსიგანე * fbსიმაღლე,
		Cap:	fbსიგანე * fbსიმაღლე,
		Data:	fbphysaddress,
	}))

}

func ტექსტირეჟიმიenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorსიმაღლე+cursorstart)
}

func ტექსტირეჟიმიdisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func ტექსტირეჟიმიგანახლებაcursor(x int, y int) {
	position := y*fbსიგანე + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func ტექსტირეჟიმიflushეკრანი() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func ტექსტირეჟიმიcheckfbგადაადგილება() {
	for fbcurrentline >= fbსიმაღლე {
		copy(fb[:len(fb)-fbსიგანე], fb[fbსიგანე:])

		for i := 0; i < fbსიგანე; i++ {
			fb[(fbსიმაღლე-1)*fbსიგანე+i] = 0xf00
		}
		fbcurrentline--
	}
}

func ტექსტირეჟიმიბეჭდვაcol(s string, ატრიბუტი uint8) {
	for _, b := range s {
		ტექსტირეჟიმიბეჭდვაcharcol(uint8(b), ატრიბუტი)
	}
}

func ტექსტირეჟიმიprintlncol(s string, ატრიბუტი uint8) {
	for _, b := range s {
		ტექსტირეჟიმიბეჭდვაcharcol(uint8(b), ატრიბუტი)
	}
	ტექსტირეჟიმიბეჭდვაchar(0xa)
}

func ტექსტირეჟიმიბეჭდვა(s string) {
	for _, b := range s {
		ტექსტირეჟიმიბეჭდვაchar(uint8(b))
	}
}

func ტექსტირეჟიმიბეჭდვაბაიტი(a []byte) {
	for _, b := range a {
		ტექსტირეჟიმიბეჭდვაchar(uint8(b))
	}
}

func ტექსტირეჟიმიბეჭდვაშეცდომაბაიტი(a []byte) {
	for _, b := range a {
		ტექსტირეჟიმიბეჭდვაcharcol(uint8(b), 4<<4|0xf)
	}
}

func ტექსტირეჟიმიprintln(s string) {
	for _, b := range s {
		ტექსტირეჟიმიბეჭდვაchar(uint8(b))
	}
	ტექსტირეჟიმიბეჭდვაchar(0xa)
}

func ტექსტირეჟიმიბეჭდვაშეცდომა(s string) {
	for _, b := range s {
		ტექსტირეჟიმიბეჭდვაcharcol(uint8(b), 4<<4|0xf)
	}
}

func ტექსტირეჟიმიბეჭდვაerrorln(s string) {
	ტექსტირეჟიმიბეჭდვაშეცდომა(s)
	ტექსტირეჟიმიბეჭდვაchar(0xa)
}

func ტექსტირეჟიმიბეჭდვაchar(char uint8) {
	ტექსტირეჟიმიბეჭდვაcharcol(char, 0<<4|0xf)
}

func ტექსტირეჟიმიბეჭდვაcharcol(char uint8, ატრიბუტი uint8) {
	ტექსტირეჟიმიcheckfbგადაადგილება()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		ტექსტირეჟიმიcheckfbგადაადგილება()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbსიგანე] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbსიგანე {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbსიგანე] = uint16(ატრიბუტი)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func ტექსტირეჟიმიბეჭდვაhex64(რიცხვი uint64) {
	ტექსტირეჟიმიბეჭდვაhex32(uint32(რიცხვი >> 32))
	ტექსტირეჟიმიბეჭდვაhex32(uint32(რიცხვი))
}

func ტექსტირეჟიმიბეჭდვაhex32(რიცხვი uint32) {
	ტექსტირეჟიმიბეჭდვაhex16(uint16(რიცხვი >> 16))
	ტექსტირეჟიმიბეჭდვაhex16(uint16(რიცხვი))
}

func ტექსტირეჟიმიბეჭდვაhex16(რიცხვი uint16) {
	ტექსტირეჟიმიბეჭდვაhex(uint8(რიცხვი >> 8))
	ტექსტირეჟიმიბეჭდვაhex(uint8(რიცხვი))
}

func ტექსტირეჟიმიბეჭდვაhex(რიცხვი uint8) {
	ტექსტირეჟიმიბეჭდვაhexchar(რიცხვი >> 4)
	ტექსტირეჟიმიბეჭდვაhexchar(რიცხვი)
}

func ტექსტირეჟიმიბეჭდვაhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		ტექსტირეჟიმიბეჭდვაchar(0x30 + n)
	} else {
		ტექსტირეჟიმიბეჭდვაchar(0x41 + n - 10)
	}
}
