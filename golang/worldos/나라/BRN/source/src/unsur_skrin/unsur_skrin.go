/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package unsur_skrin

import . "vga"

type IUnsur_skrin interface {
	Init(induk IUnsur_skrin, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(unsur_skrin IUnsur_skrin)
	Tetapkan_koordinat_setempat(x int32, y int32)
	TetapkanWarna(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikTatasusunan)
	Containscoordinate(x uint32, y uint32) bool
}

type TUnsur_skrin struct {
	induk	IUnsur_skrin
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (diri *TUnsur_skrin) Init(induk IUnsur_skrin, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	diri.induk = induk

	diri.x = x
	diri.y = y
	diri.w = w
	diri.h = h

	diri.r = r
	diri.g = g
	diri.b = b

	diri.Focussable = true

}
func (diri *TUnsur_skrin) GetFokus(unsur_skrin IUnsur_skrin) {
	if diri.induk != nil {
		diri.induk.GetFokus(unsur_skrin)
	}
}
func (diri *TUnsur_skrin) Tetapkan_koordinat_setempat(x uint32, y uint32) {
	if diri.induk != nil {

	}
	diri.x = x
	diri.y = y

}
func (diri *TUnsur_skrin) TetapkanWarna(r uint32, g uint32, b uint32) {
	diri.r = r
	diri.g = g
	diri.b = b
}

func (diri *TUnsur_skrin) Draw(vga *TVideoGrafikTatasusunan) {
	vga.Fillrectangle(diri.x, diri.y, diri.w, diri.h, uint8(diri.r), uint8(diri.g), uint8(diri.b))
}

func (diri *TUnsur_skrin) Containscoordinate(x uint32, y uint32) bool {
	return diri.x <= x && x < (diri.x+diri.w) && diri.y <= y && y < (diri.y+diri.h)
}

type TWidgetTetikusPeristiwahandler struct {
}

var tetikuswidget TUnsur_skrin
var tetikusvga TVideoGrafikTatasusunan
var previousx int16 = 0
var previousy int16 = 0
var xKedudukan int16 = 0
var yKedudukan int16 = 0

func (diri *TWidgetTetikusPeristiwahandler) Init(unsur_skrin TUnsur_skrin, vga TVideoGrafikTatasusunan) {
	tetikuswidget = unsur_skrin
	tetikusvga = vga
}
func (diri *TWidgetTetikusPeristiwahandler) BukaTetikusTurun(butang int8) {

	tetikuswidget.Tetapkan_koordinat_setempat(uint32(previousx), uint32(previousy))
	tetikuswidget.TetapkanWarna(0xA8, 0x00, 0x00)
	tetikuswidget.Draw(&tetikusvga)

	tetikuswidget.Draw(&tetikusvga)

}

func (diri *TWidgetTetikusPeristiwahandler) BukaTetikusNaik(butang int8) {
}

func (diri *TWidgetTetikusPeristiwahandler) BukaTetikusAlih(x int8, y int8) {
	xKedudukan += int16(x)
	if xKedudukan < 0 {
		xKedudukan = 0
	}
	if xKedudukan >= 320 {
		xKedudukan = 320
	}

	yKedudukan -= int16(y)

	if yKedudukan < 0 {
		yKedudukan = 0
	}
	if yKedudukan >= 200 {
		yKedudukan = 200
	}

	tetikuswidget.Tetapkan_koordinat_setempat(uint32(previousx), uint32(previousy))
	tetikuswidget.TetapkanWarna(0x00, 0x00, 0x00)
	tetikuswidget.Draw(&tetikusvga)

	tetikuswidget.Tetapkan_koordinat_setempat(uint32(xKedudukan), uint32(yKedudukan))
	tetikuswidget.TetapkanWarna(0x00, 0x00, 0xA8)
	tetikuswidget.Draw(&tetikusvga)

	previousx = xKedudukan
	previousy = yKedudukan

}
