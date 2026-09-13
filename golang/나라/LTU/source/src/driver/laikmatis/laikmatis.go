package laikmatis

import . "unsafe"

import . "pertraukimas"
import . "console"

type ILaikmatisĮvykishandler interface {
	Įjungtatick()
}

var iLaikmatisĮvykishandler ILaikmatisĮvykishandler

type TNumatytasisLaikmatisĮvykishandler struct {
}

func (self *TNumatytasisLaikmatisĮvykishandler) Įjungtatick() {
}

type TLaikmatisdriver struct {
	TPertraukimashandler
}

var pertraukimashandler func(*TLaikmatisdriver, uint32) uint32

func (self *TLaikmatisdriver) Init(manager *TPertraukimasmanager, klaviatūraĮvykishandler ILaikmatisĮvykishandler) {
	iLaikmatisĮvykishandler = &TNumatytasisLaikmatisĮvykishandler{}
	if klaviatūraĮvykishandler != nil {
		iLaikmatisĮvykishandler = klaviatūraĮvykishandler
	}

	pertraukimashandler = (*TLaikmatisdriver).PozicijaPertraukimas
	var address uintptr
	address = uintptr(Pointer(&pertraukimashandler))

	self.TPertraukimashandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TLaikmatisdriver) PozicijaPertraukimas(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Spausdintixy(tickcount, 3, 1)
	tickcount++

	return esp
}
