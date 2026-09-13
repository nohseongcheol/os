package ጊዜቆጣሪ

import . "unsafe"

import . "ማቋረጫ"
import . "console"

type Iጊዜቆጣሪeventhandler interface {
	Oማብሪያtick()
}

var iጊዜቆጣሪeventhandler Iጊዜቆጣሪeventhandler

type Tነባርጊዜቆጣሪeventhandler struct {
}

func (self *Tነባርጊዜቆጣሪeventhandler) Oማብሪያtick() {
}

type Tጊዜቆጣሪdriver struct {
	Tማቋረጫhandler
}

var ማቋረጫhandler func(*Tጊዜቆጣሪdriver, uint32) uint32

func (self *Tጊዜቆጣሪdriver) Init(manager *Tማቋረጫmanager, የፊደልሠሌዳeventhandler Iጊዜቆጣሪeventhandler) {
	iጊዜቆጣሪeventhandler = &Tነባርጊዜቆጣሪeventhandler{}
	if የፊደልሠሌዳeventhandler != nil {
		iጊዜቆጣሪeventhandler = የፊደልሠሌዳeventhandler
	}

	ማቋረጫhandler = (*Tጊዜቆጣሪdriver).Handleማቋረጫ
	var address uintptr
	address = uintptr(Pointer(&ማቋረጫhandler))

	self.Tማቋረጫhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *Tጊዜቆጣሪdriver) Handleማቋረጫ(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32ማተሚያxy(tickcount, 3, 1)
	tickcount++

	return esp
}
