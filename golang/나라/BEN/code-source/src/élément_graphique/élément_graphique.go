package élément_graphique

import . "vga"

type IÉlément_graphique interface {
	Init(parent IÉlément_graphique, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetFocalisation(élément_graphique IÉlément_graphique)
	Définir_les_coordonnées_locales(x int32, y int32)
	EnsembleCouleur(r uint32, g uint32, b uint32)
	Draw(vga *TVidéoAffichagetableau)
	Containscoordinate(x uint32, y uint32) bool
}

type TÉlément_graphique struct {
	parent	IÉlément_graphique
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (self *TÉlément_graphique) Init(parent IÉlément_graphique, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	self.parent = parent

	self.x = x
	self.y = y
	self.w = w
	self.h = h

	self.r = r
	self.g = g
	self.b = b

	self.Focussable = true

}
func (self *TÉlément_graphique) GetFocalisation(élément_graphique IÉlément_graphique) {
	if self.parent != nil {
		self.parent.GetFocalisation(élément_graphique)
	}
}
func (self *TÉlément_graphique) Définir_les_coordonnées_locales(x uint32, y uint32) {
	if self.parent != nil {

	}
	self.x = x
	self.y = y

}
func (self *TÉlément_graphique) EnsembleCouleur(r uint32, g uint32, b uint32) {
	self.r = r
	self.g = g
	self.b = b
}

func (self *TÉlément_graphique) Draw(vga *TVidéoAffichagetableau) {
	vga.Fillrectangle(self.x, self.y, self.w, self.h, uint8(self.r), uint8(self.g), uint8(self.b))
}

func (self *TÉlément_graphique) Containscoordinate(x uint32, y uint32) bool {
	return self.x <= x && x < (self.x+self.w) && self.y <= y && y < (self.y+self.h)
}

type TComposantsourisévénementhandler struct {
}

var souriscomposant TÉlément_graphique
var sourisvga TVidéoAffichagetableau
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TComposantsourisévénementhandler) Init(élément_graphique TÉlément_graphique, vga TVidéoAffichagetableau) {
	souriscomposant = élément_graphique
	sourisvga = vga
}
func (self *TComposantsourisévénementhandler) SursourisVerslebas(bouton int8) {

	souriscomposant.Définir_les_coordonnées_locales(uint32(previousx), uint32(previousy))
	souriscomposant.EnsembleCouleur(0xA8, 0x00, 0x00)
	souriscomposant.Draw(&sourisvga)

	souriscomposant.Draw(&sourisvga)

}

func (self *TComposantsourisévénementhandler) SursourisHaut(bouton int8) {
}

func (self *TComposantsourisévénementhandler) SursourisDéplacer(x int8, y int8) {
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

	souriscomposant.Définir_les_coordonnées_locales(uint32(previousx), uint32(previousy))
	souriscomposant.EnsembleCouleur(0x00, 0x00, 0x00)
	souriscomposant.Draw(&sourisvga)

	souriscomposant.Définir_les_coordonnées_locales(uint32(xposition), uint32(yposition))
	souriscomposant.EnsembleCouleur(0x00, 0x00, 0xA8)
	souriscomposant.Draw(&sourisvga)

	previousx = xposition
	previousy = yposition

}
