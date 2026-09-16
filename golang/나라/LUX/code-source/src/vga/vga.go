/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "port"

type TVidéoAffichagetableau struct {
}

var micsport uint16 = 0x3c2
var crtcindexport uint16 = 0x3d4
var crtcdonnéesport uint16 = 0x3d5
var sequencerindexport uint16 = 0x3c4
var sequencerdonnéesport uint16 = 0x3c5
var affichagecontrôleurindexport uint16 = 0x3ce
var affichagecontrôleurdonnéesport uint16 = 0x3cf
var attributcontrôleurindexport uint16 = 0x3c0
var attributcontrôleurlireport uint16 = 0x3c1
var attributcontrôleurécrireport uint16 = 0x3c0
var attributcontrôleurRéinitialiserport uint16 = 0x3da

func (self *TVidéoAffichagetableau) Écrireregistre(registre []byte) {
	var regindex uint16 = 0

	Portécrireoctet(micsport, registre[regindex])
	regindex++

	var i uint8
	for i = 0; i < 5; i++ {
		Portécrireoctet(sequencerindexport, i)
		Portécrireoctet(sequencerdonnéesport, registre[regindex])
		regindex++
	}

	Portécrireoctet(crtcindexport, 0x03)

	Portécrireoctet(crtcdonnéesport, (Portlireoctet(crtcdonnéesport) | 0x80))
	Portécrireoctet(crtcindexport, 0x11)
	Portécrireoctet(crtcdonnéesport, (Portlireoctet(crtcdonnéesport) & ^uint8(0x80)))

	registre[0x03] = registre[0x03] | 0x80
	registre[0x11] = registre[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Portécrireoctet(crtcindexport, i)
		Portécrireoctet(crtcdonnéesport, registre[regindex])
		regindex++
	}

	for i = 0; i < 9; i++ {
		Portécrireoctet(affichagecontrôleurindexport, i)
		Portécrireoctet(affichagecontrôleurdonnéesport, registre[regindex])
		regindex++
	}

	for i = 0; i < 21; i++ {
		Portlireoctet(attributcontrôleurRéinitialiserport)
		Portécrireoctet(attributcontrôleurindexport, i)
		Portécrireoctet(attributcontrôleurécrireport, registre[regindex])
		regindex++
	}

	Portlireoctet(attributcontrôleurRéinitialiserport)
	Portécrireoctet(attributcontrôleurindexport, 0x20)

}

func (self *TVidéoAffichagetableau) Gettramebuffersegment() uintptr {
	Portécrireoctet(affichagecontrôleurindexport, 0x06)
	var segmentNombre uint8 = ((Portlireoctet(affichagecontrôleurdonnéesport) >> 2) & 0x03)
	switch segmentNombre {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (self *TVidéoAffichagetableau) Putpixel(x uint32, y uint32, couleurindex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Gettramebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = couleurindex

}
func (self *TVidéoAffichagetableau) GetCouleurindex(r uint8, g uint8, b uint8) uint8 {
	if r == 0x00 && g == 0x00 && b == 0x00 {
		return 0x00
	}
	if r == 0x00 && g == 0x00 && b == 0xA8 {
		return 0x01
	}
	if r == 0x00 && g == 0xA8 && b == 0x00 {
		return 0x02
	}
	if r == 0xA8 && g == 0x00 && b == 0x00 {
		return 0x04
	}
	if r == 0xFF && g == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (self *TVidéoAffichagetableau) PutpixelRVB(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.GetCouleurindex(r, g, b))
}
func (self *TVidéoAffichagetableau) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.PutpixelRVB(X, Y, r, g, b)
		}
	}
}
func (self *TVidéoAffichagetableau) Priseenchargemode(largeur uint32, hauteur uint32, couleurProfondeur uint32) bool {
	return largeur == 320 && hauteur == 200 && couleurProfondeur == 8
}
func (self *TVidéoAffichagetableau) Ensemblemode(largeur uint32, hauteur uint32, couleurProfondeur uint32) bool {
	if !self.Priseenchargemode(largeur, hauteur, couleurProfondeur) {
		return false
	}

	var g320x200x256 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	self.Écrireregistre(g320x200x256)

	return true
}
