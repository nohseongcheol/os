/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"reflect"
	"unsafe"
)

type metinKİPwriter struct {
}

func (e metinKİPwriter) Yazma(p []byte) (int, error) {
	metinKİPYazdırBayt(p)
	return len(p), nil
}

type metinKİPHatawriter struct {
}

func (e metinKİPHatawriter) Yazma(p []byte) (int, error) {
	metinKİPYazdırHataBayt(p)
	return len(p), nil
}

const (
	fbGenişlik		= 80
	fbBaşlık		= 25
	fbphysaddress	uintptr	= 0xb8000
	imleçBaşlık		= 1
	imleçBaşlat		= 11
)

var (
	fbŞuanSatır	= 0
	fbŞuancol	= 0
)

var fb []uint16

func metinKİPinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbGenişlik * fbBaşlık,
		Cap:	fbGenişlik * fbBaşlık,
		Data:	fbphysaddress,
	}))

}

func metinKİPEtkinleştirİmleç() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|imleçBaşlat)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|imleçBaşlık+imleçBaşlat)
}

func metinKİPKapatİmleç() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func metinKİPGüncelleİmleç(x int, y int) {
	konum := y*fbGenişlik + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(konum&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((konum>>8)&0xFF))
}

func metinKİPflushEkran() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func metinKİPcheckfbTaşı() {
	for fbŞuanSatır >= fbBaşlık {
		copy(fb[:len(fb)-fbGenişlik], fb[fbGenişlik:])

		for i := 0; i < fbGenişlik; i++ {
			fb[(fbBaşlık-1)*fbGenişlik+i] = 0xf00
		}
		fbŞuanSatır--
	}
}

func metinKİPYazdırcol(s string, öznitelik uint8) {
	for _, b := range s {
		metinKİPYazdırcharcol(uint8(b), öznitelik)
	}
}

func metinKİPprintlncol(s string, öznitelik uint8) {
	for _, b := range s {
		metinKİPYazdırcharcol(uint8(b), öznitelik)
	}
	metinKİPYazdırchar(0xa)
}

func metinKİPYazdır(s string) {
	for _, b := range s {
		metinKİPYazdırchar(uint8(b))
	}
}

func metinKİPYazdırBayt(a []byte) {
	for _, b := range a {
		metinKİPYazdırchar(uint8(b))
	}
}

func metinKİPYazdırHataBayt(a []byte) {
	for _, b := range a {
		metinKİPYazdırcharcol(uint8(b), 4<<4|0xf)
	}
}

func metinKİPprintln(s string) {
	for _, b := range s {
		metinKİPYazdırchar(uint8(b))
	}
	metinKİPYazdırchar(0xa)
}

func metinKİPYazdırHata(s string) {
	for _, b := range s {
		metinKİPYazdırcharcol(uint8(b), 4<<4|0xf)
	}
}

func metinKİPYazdırerrorln(s string) {
	metinKİPYazdırHata(s)
	metinKİPYazdırchar(0xa)
}

func metinKİPYazdırchar(char uint8) {
	metinKİPYazdırcharcol(char, 0<<4|0xf)
}

func metinKİPYazdırcharcol(char uint8, öznitelik uint8) {
	metinKİPcheckfbTaşı()
	if char == '\n' {
		fbŞuanSatır++
		fbŞuancol = 0
		metinKİPcheckfbTaşı()
	} else if char == '\b' {
		fb[fbŞuancol+fbŞuanSatır*fbGenişlik] = 0xf00
		fbŞuancol = fbŞuancol - 1
		if fbŞuancol < 0 {
			fbŞuancol = 0
		}
	} else if char == '\r' {
		fbŞuancol = 0
	} else {
		if fbŞuancol >= fbGenişlik {
			return
		}
		fb[fbŞuancol+fbŞuanSatır*fbGenişlik] = uint16(öznitelik)<<8 | uint16(char)
		fbŞuancol++
	}

}

func metinKİPYazdırOnaltılık64(sayı uint64) {
	metinKİPYazdırOnaltılık32(uint32(sayı >> 32))
	metinKİPYazdırOnaltılık32(uint32(sayı))
}

func metinKİPYazdırOnaltılık32(sayı uint32) {
	metinKİPYazdırOnaltılık16(uint16(sayı >> 16))
	metinKİPYazdırOnaltılık16(uint16(sayı))
}

func metinKİPYazdırOnaltılık16(sayı uint16) {
	metinKİPYazdırOnaltılık(uint8(sayı >> 8))
	metinKİPYazdırOnaltılık(uint8(sayı))
}

func metinKİPYazdırOnaltılık(sayı uint8) {
	metinKİPYazdırOnaltılıkchar(sayı >> 4)
	metinKİPYazdırOnaltılıkchar(sayı)
}

func metinKİPYazdırOnaltılıkchar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		metinKİPYazdırchar(0x30 + n)
	} else {
		metinKİPYazdırchar(0x41 + n - 10)
	}
}
