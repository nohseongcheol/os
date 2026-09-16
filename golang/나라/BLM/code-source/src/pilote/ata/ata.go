/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Octetspersector int = 512

type TAvancéTechnologieattachment struct {
	maître			bool
	donnéesport		TPort16bit
	erreurport		TPort8bit
	sectorNombreport	TPort8bit
	lbaBasseport		TPort8bit
	lbamidport		TPort8bit
	lbahiport		TPort8bit
	périphériqueport	TPort8bit
	commandeport		TPort8bit
	ctrlport		TPort8bit
}

func (self *TAvancéTechnologieattachment) Init(maître bool, portbase uint16) {
	self.maître = maître
	self.donnéesport.Init(portbase)
	self.erreurport.Init(portbase + 0x1)
	self.sectorNombreport.Init(portbase + 0x2)
	self.lbaBasseport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.périphériqueport.Init(portbase + 0x6)
	self.commandeport.Init(portbase + 0x7)
	self.ctrlport.Init(portbase + 0x8)

}

func (self *TAvancéTechnologieattachment) Identify() {

	var console_2 = TConsole{}

	if self.maître {
		self.périphériqueport.Écrire(0xA0)
	} else {
		self.périphériqueport.Écrire(0xB0)
	}
	self.ctrlport.Écrire(0)
	self.périphériqueport.Écrire(0xA0)

	var état uint8 = self.commandeport.Lire()
	if état == 0xFF {
		console_2.MImprimer(([]byte)("Invalid Status"))
		return
	}

	if self.maître {
		self.périphériqueport.Écrire(0xA0)
	} else {
		self.périphériqueport.Écrire(0xB0)
	}
	self.sectorNombreport.Écrire(0)
	self.lbaBasseport.Écrire(0)
	self.lbamidport.Écrire(0)
	self.lbahiport.Écrire(0)
	self.commandeport.Écrire(0xEC)

	état = self.commandeport.Lire()
	if état == 0x00 {
		console_2.MImprimer(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (état&0x80) == 0x80 && (état&0x01) != 0x01 {
		état = self.commandeport.Lire()
	}

	if (état & 0x01) != 0 {
		console_2.MImprimer(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var données = self.donnéesport.Lire()
		texte := []byte("  ")
		texte[0] = uint8((données >> 8) & 0xFF)
		texte[1] = uint8(données & 0xFF)

	}
	console_2.MImprimerxy(([]byte)("ata ok"), 10, 22)

}
func (self *TAvancéTechnologieattachment) Lire28(sector uint32, données *[]byte, nombre int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MImprimer(([]byte)("ata read error "))
		return
	}
	if nombre > Octetspersector {
		console_2.MImprimer(([]byte)("ata read error "))
		return
	}

	if self.maître {
		self.périphériqueport.Écrire(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.périphériqueport.Écrire(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.erreurport.Écrire(0)
	self.sectorNombreport.Écrire(1)

	self.lbaBasseport.Écrire(uint8(sector & 0x000000FF))
	self.lbamidport.Écrire(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Écrire(uint8((sector & 0x00FF0000) >> 16))
	self.commandeport.Écrire(0x20)

	var état uint8 = self.commandeport.Lire()
	for ((état & 0x80) == 0x80) && ((état & 0x01) != 0x01) {
		état = self.commandeport.Lire()
	}

	if (état & 0x01) != 0 {
		console_2.MImprimer(([]byte)("ata read error "))
		return
	}

	console_2.MImprimerxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < nombre; i += 2 {
		var wdata uint16 = self.donnéesport.Lire()

		(*données)[i] = uint8(wdata & 0x00FF)
		if i+1 < nombre {

			(*données)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (nombre + (nombre % 2)); i < Octetspersector; i += 2 {
		self.donnéesport.Lire()
	}
}
func (self *TAvancéTechnologieattachment) Écrire28(sectorNombre uint32, données []byte, nombre uint32) {

	if sectorNombre > 0x0FFFFFFF {
		return
	}

	if nombre > 512 {
		return
	}

	if self.maître {
		self.périphériqueport.Écrire(uint8(0xE0 | uint8((sectorNombre&0x0F000000)>>24)))
	} else {
		self.périphériqueport.Écrire(uint8(0xF0 | uint8((sectorNombre&0x0F000000)>>24)))
	}

	self.erreurport.Écrire(0)
	self.sectorNombreport.Écrire(1)
	self.lbaBasseport.Écrire(uint8(sectorNombre & 0x000000FF))
	self.lbamidport.Écrire(uint8((sectorNombre & 0x0000FF00) >> 8))
	self.lbahiport.Écrire(uint8((sectorNombre & 0x00FF0000) >> 16))
	self.commandeport.Écrire(0x30)

	var console_2 = TConsole{}
	console_2.MImprimer(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < nombre; i += 2 {

		var wdata uint16 = uint16(données[i])

		if i+1 < nombre {
			wdata = wdata | (uint16(données[i+1]) << 8)
		}

		self.donnéesport.Écrire(wdata)

		texte := []byte("  ")
		texte[0] = uint8((wdata >> 8) & 0xFF)
		texte[1] = uint8(wdata & 0xFF)

		console_2.MImprimer(texte)
	}

	for i := (nombre + (nombre % 2)); i < 512; i += 2 {
		self.donnéesport.Écrire(0x0000)
	}

}

func (self *TAvancéTechnologieattachment) Flush() {
	if self.maître {
		self.périphériqueport.Écrire(0xE0)
	} else {
		self.périphériqueport.Écrire(0xF0)
	}
	self.commandeport.Écrire(0xE7)

	var console_2 = TConsole{}

	var état uint8 = self.commandeport.Lire()
	if état == 0x00 {
		return
	}

	for ((état & 0x80) == 0x80) && ((état & 0x01) != 0x01) {
		état = self.commandeport.Lire()
	}
	if (état & 0x01) != 0 {
		console_2.MImprimer(([]byte)(" ata flush error"))
		return
	}

}
