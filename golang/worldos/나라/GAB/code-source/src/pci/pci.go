/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interruption"
import . "console"
import . "pilote/pilote"

type Ipcicontrôleurhandler interface {
	Surgetpilote(périphérique TPeripheralcomponentinterconnectPériphériquedescriptor)
}

var ipcicontrôleurhandler Ipcicontrôleurhandler

type TPardéfautpcicontrôleurhandler struct {
}

func (self TPardéfautpcicontrôleurhandler) Surgetpilote(périphérique TPeripheralcomponentinterconnectPériphériquedescriptor) {
}

type TBaseaddressregistre struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectPériphériquedescriptor struct {
	Portbase	uint32
	Interruption	uint32

	bus		uint16
	périphérique_2	uint16
	fonction	uint16

	MarqueIdentifiant	uint16
	PériphériqueIdentifiant	uint16

	classeIdentifiant	uint8
	subclassIdentifiant	uint8
	interfaceIdentifiant	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectPériphériquedescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontrôleur struct {
	ipcicontrôleurhandler	Ipcicontrôleurhandler
	donnéesport		uint16
	commandeport		uint16
}

func (self *TPeripheralcomponentinterconnectcontrôleur) Init(ipcicontrôleurhandler Ipcicontrôleurhandler) {
	self.donnéesport = 0xCFC
	self.commandeport = 0xCF8

	self.ipcicontrôleurhandler = TPardéfautpcicontrôleurhandler{}
	if ipcicontrôleurhandler != nil {
		self.ipcicontrôleurhandler = ipcicontrôleurhandler
	}
}

var iNombre int = 0

func (self *TPeripheralcomponentinterconnectcontrôleur) Lire(bus uint16, périphérique_2 uint16, fonction uint16, registeroffset uint32) uint32 {
	var identifiant uint32 = 0
	identifiant = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(périphérique_2&0x1f) << 11) | (uint32(fonction&0x07) << 8) | uint32(registeroffset&0xFC)

	Portécriredword(self.commandeport, identifiant)

	rÉSULTAT1 := Portliredword(self.donnéesport)
	rÉSULTAT2 := (rÉSULTAT1 >> (8 * (registeroffset % 4)))

	return rÉSULTAT2
}

func (self *TPeripheralcomponentinterconnectcontrôleur) Écrire(bus uint16, périphérique_2 uint16, fonction uint16, registeroffset uint32, valeur uint32) {
	var identifiant uint32
	identifiant = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((périphérique_2&0x1f)<<11) | uint32((fonction&0x07)<<8) | uint32(registeroffset&0xFC)
	Portécriredword(self.commandeport, identifiant)
	Portécriredword(self.donnéesport, valeur)
}
func (self *TPeripheralcomponentinterconnectcontrôleur) PériphériquehasFonctions(bus uint16, périphérique_2 uint16) bool {
	rÉSULTAT := self.Lire(bus, périphérique_2, 0, 0x0E)
	if (rÉSULTAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontrôleur) Sélectionnerpilote(pilotegestionnaire *TPilotegestionnaire, interrupts *TInterruptiongestionnaire) {
	for bus := 0; bus < 8; bus++ {
		for périphérique_2 := 0; périphérique_2 < 32; périphérique_2++ {

			var nombreFonctions int = 1
			if self.PériphériquehasFonctions(uint16(bus), uint16(périphérique_2)) == true {
				nombreFonctions = 8
			} else {
				nombreFonctions = 1
			}

			for fonction := 0; fonction < nombreFonctions; fonction++ {
				var périphérique TPeripheralcomponentinterconnectPériphériquedescriptor
				périphérique = self.GetPériphériquedescriptor(uint16(bus), uint16(périphérique_2), uint16(fonction))
				if périphérique.MarqueIdentifiant == 0x0000 || périphérique.MarqueIdentifiant == 0xFFFF {
					continue
				}

				for barreNombre := 0; barreNombre < 6; barreNombre++ {
					var barre TBaseaddressregistre = self.Getbaseaddressregistre(uint16(bus), uint16(périphérique_2), uint16(fonction), uint16(barreNombre))
					if barre.address_2 != 0 && (barre.regtype == 1) {
						périphérique.Portbase = barre.address_2
					}

					self.Getpilote(périphérique, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontrôleur) GetPériphériquedescriptor(bus uint16, périphérique_2 uint16, fonction uint16) TPeripheralcomponentinterconnectPériphériquedescriptor {
	var rÉSULTAT TPeripheralcomponentinterconnectPériphériquedescriptor
	rÉSULTAT = TPeripheralcomponentinterconnectPériphériquedescriptor{}
	rÉSULTAT.bus = bus
	rÉSULTAT.périphérique_2 = périphérique_2
	rÉSULTAT.fonction = fonction

	rÉSULTAT.MarqueIdentifiant = uint16(self.Lire(bus, périphérique_2, fonction, 0x00))
	rÉSULTAT.PériphériqueIdentifiant = uint16(self.Lire(bus, périphérique_2, fonction, 0x02))

	rÉSULTAT.classeIdentifiant = uint8(self.Lire(bus, périphérique_2, fonction, 0x0b))
	rÉSULTAT.subclassIdentifiant = uint8(self.Lire(bus, périphérique_2, fonction, 0x0a))
	rÉSULTAT.interfaceIdentifiant = uint8(self.Lire(bus, périphérique_2, fonction, 0x09))

	rÉSULTAT.revision = uint8(self.Lire(bus, périphérique_2, fonction, 0x08))
	rÉSULTAT.Interruption = uint32(self.Lire(bus, périphérique_2, fonction, 0x3C))

	return rÉSULTAT
}
func (self *TPeripheralcomponentinterconnectcontrôleur) Getbaseaddressregistre(bus uint16, périphérique_2 uint16, fonction uint16, barre uint16) TBaseaddressregistre {
	var rÉSULTAT TBaseaddressregistre

	headertype := self.Lire(bus, périphérique_2, fonction, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if barre >= uint16(maxbars) {
		return rÉSULTAT
	}

	barreValeur := self.Lire(bus, périphérique_2, fonction, uint32(0x10+4*barre))

	if (barreValeur & 0x1) != 0 {
		rÉSULTAT.regtype = 1
	} else {
		rÉSULTAT.regtype = 0
	}

	if rÉSULTAT.regtype == 0 {
	} else {
		rÉSULTAT.address_2 = barreValeur & ^uint32(0x3)
		rÉSULTAT.prefetchcapable = false
	}

	return rÉSULTAT
}
func (self *TPeripheralcomponentinterconnectcontrôleur) Getpilote(périphérique TPeripheralcomponentinterconnectPériphériquedescriptor, interrupts *TInterruptiongestionnaire) {

	self.ipcicontrôleurhandler.Surgetpilote(périphérique)

}
