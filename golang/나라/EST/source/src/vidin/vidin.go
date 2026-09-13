package vidin

import . "vga"

type IVidin interface {
	Init(vanem IVidin, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(vidin IVidin)
	Set_local_coordinates(x int32, y int32)
	MääraVärv(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGraafikaMassiiv)
	Containscoordinate(x uint32, y uint32) bool
}

type TVidin struct {
	vanem	IVidin
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (ise *TVidin) Init(vanem IVidin, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	ise.vanem = vanem

	ise.x = x
	ise.y = y
	ise.w = w
	ise.h = h

	ise.r = r
	ise.g = g
	ise.b = b

	ise.Focussable = true

}
func (ise *TVidin) Getfocus(vidin IVidin) {
	if ise.vanem != nil {
		ise.vanem.Getfocus(vidin)
	}
}
func (ise *TVidin) Set_local_coordinates(x uint32, y uint32) {
	if ise.vanem != nil {

	}
	ise.x = x
	ise.y = y

}
func (ise *TVidin) MääraVärv(r uint32, g uint32, b uint32) {
	ise.r = r
	ise.g = g
	ise.b = b
}

func (ise *TVidin) Draw(vga *TVideoGraafikaMassiiv) {
	vga.FillRistkülik(ise.x, ise.y, ise.w, ise.h, uint8(ise.r), uint8(ise.g), uint8(ise.b))
}

func (ise *TVidin) Containscoordinate(x uint32, y uint32) bool {
	return ise.x <= x && x < (ise.x+ise.w) && ise.y <= y && y < (ise.y+ise.h)
}

type TVidinHiirSündmushandler struct {
}

var hiirVidin TVidin
var hiirvga TVideoGraafikaMassiiv
var previousx int16 = 0
var previousy int16 = 0
var xAsukoht int16 = 0
var yAsukoht int16 = 0

func (ise *TVidinHiirSündmushandler) Init(vidin TVidin, vga TVideoGraafikaMassiiv) {
	hiirVidin = vidin
	hiirvga = vga
}
func (ise *TVidinHiirSündmushandler) SeesHiirNoolalla(nupp int8) {

	hiirVidin.Set_local_coordinates(uint32(previousx), uint32(previousy))
	hiirVidin.MääraVärv(0xA8, 0x00, 0x00)
	hiirVidin.Draw(&hiirvga)

	hiirVidin.Draw(&hiirvga)

}

func (ise *TVidinHiirSündmushandler) SeesHiirÜles(nupp int8) {
}

func (ise *TVidinHiirSündmushandler) SeesHiirLiiguta(x int8, y int8) {
	xAsukoht += int16(x)
	if xAsukoht < 0 {
		xAsukoht = 0
	}
	if xAsukoht >= 320 {
		xAsukoht = 320
	}

	yAsukoht -= int16(y)

	if yAsukoht < 0 {
		yAsukoht = 0
	}
	if yAsukoht >= 200 {
		yAsukoht = 200
	}

	hiirVidin.Set_local_coordinates(uint32(previousx), uint32(previousy))
	hiirVidin.MääraVärv(0x00, 0x00, 0x00)
	hiirVidin.Draw(&hiirvga)

	hiirVidin.Set_local_coordinates(uint32(xAsukoht), uint32(yAsukoht))
	hiirVidin.MääraVärv(0x00, 0x00, 0xA8)
	hiirVidin.Draw(&hiirvga)

	previousx = xAsukoht
	previousy = yAsukoht

}
