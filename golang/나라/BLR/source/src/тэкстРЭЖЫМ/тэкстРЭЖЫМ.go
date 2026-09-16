/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type тэкстРЭЖЫМwriter struct {
}

func (e тэкстРЭЖЫМwriter) Запіс(p []byte) (int, error) {
	тэкстРЭЖЫМДрукавацьБайтаў(p)
	return len(p), nil
}

type тэкстРЭЖЫМПамылкаwriter struct {
}

func (e тэкстРЭЖЫМПамылкаwriter) Запіс(p []byte) (int, error) {
	тэкстРЭЖЫМДрукавацьПамылкаБайтаў(p)
	return len(p), nil
}

const (
	fbШырыня		= 80
	fbВышыня		= 25
	fbphysaddress	uintptr	= 0xb8000
	курсорВышыня		= 1
	курсорУключыць		= 11
)

var (
	fbДзейныline	= 0
	fbДзейныcol	= 0
)

var fb []uint16

func тэкстРЭЖЫМinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШырыня * fbВышыня,
		Cap:	fbШырыня * fbВышыня,
		Data:	fbphysaddress,
	}))

}

func тэкстРЭЖЫМenableКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|курсорУключыць)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|курсорВышыня+курсорУключыць)
}

func тэкстРЭЖЫМВыключыцьКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func тэкстРЭЖЫМАбнавіцьКурсор(x int, y int) {
	пазіцыя := y*fbШырыня + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(пазіцыя&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((пазіцыя>>8)&0xFF))
}

func тэкстРЭЖЫМflushЭкран() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func тэкстРЭЖЫМcheckfbПеранесці() {
	for fbДзейныline >= fbВышыня {
		copy(fb[:len(fb)-fbШырыня], fb[fbШырыня:])

		for i := 0; i < fbШырыня; i++ {
			fb[(fbВышыня-1)*fbШырыня+i] = 0xf00
		}
		fbДзейныline--
	}
}

func тэкстРЭЖЫМДрукавацьcol(s string, атрыбут uint8) {
	for _, b := range s {
		тэкстРЭЖЫМДрукавацьcharcol(uint8(b), атрыбут)
	}
}

func тэкстРЭЖЫМprintlncol(s string, атрыбут uint8) {
	for _, b := range s {
		тэкстРЭЖЫМДрукавацьcharcol(uint8(b), атрыбут)
	}
	тэкстРЭЖЫМДрукавацьchar(0xa)
}

func тэкстРЭЖЫМДрукаваць(s string) {
	for _, b := range s {
		тэкстРЭЖЫМДрукавацьchar(uint8(b))
	}
}

func тэкстРЭЖЫМДрукавацьБайтаў(a []byte) {
	for _, b := range a {
		тэкстРЭЖЫМДрукавацьchar(uint8(b))
	}
}

func тэкстРЭЖЫМДрукавацьПамылкаБайтаў(a []byte) {
	for _, b := range a {
		тэкстРЭЖЫМДрукавацьcharcol(uint8(b), 4<<4|0xf)
	}
}

func тэкстРЭЖЫМprintln(s string) {
	for _, b := range s {
		тэкстРЭЖЫМДрукавацьchar(uint8(b))
	}
	тэкстРЭЖЫМДрукавацьchar(0xa)
}

func тэкстРЭЖЫМДрукавацьПамылка(s string) {
	for _, b := range s {
		тэкстРЭЖЫМДрукавацьcharcol(uint8(b), 4<<4|0xf)
	}
}

func тэкстРЭЖЫМДрукавацьerrorln(s string) {
	тэкстРЭЖЫМДрукавацьПамылка(s)
	тэкстРЭЖЫМДрукавацьchar(0xa)
}

func тэкстРЭЖЫМДрукавацьchar(char uint8) {
	тэкстРЭЖЫМДрукавацьcharcol(char, 0<<4|0xf)
}

func тэкстРЭЖЫМДрукавацьcharcol(char uint8, атрыбут uint8) {
	тэкстРЭЖЫМcheckfbПеранесці()
	if char == '\n' {
		fbДзейныline++
		fbДзейныcol = 0
		тэкстРЭЖЫМcheckfbПеранесці()
	} else if char == '\b' {
		fb[fbДзейныcol+fbДзейныline*fbШырыня] = 0xf00
		fbДзейныcol = fbДзейныcol - 1
		if fbДзейныcol < 0 {
			fbДзейныcol = 0
		}
	} else if char == '\r' {
		fbДзейныcol = 0
	} else {
		if fbДзейныcol >= fbШырыня {
			return
		}
		fb[fbДзейныcol+fbДзейныline*fbШырыня] = uint16(атрыбут)<<8 | uint16(char)
		fbДзейныcol++
	}

}

func тэкстРЭЖЫМДрукавацьШаснаццатковы64(нУМАР uint64) {
	тэкстРЭЖЫМДрукавацьШаснаццатковы32(uint32(нУМАР >> 32))
	тэкстРЭЖЫМДрукавацьШаснаццатковы32(uint32(нУМАР))
}

func тэкстРЭЖЫМДрукавацьШаснаццатковы32(нУМАР uint32) {
	тэкстРЭЖЫМДрукавацьШаснаццатковы16(uint16(нУМАР >> 16))
	тэкстРЭЖЫМДрукавацьШаснаццатковы16(uint16(нУМАР))
}

func тэкстРЭЖЫМДрукавацьШаснаццатковы16(нУМАР uint16) {
	тэкстРЭЖЫМДрукавацьШаснаццатковы(uint8(нУМАР >> 8))
	тэкстРЭЖЫМДрукавацьШаснаццатковы(uint8(нУМАР))
}

func тэкстРЭЖЫМДрукавацьШаснаццатковы(нУМАР uint8) {
	тэкстРЭЖЫМДрукавацьШаснаццатковыchar(нУМАР >> 4)
	тэкстРЭЖЫМДрукавацьШаснаццатковыchar(нУМАР)
}

func тэкстРЭЖЫМДрукавацьШаснаццатковыchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		тэкстРЭЖЫМДрукавацьchar(0x30 + n)
	} else {
		тэкстРЭЖЫМДрукавацьchar(0x41 + n - 10)
	}
}
