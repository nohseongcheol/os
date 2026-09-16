/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type κείμενοΚΑΤΑΣΤΑΣΗwriter struct {
}

func (e κείμενοΚΑΤΑΣΤΑΣΗwriter) Εγγραφή(p []byte) (int, error) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηbytes(p)
	return len(p), nil
}

type κείμενοΚΑΤΑΣΤΑΣΗΣφάλμαwriter struct {
}

func (e κείμενοΚΑΤΑΣΤΑΣΗΣφάλμαwriter) Εγγραφή(p []byte) (int, error) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΣφάλμαbytes(p)
	return len(p), nil
}

const (
	fbΠλάτος		= 80
	fbΎψος			= 25
	fbphysaddress	uintptr	= 0xb8000
	δείκτηςΎψος		= 1
	δείκτηςΈναρξη		= 11
)

var (
	fbΤρέχονΓραμμή	= 0
	fbΤρέχονcol	= 0
)

var fb []uint16

func κείμενοΚΑΤΑΣΤΑΣΗinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbΠλάτος * fbΎψος,
		Cap:	fbΠλάτος * fbΎψος,
		Data:	fbphysaddress,
	}))

}

func κείμενοΚΑΤΑΣΤΑΣΗΕνεργοποίησηΔείκτης() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|δείκτηςΈναρξη)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|δείκτηςΎψος+δείκτηςΈναρξη)
}

func κείμενοΚΑΤΑΣΤΑΣΗΑπενεργοποίησηΔείκτης() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕνημέρωσηΔείκτης(x int, y int) {
	θέση := y*fbΠλάτος + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(θέση&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((θέση>>8)&0xFF))
}

func κείμενοΚΑΤΑΣΤΑΣΗflushΟθόνη() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗcheckfbΜετακίνηση() {
	for fbΤρέχονΓραμμή >= fbΎψος {
		copy(fb[:len(fb)-fbΠλάτος], fb[fbΠλάτος:])

		for i := 0; i < fbΠλάτος; i++ {
			fb[(fbΎψος-1)*fbΠλάτος+i] = 0xf00
		}
		fbΤρέχονΓραμμή--
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcol(s string, γνώρισμα uint8) {
	for _, b := range s {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(uint8(b), γνώρισμα)
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗprintlncol(s string, γνώρισμα uint8) {
	for _, b := range s {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(uint8(b), γνώρισμα)
	}
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(0xa)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωση(s string) {
	for _, b := range s {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(uint8(b))
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηbytes(a []byte) {
	for _, b := range a {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(uint8(b))
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΣφάλμαbytes(a []byte) {
	for _, b := range a {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(uint8(b), 4<<4|0xf)
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗprintln(s string) {
	for _, b := range s {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(uint8(b))
	}
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(0xa)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΣφάλμα(s string) {
	for _, b := range s {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(uint8(b), 4<<4|0xf)
	}
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηerrorln(s string) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΣφάλμα(s)
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(0xa)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(char uint8) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(char, 0<<4|0xf)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηcharcol(char uint8, γνώρισμα uint8) {
	κείμενοΚΑΤΑΣΤΑΣΗcheckfbΜετακίνηση()
	if char == '\n' {
		fbΤρέχονΓραμμή++
		fbΤρέχονcol = 0
		κείμενοΚΑΤΑΣΤΑΣΗcheckfbΜετακίνηση()
	} else if char == '\b' {
		fb[fbΤρέχονcol+fbΤρέχονΓραμμή*fbΠλάτος] = 0xf00
		fbΤρέχονcol = fbΤρέχονcol - 1
		if fbΤρέχονcol < 0 {
			fbΤρέχονcol = 0
		}
	} else if char == '\r' {
		fbΤρέχονcol = 0
	} else {
		if fbΤρέχονcol >= fbΠλάτος {
			return
		}
		fb[fbΤρέχονcol+fbΤρέχονΓραμμή*fbΠλάτος] = uint16(γνώρισμα)<<8 | uint16(char)
		fbΤρέχονcol++
	}

}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό64(αριθμός uint64) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό32(uint32(αριθμός >> 32))
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό32(uint32(αριθμός))
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό32(αριθμός uint32) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό16(uint16(αριθμός >> 16))
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό16(uint16(αριθμός))
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό16(αριθμός uint16) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό(uint8(αριθμός >> 8))
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό(uint8(αριθμός))
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικό(αριθμός uint8) {
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικόchar(αριθμός >> 4)
	κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικόchar(αριθμός)
}

func κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηΔεκαεξαδικόchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(0x30 + n)
	} else {
		κείμενοΚΑΤΑΣΤΑΣΗΕκτύπωσηchar(0x41 + n - 10)
	}
}
