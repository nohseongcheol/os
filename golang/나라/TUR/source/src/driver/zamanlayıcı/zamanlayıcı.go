package zamanlayıcı

import . "unsafe"

import . "kesme"
import . "konsol"

type IZamanlayıcıOlayhandler interface {
	Açıktick()
}

var iZamanlayıcıOlayhandler IZamanlayıcıOlayhandler

type TÖntanımlıZamanlayıcıOlayhandler struct {
}

func (self *TÖntanımlıZamanlayıcıOlayhandler) Açıktick() {
}

type TZamanlayıcıdriver struct {
	TKesmehandler
}

var kesmehandler func(*TZamanlayıcıdriver, uint32) uint32

func (self *TZamanlayıcıdriver) Init(manager *TKesmemanager, klavyeOlayhandler IZamanlayıcıOlayhandler) {
	iZamanlayıcıOlayhandler = &TÖntanımlıZamanlayıcıOlayhandler{}
	if klavyeOlayhandler != nil {
		iZamanlayıcıOlayhandler = klavyeOlayhandler
	}

	kesmehandler = (*TZamanlayıcıdriver).HandleKesme
	var address uintptr
	address = uintptr(Pointer(&kesmehandler))

	self.TKesmehandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TZamanlayıcıdriver) HandleKesme(esp uint32) uint32 {
	konsol_2 := TKonsol{}
	konsol_2.MUnsignedinteger32Yazdırxy(tickcount, 3, 1)
	tickcount++

	return esp
}
