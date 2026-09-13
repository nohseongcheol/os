package main

import (
	"reflect"
	"unsafe"
)

type текстREŽIMwriter struct {
}

func (e текстREŽIMwriter) Upis(p []byte) (int, error) {
	текстREŽIMŠtampajBajtova(p)
	return len(p), nil
}

type текстREŽIMГрешкаwriter struct {
}

func (e текстREŽIMГрешкаwriter) Upis(p []byte) (int, error) {
	текстREŽIMŠtampajГрешкаBajtova(p)
	return len(p), nil
}

const (
	fbŠirina			= 80
	fbVisina			= 25
	fbphysaddress		uintptr	= 0xb8000
	показивачVisina			= 1
	показивачPokreni		= 11
)

var (
	fbТренутноред	= 0
	fbТренутноcol	= 0
)

var fb []uint16

func текстREŽIMinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠirina * fbVisina,
		Cap:	fbŠirina * fbVisina,
		Data:	fbphysaddress,
	}))

}

func текстREŽIMукљученоПоказивач() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|показивачPokreni)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|показивачVisina+показивачPokreni)
}

func текстREŽIMИскључиПоказивач() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстREŽIMОсвежиПоказивач(x int, y int) {
	положај := y*fbŠirina + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(положај&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((положај>>8)&0xFF))
}

func текстREŽIMflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстREŽIMcheckfbПремести() {
	for fbТренутноред >= fbVisina {
		copy(fb[:len(fb)-fbŠirina], fb[fbŠirina:])

		for i := 0; i < fbŠirina; i++ {
			fb[(fbVisina-1)*fbŠirina+i] = 0xf00
		}
		fbТренутноред--
	}
}

func текстREŽIMŠtampajcol(s string, atribut uint8) {
	for _, b := range s {
		текстREŽIMŠtampajcharcol(uint8(b), atribut)
	}
}

func текстREŽIMprintlncol(s string, atribut uint8) {
	for _, b := range s {
		текстREŽIMŠtampajcharcol(uint8(b), atribut)
	}
	текстREŽIMŠtampajchar(0xa)
}

func текстREŽIMŠtampaj(s string) {
	for _, b := range s {
		текстREŽIMŠtampajchar(uint8(b))
	}
}

func текстREŽIMŠtampajBajtova(a []byte) {
	for _, b := range a {
		текстREŽIMŠtampajchar(uint8(b))
	}
}

func текстREŽIMŠtampajГрешкаBajtova(a []byte) {
	for _, b := range a {
		текстREŽIMŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстREŽIMprintln(s string) {
	for _, b := range s {
		текстREŽIMŠtampajchar(uint8(b))
	}
	текстREŽIMŠtampajchar(0xa)
}

func текстREŽIMŠtampajГрешка(s string) {
	for _, b := range s {
		текстREŽIMŠtampajcharcol(uint8(b), 4<<4|0xf)
	}
}

func текстREŽIMŠtampajerrorln(s string) {
	текстREŽIMŠtampajГрешка(s)
	текстREŽIMŠtampajchar(0xa)
}

func текстREŽIMŠtampajchar(char uint8) {
	текстREŽIMŠtampajcharcol(char, 0<<4|0xf)
}

func текстREŽIMŠtampajcharcol(char uint8, atribut uint8) {
	текстREŽIMcheckfbПремести()
	if char == '\n' {
		fbТренутноред++
		fbТренутноcol = 0
		текстREŽIMcheckfbПремести()
	} else if char == '\b' {
		fb[fbТренутноcol+fbТренутноред*fbŠirina] = 0xf00
		fbТренутноcol = fbТренутноcol - 1
		if fbТренутноcol < 0 {
			fbТренутноcol = 0
		}
	} else if char == '\r' {
		fbТренутноcol = 0
	} else {
		if fbТренутноcol >= fbŠirina {
			return
		}
		fb[fbТренутноcol+fbТренутноред*fbŠirina] = uint16(atribut)<<8 | uint16(char)
		fbТренутноcol++
	}

}

func текстREŽIMŠtampajHeksadecimalno64(број uint64) {
	текстREŽIMŠtampajHeksadecimalno32(uint32(број >> 32))
	текстREŽIMŠtampajHeksadecimalno32(uint32(број))
}

func текстREŽIMŠtampajHeksadecimalno32(број uint32) {
	текстREŽIMŠtampajHeksadecimalno16(uint16(број >> 16))
	текстREŽIMŠtampajHeksadecimalno16(uint16(број))
}

func текстREŽIMŠtampajHeksadecimalno16(број uint16) {
	текстREŽIMŠtampajHeksadecimalno(uint8(број >> 8))
	текстREŽIMŠtampajHeksadecimalno(uint8(број))
}

func текстREŽIMŠtampajHeksadecimalno(број uint8) {
	текстREŽIMŠtampajHeksadecimalnochar(број >> 4)
	текстREŽIMŠtampajHeksadecimalnochar(број)
}

func текстREŽIMŠtampajHeksadecimalnochar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстREŽIMŠtampajchar(0x30 + n)
	} else {
		текстREŽIMŠtampajchar(0x41 + n - 10)
	}
}
