package elemento_de_pantalla

import . "vga"

type IElemento_de_pantalla interface {
	Init(padre IElemento_de_pantalla, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFoco(elemento_de_pantalla IElemento_de_pantalla)
	Establecer_las_coordenadas_locales(x int32, y int32)
	Establecercolor(r uint32, g uint32, b uint32)
	Draw(vga *TVídeoGráficosmatriz)
	Containscoordinate(x uint32, y uint32) bool
}

type TElemento_de_pantalla struct {
	padre	IElemento_de_pantalla
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (propio *TElemento_de_pantalla) Init(padre IElemento_de_pantalla, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	propio.padre = padre

	propio.x = x
	propio.y = y
	propio.w = w
	propio.h = h

	propio.r = r
	propio.g = g
	propio.b = b

	propio.Focussable = true

}
func (propio *TElemento_de_pantalla) GetFoco(elemento_de_pantalla IElemento_de_pantalla) {
	if propio.padre != nil {
		propio.padre.GetFoco(elemento_de_pantalla)
	}
}
func (propio *TElemento_de_pantalla) Establecer_las_coordenadas_locales(x uint32, y uint32) {
	if propio.padre != nil {

	}
	propio.x = x
	propio.y = y

}
func (propio *TElemento_de_pantalla) Establecercolor(r uint32, g uint32, b uint32) {
	propio.r = r
	propio.g = g
	propio.b = b
}

func (propio *TElemento_de_pantalla) Draw(vga *TVídeoGráficosmatriz) {
	vga.FillRectángulo(propio.x, propio.y, propio.w, propio.h, uint8(propio.r), uint8(propio.g), uint8(propio.b))
}

func (propio *TElemento_de_pantalla) Containscoordinate(x uint32, y uint32) bool {
	return propio.x <= x && x < (propio.x+propio.w) && propio.y <= y && y < (propio.y+propio.h)
}

type TComponenteratóneventohandler struct {
}

var ratóncomponente TElemento_de_pantalla
var ratónvga TVídeoGráficosmatriz
var previousx int16 = 0
var previousy int16 = 0
var xPosición int16 = 0
var yPosición int16 = 0

func (propio *TComponenteratóneventohandler) Init(elemento_de_pantalla TElemento_de_pantalla, vga TVídeoGráficosmatriz) {
	ratóncomponente = elemento_de_pantalla
	ratónvga = vga
}
func (propio *TComponenteratóneventohandler) AlratónAbajo(botón int8) {

	ratóncomponente.Establecer_las_coordenadas_locales(uint32(previousx), uint32(previousy))
	ratóncomponente.Establecercolor(0xA8, 0x00, 0x00)
	ratóncomponente.Draw(&ratónvga)

	ratóncomponente.Draw(&ratónvga)

}

func (propio *TComponenteratóneventohandler) AlratónSubir(botón int8) {
}

func (propio *TComponenteratóneventohandler) AlratónMover(x int8, y int8) {
	xPosición += int16(x)
	if xPosición < 0 {
		xPosición = 0
	}
	if xPosición >= 320 {
		xPosición = 320
	}

	yPosición -= int16(y)

	if yPosición < 0 {
		yPosición = 0
	}
	if yPosición >= 200 {
		yPosición = 200
	}

	ratóncomponente.Establecer_las_coordenadas_locales(uint32(previousx), uint32(previousy))
	ratóncomponente.Establecercolor(0x00, 0x00, 0x00)
	ratóncomponente.Draw(&ratónvga)

	ratóncomponente.Establecer_las_coordenadas_locales(uint32(xPosición), uint32(yPosición))
	ratóncomponente.Establecercolor(0x00, 0x00, 0xA8)
	ratóncomponente.Draw(&ratónvga)

	previousx = xPosición
	previousy = yPosición

}
