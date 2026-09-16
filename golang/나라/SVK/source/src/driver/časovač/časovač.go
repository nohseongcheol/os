/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package časovač

import . "unsafe"

import . "prerušenie"
import . "konzola"

type IČasovačUdalosťhandler interface {
	Zapnutétick()
}

var iČasovačUdalosťhandler IČasovačUdalosťhandler

type TPredvolenéČasovačUdalosťhandler struct {
}

func (vlastný *TPredvolenéČasovačUdalosťhandler) Zapnutétick() {
}

type TČasovačdriver struct {
	TPrerušeniehandler
}

var prerušeniehandler func(*TČasovačdriver, uint32) uint32

func (vlastný *TČasovačdriver) Init(manager *TPrerušeniemanager, klávesnicaUdalosťhandler IČasovačUdalosťhandler) {
	iČasovačUdalosťhandler = &TPredvolenéČasovačUdalosťhandler{}
	if klávesnicaUdalosťhandler != nil {
		iČasovačUdalosťhandler = klávesnicaUdalosťhandler
	}

	prerušeniehandler = (*TČasovačdriver).UškoPrerušenie
	var address uintptr
	address = uintptr(Pointer(&prerušeniehandler))

	vlastný.TPrerušeniehandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (vlastný *TČasovačdriver) UškoPrerušenie(esp uint32) uint32 {
	konzola_2 := TKonzola{}
	konzola_2.MUnsignedinteger32Tlačiťxy(tickcount, 3, 1)
	tickcount++

	return esp
}
