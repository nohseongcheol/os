package main

import (
	"reflect"
	"unsafe"
)

type متنmodewriter struct {
}

func (e متنmodewriter) Wلکھیں(p []byte) (int, error) {
	متنmodeچھاپیںبائٹس(p)
	return len(p), nil
}

type متنmodeغلطیwriter struct {
}

func (e متنmodeغلطیwriter) Wلکھیں(p []byte) (int, error) {
	متنmodeچھاپیںغلطیبائٹس(p)
	return len(p), nil
}

const (
	fbچوڑائی		= 80
	fbاونچائی		= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorاونچائی		= 1
	cursorچلائیں		= 11
)

var (
	fbحالیہline	= 0
	fbحالیہcol	= 0
)

var fb []uint16

func متنmodeinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbچوڑائی * fbاونچائی,
		Cap:	fbچوڑائی * fbاونچائی,
		Data:	fbphysaddress,
	}))

}

func متنmodeenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorچلائیں)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorاونچائی+cursorچلائیں)
}

func متنmodeمعطلکریںcursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func متنmodeتجدیدکریںcursor(x int, y int) {
	position := y*fbچوڑائی + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(position&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((position>>8)&0xFF))
}

func متنmodeflushscreen() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func متنmodecheckfbمنتقلکریں() {
	for fbحالیہline >= fbاونچائی {
		copy(fb[:len(fb)-fbچوڑائی], fb[fbچوڑائی:])

		for i := 0; i < fbچوڑائی; i++ {
			fb[(fbاونچائی-1)*fbچوڑائی+i] = 0xf00
		}
		fbحالیہline--
	}
}

func متنmodeچھاپیںcol(s string, وصف uint8) {
	for _, b := range s {
		متنmodeچھاپیںcharcol(uint8(b), وصف)
	}
}

func متنmodeprintlncol(s string, وصف uint8) {
	for _, b := range s {
		متنmodeچھاپیںcharcol(uint8(b), وصف)
	}
	متنmodeچھاپیںchar(0xa)
}

func متنmodeچھاپیں(s string) {
	for _, b := range s {
		متنmodeچھاپیںchar(uint8(b))
	}
}

func متنmodeچھاپیںبائٹس(a []byte) {
	for _, b := range a {
		متنmodeچھاپیںchar(uint8(b))
	}
}

func متنmodeچھاپیںغلطیبائٹس(a []byte) {
	for _, b := range a {
		متنmodeچھاپیںcharcol(uint8(b), 4<<4|0xf)
	}
}

func متنmodeprintln(s string) {
	for _, b := range s {
		متنmodeچھاپیںchar(uint8(b))
	}
	متنmodeچھاپیںchar(0xa)
}

func متنmodeچھاپیںغلطی(s string) {
	for _, b := range s {
		متنmodeچھاپیںcharcol(uint8(b), 4<<4|0xf)
	}
}

func متنmodeچھاپیںerrorln(s string) {
	متنmodeچھاپیںغلطی(s)
	متنmodeچھاپیںchar(0xa)
}

func متنmodeچھاپیںchar(char uint8) {
	متنmodeچھاپیںcharcol(char, 0<<4|0xf)
}

func متنmodeچھاپیںcharcol(char uint8, وصف uint8) {
	متنmodecheckfbمنتقلکریں()
	if char == '\n' {
		fbحالیہline++
		fbحالیہcol = 0
		متنmodecheckfbمنتقلکریں()
	} else if char == '\b' {
		fb[fbحالیہcol+fbحالیہline*fbچوڑائی] = 0xf00
		fbحالیہcol = fbحالیہcol - 1
		if fbحالیہcol < 0 {
			fbحالیہcol = 0
		}
	} else if char == '\r' {
		fbحالیہcol = 0
	} else {
		if fbحالیہcol >= fbچوڑائی {
			return
		}
		fb[fbحالیہcol+fbحالیہline*fbچوڑائی] = uint16(وصف)<<8 | uint16(char)
		fbحالیہcol++
	}

}

func متنmodeچھاپیںhex64(number uint64) {
	متنmodeچھاپیںhex32(uint32(number >> 32))
	متنmodeچھاپیںhex32(uint32(number))
}

func متنmodeچھاپیںhex32(number uint32) {
	متنmodeچھاپیںhex16(uint16(number >> 16))
	متنmodeچھاپیںhex16(uint16(number))
}

func متنmodeچھاپیںhex16(number uint16) {
	متنmodeچھاپیںhex(uint8(number >> 8))
	متنmodeچھاپیںhex(uint8(number))
}

func متنmodeچھاپیںhex(number uint8) {
	متنmodeچھاپیںhexchar(number >> 4)
	متنmodeچھاپیںhexchar(number)
}

func متنmodeچھاپیںhexchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		متنmodeچھاپیںchar(0x30 + n)
	} else {
		متنmodeچھاپیںchar(0x41 + n - 10)
	}
}
