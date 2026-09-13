package main

import (
	"reflect"
	"unsafe"
)

type tekstNAČINwriter struct {
}

func (e tekstNAČINwriter) Zapiši(p []byte) (int, error) {
	tekstNAČINIspisBajtova(p)
	return len(p), nil
}

type tekstNAČINGreškawriter struct {
}

func (e tekstNAČINGreškawriter) Zapiši(p []byte) (int, error) {
	tekstNAČINIspisGreškaBajtova(p)
	return len(p), nil
}

const (
	fbŠirina			= 80
	fbVisina			= 25
	fbphysaddress		uintptr	= 0xb8000
	pokazivačVisina			= 1
	pokazivačPokreni		= 11
)

var (
	fbTrenutnoline	= 0
	fbTrenutnocol	= 0
)

var fb []uint16

func tekstNAČINinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠirina * fbVisina,
		Cap:	fbŠirina * fbVisina,
		Data:	fbphysaddress,
	}))

}

func tekstNAČINenablePokazivač() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|pokazivačPokreni)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|pokazivačVisina+pokazivačPokreni)
}

func tekstNAČINOnemogućiPokazivač() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstNAČINAžurirajPokazivač(x int, y int) {
	pozicija := y*fbŠirina + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozicija&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozicija>>8)&0xFF))
}

func tekstNAČINflushZaslon() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstNAČINcheckfbPremjesti() {
	for fbTrenutnoline >= fbVisina {
		copy(fb[:len(fb)-fbŠirina], fb[fbŠirina:])

		for i := 0; i < fbŠirina; i++ {
			fb[(fbVisina-1)*fbŠirina+i] = 0xf00
		}
		fbTrenutnoline--
	}
}

func tekstNAČINIspiscol(s string, atribut uint8) {
	for _, b := range s {
		tekstNAČINIspischarcol(uint8(b), atribut)
	}
}

func tekstNAČINprintlncol(s string, atribut uint8) {
	for _, b := range s {
		tekstNAČINIspischarcol(uint8(b), atribut)
	}
	tekstNAČINIspischar(0xa)
}

func tekstNAČINIspis(s string) {
	for _, b := range s {
		tekstNAČINIspischar(uint8(b))
	}
}

func tekstNAČINIspisBajtova(a []byte) {
	for _, b := range a {
		tekstNAČINIspischar(uint8(b))
	}
}

func tekstNAČINIspisGreškaBajtova(a []byte) {
	for _, b := range a {
		tekstNAČINIspischarcol(uint8(b), 4<<4|0xf)
	}
}

func tekstNAČINprintln(s string) {
	for _, b := range s {
		tekstNAČINIspischar(uint8(b))
	}
	tekstNAČINIspischar(0xa)
}

func tekstNAČINIspisGreška(s string) {
	for _, b := range s {
		tekstNAČINIspischarcol(uint8(b), 4<<4|0xf)
	}
}

func tekstNAČINIspiserrorln(s string) {
	tekstNAČINIspisGreška(s)
	tekstNAČINIspischar(0xa)
}

func tekstNAČINIspischar(char uint8) {
	tekstNAČINIspischarcol(char, 0<<4|0xf)
}

func tekstNAČINIspischarcol(char uint8, atribut uint8) {
	tekstNAČINcheckfbPremjesti()
	if char == '\n' {
		fbTrenutnoline++
		fbTrenutnocol = 0
		tekstNAČINcheckfbPremjesti()
	} else if char == '\b' {
		fb[fbTrenutnocol+fbTrenutnoline*fbŠirina] = 0xf00
		fbTrenutnocol = fbTrenutnocol - 1
		if fbTrenutnocol < 0 {
			fbTrenutnocol = 0
		}
	} else if char == '\r' {
		fbTrenutnocol = 0
	} else {
		if fbTrenutnocol >= fbŠirina {
			return
		}
		fb[fbTrenutnocol+fbTrenutnoline*fbŠirina] = uint16(atribut)<<8 | uint16(char)
		fbTrenutnocol++
	}

}

func tekstNAČINIspisHeks64(bROJ uint64) {
	tekstNAČINIspisHeks32(uint32(bROJ >> 32))
	tekstNAČINIspisHeks32(uint32(bROJ))
}

func tekstNAČINIspisHeks32(bROJ uint32) {
	tekstNAČINIspisHeks16(uint16(bROJ >> 16))
	tekstNAČINIspisHeks16(uint16(bROJ))
}

func tekstNAČINIspisHeks16(bROJ uint16) {
	tekstNAČINIspisHeks(uint8(bROJ >> 8))
	tekstNAČINIspisHeks(uint8(bROJ))
}

func tekstNAČINIspisHeks(bROJ uint8) {
	tekstNAČINIspisHekschar(bROJ >> 4)
	tekstNAČINIspisHekschar(bROJ)
}

func tekstNAČINIspisHekschar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstNAČINIspischar(0x30 + n)
	} else {
		tekstNAČINIspischar(0x41 + n - 10)
	}
}
