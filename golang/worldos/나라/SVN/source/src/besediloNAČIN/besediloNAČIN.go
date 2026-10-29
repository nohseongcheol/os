/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type besediloNAČINwriter struct {
}

func (e besediloNAČINwriter) Pisanje(p []byte) (int, error) {
	besediloNAČINNatisniBajtov(p)
	return len(p), nil
}

type besediloNAČINNapakawriter struct {
}

func (e besediloNAČINNapakawriter) Pisanje(p []byte) (int, error) {
	besediloNAČINNatisniNapakaBajtov(p)
	return len(p), nil
}

const (
	fbŠirina		= 80
	fbVišina		= 25
	fbphysaddress	uintptr	= 0xb8000
	kazalecVišina		= 1
	kazalecZačni		= 11
)

var (
	fbcurrentVrstica	= 0
	fbcurrentcol		= 0
)

var fb []uint16

func besediloNAČINinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbŠirina * fbVišina,
		Cap:	fbŠirina * fbVišina,
		Data:	fbphysaddress,
	}))

}

func besediloNAČINOmogočiKazalec() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|kazalecZačni)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|kazalecVišina+kazalecZačni)
}

func besediloNAČINOnemogočiKazalec() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func besediloNAČINPosodobiKazalec(x int, y int) {
	položaj := y*fbŠirina + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(položaj&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((položaj>>8)&0xFF))
}

func besediloNAČINflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func besediloNAČINcheckfbPremakni() {
	for fbcurrentVrstica >= fbVišina {
		copy(fb[:len(fb)-fbŠirina], fb[fbŠirina:])

		for i := 0; i < fbŠirina; i++ {
			fb[(fbVišina-1)*fbŠirina+i] = 0xf00
		}
		fbcurrentVrstica--
	}
}

func besediloNAČINNatisnicol(s string, atribut uint8) {
	for _, b := range s {
		besediloNAČINNatisnicharcol(uint8(b), atribut)
	}
}

func besediloNAČINprintlncol(s string, atribut uint8) {
	for _, b := range s {
		besediloNAČINNatisnicharcol(uint8(b), atribut)
	}
	besediloNAČINNatisnichar(0xa)
}

func besediloNAČINNatisni(s string) {
	for _, b := range s {
		besediloNAČINNatisnichar(uint8(b))
	}
}

func besediloNAČINNatisniBajtov(a []byte) {
	for _, b := range a {
		besediloNAČINNatisnichar(uint8(b))
	}
}

func besediloNAČINNatisniNapakaBajtov(a []byte) {
	for _, b := range a {
		besediloNAČINNatisnicharcol(uint8(b), 4<<4|0xf)
	}
}

func besediloNAČINprintln(s string) {
	for _, b := range s {
		besediloNAČINNatisnichar(uint8(b))
	}
	besediloNAČINNatisnichar(0xa)
}

func besediloNAČINNatisniNapaka(s string) {
	for _, b := range s {
		besediloNAČINNatisnicharcol(uint8(b), 4<<4|0xf)
	}
}

func besediloNAČINNatisnierrorln(s string) {
	besediloNAČINNatisniNapaka(s)
	besediloNAČINNatisnichar(0xa)
}

func besediloNAČINNatisnichar(char uint8) {
	besediloNAČINNatisnicharcol(char, 0<<4|0xf)
}

func besediloNAČINNatisnicharcol(char uint8, atribut uint8) {
	besediloNAČINcheckfbPremakni()
	if char == '\n' {
		fbcurrentVrstica++
		fbcurrentcol = 0
		besediloNAČINcheckfbPremakni()
	} else if char == '\b' {
		fb[fbcurrentcol+fbcurrentVrstica*fbŠirina] = 0xf00
		fbcurrentcol = fbcurrentcol - 1
		if fbcurrentcol < 0 {
			fbcurrentcol = 0
		}
	} else if char == '\r' {
		fbcurrentcol = 0
	} else {
		if fbcurrentcol >= fbŠirina {
			return
		}
		fb[fbcurrentcol+fbcurrentVrstica*fbŠirina] = uint16(atribut)<<8 | uint16(char)
		fbcurrentcol++
	}

}

func besediloNAČINNatisniŠestnajstiško64(številka uint64) {
	besediloNAČINNatisniŠestnajstiško32(uint32(številka >> 32))
	besediloNAČINNatisniŠestnajstiško32(uint32(številka))
}

func besediloNAČINNatisniŠestnajstiško32(številka uint32) {
	besediloNAČINNatisniŠestnajstiško16(uint16(številka >> 16))
	besediloNAČINNatisniŠestnajstiško16(uint16(številka))
}

func besediloNAČINNatisniŠestnajstiško16(številka uint16) {
	besediloNAČINNatisniŠestnajstiško(uint8(številka >> 8))
	besediloNAČINNatisniŠestnajstiško(uint8(številka))
}

func besediloNAČINNatisniŠestnajstiško(številka uint8) {
	besediloNAČINNatisniŠestnajstiškochar(številka >> 4)
	besediloNAČINNatisniŠestnajstiškochar(številka)
}

func besediloNAČINNatisniŠestnajstiškochar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		besediloNAČINNatisnichar(0x30 + n)
	} else {
		besediloNAČINNatisnichar(0x41 + n - 10)
	}
}
