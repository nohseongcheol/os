/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package kontrola

import . "vga"

type IKontrola interface {
	Init(nadređeni IKontrola, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetŽiža(kontrola IKontrola)
	Set_local_coordinates(x int32, y int32)
	SkupBoja(r uint32, g uint32, b uint32)
	Draw(vga *TVideografikaNiz)
	Containscoordinate(x uint32, y uint32) bool
}

type TKontrola struct {
	nadređeni	IKontrola
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (isti *TKontrola) Init(nadređeni IKontrola, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	isti.nadređeni = nadređeni

	isti.x = x
	isti.y = y
	isti.w = w
	isti.h = h

	isti.r = r
	isti.g = g
	isti.b = b

	isti.Focussable = true

}
func (isti *TKontrola) GetŽiža(kontrola IKontrola) {
	if isti.nadređeni != nil {
		isti.nadređeni.GetŽiža(kontrola)
	}
}
func (isti *TKontrola) Set_local_coordinates(x uint32, y uint32) {
	if isti.nadređeni != nil {

	}
	isti.x = x
	isti.y = y

}
func (isti *TKontrola) SkupBoja(r uint32, g uint32, b uint32) {
	isti.r = r
	isti.g = g
	isti.b = b
}

func (isti *TKontrola) Draw(vga *TVideografikaNiz) {
	vga.FillPravougaonik(isti.x, isti.y, isti.w, isti.h, uint8(isti.r), uint8(isti.g), uint8(isti.b))
}

func (isti *TKontrola) Containscoordinate(x uint32, y uint32) bool {
	return isti.x <= x && x < (isti.x+isti.w) && isti.y <= y && y < (isti.y+isti.h)
}

type TKontrolaMišDogađajhandler struct {
}

var mišKontrola TKontrola
var mišvga TVideografikaNiz
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (isti *TKontrolaMišDogađajhandler) Init(kontrola TKontrola, vga TVideografikaNiz) {
	mišKontrola = kontrola
	mišvga = vga
}
func (isti *TKontrolaMišDogađajhandler) NaMišNiže(dugme int8) {

	mišKontrola.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišKontrola.SkupBoja(0xA8, 0x00, 0x00)
	mišKontrola.Draw(&mišvga)

	mišKontrola.Draw(&mišvga)

}

func (isti *TKontrolaMišDogađajhandler) NaMišGore(dugme int8) {
}

func (isti *TKontrolaMišDogađajhandler) NaMišPremesti(x int8, y int8) {
	xPoložaj += int16(x)
	if xPoložaj < 0 {
		xPoložaj = 0
	}
	if xPoložaj >= 320 {
		xPoložaj = 320
	}

	yPoložaj -= int16(y)

	if yPoložaj < 0 {
		yPoložaj = 0
	}
	if yPoložaj >= 200 {
		yPoložaj = 200
	}

	mišKontrola.Set_local_coordinates(uint32(previousx), uint32(previousy))
	mišKontrola.SkupBoja(0x00, 0x00, 0x00)
	mišKontrola.Draw(&mišvga)

	mišKontrola.Set_local_coordinates(uint32(xPoložaj), uint32(yPoložaj))
	mišKontrola.SkupBoja(0x00, 0x00, 0xA8)
	mišKontrola.Draw(&mišvga)

	previousx = xPoložaj
	previousy = yPoložaj

}
