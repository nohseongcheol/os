/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package schermelement

import . "vga"

type ISchermelement interface {
	Init(ouder ISchermelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetScherpstellen(schermelement ISchermelement)
	Lokale_coördinaten_instellen(x int32, y int32)
	InstellenKleur(r uint32, g uint32, b uint32)
	Draw(vga *TVideoGrafischReeks)
	Containscoordinate(x uint32, y uint32) bool
}

type TSchermelement struct {
	ouder	ISchermelement
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (zelf *TSchermelement) Init(ouder ISchermelement, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	zelf.ouder = ouder

	zelf.x = x
	zelf.y = y
	zelf.w = w
	zelf.h = h

	zelf.r = r
	zelf.g = g
	zelf.b = b

	zelf.Focussable = true

}
func (zelf *TSchermelement) GetScherpstellen(schermelement ISchermelement) {
	if zelf.ouder != nil {
		zelf.ouder.GetScherpstellen(schermelement)
	}
}
func (zelf *TSchermelement) Lokale_coördinaten_instellen(x uint32, y uint32) {
	if zelf.ouder != nil {

	}
	zelf.x = x
	zelf.y = y

}
func (zelf *TSchermelement) InstellenKleur(r uint32, g uint32, b uint32) {
	zelf.r = r
	zelf.g = g
	zelf.b = b
}

func (zelf *TSchermelement) Draw(vga *TVideoGrafischReeks) {
	vga.FillRechthoek(zelf.x, zelf.y, zelf.w, zelf.h, uint8(zelf.r), uint8(zelf.g), uint8(zelf.b))
}

func (zelf *TSchermelement) Containscoordinate(x uint32, y uint32) bool {
	return zelf.x <= x && x < (zelf.x+zelf.w) && zelf.y <= y && y < (zelf.y+zelf.h)
}

type TWidgetMuisGebeurtenishandler struct {
}

var muiswidget TSchermelement
var muisvga TVideoGrafischReeks
var previousx int16 = 0
var previousy int16 = 0
var xPositie int16 = 0
var yPositie int16 = 0

func (zelf *TWidgetMuisGebeurtenishandler) Init(schermelement TSchermelement, vga TVideoGrafischReeks) {
	muiswidget = schermelement
	muisvga = vga
}
func (zelf *TWidgetMuisGebeurtenishandler) AanMuisOmlaag(knop int8) {

	muiswidget.Lokale_coördinaten_instellen(uint32(previousx), uint32(previousy))
	muiswidget.InstellenKleur(0xA8, 0x00, 0x00)
	muiswidget.Draw(&muisvga)

	muiswidget.Draw(&muisvga)

}

func (zelf *TWidgetMuisGebeurtenishandler) AanMuisOmhoog(knop int8) {
}

func (zelf *TWidgetMuisGebeurtenishandler) AanMuisVerplaatsen(x int8, y int8) {
	xPositie += int16(x)
	if xPositie < 0 {
		xPositie = 0
	}
	if xPositie >= 320 {
		xPositie = 320
	}

	yPositie -= int16(y)

	if yPositie < 0 {
		yPositie = 0
	}
	if yPositie >= 200 {
		yPositie = 200
	}

	muiswidget.Lokale_coördinaten_instellen(uint32(previousx), uint32(previousy))
	muiswidget.InstellenKleur(0x00, 0x00, 0x00)
	muiswidget.Draw(&muisvga)

	muiswidget.Lokale_coördinaten_instellen(uint32(xPositie), uint32(yPositie))
	muiswidget.InstellenKleur(0x00, 0x00, 0xA8)
	muiswidget.Draw(&muisvga)

	previousx = xPositie
	previousy = yPositie

}
