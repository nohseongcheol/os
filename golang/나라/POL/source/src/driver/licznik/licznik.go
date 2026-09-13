package licznik

import . "unsafe"

import . "przerwanie"
import . "konsola"

type ILicznikWydarzeniehandler interface {
	Włącztick()
}

var iLicznikWydarzeniehandler ILicznikWydarzeniehandler

type TDomyślneLicznikWydarzeniehandler struct {
}

func (bieżący *TDomyślneLicznikWydarzeniehandler) Włącztick() {
}

type TLicznikdriver struct {
	TPrzerwaniehandler
}

var przerwaniehandler func(*TLicznikdriver, uint32) uint32

func (bieżący *TLicznikdriver) Init(manager *TPrzerwaniemanager, klawiaturaWydarzeniehandler ILicznikWydarzeniehandler) {
	iLicznikWydarzeniehandler = &TDomyślneLicznikWydarzeniehandler{}
	if klawiaturaWydarzeniehandler != nil {
		iLicznikWydarzeniehandler = klawiaturaWydarzeniehandler
	}

	przerwaniehandler = (*TLicznikdriver).UchwytPrzerwanie
	var adres uintptr
	adres = uintptr(Pointer(&przerwaniehandler))

	bieżący.TPrzerwaniehandler.Init(0x20, uintptr(Pointer(manager)), adres)

}

var tickLiczba uint32 = 0

func (bieżący *TLicznikdriver) UchwytPrzerwanie(esp uint32) uint32 {
	konsola_2 := TKonsola{}
	konsola_2.MUnsignedinteger32Wydrukujxy(tickLiczba, 3, 1)
	tickLiczba++

	return esp
}
