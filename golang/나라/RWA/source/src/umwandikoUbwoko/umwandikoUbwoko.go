package main

import (
	"reflect"
	"unsafe"
)

type umwandikoUbwokowriter struct {
}

func (e umwandikoUbwokowriter) Kwandika(p []byte) (int, error) {
	umwandikoUbwokoGucapaBayite(p)
	return len(p), nil
}

type umwandikoUbwokoIkosawriter struct {
}

func (e umwandikoUbwokoIkosawriter) Kwandika(p []byte) (int, error) {
	umwandikoUbwokoGucapaIkosaBayite(p)
	return len(p), nil
}

const (
	fbUbugari			= 80
	fbUbuhagarike			= 25
	fbphysaddress		uintptr	= 0xb8000
	cursorUbuhagarike		= 1
	cursorstart			= 11
)

var (
	fbcurrentline	= 0
	fbcurrentcol	= 0
)

var fb []uint16

func umwandikoUbwokoinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbUbugari * fbUbuhagarike,
		Cap:	fbUbugari * fbUbuhagarike,
		Data:	fbphysaddress,
	}))

}

func umwandikoUbwokoenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorstart)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorUbuhagarike+cursorstart)
}

func umwandikoUbwokodisablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func umwandikoUbwokoKuvugururacursor(x int, y int) {
	position := y*fbUbugari + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func umwandikoUbwokoflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func umwandikoUbwokocheckfbmove() {
	for fbcurrentline >= fbUbuhagarike {
		copy(fb[:len(fb)-fbUbugari], fb[fbUbugari:])

		for i := 0; i < fbUbugari; i++ {
			fb[(fbUbuhagarike-1)*fbUbugari+i] = 0xf00
		}
		fbcurrentline--
	}
}

func umwandikoUbwokoGucapacol(s string, attribute uint8) {
	for _, b := range s {
		umwandikoUbwokoGucapacharcol(uint8(b), attribute)
	}
}

func umwandikoUbwokoprintlncol(s string, attribute uint8) {
	for _, b := range s {
		umwandikoUbwokoGucapacharcol(uint8(b), attribute)
	}
	umwandikoUbwokoGucapachar(0xa)
}

func umwandikoUbwokoGucapa(s string) {
	for _, b := range s {
		umwandikoUbwokoGucapachar(uint8(b))
	}
}

func umwandikoUbwokoGucapaBayite(a []byte) {
	for _, b := range a {
		umwandikoUbwokoGucapachar(uint8(b))
	}
}

func umwandikoUbwokoGucapaIkosaBayite(a []byte) {
	for _, b := range a {
		umwandikoUbwokoGucapacharcol(uint8(b), 4<<4|0xf)
	}
}

func umwandikoUbwokoprintln(s string) {
	for _, b := range s {
		umwandikoUbwokoGucapachar(uint8(b))
	}
	umwandikoUbwokoGucapachar(0xa)
}

func umwandikoUbwokoGucapaIkosa(s string) {
	for _, b := range s {
		umwandikoUbwokoGucapacharcol(uint8(b), 4<<4|0xf)
	}
}

func umwandikoUbwokoGucapaerrorln(s string) {
	umwandikoUbwokoGucapaIkosa(s)
	umwandikoUbwokoGucapachar(0xa)
}

func umwandikoUbwokoGucapachar(char uint8) {
	umwandikoUbwokoGucapacharcol(char, 0<<4|0xf)
}

func umwandikoUbwokoGucapacharcol(char uint8, attribute uint8) {
	umwandikoUbwokocheckfbmove()
	if char == '\n' {
		fbcurrentline++
		fbcurrentcol = 0
		umwandikoUbwokocheckfbmove()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentline*fbUbugari] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbUbugari {
			return
		}
		fb[fbcurrentcol+fbcurrentline*fbUbugari] = uint16(attribute)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func umwandikoUbwokoGucapahex64(number uint64) {
	umwandikoUbwokoGucapahex32(uint32(number >> 32))
	umwandikoUbwokoGucapahex32(uint32(number))
}

func umwandikoUbwokoGucapahex32(number uint32) {
	umwandikoUbwokoGucapahex16(uint16(number >> 16))
	umwandikoUbwokoGucapahex16(uint16(number))
}

func umwandikoUbwokoGucapahex16(number uint16) {
	umwandikoUbwokoGucapahex(uint8(number >> 8))
	umwandikoUbwokoGucapahex(uint8(number))
}

func umwandikoUbwokoGucapahex(number uint8) {
	umwandikoUbwokoGucapahexchar(number >> 4)
	umwandikoUbwokoGucapahexchar(number)
}

func umwandikoUbwokoGucapahexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		umwandikoUbwokoGucapachar(0x30 + n)
	} else {
		umwandikoUbwokoGucapachar(0x41 + n - 10)
	}
}
