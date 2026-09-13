package bildschirmelement

import . "vga"

type IBildschirmelement interface {
	Init(elternelement IBildschirmelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFokus(bildschirmelement IBildschirmelement)
	Lokale_Koordinaten_setzen(x int32, y int32)
	SetzenFarbe(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafikFeld)
	Containscoordinate(x uint32, y uint32) bool
}

type TBildschirmelement struct {
	elternelement	IBildschirmelement
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (selbst *TBildschirmelement) Init(elternelement IBildschirmelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	selbst.elternelement = elternelement

	selbst.x = x
	selbst.y = y
	selbst.w = w
	selbst.h = h

	selbst.r = r
	selbst.g = g
	selbst.b = b

	selbst.Focussable = true

}
func (selbst *TBildschirmelement) GetFokus(bildschirmelement IBildschirmelement) {
	if selbst.elternelement != nil {
		selbst.elternelement.GetFokus(bildschirmelement)
	}
}
func (selbst *TBildschirmelement) Lokale_Koordinaten_setzen(x uint32, y uint32) {
	if selbst.elternelement != nil {

	}
	selbst.x = x
	selbst.y = y

}
func (selbst *TBildschirmelement) SetzenFarbe(r uint32, g uint32, b uint32) {
	selbst.r = r
	selbst.g = g
	selbst.b = b
}

func (selbst *TBildschirmelement) Draw(vga *TVideoGrafikFeld) {
	vga.FillRechteck(selbst.x, selbst.y, selbst.w, selbst.h, uint8(selbst.r), uint8(selbst.g), uint8(selbst.b))
}

func (selbst *TBildschirmelement) Containscoordinate(x uint32, y uint32) bool {
	return selbst.x <= x && x < (selbst.x+selbst.w) && selbst.y <= y && y < (selbst.y+selbst.h)
}

type TSteuerelementMausEreignishandler struct {
}

var mausSteuerelement TBildschirmelement
var mausvga TVideoGrafikFeld
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (selbst *TSteuerelementMausEreignishandler) Init(bildschirmelement TBildschirmelement, vga TVideoGrafikFeld) {
	mausSteuerelement = bildschirmelement
	mausvga = vga
}
func (selbst *TSteuerelementMausEreignishandler) BeiMausAbwärts(knopf int8) {

	mausSteuerelement.Lokale_Koordinaten_setzen(uint32(previousx), uint32(previousy))
	mausSteuerelement.SetzenFarbe(0xA8, 0x00, 0x00)
	mausSteuerelement.Draw(&mausvga)

	mausSteuerelement.Draw(&mausvga)

}

func (selbst *TSteuerelementMausEreignishandler) BeiMausAufwärts(knopf int8) {
}

func (selbst *TSteuerelementMausEreignishandler) BeiMausVerschieben(x int8, y int8) {
	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 320 {
		xposition = 320
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 200 {
		yposition = 200
	}

	mausSteuerelement.Lokale_Koordinaten_setzen(uint32(previousx), uint32(previousy))
	mausSteuerelement.SetzenFarbe(0x00, 0x00, 0x00)
	mausSteuerelement.Draw(&mausvga)

	mausSteuerelement.Lokale_Koordinaten_setzen(uint32(xposition), uint32(yposition))
	mausSteuerelement.SetzenFarbe(0x00, 0x00, 0xA8)
	mausSteuerelement.Draw(&mausvga)

	previousx = xposition
	previousy = yposition

}
