package kontrol

import . "vga"

type IKontrol interface {
	Init(forælder IKontrol, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(kontrol IKontrol)
	Set_local_coordinates(x int32, y int32)
	SatFarve(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikTabel)
	Containscoordinate(x uint32, y uint32) bool
}

type TKontrol struct {
	forælder	IKontrol
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (selv *TKontrol) Init(forælder IKontrol, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	selv.forælder = forælder

	selv.x = x
	selv.y = y
	selv.w = w
	selv.h = h

	selv.r = r
	selv.g = g
	selv.b = b

	selv.Focussable = true

}
func (selv *TKontrol) GetFokus(kontrol IKontrol) {
	if selv.forælder != nil {
		selv.forælder.GetFokus(kontrol)
	}
}
func (selv *TKontrol) Set_local_coordinates(x uint32, y uint32) {
	if selv.forælder != nil {

	}
	selv.x = x
	selv.y = y

}
func (selv *TKontrol) SatFarve(r uint32, g uint32, b uint32) {
	selv.r = r
	selv.g = g
	selv.b = b
}

func (selv *TKontrol) Draw(vga *TVideoGrafikTabel) {
	vga.FillRektangel(selv.x, selv.y, selv.w, selv.h, uint8(selv.r), uint8(selv.g), uint8(selv.b))
}

func (selv *TKontrol) Containscoordinate(x uint32, y uint32) bool {
	return selv.x <= x && x < (selv.x+selv.w) && selv.y <= y && y < (selv.y+selv.h)
}

type TKontrolMuseventhandler struct {
}

var musKontrol TKontrol
var musvga TVideoGrafikTabel
var previousx int16 = 0
var previousy int16 = 0
var xPlacering int16 = 0
var yPlacering int16 = 0

func (selv *TKontrolMuseventhandler) Init(kontrol TKontrol, vga TVideoGrafikTabel) {
	musKontrol = kontrol
	musvga = vga
}
func (selv *TKontrolMuseventhandler) TændtMusNed(knap int8) {

	musKontrol.Set_local_coordinates(uint32(previousx), uint32(previousy))
	musKontrol.SatFarve(0xA8, 0x00, 0x00)
	musKontrol.Draw(&musvga)

	musKontrol.Draw(&musvga)

}

func (selv *TKontrolMuseventhandler) TændtMusOp(knap int8) {
}

func (selv *TKontrolMuseventhandler) TændtMusFlyt(x int8, y int8) {
	xPlacering += int16(x)
	if xPlacering < 0 {
		xPlacering = 0
	}
	if xPlacering >= 320 {
		xPlacering = 320
	}

	yPlacering -= int16(y)

	if yPlacering < 0 {
		yPlacering = 0
	}
	if yPlacering >= 200 {
		yPlacering = 200
	}

	musKontrol.Set_local_coordinates(uint32(previousx), uint32(previousy))
	musKontrol.SatFarve(0x00, 0x00, 0x00)
	musKontrol.Draw(&musvga)

	musKontrol.Set_local_coordinates(uint32(xPlacering), uint32(yPlacering))
	musKontrol.SatFarve(0x00, 0x00, 0xA8)
	musKontrol.Draw(&musvga)

	previousx = xPlacering
	previousy = yPlacering

}
