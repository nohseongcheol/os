/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textiHAMURwriter struct {
}

func (e textiHAMURwriter) Skrift(p []byte) (int, error) {
	textiHAMURPrentaBæti(p)
	return len(p), nil
}

type textiHAMURVillawriter struct {
}

func (e textiHAMURVillawriter) Skrift(p []byte) (int, error) {
	textiHAMURPrentaVillaBæti(p)
	return len(p), nil
}

const (
	fbBreidd		= 80
	fbHæð			= 25
	fbphysaddress	uintptr	= 0xb8000
	bendillHæð		= 1
	bendillRæsa		= 11
)

var (
	fbNúverandiLína	= 0
	fbNúverandicol	= 0
)

var fb []uint16

func textiHAMURinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBreidd * fbHæð,
		Cap:	fbBreidd * fbHæð,
		Data:	fbphysaddress,
	}))

}

func textiHAMURenableBendill() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|bendillRæsa)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|bendillHæð+bendillRæsa)
}

func textiHAMURAfvirkjaBendill() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textiHAMURUppfæraBendill(x int, y int) {
	staða := y*fbBreidd + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(staða&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((staða>>8)&0xFF))
}

func textiHAMURflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textiHAMURcheckfbFæra() {
	for fbNúverandiLína >= fbHæð {
		copy(fb[:len(fb)-fbBreidd], fb[fbBreidd:])

		for i := 0; i < fbBreidd; i++ {
			fb[(fbHæð-1)*fbBreidd+i] = 0xf00
		}
		fbNúverandiLína--
	}
}

func textiHAMURPrentacol(s string, eigindi uint8) {
	for _, b := range s {
		textiHAMURPrentacharcol(uint8(b), eigindi)
	}
}

func textiHAMURprintlncol(s string, eigindi uint8) {
	for _, b := range s {
		textiHAMURPrentacharcol(uint8(b), eigindi)
	}
	textiHAMURPrentachar(0xa)
}

func textiHAMURPrenta(s string) {
	for _, b := range s {
		textiHAMURPrentachar(uint8(b))
	}
}

func textiHAMURPrentaBæti(a []byte) {
	for _, b := range a {
		textiHAMURPrentachar(uint8(b))
	}
}

func textiHAMURPrentaVillaBæti(a []byte) {
	for _, b := range a {
		textiHAMURPrentacharcol(uint8(b), 4<<4|0xf)
	}
}

func textiHAMURprintln(s string) {
	for _, b := range s {
		textiHAMURPrentachar(uint8(b))
	}
	textiHAMURPrentachar(0xa)
}

func textiHAMURPrentaVilla(s string) {
	for _, b := range s {
		textiHAMURPrentacharcol(uint8(b), 4<<4|0xf)
	}
}

func textiHAMURPrentaerrorln(s string) {
	textiHAMURPrentaVilla(s)
	textiHAMURPrentachar(0xa)
}

func textiHAMURPrentachar(char uint8) {
	textiHAMURPrentacharcol(char, 0<<4|0xf)
}

func textiHAMURPrentacharcol(char uint8, eigindi uint8) {
	textiHAMURcheckfbFæra()
	if char == '\n' {
		fbNúverandiLína++
		fbNúverandicol = 0
		textiHAMURcheckfbFæra()
	} else if char == '\b' {
		fb[fbNúverandicol+fbNúverandiLína*fbBreidd] = 0xf00
		fbNúverandicol = fbNúverandicol - 1
		if fbNúverandicol < 0 {
			fbNúverandicol = 0
		}
	} else if char == '\r' {
		fbNúverandicol = 0
	} else {
		if fbNúverandicol >= fbBreidd {
			return
		}
		fb[fbNúverandicol+fbNúverandiLína*fbBreidd] = uint16(eigindi)<<8 | uint16(char)
		fbNúverandicol++
	}

}

func textiHAMURPrentahex64(number uint64) {
	textiHAMURPrentahex32(uint32(number >> 32))
	textiHAMURPrentahex32(uint32(number))
}

func textiHAMURPrentahex32(number uint32) {
	textiHAMURPrentahex16(uint16(number >> 16))
	textiHAMURPrentahex16(uint16(number))
}

func textiHAMURPrentahex16(number uint16) {
	textiHAMURPrentahex(uint8(number >> 8))
	textiHAMURPrentahex(uint8(number))
}

func textiHAMURPrentahex(number uint8) {
	textiHAMURPrentahexchar(number >> 4)
	textiHAMURPrentahexchar(number)
}

func textiHAMURPrentahexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textiHAMURPrentachar(0x30 + n)
	} else {
		textiHAMURPrentachar(0x41 + n - 10)
	}
}
