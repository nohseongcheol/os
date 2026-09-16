/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type tekstiTILAwriter struct {
}

func (e tekstiTILAwriter) Kirjoitus(p []byte) (int, error) {
	tekstiTILATulostatavua(p)
	return len(p), nil
}

type tekstiTILAVirhewriter struct {
}

func (e tekstiTILAVirhewriter) Kirjoitus(p []byte) (int, error) {
	tekstiTILATulostaVirhetavua(p)
	return len(p), nil
}

const (
	fbLeveys			= 80
	fbKorkeus			= 25
	fbphysaddress		uintptr	= 0xb8000
	kursoriKorkeus			= 1
	kursoriKäynnistä		= 11
)

var (
	fbNykyinenRivi	= 0
	fbNykyinencol	= 0
)

var fb []uint16

func tekstiTILAinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLeveys * fbKorkeus,
		Cap:	fbLeveys * fbKorkeus,
		Data:	fbphysaddress,
	}))

}

func tekstiTILAOtakäyttöönKursori() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kursoriKäynnistä)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kursoriKorkeus+kursoriKäynnistä)
}

func tekstiTILAPoistakäytöstäKursori() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstiTILAPäivitäKursori(x int, y int) {
	sijainti := y*fbLeveys + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(sijainti&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((sijainti>>8)&0xFF))
}

func tekstiTILAflushNäyttö() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstiTILAcheckfbSiirrä() {
	for fbNykyinenRivi >= fbKorkeus {
		copy(fb[:len(fb)-fbLeveys], fb[fbLeveys:])

		for i := 0; i < fbLeveys; i++ {
			fb[(fbKorkeus-1)*fbLeveys+i] = 0xf00
		}
		fbNykyinenRivi--
	}
}

func tekstiTILATulostacol(s string, määre uint8) {
	for _, b := range s {
		tekstiTILATulostacharcol(uint8(b), määre)
	}
}

func tekstiTILAprintlncol(s string, määre uint8) {
	for _, b := range s {
		tekstiTILATulostacharcol(uint8(b), määre)
	}
	tekstiTILATulostachar(0xa)
}

func tekstiTILATulosta(s string) {
	for _, b := range s {
		tekstiTILATulostachar(uint8(b))
	}
}

func tekstiTILATulostatavua(a []byte) {
	for _, b := range a {
		tekstiTILATulostachar(uint8(b))
	}
}

func tekstiTILATulostaVirhetavua(a []byte) {
	for _, b := range a {
		tekstiTILATulostacharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstiTILAprintln(s string) {
	for _, b := range s {
		tekstiTILATulostachar(uint8(b))
	}
	tekstiTILATulostachar(0xa)
}

func tekstiTILATulostaVirhe(s string) {
	for _, b := range s {
		tekstiTILATulostacharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstiTILATulostaerrorln(s string) {
	tekstiTILATulostaVirhe(s)
	tekstiTILATulostachar(0xa)
}

func tekstiTILATulostachar(char uint8) {
	tekstiTILATulostacharcol(char, 0<<4|0xf)
}

func tekstiTILATulostacharcol(char uint8, määre uint8) {
	tekstiTILAcheckfbSiirrä()
	if char == '\n' {
		fbNykyinenRivi++
		fbNykyinencol = 0
		tekstiTILAcheckfbSiirrä()
	} else if char == '\b' {
		fb[fbNykyinencol+fbNykyinenRivi*fbLeveys] = 0xf00
		fbNykyinencol = fbNykyinencol - 1
		if fbNykyinencol < 0 {
			fbNykyinencol = 0
		}
	} else if char == '\r' {
		fbNykyinencol = 0
	} else {
		if fbNykyinencol >= fbLeveys {
			return
		}
		fb[fbNykyinencol+fbNykyinenRivi*fbLeveys] = uint16(määre)<<8 | uint16(char)
		fbNykyinencol++
	}

}

func tekstiTILATulostaHeksa64(numero uint64) {
	tekstiTILATulostaHeksa32(uint32(numero >> 32))
	tekstiTILATulostaHeksa32(uint32(numero))
}

func tekstiTILATulostaHeksa32(numero uint32) {
	tekstiTILATulostaHeksa16(uint16(numero >> 16))
	tekstiTILATulostaHeksa16(uint16(numero))
}

func tekstiTILATulostaHeksa16(numero uint16) {
	tekstiTILATulostaHeksa(uint8(numero >> 8))
	tekstiTILATulostaHeksa(uint8(numero))
}

func tekstiTILATulostaHeksa(numero uint8) {
	tekstiTILATulostaHeksachar(numero >> 4)
	tekstiTILATulostaHeksachar(numero)
}

func tekstiTILATulostaHeksachar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstiTILATulostachar(0x30 + n)
	} else {
		tekstiTILATulostachar(0x41 + n - 10)
	}
}
