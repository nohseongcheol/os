/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type teksmodwriter struct {
}

func (e teksmodwriter) Tulis(p []byte) (int, error) {
	teksmodCetakBait(p)
	return len(p), nil
}

type teksmodRalatwriter struct {
}

func (e teksmodRalatwriter) Tulis(p []byte) (int, error) {
	teksmodCetakRalatBait(p)
	return len(p), nil
}

const (
	fbLebar			= 80
	fbTinggi		= 25
	fbphysaddress	uintptr	= 0xb8000
	kursorTinggi		= 1
	kursorMula		= 11
)

var (
	fbSemasaline	= 0
	fbSemasacol	= 0
)

var fb []uint16

func teksmodinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLebar * fbTinggi,
		Cap:	fbLebar * fbTinggi,
		Data:	fbphysaddress,
	}))

}

func teksmodBenarkanKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kursorMula)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kursorTinggi+kursorMula)
}

func teksmodLumpuhKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func teksmodKemaskiniKursor(x int, y int) {
	kedudukan := y*fbLebar + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(kedudukan&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((kedudukan>>8)&0xFF))
}

func teksmodflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func teksmodcheckfbAlih() {
	for fbSemasaline >= fbTinggi {
		copy(fb[:len(fb)-fbLebar], fb[fbLebar:])

		for i := 0; i < fbLebar; i++ {
			fb[(fbTinggi-1)*fbLebar+i] = 0xf00
		}
		fbSemasaline--
	}
}

func teksmodCetakcol(s string, atribut uint8) {
	for _, b := range s {
		teksmodCetakcharcol(uint8(b), atribut)
	}
}

func teksmodprintlncol(s string, atribut uint8) {
	for _, b := range s {
		teksmodCetakcharcol(uint8(b), atribut)
	}
	teksmodCetakchar(0xa)
}

func teksmodCetak(s string) {
	for _, b := range s {
		teksmodCetakchar(uint8(b))
	}
}

func teksmodCetakBait(a []byte) {
	for _, b := range a {
		teksmodCetakchar(uint8(b))
	}
}

func teksmodCetakRalatBait(a []byte) {
	for _, b := range a {
		teksmodCetakcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksmodprintln(s string) {
	for _, b := range s {
		teksmodCetakchar(uint8(b))
	}
	teksmodCetakchar(0xa)
}

func teksmodCetakRalat(s string) {
	for _, b := range s {
		teksmodCetakcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksmodCetakerrorln(s string) {
	teksmodCetakRalat(s)
	teksmodCetakchar(0xa)
}

func teksmodCetakchar(char uint8) {
	teksmodCetakcharcol(char, 0<<4|0xf)
}

func teksmodCetakcharcol(char uint8, atribut uint8) {
	teksmodcheckfbAlih()
	if char == '\n' {
		fbSemasaline++
		fbSemasacol = 0
		teksmodcheckfbAlih()
	} else if char == '\b' {
		fb[fbSemasacol+fbSemasaline*fbLebar] = 0xf00
		fbSemasacol = fbSemasacol - 1
		if fbSemasacol < 0 {
			fbSemasacol = 0
		}
	} else if char == '\r' {
		fbSemasacol = 0
	} else {
		if fbSemasacol >= fbLebar {
			return
		}
		fb[fbSemasacol+fbSemasaline*fbLebar] = uint16(atribut)<<8 | uint16(char)
		fbSemasacol++
	}

}

func teksmodCetakHeks64(nOMBOR uint64) {
	teksmodCetakHeks32(uint32(nOMBOR >> 32))
	teksmodCetakHeks32(uint32(nOMBOR))
}

func teksmodCetakHeks32(nOMBOR uint32) {
	teksmodCetakHeks16(uint16(nOMBOR >> 16))
	teksmodCetakHeks16(uint16(nOMBOR))
}

func teksmodCetakHeks16(nOMBOR uint16) {
	teksmodCetakHeks(uint8(nOMBOR >> 8))
	teksmodCetakHeks(uint8(nOMBOR))
}

func teksmodCetakHeks(nOMBOR uint8) {
	teksmodCetakHekschar(nOMBOR >> 4)
	teksmodCetakHekschar(nOMBOR)
}

func teksmodCetakHekschar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		teksmodCetakchar(0x30 + n)
	} else {
		teksmodCetakchar(0x41 + n - 10)
	}
}
