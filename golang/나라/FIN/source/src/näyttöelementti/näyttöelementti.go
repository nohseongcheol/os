package näyttöelementti

import . "vga"

type INäyttöelementti interface {
	Init(vanhempi INäyttöelementti, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetKohdistus(näyttöelementti INäyttöelementti)
	Aseta_paikalliset_koordinaatit(x int32, y int32)
	AsetaVäri(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafiikkaTaulukko)
	Containscoordinate(x uint32, y uint32) bool
}

type TNäyttöelementti struct {
	vanhempi	INäyttöelementti
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (itse *TNäyttöelementti) Init(vanhempi INäyttöelementti, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	itse.vanhempi = vanhempi

	itse.x = x
	itse.y = y
	itse.w = w
	itse.h = h

	itse.r = r
	itse.g = g
	itse.b = b

	itse.Focussable = true

}
func (itse *TNäyttöelementti) GetKohdistus(näyttöelementti INäyttöelementti) {
	if itse.vanhempi != nil {
		itse.vanhempi.GetKohdistus(näyttöelementti)
	}
}
func (itse *TNäyttöelementti) Aseta_paikalliset_koordinaatit(x uint32, y uint32) {
	if itse.vanhempi != nil {

	}
	itse.x = x
	itse.y = y

}
func (itse *TNäyttöelementti) AsetaVäri(r uint32, g uint32, b uint32) {
	itse.r = r
	itse.g = g
	itse.b = b
}

func (itse *TNäyttöelementti) Draw(vga *TVideoGrafiikkaTaulukko) {
	vga.FillNeliö(itse.x, itse.y, itse.w, itse.h, uint8(itse.r), uint8(itse.g), uint8(itse.b))
}

func (itse *TNäyttöelementti) Containscoordinate(x uint32, y uint32) bool {
	return itse.x <= x && x < (itse.x+itse.w) && itse.y <= y && y < (itse.y+itse.h)
}

type TIkkunaelementtiHiiriTapahtumahandler struct {
}

var hiiriIkkunaelementti TNäyttöelementti
var hiirivga TVideoGrafiikkaTaulukko
var previousx int16 = 0
var previousy int16 = 0
var xSijainti int16 = 0
var ySijainti int16 = 0

func (itse *TIkkunaelementtiHiiriTapahtumahandler) Init(näyttöelementti TNäyttöelementti, vga TVideoGrafiikkaTaulukko) {
	hiiriIkkunaelementti = näyttöelementti
	hiirivga = vga
}
func (itse *TIkkunaelementtiHiiriTapahtumahandler) PäälläHiiriAlas(painike int8) {

	hiiriIkkunaelementti.Aseta_paikalliset_koordinaatit(uint32(previousx), uint32(previousy))
	hiiriIkkunaelementti.AsetaVäri(0xA8, 0x00, 0x00)
	hiiriIkkunaelementti.Draw(&hiirivga)

	hiiriIkkunaelementti.Draw(&hiirivga)

}

func (itse *TIkkunaelementtiHiiriTapahtumahandler) PäälläHiiriYlös(painike int8) {
}

func (itse *TIkkunaelementtiHiiriTapahtumahandler) PäälläHiiriSiirrä(x int8, y int8) {
	xSijainti += int16(x)
	if xSijainti < 0 {
		xSijainti = 0
	}
	if xSijainti >= 320 {
		xSijainti = 320
	}

	ySijainti -= int16(y)

	if ySijainti < 0 {
		ySijainti = 0
	}
	if ySijainti >= 200 {
		ySijainti = 200
	}

	hiiriIkkunaelementti.Aseta_paikalliset_koordinaatit(uint32(previousx), uint32(previousy))
	hiiriIkkunaelementti.AsetaVäri(0x00, 0x00, 0x00)
	hiiriIkkunaelementti.Draw(&hiirivga)

	hiiriIkkunaelementti.Aseta_paikalliset_koordinaatit(uint32(xSijainti), uint32(ySijainti))
	hiiriIkkunaelementti.AsetaVäri(0x00, 0x00, 0xA8)
	hiiriIkkunaelementti.Draw(&hiirivga)

	previousx = xSijainti
	previousy = ySijainti

}
