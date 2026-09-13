package unsur_layar

import . "vga"

type IUnsur_layar interface {
	Init(orangtua IUnsur_layar, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(unsur_layar IUnsur_layar)
	Atur_koordinat_lokal(x int32, y int32)
	AturWarna(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikJajaran)
	Containscoordinate(x uint32, y uint32) bool
}

type TUnsur_layar struct {
	orangtua	IUnsur_layar
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (dirisendiri *TUnsur_layar) Init(orangtua IUnsur_layar, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	dirisendiri.orangtua = orangtua

	dirisendiri.x = x
	dirisendiri.y = y
	dirisendiri.w = w
	dirisendiri.h = h

	dirisendiri.r = r
	dirisendiri.g = g
	dirisendiri.b = b

	dirisendiri.Focussable = true

}
func (dirisendiri *TUnsur_layar) GetFokus(unsur_layar IUnsur_layar) {
	if dirisendiri.orangtua != nil {
		dirisendiri.orangtua.GetFokus(unsur_layar)
	}
}
func (dirisendiri *TUnsur_layar) Atur_koordinat_lokal(x uint32, y uint32) {
	if dirisendiri.orangtua != nil {

	}
	dirisendiri.x = x
	dirisendiri.y = y

}
func (dirisendiri *TUnsur_layar) AturWarna(r uint32, g uint32, b uint32) {
	dirisendiri.r = r
	dirisendiri.g = g
	dirisendiri.b = b
}

func (dirisendiri *TUnsur_layar) Draw(vga *TVideoGrafikJajaran) {
	vga.FillBujurSangkar(dirisendiri.x, dirisendiri.y, dirisendiri.w, dirisendiri.h, uint8(dirisendiri.r), uint8(dirisendiri.g), uint8(dirisendiri.b))
}

func (dirisendiri *TUnsur_layar) Containscoordinate(x uint32, y uint32) bool {
	return dirisendiri.x <= x && x < (dirisendiri.x+dirisendiri.w) && dirisendiri.y <= y && y < (dirisendiri.y+dirisendiri.h)
}

type TWidgetTetikusEvenhandler struct {
}

var tetikuswidget TUnsur_layar
var tetikusvga TVideoGrafikJajaran
var previousx int16 = 0
var previousy int16 = 0
var xPosisi int16 = 0
var yPosisi int16 = 0

func (dirisendiri *TWidgetTetikusEvenhandler) Init(unsur_layar TUnsur_layar, vga TVideoGrafikJajaran) {
	tetikuswidget = unsur_layar
	tetikusvga = vga
}
func (dirisendiri *TWidgetTetikusEvenhandler) HidupTetikusBawah(tombol int8) {

	tetikuswidget.Atur_koordinat_lokal(uint32(previousx), uint32(previousy))
	tetikuswidget.AturWarna(0xA8, 0x00, 0x00)
	tetikuswidget.Draw(&tetikusvga)

	tetikuswidget.Draw(&tetikusvga)

}

func (dirisendiri *TWidgetTetikusEvenhandler) HidupTetikusNaik(tombol int8) {
}

func (dirisendiri *TWidgetTetikusEvenhandler) HidupTetikusPindah(x int8, y int8) {
	xPosisi += int16(x)
	if xPosisi < 0 {
		xPosisi = 0
	}
	if xPosisi >= 320 {
		xPosisi = 320
	}

	yPosisi -= int16(y)

	if yPosisi < 0 {
		yPosisi = 0
	}
	if yPosisi >= 200 {
		yPosisi = 200
	}

	tetikuswidget.Atur_koordinat_lokal(uint32(previousx), uint32(previousy))
	tetikuswidget.AturWarna(0x00, 0x00, 0x00)
	tetikuswidget.Draw(&tetikusvga)

	tetikuswidget.Atur_koordinat_lokal(uint32(xPosisi), uint32(yPosisi))
	tetikuswidget.AturWarna(0x00, 0x00, 0xA8)
	tetikuswidget.Draw(&tetikusvga)

	previousx = xPosisi
	previousy = yPosisi

}
