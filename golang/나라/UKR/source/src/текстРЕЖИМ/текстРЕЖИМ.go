package main

import (
	"reflect"
	"unsafe"
)

type текстРЕЖИМwriter struct {
}

func (e текстРЕЖИМwriter) Запис(p []byte) (int, error) {
	текстРЕЖИМДрукБайт(p)
	return len(p), nil
}

type текстРЕЖИМПомилкаwriter struct {
}

func (e текстРЕЖИМПомилкаwriter) Запис(p []byte) (int, error) {
	текстРЕЖИМДрукПомилкаБайт(p)
	return len(p), nil
}

const (
	fbШирина		= 80
	fbВисота		= 25
	fbphysАдреса	uintptr	= 0xb8000
	курсорВисота		= 1
	курсорЗапустити		= 11
)

var (
	fbПоточнаРядок	= 0
	fbПоточнакол	= 0
)

var fb []uint16

func текстРЕЖИМinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbШирина * fbВисота,
		Cap:	fbШирина * fbВисота,
		Data:	fbphysАдреса,
	}))

}

func текстРЕЖИМДозволитиКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|курсорЗапустити)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|курсорВисота+курсорЗапустити)
}

func текстРЕЖИМВимкнутиКурсор() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func текстРЕЖИМОновитиКурсор(x int, y int) {
	позиція := y*fbШирина + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(позиція&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((позиція>>8)&0xFF))
}

func текстРЕЖИМflushЕкран() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func текстРЕЖИМcheckfbПеремістити() {
	for fbПоточнаРядок >= fbВисота {
		copy(fb[:len(fb)-fbШирина], fb[fbШирина:])

		for i := 0; i < fbШирина; i++ {
			fb[(fbВисота-1)*fbШирина+i] = 0xf00
		}
		fbПоточнаРядок--
	}
}

func текстРЕЖИМДруккол(s string, ознака uint8) {
	for _, b := range s {
		текстРЕЖИМДрукcharкол(uint8(b), ознака)
	}
}

func текстРЕЖИМprintlnкол(s string, ознака uint8) {
	for _, b := range s {
		текстРЕЖИМДрукcharкол(uint8(b), ознака)
	}
	текстРЕЖИМДрукchar(0xa)
}

func текстРЕЖИМДрук(s string) {
	for _, b := range s {
		текстРЕЖИМДрукchar(uint8(b))
	}
}

func текстРЕЖИМДрукБайт(a []byte) {
	for _, b := range a {
		текстРЕЖИМДрукchar(uint8(b))
	}
}

func текстРЕЖИМДрукПомилкаБайт(a []byte) {
	for _, b := range a {
		текстРЕЖИМДрукcharкол(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМprintln(s string) {
	for _, b := range s {
		текстРЕЖИМДрукchar(uint8(b))
	}
	текстРЕЖИМДрукchar(0xa)
}

func текстРЕЖИМДрукПомилка(s string) {
	for _, b := range s {
		текстРЕЖИМДрукcharкол(uint8(b), 4<<4|0xf)
	}
}

func текстРЕЖИМДрукerrorln(s string) {
	текстРЕЖИМДрукПомилка(s)
	текстРЕЖИМДрукchar(0xa)
}

func текстРЕЖИМДрукchar(char uint8) {
	текстРЕЖИМДрукcharкол(char, 0<<4|0xf)
}

func текстРЕЖИМДрукcharкол(char uint8, ознака uint8) {
	текстРЕЖИМcheckfbПеремістити()
	if char == '\n' {
		fbПоточнаРядок++
		fbПоточнакол = 0
		текстРЕЖИМcheckfbПеремістити()
	} else if char == '\b' {
		fb[fbПоточнакол+fbПоточнаРядок*fbШирина] = 0xf00
		fbПоточнакол = fbПоточнакол - 1
		if fbПоточнакол < 0 {
			fbПоточнакол = 0
		}
	} else if char == '\r' {
		fbПоточнакол = 0
	} else {
		if fbПоточнакол >= fbШирина {
			return
		}
		fb[fbПоточнакол+fbПоточнаРядок*fbШирина] = uint16(ознака)<<8 | uint16(char)
		fbПоточнакол++
	}

}

func текстРЕЖИМДрукШістнадцяткова64(число uint64) {
	текстРЕЖИМДрукШістнадцяткова32(uint32(число >> 32))
	текстРЕЖИМДрукШістнадцяткова32(uint32(число))
}

func текстРЕЖИМДрукШістнадцяткова32(число uint32) {
	текстРЕЖИМДрукШістнадцяткова16(uint16(число >> 16))
	текстРЕЖИМДрукШістнадцяткова16(uint16(число))
}

func текстРЕЖИМДрукШістнадцяткова16(число uint16) {
	текстРЕЖИМДрукШістнадцяткова(uint8(число >> 8))
	текстРЕЖИМДрукШістнадцяткова(uint8(число))
}

func текстРЕЖИМДрукШістнадцяткова(число uint8) {
	текстРЕЖИМДрукШістнадцятковаchar(число >> 4)
	текстРЕЖИМДрукШістнадцятковаchar(число)
}

func текстРЕЖИМДрукШістнадцятковаchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		текстРЕЖИМДрукchar(0x30 + n)
	} else {
		текстРЕЖИМДрукchar(0x41 + n - 10)
	}
}
