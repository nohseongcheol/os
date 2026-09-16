/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textemodewriter struct {
}

func (e textemodewriter) Écrire(p []byte) (int, error) {
	textemodeImprimerOctets(p)
	return len(p), nil
}

type textemodeErreurwriter struct {
}

func (e textemodeErreurwriter) Écrire(p []byte) (int, error) {
	textemodeImprimerErreurOctets(p)
	return len(p), nil
}

const (
	fbLargeur		= 80
	fbHauteur		= 25
	fbphysaddress	uintptr	= 0xb8000
	curseurHauteur		= 1
	curseurDémarrer		= 11
)

var (
	fbCouranteLigne	= 0
	fbCourantecol	= 0
)

var fb []uint16

func textemodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLargeur * fbHauteur,
		Cap:	fbLargeur * fbHauteur,
		Data:	fbphysaddress,
	}))

}

func textemodeActiverCurseur() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|curseurDémarrer)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|curseurHauteur+curseurDémarrer)
}

func textemodeDésactiverCurseur() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textemodeMettreàjourCurseur(x int, y int) {
	position := y*fbLargeur + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func textemodeflushÉcran() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textemodecheckfbDéplacer() {
	for fbCouranteLigne >= fbHauteur {
		copy(fb[:len(fb)-fbLargeur], fb[fbLargeur:])

		for i := 0; i < fbLargeur; i++ {
			fb[(fbHauteur-1)*fbLargeur+i] = 0xf00
		}
		fbCouranteLigne--
	}
}

func textemodeImprimercol(s string, attribut uint8) {
	for _, b := range s {
		textemodeImprimercharcol(uint8(b), attribut)
	}
}

func textemodeprintlncol(s string, attribut uint8) {
	for _, b := range s {
		textemodeImprimercharcol(uint8(b), attribut)
	}
	textemodeImprimerchar(0xa)
}

func textemodeImprimer(s string) {
	for _, b := range s {
		textemodeImprimerchar(uint8(b))
	}
}

func textemodeImprimerOctets(a []byte) {
	for _, b := range a {
		textemodeImprimerchar(uint8(b))
	}
}

func textemodeImprimerErreurOctets(a []byte) {
	for _, b := range a {
		textemodeImprimercharcol(uint8(b), 4<<4|0xf)
	}
}

func textemodeprintln(s string) {
	for _, b := range s {
		textemodeImprimerchar(uint8(b))
	}
	textemodeImprimerchar(0xa)
}

func textemodeImprimerErreur(s string) {
	for _, b := range s {
		textemodeImprimercharcol(uint8(b), 4<<4|0xf)
	}
}

func textemodeImprimererrorln(s string) {
	textemodeImprimerErreur(s)
	textemodeImprimerchar(0xa)
}

func textemodeImprimerchar(char uint8) {
	textemodeImprimercharcol(char, 0<<4|0xf)
}

func textemodeImprimercharcol(char uint8, attribut uint8) {
	textemodecheckfbDéplacer()
	if char == '\n' {
		fbCouranteLigne++
		fbCourantecol = 0
		textemodecheckfbDéplacer()
	} else if char == '\b' {
		fb[fbCourantecol+fbCouranteLigne*fbLargeur] = 0xf00
		fbCourantecol = fbCourantecol - 1
		if fbCourantecol < 0 {
			fbCourantecol = 0
		}
	} else if char == '\r' {
		fbCourantecol = 0
	} else {
		if fbCourantecol >= fbLargeur {
			return
		}
		fb[fbCourantecol+fbCouranteLigne*fbLargeur] = uint16(attribut)<<8 | uint16(char)
		fbCourantecol++
	}

}

func textemodeImprimerhex64(nombre_2 uint64) {
	textemodeImprimerhex32(uint32(nombre_2 >> 32))
	textemodeImprimerhex32(uint32(nombre_2))
}

func textemodeImprimerhex32(nombre_2 uint32) {
	textemodeImprimerhex16(uint16(nombre_2 >> 16))
	textemodeImprimerhex16(uint16(nombre_2))
}

func textemodeImprimerhex16(nombre_2 uint16) {
	textemodeImprimerhex(uint8(nombre_2 >> 8))
	textemodeImprimerhex(uint8(nombre_2))
}

func textemodeImprimerhex(nombre_2 uint8) {
	textemodeImprimerhexchar(nombre_2 >> 4)
	textemodeImprimerhexchar(nombre_2)
}

func textemodeImprimerhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textemodeImprimerchar(0x30 + n)
	} else {
		textemodeImprimerchar(0x41 + n - 10)
	}
}
