/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstsRežīmswriter struct {
}

func (e tekstsRežīmswriter) Rakstīt(p []byte) (int, error) {
	tekstsRežīmsDrukātBaiti(p)
	return len(p), nil
}

type tekstsRežīmsKļūdawriter struct {
}

func (e tekstsRežīmsKļūdawriter) Rakstīt(p []byte) (int, error) {
	tekstsRežīmsDrukātKļūdaBaiti(p)
	return len(p), nil
}

const (
	fbPlatums		= 80
	fbAugstums		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorAugstums		= 1
	cursorStartēt		= 11
)

var (
	fbPašreizējaisRinda	= 0
	fbPašreizējaiscol	= 0
)

var fb []uint16

func tekstsRežīmsinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbPlatums * fbAugstums,
		Cap:	fbPlatums * fbAugstums,
		Data:	fbphysaddress,
	}))

}

func tekstsRežīmsIeslēgtcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorStartēt)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorAugstums+cursorStartēt)
}

func tekstsRežīmsIzslēgtcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstsRežīmsAtjauninātcursor(x int, y int) {
	novietojums := y*fbPlatums + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(novietojums&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((novietojums>>8)&0xFF))
}

func tekstsRežīmsflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstsRežīmscheckfbPārvietot() {
	for fbPašreizējaisRinda >= fbAugstums {
		copy(fb[:len(fb)-fbPlatums], fb[fbPlatums:])

		for i := 0; i < fbPlatums; i++ {
			fb[(fbAugstums-1)*fbPlatums+i] = 0xf00
		}
		fbPašreizējaisRinda--
	}
}

func tekstsRežīmsDrukātcol(s string, atribūts uint8) {
	for _, b := range s {
		tekstsRežīmsDrukātcharcol(uint8(b), atribūts)
	}
}

func tekstsRežīmsprintlncol(s string, atribūts uint8) {
	for _, b := range s {
		tekstsRežīmsDrukātcharcol(uint8(b), atribūts)
	}
	tekstsRežīmsDrukātchar(0xa)
}

func tekstsRežīmsDrukāt(s string) {
	for _, b := range s {
		tekstsRežīmsDrukātchar(uint8(b))
	}
}

func tekstsRežīmsDrukātBaiti(a []byte) {
	for _, b := range a {
		tekstsRežīmsDrukātchar(uint8(b))
	}
}

func tekstsRežīmsDrukātKļūdaBaiti(a []byte) {
	for _, b := range a {
		tekstsRežīmsDrukātcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstsRežīmsprintln(s string) {
	for _, b := range s {
		tekstsRežīmsDrukātchar(uint8(b))
	}
	tekstsRežīmsDrukātchar(0xa)
}

func tekstsRežīmsDrukātKļūda(s string) {
	for _, b := range s {
		tekstsRežīmsDrukātcharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstsRežīmsDrukāterrorln(s string) {
	tekstsRežīmsDrukātKļūda(s)
	tekstsRežīmsDrukātchar(0xa)
}

func tekstsRežīmsDrukātchar(char uint8) {
	tekstsRežīmsDrukātcharcol(char, 0<<4|0xf)
}

func tekstsRežīmsDrukātcharcol(char uint8, atribūts uint8) {
	tekstsRežīmscheckfbPārvietot()
	if char == '\n' {
		fbPašreizējaisRinda++
		fbPašreizējaiscol = 0
		tekstsRežīmscheckfbPārvietot()
	} else if char == '\b' {
		fb[fbPašreizējaiscol+fbPašreizējaisRinda*fbPlatums] = 0xf00
		fbPašreizējaiscol = fbPašreizējaiscol - 1
		if fbPašreizējaiscol < 0 {
			fbPašreizējaiscol = 0
		}
	} else if char == '\r' {
		fbPašreizējaiscol = 0
	} else {
		if fbPašreizējaiscol >= fbPlatums {
			return
		}
		fb[fbPašreizējaiscol+fbPašreizējaisRinda*fbPlatums] = uint16(atribūts)<<8 | uint16(char)
		fbPašreizējaiscol++
	}

}

func tekstsRežīmsDrukātHeksa64(skaitlis uint64) {
	tekstsRežīmsDrukātHeksa32(uint32(skaitlis >> 32))
	tekstsRežīmsDrukātHeksa32(uint32(skaitlis))
}

func tekstsRežīmsDrukātHeksa32(skaitlis uint32) {
	tekstsRežīmsDrukātHeksa16(uint16(skaitlis >> 16))
	tekstsRežīmsDrukātHeksa16(uint16(skaitlis))
}

func tekstsRežīmsDrukātHeksa16(skaitlis uint16) {
	tekstsRežīmsDrukātHeksa(uint8(skaitlis >> 8))
	tekstsRežīmsDrukātHeksa(uint8(skaitlis))
}

func tekstsRežīmsDrukātHeksa(skaitlis uint8) {
	tekstsRežīmsDrukātHeksachar(skaitlis >> 4)
	tekstsRežīmsDrukātHeksachar(skaitlis)
}

func tekstsRežīmsDrukātHeksachar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstsRežīmsDrukātchar(0x30 + n)
	} else {
		tekstsRežīmsDrukātchar(0x41 + n - 10)
	}
}
