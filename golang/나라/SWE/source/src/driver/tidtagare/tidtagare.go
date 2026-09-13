package tidtagare

import . "unsafe"

import . "avbrott"
import . "konsol"

type ITidtagareHändelsehandler interface {
	Påtick()
}

var iTidtagareHändelsehandler ITidtagareHändelsehandler

type TStandardTidtagareHändelsehandler struct {
}

func (själv *TStandardTidtagareHändelsehandler) Påtick() {
}

type TTidtagaredriver struct {
	TAvbrotthandler
}

var avbrotthandler func(*TTidtagaredriver, uint32) uint32

func (själv *TTidtagaredriver) Init(manager *TAvbrottmanager, tangentbordHändelsehandler ITidtagareHändelsehandler) {
	iTidtagareHändelsehandler = &TStandardTidtagareHändelsehandler{}
	if tangentbordHändelsehandler != nil {
		iTidtagareHändelsehandler = tangentbordHändelsehandler
	}

	avbrotthandler = (*TTidtagaredriver).HandtagAvbrott
	var adress uintptr
	adress = uintptr(Pointer(&avbrotthandler))

	själv.TAvbrotthandler.Init(0x20, uintptr(Pointer(manager)), adress)

}

var tickAntal uint32 = 0

func (själv *TTidtagaredriver) HandtagAvbrott(esp uint32) uint32 {
	konsol_2 := TKonsol{}
	konsol_2.MUnsignedinteger32Skrivutxy(tickAntal, 3, 1)
	tickAntal++

	return esp
}
