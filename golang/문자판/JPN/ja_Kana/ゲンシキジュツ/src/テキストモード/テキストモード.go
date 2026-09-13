package main

import (
	"reflect"
	"unsafe"
)

type テキストモードwriter struct {
}

func (e テキストモードwriter) Wカキコミ(p []byte) (int, error) {
	テキストモードインサツバイト(p)
	return len(p), nil
}

type テキストモードエラーwriter struct {
}

func (e テキストモードエラーwriter) Wカキコミ(p []byte) (int, error) {
	テキストモードインサツエラーバイト(p)
	return len(p), nil
}

const (
	fbハバ			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	カーソルheight		= 1
	カーソルカイシ			= 11
)

var (
	fbゲンザイノニチジギョウ	= 0
	fbゲンザイノニチジcol	= 0
)

var fb []uint16

func テキストモードinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbハバ * fbheight,
		Cap:	fbハバ * fbheight,
		Data:	fbphysaddress,
	}))

}

func テキストモードenableカーソル() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|カーソルカイシ)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|カーソルheight+カーソルカイシ)
}

func テキストモードフカカーソル() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func テキストモードコウシンカーソル(x int, y int) {
	ハイチ := y*fbハバ + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(ハイチ&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((ハイチ>>8)&0xFF))
}

func テキストモードflushガメン() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func テキストモードcheckfbイドウ() {
	for fbゲンザイノニチジギョウ >= fbheight {
		copy(fb[:len(fb)-fbハバ], fb[fbハバ:])

		for i := 0; i < fbハバ; i++ {
			fb[(fbheight-1)*fbハバ+i] = 0xf00
		}
		fbゲンザイノニチジギョウ--
	}
}

func テキストモードインサツcol(s string, ゾクセイ uint8) {
	for _, b := range s {
		テキストモードインサツcharcol(uint8(b), ゾクセイ)
	}
}

func テキストモードprintlncol(s string, ゾクセイ uint8) {
	for _, b := range s {
		テキストモードインサツcharcol(uint8(b), ゾクセイ)
	}
	テキストモードインサツchar(0xa)
}

func テキストモードインサツ(s string) {
	for _, b := range s {
		テキストモードインサツchar(uint8(b))
	}
}

func テキストモードインサツバイト(a []byte) {
	for _, b := range a {
		テキストモードインサツchar(uint8(b))
	}
}

func テキストモードインサツエラーバイト(a []byte) {
	for _, b := range a {
		テキストモードインサツcharcol(uint8(b), 4<<4|0xf)
	}
}

func テキストモードprintln(s string) {
	for _, b := range s {
		テキストモードインサツchar(uint8(b))
	}
	テキストモードインサツchar(0xa)
}

func テキストモードインサツエラー(s string) {
	for _, b := range s {
		テキストモードインサツcharcol(uint8(b), 4<<4|0xf)
	}
}

func テキストモードインサツerrorln(s string) {
	テキストモードインサツエラー(s)
	テキストモードインサツchar(0xa)
}

func テキストモードインサツchar(char uint8) {
	テキストモードインサツcharcol(char, 0<<4|0xf)
}

func テキストモードインサツcharcol(char uint8, ゾクセイ uint8) {
	テキストモードcheckfbイドウ()
	if char == '\n' {
		fbゲンザイノニチジギョウ++
		fbゲンザイノニチジcol = 0
		テキストモードcheckfbイドウ()
	} else if char == '\b' {
		fb[fbゲンザイノニチジcol+fbゲンザイノニチジギョウ*fbハバ] = 0xf00
		fbゲンザイノニチジcol = fbゲンザイノニチジcol - 1
		if fbゲンザイノニチジcol < 0 {
			fbゲンザイノニチジcol = 0
		}
	} else if char == '\r' {
		fbゲンザイノニチジcol = 0
	} else {
		if fbゲンザイノニチジcol >= fbハバ {
			return
		}
		fb[fbゲンザイノニチジcol+fbゲンザイノニチジギョウ*fbハバ] = uint16(ゾクセイ)<<8 | uint16(char)
		fbゲンザイノニチジcol++
	}

}

func テキストモードインサツ16ススム64(number uint64) {
	テキストモードインサツ16ススム32(uint32(number >> 32))
	テキストモードインサツ16ススム32(uint32(number))
}

func テキストモードインサツ16ススム32(number uint32) {
	テキストモードインサツ16ススム16(uint16(number >> 16))
	テキストモードインサツ16ススム16(uint16(number))
}

func テキストモードインサツ16ススム16(number uint16) {
	テキストモードインサツ16ススム(uint8(number >> 8))
	テキストモードインサツ16ススム(uint8(number))
}

func テキストモードインサツ16ススム(number uint8) {
	テキストモードインサツ16ススムchar(number >> 4)
	テキストモードインサツ16ススムchar(number)
}

func テキストモードインサツ16ススムchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		テキストモードインサツchar(0x30 + n)
	} else {
		テキストモードインサツchar(0x41 + n - 10)
	}
}
