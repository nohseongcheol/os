/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstREŽIIMwriter struct {
}

func (e tekstREŽIIMwriter) Kirjutamine(p []byte) (int, error) {
	tekstREŽIIMPrindibaiti(p)
	return len(p), nil
}

type tekstREŽIIMVigawriter struct {
}

func (e tekstREŽIIMVigawriter) Kirjutamine(p []byte) (int, error) {
	tekstREŽIIMPrindiVigabaiti(p)
	return len(p), nil
}

const (
	fbKõrgus		= 80
	fbLaius			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorLaius		= 1
	cursorKäivita		= 11
)

var (
	fbKäesolevRida	= 0
	fbKäesolevcol	= 0
)

var fb []uint16

func tekstREŽIIMinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbKõrgus * fbLaius,
		Cap:	fbKõrgus * fbLaius,
		Data:	fbphysaddress,
	}))

}

func tekstREŽIIMLubatudcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorKäivita)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorLaius+cursorKäivita)
}

func tekstREŽIIMKeelacursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstREŽIIMUuendacursor(x int, y int) {
	asukoht := y*fbKõrgus + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(asukoht&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((asukoht>>8)&0xFF))
}

func tekstREŽIIMflushEkraan() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstREŽIIMcheckfbLiiguta() {
	for fbKäesolevRida >= fbLaius {
		copy(fb[:len(fb)-fbKõrgus], fb[fbKõrgus:])

		for i := 0; i < fbKõrgus; i++ {
			fb[(fbLaius-1)*fbKõrgus+i] = 0xf00
		}
		fbKäesolevRida--
	}
}

func tekstREŽIIMPrindicol(s string, atribuut uint8) {
	for _, b := range s {
		tekstREŽIIMPrindicharcol(uint8(b), atribuut)
	}
}

func tekstREŽIIMprintlncol(s string, atribuut uint8) {
	for _, b := range s {
		tekstREŽIIMPrindicharcol(uint8(b), atribuut)
	}
	tekstREŽIIMPrindichar(0xa)
}

func tekstREŽIIMPrindi(s string) {
	for _, b := range s {
		tekstREŽIIMPrindichar(uint8(b))
	}
}

func tekstREŽIIMPrindibaiti(a []byte) {
	for _, b := range a {
		tekstREŽIIMPrindichar(uint8(b))
	}
}

func tekstREŽIIMPrindiVigabaiti(a []byte) {
	for _, b := range a {
		tekstREŽIIMPrindicharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstREŽIIMprintln(s string) {
	for _, b := range s {
		tekstREŽIIMPrindichar(uint8(b))
	}
	tekstREŽIIMPrindichar(0xa)
}

func tekstREŽIIMPrindiViga(s string) {
	for _, b := range s {
		tekstREŽIIMPrindicharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstREŽIIMPrindierrorln(s string) {
	tekstREŽIIMPrindiViga(s)
	tekstREŽIIMPrindichar(0xa)
}

func tekstREŽIIMPrindichar(char uint8) {
	tekstREŽIIMPrindicharcol(char, 0<<4|0xf)
}

func tekstREŽIIMPrindicharcol(char uint8, atribuut uint8) {
	tekstREŽIIMcheckfbLiiguta()
	if char == '\n' {
		fbKäesolevRida++
		fbKäesolevcol = 0
		tekstREŽIIMcheckfbLiiguta()
	} else if char == '\b' {
		fb[fbKäesolevcol+fbKäesolevRida*fbKõrgus] = 0xf00
		fbKäesolevcol = fbKäesolevcol - 1
		if fbKäesolevcol < 0 {
			fbKäesolevcol = 0
		}
	} else if char == '\r' {
		fbKäesolevcol = 0
	} else {
		if fbKäesolevcol >= fbKõrgus {
			return
		}
		fb[fbKäesolevcol+fbKäesolevRida*fbKõrgus] = uint16(atribuut)<<8 | uint16(char)
		fbKäesolevcol++
	}

}

func tekstREŽIIMPrindi16ndsüsteem64(arv uint64) {
	tekstREŽIIMPrindi16ndsüsteem32(uint32(arv >> 32))
	tekstREŽIIMPrindi16ndsüsteem32(uint32(arv))
}

func tekstREŽIIMPrindi16ndsüsteem32(arv uint32) {
	tekstREŽIIMPrindi16ndsüsteem16(uint16(arv >> 16))
	tekstREŽIIMPrindi16ndsüsteem16(uint16(arv))
}

func tekstREŽIIMPrindi16ndsüsteem16(arv uint16) {
	tekstREŽIIMPrindi16ndsüsteem(uint8(arv >> 8))
	tekstREŽIIMPrindi16ndsüsteem(uint8(arv))
}

func tekstREŽIIMPrindi16ndsüsteem(arv uint8) {
	tekstREŽIIMPrindi16ndsüsteemchar(arv >> 4)
	tekstREŽIIMPrindi16ndsüsteemchar(arv)
}

func tekstREŽIIMPrindi16ndsüsteemchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstREŽIIMPrindichar(0x30 + n)
	} else {
		tekstREŽIIMPrindichar(0x41 + n - 10)
	}
}
