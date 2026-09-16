/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type טקסטמצבwriter struct {
}

func (e טקסטמצבwriter) Wכתיבה(p []byte) (int, error) {
	טקסטמצבהדפסהבתים(p)
	return len(p), nil
}

type טקסטמצבשגיאהwriter struct {
}

func (e טקסטמצבשגיאהwriter) Wכתיבה(p []byte) (int, error) {
	טקסטמצבהדפסהשגיאהבתים(p)
	return len(p), nil
}

const (
	fbwidth			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	סמןheight		= 1
	סמןהתחלה		= 11
)

var (
	fbנוכחישורה	= 0
	fbנוכחיcol	= 0
)

var fb []uint16

func טקסטמצבinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbwidth * fbheight,
		Cap:	fbwidth * fbheight,
		Data:	fbphysaddress,
	}))

}

func טקסטמצבenableסמן() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|סמןהתחלה)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|סמןheight+סמןהתחלה)
}

func טקסטמצבנטרלסמן() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func טקסטמצבעדכוןסמן(x int, y int) {
	מיקום := y*fbwidth + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(מיקום&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((מיקום>>8)&0xFF))
}

func טקסטמצבflushמסך() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func טקסטמצבcheckfbהזז() {
	for fbנוכחישורה >= fbheight {
		copy(fb[:len(fb)-fbwidth], fb[fbwidth:])

		for i := 0; i < fbwidth; i++ {
			fb[(fbheight-1)*fbwidth+i] = 0xf00
		}
		fbנוכחישורה--
	}
}

func טקסטמצבהדפסהcol(s string, תכונה uint8) {
	for _, b := range s {
		טקסטמצבהדפסהcharcol(uint8(b), תכונה)
	}
}

func טקסטמצבprintlncol(s string, תכונה uint8) {
	for _, b := range s {
		טקסטמצבהדפסהcharcol(uint8(b), תכונה)
	}
	טקסטמצבהדפסהchar(0xa)
}

func טקסטמצבהדפסה(s string) {
	for _, b := range s {
		טקסטמצבהדפסהchar(uint8(b))
	}
}

func טקסטמצבהדפסהבתים(a []byte) {
	for _, b := range a {
		טקסטמצבהדפסהchar(uint8(b))
	}
}

func טקסטמצבהדפסהשגיאהבתים(a []byte) {
	for _, b := range a {
		טקסטמצבהדפסהcharcol(uint8(b), 4<<4|0xf)
	}
}

func טקסטמצבprintln(s string) {
	for _, b := range s {
		טקסטמצבהדפסהchar(uint8(b))
	}
	טקסטמצבהדפסהchar(0xa)
}

func טקסטמצבהדפסהשגיאה(s string) {
	for _, b := range s {
		טקסטמצבהדפסהcharcol(uint8(b), 4<<4|0xf)
	}
}

func טקסטמצבהדפסהerrorln(s string) {
	טקסטמצבהדפסהשגיאה(s)
	טקסטמצבהדפסהchar(0xa)
}

func טקסטמצבהדפסהchar(char uint8) {
	טקסטמצבהדפסהcharcol(char, 0<<4|0xf)
}

func טקסטמצבהדפסהcharcol(char uint8, תכונה uint8) {
	טקסטמצבcheckfbהזז()
	if char == '\n' {
		fbנוכחישורה++
		fbנוכחיcol = 0
		טקסטמצבcheckfbהזז()
	} else if char == '\b' {
		fb[fbנוכחיcol+fbנוכחישורה*fbwidth] = 0xf00
		fbנוכחיcol = fbנוכחיcol - 1
		if fbנוכחיcol < 0 {
			fbנוכחיcol = 0
		}
	} else if char == '\r' {
		fbנוכחיcol = 0
	} else {
		if fbנוכחיcol >= fbwidth {
			return
		}
		fb[fbנוכחיcol+fbנוכחישורה*fbwidth] = uint16(תכונה)<<8 | uint16(char)
		fbנוכחיcol++
	}

}

func טקסטמצבהדפסההקסדצימלי64(מספר uint64) {
	טקסטמצבהדפסההקסדצימלי32(uint32(מספר >> 32))
	טקסטמצבהדפסההקסדצימלי32(uint32(מספר))
}

func טקסטמצבהדפסההקסדצימלי32(מספר uint32) {
	טקסטמצבהדפסההקסדצימלי16(uint16(מספר >> 16))
	טקסטמצבהדפסההקסדצימלי16(uint16(מספר))
}

func טקסטמצבהדפסההקסדצימלי16(מספר uint16) {
	טקסטמצבהדפסההקסדצימלי(uint8(מספר >> 8))
	טקסטמצבהדפסההקסדצימלי(uint8(מספר))
}

func טקסטמצבהדפסההקסדצימלי(מספר uint8) {
	טקסטמצבהדפסההקסדצימליchar(מספר >> 4)
	טקסטמצבהדפסההקסדצימליchar(מספר)
}

func טקסטמצבהדפסההקסדצימליchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		טקסטמצבהדפסהchar(0x30 + n)
	} else {
		טקסטמצבהדפסהchar(0x41 + n - 10)
	}
}
