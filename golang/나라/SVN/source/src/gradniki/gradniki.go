/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gradniki

import . "vga"

type IGradniki interface {
	Init(nadrejenipredmet IGradniki, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetŽarišče(gradniki IGradniki)
	Set_local_coordinates(x int32, y int32)
	MnožicaBarva(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikaPolje)
	Containscoordinate(x uint32, y uint32) bool
}

type TGradniki struct {
	nadrejenipredmet	IGradniki
	x			uint32
	y			uint32
	w			uint32
	h			uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (sam *TGradniki) Init(nadrejenipredmet IGradniki, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	sam.nadrejenipredmet = nadrejenipredmet

	sam.x = x
	sam.y = y
	sam.w = w
	sam.h = h

	sam.r = r
	sam.g = g
	sam.b = b

	sam.Focussable = true

}
func (sam *TGradniki) GetŽarišče(gradniki IGradniki) {
	if sam.nadrejenipredmet != nil {
		sam.nadrejenipredmet.GetŽarišče(gradniki)
	}
}
func (sam *TGradniki) Set_local_coordinates(x uint32, y uint32) {
	if sam.nadrejenipredmet != nil {

	}
	sam.x = x
	sam.y = y

}
func (sam *TGradniki) MnožicaBarva(r uint32, g uint32, b uint32) {
	sam.r = r
	sam.g = g
	sam.b = b
}

func (sam *TGradniki) Draw(vga *TVideoGrafikaPolje) {
	vga.FillPravokotnik(sam.x, sam.y, sam.w, sam.h, uint8(sam.r), uint8(sam.g), uint8(sam.b))
}

func (sam *TGradniki) Containscoordinate(x uint32, y uint32) bool {
	return sam.x <= x && x < (sam.x+sam.w) && sam.y <= y && y < (sam.y+sam.h)
}

type TGradnikiMiškaeventhandler struct {
}

var miškaGradniki TGradniki
var miškavga TVideoGrafikaPolje
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (sam *TGradnikiMiškaeventhandler) Init(gradniki TGradniki, vga TVideoGrafikaPolje) {
	miškaGradniki = gradniki
	miškavga = vga
}
func (sam *TGradnikiMiškaeventhandler) VključenoMiškaDol(gumb int8) {

	miškaGradniki.Set_local_coordinates(uint32(previousx), uint32(previousy))
	miškaGradniki.MnožicaBarva(0xA8, 0x00, 0x00)
	miškaGradniki.Draw(&miškavga)

	miškaGradniki.Draw(&miškavga)

}

func (sam *TGradnikiMiškaeventhandler) VključenoMiškaGor(gumb int8) {
}

func (sam *TGradnikiMiškaeventhandler) VključenoMiškaPremakni(x int8, y int8) {
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

	miškaGradniki.Set_local_coordinates(uint32(previousx), uint32(previousy))
	miškaGradniki.MnožicaBarva(0x00, 0x00, 0x00)
	miškaGradniki.Draw(&miškavga)

	miškaGradniki.Set_local_coordinates(uint32(xPoložaj), uint32(yPoložaj))
	miškaGradniki.MnožicaBarva(0x00, 0x00, 0xA8)
	miškaGradniki.Draw(&miškavga)

	previousx = xPoložaj
	previousy = yPoložaj

}
