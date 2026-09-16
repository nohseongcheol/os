/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package teclado

import . "unsafe"

import . "porto"
import . "interrupção"
import . "console"

type IRatoeventohandler interface {
	AoratoAbaixo(botão int8)
	AoratoParacima(botão int8)
	AoratoMover(x int8, y int8)
}

var iratoeventohandler IRatoeventohandler

type TPredefiniçãoratoeventohandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosição int16 = 0
var yPosição int16 = 0

func (próprio TPredefiniçãoratoeventohandler) AoratoAbaixo(botão int8) {
	buffer := []byte("+")
	console_2.MImprimirxy(buffer, uint16(previousx), uint16(previousy))
}
func (próprio TPredefiniçãoratoeventohandler) AoratoParacima(botão int8)	{}
func (próprio TPredefiniçãoratoeventohandler) AoratoMover(x int8, y int8) {

	xPosição += int16(x)
	if xPosição < 0 {
		xPosição = 0
	}
	if xPosição >= 80 {
		xPosição = 79
	}

	yPosição -= int16(y)

	if yPosição < 0 {
		yPosição = 0
	}
	if yPosição >= 25 {
		yPosição = 24
	}

	buffer := []byte(" ")
	console_2.MImprimirxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MImprimirxy(buffer, uint16(xPosição), uint16(yPosição))

	previousx = xPosição
	previousy = yPosição
}

type TRatocontrolador struct {
	TInterrupçãohandler
}

var ativoratocontrolador *TRatocontrolador
var interrupçãohandler func(uint32) uint32

var dadosporto_2 uint16 = 0x60
var comandoporto_2 uint16 = 0x64

const ps2EsperarLimite = 100000

func esperarps2EntradaVazio() bool {
	for i := 0; i < ps2EsperarLimite; i++ {
		if (Portolerocteto(comandoporto_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func esperarps2ResultadoTotal() bool {
	for i := 0; i < ps2EsperarLimite; i++ {
		if (Portolerocteto(comandoporto_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func escreverps2Comando(valor uint8) bool {
	if !esperarps2EntradaVazio() {
		return false
	}
	Portoescreverocteto(comandoporto_2, valor)
	return true
}

func escreverps2dados(valor uint8) bool {
	if !esperarps2EntradaVazio() {
		return false
	}
	Portoescreverocteto(dadosporto_2, valor)
	return true
}

func lerps2dados() (uint8, bool) {
	if !esperarps2ResultadoTotal() {
		return 0, false
	}
	return Portolerocteto(dadosporto_2), true
}

func enviarratoComando(valor uint8) bool {
	if !escreverps2Comando(0xD4) || !escreverps2dados(valor) {
		return false
	}
	ack, aceitar := lerps2dados()
	return aceitar && ack == 0xFA
}

func (próprio *TRatocontrolador) Initcontrolador(gestor *TInterrupçãogestor, ratoeventohandler IRatoeventohandler) {

	iratoeventohandler = TPredefiniçãoratoeventohandler{}

	if ratoeventohandler != nil {
		iratoeventohandler = ratoeventohandler
	}

	ativoratocontrolador = próprio
	interrupçãohandler = manípuloratointerrupção
	var endereço uintptr
	endereço = uintptr(Pointer(&interrupçãohandler))
	próprio.Init(0x2C, uintptr(Pointer(gestor)), endereço)

	for i := 0; i < 32 && (Portolerocteto(comandoporto_2)&0x01) != 0; i++ {
		Portolerocteto(dadosporto_2)
	}

	if !escreverps2Comando(0xA8) || !escreverps2Comando(0x20) {
		return
	}
	estado, aceitar := lerps2dados()
	if !aceitar {
		return
	}
	estado |= 0x02
	estado &^= 0x20
	if !escreverps2Comando(0x60) || !escreverps2dados(estado) {
		return
	}

	if !enviarratoComando(0xF6) || !enviarratoComando(0xF4) {
		return
	}
	deslocamento = 0

}

func manípuloratointerrupção(esp uint32) uint32 {
	if ativoratocontrolador == nil {
		Portolerocteto(dadosporto_2)
		return esp
	}
	return ativoratocontrolador.Manípulointerrupção(esp)
}

var contar uint8 = 0
var buffer_2 [3]int8
var deslocamento uint8 = 0

var botão_2 int8
var pendentex int16
var pendentey int16
var pendenteBotão int8
var pendenteratoevento bool

func (próprio *TRatocontrolador) Manípulointerrupção(esp uint32) uint32 {
	estado := Portolerocteto(comandoporto_2)
	if (estado&0x01) == 0 || (estado&0x20) == 0 {
		return esp
	}

	dados := Portolerocteto(dadosporto_2)

	if deslocamento == 0 && (dados&0x08) == 0 {
		return esp
	}
	buffer_2[deslocamento] = int8(dados)
	deslocamento = (deslocamento + 1) % 3
	if deslocamento == 0 {
		packetEstado := uint8(buffer_2[0])

		if (packetEstado & 0xC0) == 0 {
			pendentex += int16(buffer_2[1])
			pendentey += int16(buffer_2[2])
			if pendentex > 127 {
				pendentex = 127
			} else if pendentex < -127 {
				pendentex = -127
			}
			if pendentey > 127 {
				pendentey = 127
			} else if pendentey < -127 {
				pendentey = -127
			}
		}
		pendenteBotão = int8(packetEstado & 0x07)
		pendenteratoevento = true
	}

	return esp

}

func Processopendenteratoeventos() {
	if iratoeventohandler == nil {
		return
	}

	Interrupçãodeactive()
	if !pendenteratoevento {
		InterrupçãoAtivo()
		return
	}
	x := int8(pendentex)
	y := int8(pendentey)
	novoBotão := pendenteBotão
	oldBotão := botão_2

	pendentex = 0
	pendentey = 0
	pendenteratoevento = false
	InterrupçãoAtivo()

	if x != 0 || y != 0 {
		iratoeventohandler.AoratoMover(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		máscara := int8(0x1 << i)
		if (novoBotão & máscara) != (oldBotão & máscara) {
			if (novoBotão & máscara) != 0 {
				iratoeventohandler.AoratoAbaixo(int8(i + 1))
			} else {
				iratoeventohandler.AoratoParacima(int8(i + 1))
			}
		}
	}
	botão_2 = novoBotão
}
