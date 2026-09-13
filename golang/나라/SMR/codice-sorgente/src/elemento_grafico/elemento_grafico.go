package elemento_grafico

import . "vga"

type IElemento_grafico interface {
	Init(genitore IElemento_grafico, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFuoco(elemento_grafico IElemento_grafico)
	Imposta_le_coordinate_locali(x int32, y int32)
	ImpostaColore(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGraficaSerie)
	Containscoordinate(x uint32, y uint32) bool
}

type TElemento_grafico struct {
	genitore	IElemento_grafico
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (séstesso *TElemento_grafico) Init(genitore IElemento_grafico, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	séstesso.genitore = genitore

	séstesso.x = x
	séstesso.y = y
	séstesso.w = w
	séstesso.h = h

	séstesso.r = r
	séstesso.g = g
	séstesso.b = b

	séstesso.Focussable = true

}
func (séstesso *TElemento_grafico) GetFuoco(elemento_grafico IElemento_grafico) {
	if séstesso.genitore != nil {
		séstesso.genitore.GetFuoco(elemento_grafico)
	}
}
func (séstesso *TElemento_grafico) Imposta_le_coordinate_locali(x uint32, y uint32) {
	if séstesso.genitore != nil {

	}
	séstesso.x = x
	séstesso.y = y

}
func (séstesso *TElemento_grafico) ImpostaColore(r uint32, g uint32, b uint32) {
	séstesso.r = r
	séstesso.g = g
	séstesso.b = b
}

func (séstesso *TElemento_grafico) Draw(vga *TVideoGraficaSerie) {
	vga.FillRettangolo(séstesso.x, séstesso.y, séstesso.w, séstesso.h, uint8(séstesso.r), uint8(séstesso.g), uint8(séstesso.b))
}

func (séstesso *TElemento_grafico) Containscoordinate(x uint32, y uint32) bool {
	return séstesso.x <= x && x < (séstesso.x+séstesso.w) && séstesso.y <= y && y < (séstesso.y+séstesso.h)
}

type TElementimouseEventohandler struct {
}

var mouseElementi TElemento_grafico
var mousevga TVideoGraficaSerie
var previousx int16 = 0
var previousy int16 = 0
var xPosizione int16 = 0
var yPosizione int16 = 0

func (séstesso *TElementimouseEventohandler) Init(elemento_grafico TElemento_grafico, vga TVideoGraficaSerie) {
	mouseElementi = elemento_grafico
	mousevga = vga
}
func (séstesso *TElementimouseEventohandler) AccesomouseGiù(pulsante int8) {

	mouseElementi.Imposta_le_coordinate_locali(uint32(previousx), uint32(previousy))
	mouseElementi.ImpostaColore(0xA8, 0x00, 0x00)
	mouseElementi.Draw(&mousevga)

	mouseElementi.Draw(&mousevga)

}

func (séstesso *TElementimouseEventohandler) AccesomouseSu(pulsante int8) {
}

func (séstesso *TElementimouseEventohandler) AccesomouseSposta(x int8, y int8) {
	xPosizione += int16(x)
	if xPosizione < 0 {
		xPosizione = 0
	}
	if xPosizione >= 320 {
		xPosizione = 320
	}

	yPosizione -= int16(y)

	if yPosizione < 0 {
		yPosizione = 0
	}
	if yPosizione >= 200 {
		yPosizione = 200
	}

	mouseElementi.Imposta_le_coordinate_locali(uint32(previousx), uint32(previousy))
	mouseElementi.ImpostaColore(0x00, 0x00, 0x00)
	mouseElementi.Draw(&mousevga)

	mouseElementi.Imposta_le_coordinate_locali(uint32(xPosizione), uint32(yPosizione))
	mouseElementi.ImpostaColore(0x00, 0x00, 0xA8)
	mouseElementi.Draw(&mousevga)

	previousx = xPosizione
	previousy = yPosizione

}
