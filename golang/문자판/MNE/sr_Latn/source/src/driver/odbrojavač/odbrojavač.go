/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package odbrojavač

import . "unsafe"

import . "ometanje"
import . "konzola"

type IOdbrojavačDogađajhandler interface {
	Natick()
}

var iOdbrojavačDogađajhandler IOdbrojavačDogađajhandler

type TPodrazumevanoOdbrojavačDogađajhandler struct {
}

func (isti *TPodrazumevanoOdbrojavačDogađajhandler) Natick() {
}

type TOdbrojavačdriver struct {
	TOmetanjehandler
}

var ometanjehandler func(*TOdbrojavačdriver, uint32) uint32

func (isti *TOdbrojavačdriver) Init(manager *TOmetanjemanager, tastaturaDogađajhandler IOdbrojavačDogađajhandler) {
	iOdbrojavačDogađajhandler = &TPodrazumevanoOdbrojavačDogađajhandler{}
	if tastaturaDogađajhandler != nil {
		iOdbrojavačDogađajhandler = tastaturaDogađajhandler
	}

	ometanjehandler = (*TOdbrojavačdriver).RučkaOmetanje
	var address uintptr
	address = uintptr(Pointer(&ometanjehandler))

	isti.TOmetanjehandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (isti *TOdbrojavačdriver) RučkaOmetanje(esp uint32) uint32 {
	konzola_2 := TKonzola{}
	konzola_2.MUnsignedinteger32Štampajxy(tickcount, 3, 1)
	tickcount++

	return esp
}
