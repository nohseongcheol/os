package időzítő

import . "unsafe"

import . "megszakítás"
import . "konzol"

type IIdőzítőEseményhandler interface {
	Betick()
}

var iIdőzítőEseményhandler IIdőzítőEseményhandler

type TAlapértelmezettIdőzítőEseményhandler struct {
}

func (self *TAlapértelmezettIdőzítőEseményhandler) Betick() {
}

type TIdőzítődriver struct {
	TMegszakításhandler
}

var megszakításhandler func(*TIdőzítődriver, uint32) uint32

func (self *TIdőzítődriver) Init(manager *TMegszakításmanager, billentyűzetEseményhandler IIdőzítőEseményhandler) {
	iIdőzítőEseményhandler = &TAlapértelmezettIdőzítőEseményhandler{}
	if billentyűzetEseményhandler != nil {
		iIdőzítőEseményhandler = billentyűzetEseményhandler
	}

	megszakításhandler = (*TIdőzítődriver).FogantyúMegszakítás
	var address uintptr
	address = uintptr(Pointer(&megszakításhandler))

	self.TMegszakításhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickSzámláló uint32 = 0

func (self *TIdőzítődriver) FogantyúMegszakítás(esp uint32) uint32 {
	konzol_2 := TKonzol{}
	konzol_2.MUnsignedinteger32Nyomtatásxy(tickSzámláló, 3, 1)
	tickSzámláló++

	return esp
}
