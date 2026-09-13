package main

import (
	"reflect"
	"unsafe"
)

type teksmodewriter struct {
}

func (e teksmodewriter) Tulis(p []byte) (int, error) {
	teksmodeCetakByte(p)
	return len(p), nil
}

type teksmodeGalatwriter struct {
}

func (e teksmodeGalatwriter) Tulis(p []byte) (int, error) {
	teksmodeCetakGalatByte(p)
	return len(p), nil
}

const (
	fbLebar			= 80
	fbTinggi		= 25
	fbphysaddress	uintptr	= 0xb8000
	kursorTinggi		= 1
	kursorMulai		= 11
)

var (
	fbSekarangBaris	= 0
	fbSekarangcol	= 0
)

var fb []uint16

func teksmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbLebar * fbTinggi,
		Cap:	fbLebar * fbTinggi,
		Data:	fbphysaddress,
	}))

}

func teksmodeAktifkanKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kursorMulai)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kursorTinggi+kursorMulai)
}

func teksmodeNonaktifkanKursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func teksmodePerbaruiKursor(x int, y int) {
	posisi := y*fbLebar + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(posisi&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((posisi>>8)&0xFF))
}

func teksmodeflushPengunciLayar() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func teksmodecheckfbPindah() {
	for fbSekarangBaris >= fbTinggi {
		copy(fb[:len(fb)-fbLebar], fb[fbLebar:])

		for i := 0; i < fbLebar; i++ {
			fb[(fbTinggi-1)*fbLebar+i] = 0xf00
		}
		fbSekarangBaris--
	}
}

func teksmodeCetakcol(s string, atribut uint8) {
	for _, b := range s {
		teksmodeCetakcharcol(uint8(b), atribut)
	}
}

func teksmodeprintlncol(s string, atribut uint8) {
	for _, b := range s {
		teksmodeCetakcharcol(uint8(b), atribut)
	}
	teksmodeCetakchar(0xa)
}

func teksmodeCetak(s string) {
	for _, b := range s {
		teksmodeCetakchar(uint8(b))
	}
}

func teksmodeCetakByte(a []byte) {
	for _, b := range a {
		teksmodeCetakchar(uint8(b))
	}
}

func teksmodeCetakGalatByte(a []byte) {
	for _, b := range a {
		teksmodeCetakcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksmodeprintln(s string) {
	for _, b := range s {
		teksmodeCetakchar(uint8(b))
	}
	teksmodeCetakchar(0xa)
}

func teksmodeCetakGalat(s string) {
	for _, b := range s {
		teksmodeCetakcharcol(uint8(b), 4<<4|0xf)
	}
}

func teksmodeCetakerrorln(s string) {
	teksmodeCetakGalat(s)
	teksmodeCetakchar(0xa)
}

func teksmodeCetakchar(char uint8) {
	teksmodeCetakcharcol(char, 0<<4|0xf)
}

func teksmodeCetakcharcol(char uint8, atribut uint8) {
	teksmodecheckfbPindah()
	if char == '\n' {
		fbSekarangBaris++
		fbSekarangcol = 0
		teksmodecheckfbPindah()
	} else if char == '\b' {
		fb[fbSekarangcol+fbSekarangBaris*fbLebar] = 0xf00
		fbSekarangcol = fbSekarangcol - 1
		if fbSekarangcol < 0 {
			fbSekarangcol = 0
		}
	} else if char == '\r' {
		fbSekarangcol = 0
	} else {
		if fbSekarangcol >= fbLebar {
			return
		}
		fb[fbSekarangcol+fbSekarangBaris*fbLebar] = uint16(atribut)<<8 | uint16(char)
		fbSekarangcol++
	}

}

func teksmodeCetakHeksa64(nomor uint64) {
	teksmodeCetakHeksa32(uint32(nomor >> 32))
	teksmodeCetakHeksa32(uint32(nomor))
}

func teksmodeCetakHeksa32(nomor uint32) {
	teksmodeCetakHeksa16(uint16(nomor >> 16))
	teksmodeCetakHeksa16(uint16(nomor))
}

func teksmodeCetakHeksa16(nomor uint16) {
	teksmodeCetakHeksa(uint8(nomor >> 8))
	teksmodeCetakHeksa(uint8(nomor))
}

func teksmodeCetakHeksa(nomor uint8) {
	teksmodeCetakHeksachar(nomor >> 4)
	teksmodeCetakHeksachar(nomor)
}

func teksmodeCetakHeksachar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		teksmodeCetakchar(0x30 + n)
	} else {
		teksmodeCetakchar(0x41 + n - 10)
	}
}
