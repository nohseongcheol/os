package temporizador

import . "unsafe"

import . "interrupción"
import . "consola"

type ITemporizadoreventohandler interface {
	Altick()
}

var itemporizadoreventohandler ITemporizadoreventohandler

type TPredeterminadotemporizadoreventohandler struct {
}

func (propio *TPredeterminadotemporizadoreventohandler) Altick() {
}

type TTemporizadorcontrolador struct {
	TInterrupciónhandler
}

var interrupciónhandler func(*TTemporizadorcontrolador, uint32) uint32

func (propio *TTemporizadorcontrolador) Init(gestor *TInterrupcióngestor, tecladoeventohandler ITemporizadoreventohandler) {
	itemporizadoreventohandler = &TPredeterminadotemporizadoreventohandler{}
	if tecladoeventohandler != nil {
		itemporizadoreventohandler = tecladoeventohandler
	}

	interrupciónhandler = (*TTemporizadorcontrolador).Manijainterrupción
	var dirección uintptr
	dirección = uintptr(Pointer(&interrupciónhandler))

	propio.TInterrupciónhandler.Init(0x20, uintptr(Pointer(gestor)), dirección)

}

var tickRecuento uint32 = 0

func (propio *TTemporizadorcontrolador) Manijainterrupción(esp uint32) uint32 {
	consola_2 := TConsola{}
	consola_2.MUnsignedinteger32Imprimirxy(tickRecuento, 3, 1)
	tickRecuento++

	return esp
}
