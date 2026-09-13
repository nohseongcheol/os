package main

import (
	"reflect"
	"unsafe"
)

type tekstasREŽIMASwriter struct {
}

func (e tekstasREŽIMASwriter) Rašymas(p []byte) (int, error) {
	tekstasREŽIMASSpausdintiBaitų(p)
	return len(p), nil
}

type tekstasREŽIMASKlaidawriter struct {
}

func (e tekstasREŽIMASKlaidawriter) Rašymas(p []byte) (int, error) {
	tekstasREŽIMASSpausdintiKlaidaBaitų(p)
	return len(p), nil
}

const (
	fbPlotis			= 80
	fbAukštis			= 25
	fbphysaddress		uintptr	= 0xb8000
	žymeklisAukštis			= 1
	žymeklisPaleisti		= 11
)

var (
	fbDabartinisEilutė	= 0
	fbDabartiniscol		= 0
)

var fb []uint16

func tekstasREŽIMASinit() {
	fb = *(*[]uint16)(unsafe.Pointer(&reflect.SliceHeader{
		Len:	fbPlotis * fbAukštis,
		Cap:	fbPlotis * fbAukštis,
		Data:	fbphysaddress,
	}))

}

func tekstasREŽIMASĮjungtiŽymeklis() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, (Inb(0x3D5)&0xC0)|žymeklisPaleisti)

	Outb(0x3D4, 0x0B)
	Outb(0x3D5, (Inb(0x3D5)&0xE0)|žymeklisAukštis+žymeklisPaleisti)
}

func tekstasREŽIMASIšjungtiŽymeklis() {
	Outb(0x3D4, 0x0A)
	Outb(0x3D5, 0x20)
}

func tekstasREŽIMASAtnaujintiŽymeklis(x int, y int) {
	pozicija := y*fbPlotis + x
	Outb(0x3D4, 0x0F)
	Outb(0x3D5, uint8(pozicija&0xFF))
	Outb(0x3D4, 0x0E)
	Outb(0x3D5, uint8((pozicija>>8)&0xFF))
}

func tekstasREŽIMASflushEkranas() {
	for i := range fb {
		fb[i] = 0xf00
	}
}

func tekstasREŽIMAScheckfbPerkelti() {
	for fbDabartinisEilutė >= fbAukštis {
		copy(fb[:len(fb)-fbPlotis], fb[fbPlotis:])

		for i := 0; i < fbPlotis; i++ {
			fb[(fbAukštis-1)*fbPlotis+i] = 0xf00
		}
		fbDabartinisEilutė--
	}
}

func tekstasREŽIMASSpausdinticol(s string, atributas uint8) {
	for _, b := range s {
		tekstasREŽIMASSpausdinticharcol(uint8(b), atributas)
	}
}

func tekstasREŽIMASprintlncol(s string, atributas uint8) {
	for _, b := range s {
		tekstasREŽIMASSpausdinticharcol(uint8(b), atributas)
	}
	tekstasREŽIMASSpausdintichar(0xa)
}

func tekstasREŽIMASSpausdinti(s string) {
	for _, b := range s {
		tekstasREŽIMASSpausdintichar(uint8(b))
	}
}

func tekstasREŽIMASSpausdintiBaitų(a []byte) {
	for _, b := range a {
		tekstasREŽIMASSpausdintichar(uint8(b))
	}
}

func tekstasREŽIMASSpausdintiKlaidaBaitų(a []byte) {
	for _, b := range a {
		tekstasREŽIMASSpausdinticharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstasREŽIMASprintln(s string) {
	for _, b := range s {
		tekstasREŽIMASSpausdintichar(uint8(b))
	}
	tekstasREŽIMASSpausdintichar(0xa)
}

func tekstasREŽIMASSpausdintiKlaida(s string) {
	for _, b := range s {
		tekstasREŽIMASSpausdinticharcol(uint8(b), 4<<4|0xf)
	}
}

func tekstasREŽIMASSpausdintierrorln(s string) {
	tekstasREŽIMASSpausdintiKlaida(s)
	tekstasREŽIMASSpausdintichar(0xa)
}

func tekstasREŽIMASSpausdintichar(char uint8) {
	tekstasREŽIMASSpausdinticharcol(char, 0<<4|0xf)
}

func tekstasREŽIMASSpausdinticharcol(char uint8, atributas uint8) {
	tekstasREŽIMAScheckfbPerkelti()
	if char == '\n' {
		fbDabartinisEilutė++
		fbDabartiniscol = 0
		tekstasREŽIMAScheckfbPerkelti()
	} else if char == '\b' {
		fb[fbDabartiniscol+fbDabartinisEilutė*fbPlotis] = 0xf00
		fbDabartiniscol = fbDabartiniscol - 1
		if fbDabartiniscol < 0 {
			fbDabartiniscol = 0
		}
	} else if char == '\r' {
		fbDabartiniscol = 0
	} else {
		if fbDabartiniscol >= fbPlotis {
			return
		}
		fb[fbDabartiniscol+fbDabartinisEilutė*fbPlotis] = uint16(atributas)<<8 | uint16(char)
		fbDabartiniscol++
	}

}

func tekstasREŽIMASSpausdintiŠešioliktainis64(skaičius uint64) {
	tekstasREŽIMASSpausdintiŠešioliktainis32(uint32(skaičius >> 32))
	tekstasREŽIMASSpausdintiŠešioliktainis32(uint32(skaičius))
}

func tekstasREŽIMASSpausdintiŠešioliktainis32(skaičius uint32) {
	tekstasREŽIMASSpausdintiŠešioliktainis16(uint16(skaičius >> 16))
	tekstasREŽIMASSpausdintiŠešioliktainis16(uint16(skaičius))
}

func tekstasREŽIMASSpausdintiŠešioliktainis16(skaičius uint16) {
	tekstasREŽIMASSpausdintiŠešioliktainis(uint8(skaičius >> 8))
	tekstasREŽIMASSpausdintiŠešioliktainis(uint8(skaičius))
}

func tekstasREŽIMASSpausdintiŠešioliktainis(skaičius uint8) {
	tekstasREŽIMASSpausdintiŠešioliktainischar(skaičius >> 4)
	tekstasREŽIMASSpausdintiŠešioliktainischar(skaičius)
}

func tekstasREŽIMASSpausdintiŠešioliktainischar(nibble uint8) {
	n := nibble & 0xf
	if n < 10 {
		tekstasREŽIMASSpausdintichar(0x30 + n)
	} else {
		tekstasREŽIMASSpausdintichar(0x41 + n - 10)
	}
}
