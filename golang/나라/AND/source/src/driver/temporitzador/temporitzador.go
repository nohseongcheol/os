package temporitzador

import . "unsafe"

import . "interrupció"
import . "consola"

type ITemporitzadorEsdevenimenthandler interface {
	Engegattick()
}

var iTemporitzadorEsdevenimenthandler ITemporitzadorEsdevenimenthandler

type TPerdefecteTemporitzadorEsdevenimenthandler struct {
}

func (unmateix *TPerdefecteTemporitzadorEsdevenimenthandler) Engegattick() {
}

type TTemporitzadordriver struct {
	TInterrupcióhandler
}

var interrupcióhandler func(*TTemporitzadordriver, uint32) uint32

func (unmateix *TTemporitzadordriver) Init(manager *TInterrupciómanager, teclatEsdevenimenthandler ITemporitzadorEsdevenimenthandler) {
	iTemporitzadorEsdevenimenthandler = &TPerdefecteTemporitzadorEsdevenimenthandler{}
	if teclatEsdevenimenthandler != nil {
		iTemporitzadorEsdevenimenthandler = teclatEsdevenimenthandler
	}

	interrupcióhandler = (*TTemporitzadordriver).GestorInterrupció
	var adreça uintptr
	adreça = uintptr(Pointer(&interrupcióhandler))

	unmateix.TInterrupcióhandler.Init(0x20, uintptr(Pointer(manager)), adreça)

}

var tickRecompte uint32 = 0

func (unmateix *TTemporitzadordriver) GestorInterrupció(esp uint32) uint32 {
	consola_2 := TConsola{}
	consola_2.MUnsignedinteger32Imprimeixxy(tickRecompte, 3, 1)
	tickRecompte++

	return esp
}
