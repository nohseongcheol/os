package main

import (
	"reflect"
	"unsafe"
)

type テキストモードwriter struct {
}

func (e テキストモードwriter) W書込み(p []byte) (int, error) {
	テキストモード印刷バイト(p)
	return len(p), nil
}

type テキストモードエラーwriter struct {
}

func (e テキストモードエラーwriter) W書込み(p []byte) (int, error) {
	テキストモード印刷エラーバイト(p)
	return len(p), nil
}

const (
	fb幅			= 80
	fbheight		= 25
	fbphysaddress	uintptr	= 0xb8000
	カーソルheight		= 1
	カーソル開始			= 11
)

var (
	fb現在の日時行	= 0
	fb現在の日時col	= 0
)

var fb []uint16

func テキストモードinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fb幅 * fbheight,
		Cap:	fb幅 * fbheight,
		Data:	fbphysaddress,
	}))

}

func テキストモードenableカーソル() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|カーソル開始)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|カーソルheight+カーソル開始)
}

func テキストモード不可カーソル() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func テキストモード更新カーソル(x int, y int) {
	配置 := y*fb幅 + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(配置&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((配置>>8)&0xFF))
}

func テキストモードflush画面() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func テキストモードcheckfb移動() {
	for fb現在の日時行 >= fbheight {
		copy(fb[:len(fb)-fb幅], fb[fb幅:])

		for i := 0; i < fb幅; i++ {
			fb[(fbheight-1)*fb幅+i] = 0xf00
		}
		fb現在の日時行--
	}
}

func テキストモード印刷col(s string, 属性 uint8) {
	for _, b := range s {
		テキストモード印刷charcol(uint8(b), 属性)
	}
}

func テキストモードprintlncol(s string, 属性 uint8) {
	for _, b := range s {
		テキストモード印刷charcol(uint8(b), 属性)
	}
	テキストモード印刷char(0xa)
}

func テキストモード印刷(s string) {
	for _, b := range s {
		テキストモード印刷char(uint8(b))
	}
}

func テキストモード印刷バイト(a []byte) {
	for _, b := range a {
		テキストモード印刷char(uint8(b))
	}
}

func テキストモード印刷エラーバイト(a []byte) {
	for _, b := range a {
		テキストモード印刷charcol(uint8(b), 4<<4|0xf)
	}
}

func テキストモードprintln(s string) {
	for _, b := range s {
		テキストモード印刷char(uint8(b))
	}
	テキストモード印刷char(0xa)
}

func テキストモード印刷エラー(s string) {
	for _, b := range s {
		テキストモード印刷charcol(uint8(b), 4<<4|0xf)
	}
}

func テキストモード印刷errorln(s string) {
	テキストモード印刷エラー(s)
	テキストモード印刷char(0xa)
}

func テキストモード印刷char(char uint8) {
	テキストモード印刷charcol(char, 0<<4|0xf)
}

func テキストモード印刷charcol(char uint8, 属性 uint8) {
	テキストモードcheckfb移動()
	if char == '\n' {
		fb現在の日時行++
		fb現在の日時col = 0
		テキストモードcheckfb移動()
	} else if char == '\b' {
		fb[fb現在の日時col+fb現在の日時行*fb幅] = 0xf00
		fb現在の日時col = fb現在の日時col - 1
		if fb現在の日時col < 0 {
			fb現在の日時col = 0
		}
	} else if char == '\r' {
		fb現在の日時col = 0
	} else {
		if fb現在の日時col >= fb幅 {
			return
		}
		fb[fb現在の日時col+fb現在の日時行*fb幅] = uint16(属性)<<8 | uint16(char)
		fb現在の日時col++
	}

}

func テキストモード印刷16進64(number uint64) {
	テキストモード印刷16進32(uint32(number >> 32))
	テキストモード印刷16進32(uint32(number))
}

func テキストモード印刷16進32(number uint32) {
	テキストモード印刷16進16(uint16(number >> 16))
	テキストモード印刷16進16(uint16(number))
}

func テキストモード印刷16進16(number uint16) {
	テキストモード印刷16進(uint8(number >> 8))
	テキストモード印刷16進(uint8(number))
}

func テキストモード印刷16進(number uint8) {
	テキストモード印刷16進char(number >> 4)
	テキストモード印刷16進char(number)
}

func テキストモード印刷16進char(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		テキストモード印刷char(0x30 + n)
	} else {
		テキストモード印刷char(0x41 + n - 10)
	}
}
