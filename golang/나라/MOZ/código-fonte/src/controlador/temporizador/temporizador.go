/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package temporizador

import . "unsafe"

import . "interrupção"
import . "console"

type ITemporizadoreventohandler interface {
	Aotick()
}

var itemporizadoreventohandler ITemporizadoreventohandler

type TPredefiniçãotemporizadoreventohandler struct {
}

func (próprio *TPredefiniçãotemporizadoreventohandler) Aotick() {
}

type TTemporizadorcontrolador struct {
	TInterrupçãohandler
}

var interrupçãohandler func(*TTemporizadorcontrolador, uint32) uint32

func (próprio *TTemporizadorcontrolador) Init(gestor *TInterrupçãogestor, tecladoeventohandler ITemporizadoreventohandler) {
	itemporizadoreventohandler = &TPredefiniçãotemporizadoreventohandler{}
	if tecladoeventohandler != nil {
		itemporizadoreventohandler = tecladoeventohandler
	}

	interrupçãohandler = (*TTemporizadorcontrolador).Manípulointerrupção
	var endereço uintptr
	endereço = uintptr(Pointer(&interrupçãohandler))

	próprio.TInterrupçãohandler.Init(0x20, uintptr(Pointer(gestor)), endereço)

}

var tickContar uint32 = 0

func (próprio *TTemporizadorcontrolador) Manípulointerrupção(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Imprimirxy(tickContar, 3, 1)
	tickContar++

	return esp
}
