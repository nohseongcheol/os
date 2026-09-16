/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elemento_de_ecrã

import . "vga"

type IElemento_de_ecrã interface {
	Init(superior IElemento_de_ecrã, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFoco(elemento_de_ecrã IElemento_de_ecrã)
	Definir_coordenadas_locais(x int32, y int32)
	ConjuntoCor(r uint32, g uint32, b uint32)
	Draw(vga *TVídeoGráficosmatriz)
	Containscoordinate(x uint32, y uint32) bool
}

type TElemento_de_ecrã struct {
	superior	IElemento_de_ecrã
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (próprio *TElemento_de_ecrã) Init(superior IElemento_de_ecrã, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	próprio.superior = superior

	próprio.x = x
	próprio.y = y
	próprio.w = w
	próprio.h = h

	próprio.r = r
	próprio.g = g
	próprio.b = b

	próprio.Focussable = true

}
func (próprio *TElemento_de_ecrã) GetFoco(elemento_de_ecrã IElemento_de_ecrã) {
	if próprio.superior != nil {
		próprio.superior.GetFoco(elemento_de_ecrã)
	}
}
func (próprio *TElemento_de_ecrã) Definir_coordenadas_locais(x uint32, y uint32) {
	if próprio.superior != nil {

	}
	próprio.x = x
	próprio.y = y

}
func (próprio *TElemento_de_ecrã) ConjuntoCor(r uint32, g uint32, b uint32) {
	próprio.r = r
	próprio.g = g
	próprio.b = b
}

func (próprio *TElemento_de_ecrã) Draw(vga *TVídeoGráficosmatriz) {
	vga.FillRectângulo(próprio.x, próprio.y, próprio.w, próprio.h, uint8(próprio.r), uint8(próprio.g), uint8(próprio.b))
}

func (próprio *TElemento_de_ecrã) Containscoordinate(x uint32, y uint32) bool {
	return próprio.x <= x && x < (próprio.x+próprio.w) && próprio.y <= y && y < (próprio.y+próprio.h)
}

type TComponenteratoeventohandler struct {
}

var ratocomponente TElemento_de_ecrã
var ratovga TVídeoGráficosmatriz
var previousx int16 = 0
var previousy int16 = 0
var xPosição int16 = 0
var yPosição int16 = 0

func (próprio *TComponenteratoeventohandler) Init(elemento_de_ecrã TElemento_de_ecrã, vga TVídeoGráficosmatriz) {
	ratocomponente = elemento_de_ecrã
	ratovga = vga
}
func (próprio *TComponenteratoeventohandler) AoratoAbaixo(botão int8) {

	ratocomponente.Definir_coordenadas_locais(uint32(previousx), uint32(previousy))
	ratocomponente.ConjuntoCor(0xA8, 0x00, 0x00)
	ratocomponente.Draw(&ratovga)

	ratocomponente.Draw(&ratovga)

}

func (próprio *TComponenteratoeventohandler) AoratoParacima(botão int8) {
}

func (próprio *TComponenteratoeventohandler) AoratoMover(x int8, y int8) {
	xPosição += int16(x)
	if xPosição < 0 {
		xPosição = 0
	}
	if xPosição >= 320 {
		xPosição = 320
	}

	yPosição -= int16(y)

	if yPosição < 0 {
		yPosição = 0
	}
	if yPosição >= 200 {
		yPosição = 200
	}

	ratocomponente.Definir_coordenadas_locais(uint32(previousx), uint32(previousy))
	ratocomponente.ConjuntoCor(0x00, 0x00, 0x00)
	ratocomponente.Draw(&ratovga)

	ratocomponente.Definir_coordenadas_locais(uint32(xPosição), uint32(yPosição))
	ratocomponente.ConjuntoCor(0x00, 0x00, 0xA8)
	ratocomponente.Draw(&ratovga)

	previousx = xPosição
	previousy = yPosição

}
