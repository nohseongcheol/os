/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klawiatura

import . "unsafe"

import . "port"
import . "przerwanie"
import . "konsola"

type IMyszWydarzeniehandler interface {
	WłączMyszWdół(przycisk int8)
	WłączMyszGóra(przycisk int8)
	WłączMyszPrzenoszenie(x int8, y int8)
}

var iMyszWydarzeniehandler IMyszWydarzeniehandler

type TDomyślneMyszWydarzeniehandler struct {
}

var konsola_2 TKonsola = TKonsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPozycja int16 = 0
var yPozycja int16 = 0

func (bieżący TDomyślneMyszWydarzeniehandler) WłączMyszWdół(przycisk int8) {
	buffer := []byte("+")
	konsola_2.MWydrukujxy(buffer, uint16(previousx), uint16(previousy))
}
func (bieżący TDomyślneMyszWydarzeniehandler) WłączMyszGóra(przycisk int8)	{}
func (bieżący TDomyślneMyszWydarzeniehandler) WłączMyszPrzenoszenie(x int8, y int8) {

	xPozycja += int16(x)
	if xPozycja < 0 {
		xPozycja = 0
	}
	if xPozycja >= 80 {
		xPozycja = 79
	}

	yPozycja -= int16(y)

	if yPozycja < 0 {
		yPozycja = 0
	}
	if yPozycja >= 25 {
		yPozycja = 24
	}

	buffer := []byte(" ")
	konsola_2.MWydrukujxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsola_2.MWydrukujxy(buffer, uint16(xPozycja), uint16(yPozycja))

	previousx = xPozycja
	previousy = yPozycja
}

type TMyszdriver struct {
	TPrzerwaniehandler
}

var aktywneMyszdriver *TMyszdriver
var przerwaniehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var polecenieport_2 uint16 = 0x64

const ps2Czekajlimit = 100000

func czekajps2WejściePusty() bool {
	for i := 0; i < ps2Czekajlimit; i++ {
		if (PortOdczytbyte(polecenieport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func czekajps2DanewyjściowePełne() bool {
	for i := 0; i < ps2Czekajlimit; i++ {
		if (PortOdczytbyte(polecenieport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zapisps2Polecenie(wartość uint8) bool {
	if !czekajps2WejściePusty() {
		return false
	}
	PortZapisbyte(polecenieport_2, wartość)
	return true
}

func zapisps2data(wartość uint8) bool {
	if !czekajps2WejściePusty() {
		return false
	}
	PortZapisbyte(dataport_2, wartość)
	return true
}

func odczytps2data() (uint8, bool) {
	if !czekajps2DanewyjściowePełne() {
		return 0, false
	}
	return PortOdczytbyte(dataport_2), true
}

func wyślijMyszPolecenie(wartość uint8) bool {
	if !zapisps2Polecenie(0xD4) || !zapisps2data(wartość) {
		return false
	}
	ack, ok := odczytps2data()
	return ok && ack == 0xFA
}

func (bieżący *TMyszdriver) Initdriver(manager *TPrzerwaniemanager, myszWydarzeniehandler IMyszWydarzeniehandler) {

	iMyszWydarzeniehandler = TDomyślneMyszWydarzeniehandler{}

	if myszWydarzeniehandler != nil {
		iMyszWydarzeniehandler = myszWydarzeniehandler
	}

	aktywneMyszdriver = bieżący
	przerwaniehandler = uchwytMyszPrzerwanie
	var adres uintptr
	adres = uintptr(Pointer(&przerwaniehandler))
	bieżący.Init(0x2C, uintptr(Pointer(manager)), adres)

	for i := 0; i < 32 && (PortOdczytbyte(polecenieport_2)&0x01) != 0; i++ {
		PortOdczytbyte(dataport_2)
	}

	if !zapisps2Polecenie(0xA8) || !zapisps2Polecenie(0x20) {
		return
	}
	stan, ok := odczytps2data()
	if !ok {
		return
	}
	stan |= 0x02
	stan &^= 0x20
	if !zapisps2Polecenie(0x60) || !zapisps2data(stan) {
		return
	}

	if !wyślijMyszPolecenie(0xF6) || !wyślijMyszPolecenie(0xF4) {
		return
	}
	przesunięcie = 0

}

func uchwytMyszPrzerwanie(esp uint32) uint32 {
	if aktywneMyszdriver == nil {
		PortOdczytbyte(dataport_2)
		return esp
	}
	return aktywneMyszdriver.UchwytPrzerwanie(esp)
}

var liczba uint8 = 0
var buffer_2 [3]int8
var przesunięcie uint8 = 0

var przycisk_2 int8
var pendingx int16
var pendingy int16
var pendingPrzycisk int8
var pendingMyszWydarzenie bool

func (bieżący *TMyszdriver) UchwytPrzerwanie(esp uint32) uint32 {
	stan := PortOdczytbyte(polecenieport_2)
	if (stan&0x01) == 0 || (stan&0x20) == 0 {
		return esp
	}

	data := PortOdczytbyte(dataport_2)

	if przesunięcie == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[przesunięcie] = int8(data)
	przesunięcie = (przesunięcie + 1) % 3
	if przesunięcie == 0 {
		pAKIETStan := uint8(buffer_2[0])

		if (pAKIETStan & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingPrzycisk = int8(pAKIETStan & 0x07)
		pendingMyszWydarzenie = true
	}

	return esp

}

func ProcespendingMyszWydarzenia() {
	if iMyszWydarzeniehandler == nil {
		return
	}

	Przerwaniedeactive()
	if !pendingMyszWydarzenie {
		PrzerwanieAktywne()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nowyPrzycisk := pendingPrzycisk
	oldPrzycisk := przycisk_2

	pendingx = 0
	pendingy = 0
	pendingMyszWydarzenie = false
	PrzerwanieAktywne()

	if x != 0 || y != 0 {
		iMyszWydarzeniehandler.WłączMyszPrzenoszenie(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (nowyPrzycisk & maska) != (oldPrzycisk & maska) {
			if (nowyPrzycisk & maska) != 0 {
				iMyszWydarzeniehandler.WłączMyszWdół(int8(i + 1))
			} else {
				iMyszWydarzeniehandler.WłączMyszGóra(int8(i + 1))
			}
		}
	}
	przycisk_2 = nowyPrzycisk
}
