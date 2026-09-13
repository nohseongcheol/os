package main

import (
	"reflect"
	"unsafe"
)

type てきすともーどwriter struct {
}

func (e てきすともーどwriter) Wかきこみ(p []byte) (int, error) {
	てきすともーどいんさつばいと(p)
	return len(p), nil
}

type てきすともーどえらーwriter struct {
}

func (e てきすともーどえらーwriter) Wかきこみ(p []byte) (int, error) {
	てきすともーどいんさつえらーばいと(p)
	return len(p), nil
}

const (
	fbはば			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	かーそるheight		= 1
	かーそるかいし			= 11
)

var (
	fbげんざいのにちじぎょう	= 0
	fbげんざいのにちじcol	= 0
)

var fb []uint16

func てきすともーどinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbはば * fbheight,
		Cap:	fbはば * fbheight,
		Data:	fbphysaddress,
	}))

}

func てきすともーどenableかーそる() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|かーそるかいし)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|かーそるheight+かーそるかいし)
}

func てきすともーどふかかーそる() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func てきすともーどこうしんかーそる(x int, y int) {
	はいち := y*fbはば + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(はいち&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((はいち>>8)&0xFF))
}

func てきすともーどflushがめん() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func てきすともーどcheckfbいどう() {
	for fbげんざいのにちじぎょう >= fbheight {
		copy(fb[:len(fb)-fbはば], fb[fbはば:])

		for i := 0; i < fbはば; i++ {
			fb[(fbheight-1)*fbはば+i] = 0xf00
		}
		fbげんざいのにちじぎょう--
	}
}

func てきすともーどいんさつcol(s string, ぞくせい uint8) {
	for _, b := range s {
		てきすともーどいんさつcharcol(uint8(b), ぞくせい)
	}
}

func てきすともーどprintlncol(s string, ぞくせい uint8) {
	for _, b := range s {
		てきすともーどいんさつcharcol(uint8(b), ぞくせい)
	}
	てきすともーどいんさつchar(0xa)
}

func てきすともーどいんさつ(s string) {
	for _, b := range s {
		てきすともーどいんさつchar(uint8(b))
	}
}

func てきすともーどいんさつばいと(a []byte) {
	for _, b := range a {
		てきすともーどいんさつchar(uint8(b))
	}
}

func てきすともーどいんさつえらーばいと(a []byte) {
	for _, b := range a {
		てきすともーどいんさつcharcol(uint8(b), 4<<4|0xf)
	}
}

func てきすともーどprintln(s string) {
	for _, b := range s {
		てきすともーどいんさつchar(uint8(b))
	}
	てきすともーどいんさつchar(0xa)
}

func てきすともーどいんさつえらー(s string) {
	for _, b := range s {
		てきすともーどいんさつcharcol(uint8(b), 4<<4|0xf)
	}
}

func てきすともーどいんさつerrorln(s string) {
	てきすともーどいんさつえらー(s)
	てきすともーどいんさつchar(0xa)
}

func てきすともーどいんさつchar(char uint8) {
	てきすともーどいんさつcharcol(char, 0<<4|0xf)
}

func てきすともーどいんさつcharcol(char uint8, ぞくせい uint8) {
	てきすともーどcheckfbいどう()
	if char == '\n' {
		fbげんざいのにちじぎょう++
		fbげんざいのにちじcol = 0
		てきすともーどcheckfbいどう()
	} else if char == '\b' {
		fb[fbげんざいのにちじcol+fbげんざいのにちじぎょう*fbはば] = 0xf00
		fbげんざいのにちじcol = fbげんざいのにちじcol - 1
		if fbげんざいのにちじcol < 0 {
			fbげんざいのにちじcol = 0
		}
	} else if char == '\r' {
		fbげんざいのにちじcol = 0
	} else {
		if fbげんざいのにちじcol >= fbはば {
			return
		}
		fb[fbげんざいのにちじcol+fbげんざいのにちじぎょう*fbはば] = uint16(ぞくせい)<<8 | uint16(char)
		fbげんざいのにちじcol++
	}

}

func てきすともーどいんさつ16すすむ64(number uint64) {
	てきすともーどいんさつ16すすむ32(uint32(number >> 32))
	てきすともーどいんさつ16すすむ32(uint32(number))
}

func てきすともーどいんさつ16すすむ32(number uint32) {
	てきすともーどいんさつ16すすむ16(uint16(number >> 16))
	てきすともーどいんさつ16すすむ16(uint16(number))
}

func てきすともーどいんさつ16すすむ16(number uint16) {
	てきすともーどいんさつ16すすむ(uint8(number >> 8))
	てきすともーどいんさつ16すすむ(uint8(number))
}

func てきすともーどいんさつ16すすむ(number uint8) {
	てきすともーどいんさつ16すすむchar(number >> 4)
	てきすともーどいんさつ16すすむchar(number)
}

func てきすともーどいんさつ16すすむchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		てきすともーどいんさつchar(0x30 + n)
	} else {
		てきすともーどいんさつchar(0x41 + n - 10)
	}
}
