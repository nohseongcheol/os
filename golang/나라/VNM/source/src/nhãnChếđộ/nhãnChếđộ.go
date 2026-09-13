package main

import (
	"reflect"
	"unsafe"
)

type nhãnChếđộwriter struct {
}

func (e nhãnChếđộwriter) Ghi(p []byte) (int, error) {
	nhãnChếđộInByte(p)
	return len(p), nil
}

type nhãnChếđộLỗiwriter struct {
}

func (e nhãnChếđộLỗiwriter) Ghi(p []byte) (int, error) {
	nhãnChếđộInLỗiByte(p)
	return len(p), nil
}

const (
	fbĐộrộng		= 80
	fbĐộcao			= 25
	fbphysaddress	uintptr	= 0xb8000
	cursorĐộcao		= 1
	cursorChạy		= 11
)

var (
	fbHiệnhànhline	= 0
	fbHiệnhànhcol	= 0
)

var fb []uint16

func nhãnChếđộinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbĐộrộng * fbĐộcao,
		Cap:	fbĐộrộng * fbĐộcao,
		Data:	fbphysaddress,
	}))

}

func nhãnChếđộenablecursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|cursorChạy)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|cursorĐộcao+cursorChạy)
}

func nhãnChếđộVôhiệuhóacursor() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func nhãnChếđộCậpnhậtcursor(x int, y int) {
	vịtrí := y*fbĐộrộng + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(vịtrí&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((vịtrí>>8)&0xFF))
}

func nhãnChếđộflushMànhình() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func nhãnChếđộcheckfbDichuyển() {
	for fbHiệnhànhline >= fbĐộcao {
		copy(fb[:len(fb)-fbĐộrộng], fb[fbĐộrộng:])

		for i := 0; i < fbĐộrộng; i++ {
			fb[(fbĐộcao-1)*fbĐộrộng+i] = 0xf00
		}
		fbHiệnhànhline--
	}
}

func nhãnChếđộIncol(s string, thuộctính uint8) {
	for _, b := range s {
		nhãnChếđộIncharcol(uint8(b), thuộctính)
	}
}

func nhãnChếđộprintlncol(s string, thuộctính uint8) {
	for _, b := range s {
		nhãnChếđộIncharcol(uint8(b), thuộctính)
	}
	nhãnChếđộInchar(0xa)
}

func nhãnChếđộIn(s string) {
	for _, b := range s {
		nhãnChếđộInchar(uint8(b))
	}
}

func nhãnChếđộInByte(a []byte) {
	for _, b := range a {
		nhãnChếđộInchar(uint8(b))
	}
}

func nhãnChếđộInLỗiByte(a []byte) {
	for _, b := range a {
		nhãnChếđộIncharcol(uint8(b), 4<<4|0xf)
	}
}

func nhãnChếđộprintln(s string) {
	for _, b := range s {
		nhãnChếđộInchar(uint8(b))
	}
	nhãnChếđộInchar(0xa)
}

func nhãnChếđộInLỗi(s string) {
	for _, b := range s {
		nhãnChếđộIncharcol(uint8(b), 4<<4|0xf)
	}
}

func nhãnChếđộInerrorln(s string) {
	nhãnChếđộInLỗi(s)
	nhãnChếđộInchar(0xa)
}

func nhãnChếđộInchar(char uint8) {
	nhãnChếđộIncharcol(char, 0<<4|0xf)
}

func nhãnChếđộIncharcol(char uint8, thuộctính uint8) {
	nhãnChếđộcheckfbDichuyển()
	if char == '\n' {
		fbHiệnhànhline++
		fbHiệnhànhcol = 0
		nhãnChếđộcheckfbDichuyển()
	} else if char == '\b' {
		fb[fbHiệnhànhcol+fbHiệnhànhline*fbĐộrộng] = 0xf00
		fbHiệnhànhcol = fbHiệnhànhcol - 1
		if fbHiệnhànhcol < 0 {
			fbHiệnhànhcol = 0
		}
	} else if char == '\r' {
		fbHiệnhànhcol = 0
	} else {
		if fbHiệnhànhcol >= fbĐộrộng {
			return
		}
		fb[fbHiệnhànhcol+fbHiệnhànhline*fbĐộrộng] = uint16(thuộctính)<<8 | uint16(char)
		fbHiệnhànhcol++
	}

}

func nhãnChếđộInThậplục64(sỐ uint64) {
	nhãnChếđộInThậplục32(uint32(sỐ >> 32))
	nhãnChếđộInThậplục32(uint32(sỐ))
}

func nhãnChếđộInThậplục32(sỐ uint32) {
	nhãnChếđộInThậplục16(uint16(sỐ >> 16))
	nhãnChếđộInThậplục16(uint16(sỐ))
}

func nhãnChếđộInThậplục16(sỐ uint16) {
	nhãnChếđộInThậplục(uint8(sỐ >> 8))
	nhãnChếđộInThậplục(uint8(sỐ))
}

func nhãnChếđộInThậplục(sỐ uint8) {
	nhãnChếđộInThậplụcchar(sỐ >> 4)
	nhãnChếđộInThậplụcchar(sỐ)
}

func nhãnChếđộInThậplụcchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		nhãnChếđộInchar(0x30 + n)
	} else {
		nhãnChếđộInchar(0x41 + n - 10)
	}
}
