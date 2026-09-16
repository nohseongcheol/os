/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type textModuswriter struct {
}

func (e textModuswriter) Schreiben(p []byte) (int, error) {
	textModusDruckenByte(p)
	return len(p), nil
}

type textModusFehlerwriter struct {
}

func (e textModusFehlerwriter) Schreiben(p []byte) (int, error) {
	textModusDruckenFehlerByte(p)
	return len(p), nil
}

const (
	fbBreite			= 80
	fbHöhe				= 25
	fbphysaddress		uintptr	= 0xb8000
	eingabemarkeHöhe		= 1
	eingabemarkeStarten		= 11
)

var (
	fbSystemzeitZeile	= 0
	fbSystemzeitKol		= 0
)

var fb []uint16

func textModusinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbBreite * fbHöhe,
		Cap:	fbBreite * fbHöhe,
		Data:	fbphysaddress,
	}))

}

func textModusAktivierenEingabemarke() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|eingabemarkeStarten)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|eingabemarkeHöhe+eingabemarkeStarten)
}

func textModusDeaktivierenEingabemarke() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func textModusAktualisierenEingabemarke(x int, y int) {
	position := y*fbBreite + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func textModusflushBildschirm() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func textModuscheckfbVerschieben() {
	for fbSystemzeitZeile >= fbHöhe {
		copy(fb[:len(fb)-fbBreite], fb[fbBreite:])

		for i := 0; i < fbBreite; i++ {
			fb[(fbHöhe-1)*fbBreite+i] = 0xf00
		}
		fbSystemzeitZeile--
	}
}

func textModusDruckenKol(s string, attribut uint8) {
	for _, b := range s {
		textModusDruckencharKol(uint8(b), attribut)
	}
}

func textModusprintlnKol(s string, attribut uint8) {
	for _, b := range s {
		textModusDruckencharKol(uint8(b), attribut)
	}
	textModusDruckenchar(0xa)
}

func textModusDrucken(s string) {
	for _, b := range s {
		textModusDruckenchar(uint8(b))
	}
}

func textModusDruckenByte(a []byte) {
	for _, b := range a {
		textModusDruckenchar(uint8(b))
	}
}

func textModusDruckenFehlerByte(a []byte) {
	for _, b := range a {
		textModusDruckencharKol(uint8(b), 4<<4|0xf)
	}
}

func textModusprintln(s string) {
	for _, b := range s {
		textModusDruckenchar(uint8(b))
	}
	textModusDruckenchar(0xa)
}

func textModusDruckenFehler(s string) {
	for _, b := range s {
		textModusDruckencharKol(uint8(b), 4<<4|0xf)
	}
}

func textModusDruckenerrorln(s string) {
	textModusDruckenFehler(s)
	textModusDruckenchar(0xa)
}

func textModusDruckenchar(char uint8) {
	textModusDruckencharKol(char, 0<<4|0xf)
}

func textModusDruckencharKol(char uint8, attribut uint8) {
	textModuscheckfbVerschieben()
	if char == '\n' {
		fbSystemzeitZeile++
		fbSystemzeitKol = 0
		textModuscheckfbVerschieben()
	} else if char == '\b' {
		fb[fbSystemzeitKol+fbSystemzeitZeile*fbBreite] = 0xf00
		fbSystemzeitKol = fbSystemzeitKol - 1
		if fbSystemzeitKol < 0 {
			fbSystemzeitKol = 0
		}
	} else if char == '\r' {
		fbSystemzeitKol = 0
	} else {
		if fbSystemzeitKol >= fbBreite {
			return
		}
		fb[fbSystemzeitKol+fbSystemzeitZeile*fbBreite] = uint16(attribut)<<8 | uint16(char)
		fbSystemzeitKol++
	}

}

func textModusDruckenhex64(nummer uint64) {
	textModusDruckenhex32(uint32(nummer >> 32))
	textModusDruckenhex32(uint32(nummer))
}

func textModusDruckenhex32(nummer uint32) {
	textModusDruckenhex16(uint16(nummer >> 16))
	textModusDruckenhex16(uint16(nummer))
}

func textModusDruckenhex16(nummer uint16) {
	textModusDruckenhex(uint8(nummer >> 8))
	textModusDruckenhex(uint8(nummer))
}

func textModusDruckenhex(nummer uint8) {
	textModusDruckenhexchar(nummer >> 4)
	textModusDruckenhexchar(nummer)
}

func textModusDruckenhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		textModusDruckenchar(0x30 + n)
	} else {
		textModusDruckenchar(0x41 + n - 10)
	}
}
