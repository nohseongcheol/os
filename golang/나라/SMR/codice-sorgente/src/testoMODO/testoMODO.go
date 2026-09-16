/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type testoMODOwriter struct {
}

func (e testoMODOwriter) Scrittura(p []byte) (int, error) {
	testoMODOStampaByte(p)
	return len(p), nil
}

type testoMODOErrorewriter struct {
}

func (e testoMODOErrorewriter) Scrittura(p []byte) (int, error) {
	testoMODOStampaErroreByte(p)
	return len(p), nil
}

const (
	fbLarghezza		= 80
	fbAltezza		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursoreAltezza		= 1
	cursoreAvvia		= 11
)

var (
	fbCorrenteRiga	= 0
	fbCorrentecol	= 0
)

var fb []uint16

func testoMODOinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLarghezza * fbAltezza,
		Cap:	fbLarghezza * fbAltezza,
		Data:	fbphysaddress,
	}))

}

func testoMODOAbilitaCursore() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursoreAvvia)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursoreAltezza+cursoreAvvia)
}

func testoMODODisabilitaCursore() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func testoMODOAggiornaCursore(x int, y int) {
	posizione := y*fbLarghezza + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posizione&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posizione>>8)&0xFF))
}

func testoMODOflushSchermo() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func testoMODOcheckfbSposta() {
	for fbCorrenteRiga >= fbAltezza {
		copy(fb[:len(fb)-fbLarghezza], fb[fbLarghezza:])

		for i := 0; i < fbLarghezza; i++ {
			fb[(fbAltezza-1)*fbLarghezza+i] = 0xf00
		}
		fbCorrenteRiga--
	}
}

func testoMODOStampacol(s string, attributo uint8) {
	for _, b := range s {
		testoMODOStampacharcol(uint8(b), attributo)
	}
}

func testoMODOprintlncol(s string, attributo uint8) {
	for _, b := range s {
		testoMODOStampacharcol(uint8(b), attributo)
	}
	testoMODOStampachar(0xa)
}

func testoMODOStampa(s string) {
	for _, b := range s {
		testoMODOStampachar(uint8(b))
	}
}

func testoMODOStampaByte(a []byte) {
	for _, b := range a {
		testoMODOStampachar(uint8(b))
	}
}

func testoMODOStampaErroreByte(a []byte) {
	for _, b := range a {
		testoMODOStampacharcol(uint8(b), 4<<4|0xf)
	}
}

func testoMODOprintln(s string) {
	for _, b := range s {
		testoMODOStampachar(uint8(b))
	}
	testoMODOStampachar(0xa)
}

func testoMODOStampaErrore(s string) {
	for _, b := range s {
		testoMODOStampacharcol(uint8(b), 4<<4|0xf)
	}
}

func testoMODOStampaerrorln(s string) {
	testoMODOStampaErrore(s)
	testoMODOStampachar(0xa)
}

func testoMODOStampachar(char uint8) {
	testoMODOStampacharcol(char, 0<<4|0xf)
}

func testoMODOStampacharcol(char uint8, attributo uint8) {
	testoMODOcheckfbSposta()
	if char == '\n' {
		fbCorrenteRiga++
		fbCorrentecol = 0
		testoMODOcheckfbSposta()
	} else if char == '\b' {
		fb[fbCorrentecol+fbCorrenteRiga*fbLarghezza] = 0xf00
		fbCorrentecol = fbCorrentecol - 1
		if fbCorrentecol < 0 {
			fbCorrentecol = 0
		}
	} else if char == '\r' {
		fbCorrentecol = 0
	} else {
		if fbCorrentecol >= fbLarghezza {
			return
		}
		fb[fbCorrentecol+fbCorrenteRiga*fbLarghezza] = uint16(attributo)<<8 | uint16(char)
		fbCorrentecol++
	}

}

func testoMODOStampaEsadecimale64(numero uint64) {
	testoMODOStampaEsadecimale32(uint32(numero >> 32))
	testoMODOStampaEsadecimale32(uint32(numero))
}

func testoMODOStampaEsadecimale32(numero uint32) {
	testoMODOStampaEsadecimale16(uint16(numero >> 16))
	testoMODOStampaEsadecimale16(uint16(numero))
}

func testoMODOStampaEsadecimale16(numero uint16) {
	testoMODOStampaEsadecimale(uint8(numero >> 8))
	testoMODOStampaEsadecimale(uint8(numero))
}

func testoMODOStampaEsadecimale(numero uint8) {
	testoMODOStampaEsadecimalechar(numero >> 4)
	testoMODOStampaEsadecimalechar(numero)
}

func testoMODOStampaEsadecimalechar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		testoMODOStampachar(0x30 + n)
	} else {
		testoMODOStampachar(0x41 + n - 10)
	}
}
