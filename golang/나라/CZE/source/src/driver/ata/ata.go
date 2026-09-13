package ata

import . "port"
import . "konzole"

const Bytůpersector int = 512

type TPokročiléTechnologieattachment struct {
	hlavní		bool
	dataport	TPort16bit
	chybaport	TPort8bit
	sectorPočetport	TPort8bit
	lbaNízkáport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	zařízeníport	TPort8bit
	příkazport	TPort8bit
	ovládáníport	TPort8bit
}

func (self *TPokročiléTechnologieattachment) Init(hlavní bool, portbase uint16) {
	self.hlavní = hlavní
	self.dataport.Init(portbase)
	self.chybaport.Init(portbase + 0x1)
	self.sectorPočetport.Init(portbase + 0x2)
	self.lbaNízkáport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.zařízeníport.Init(portbase + 0x6)
	self.příkazport.Init(portbase + 0x7)
	self.ovládáníport.Init(portbase + 0x8)

}

func (self *TPokročiléTechnologieattachment) Identify() {

	var konzole_2 = TKonzole{}

	if self.hlavní {
		self.zařízeníport.Zápis(0xA0)
	} else {
		self.zařízeníport.Zápis(0xB0)
	}
	self.ovládáníport.Zápis(0)
	self.zařízeníport.Zápis(0xA0)

	var stav uint8 = self.příkazport.Čtení()
	if stav == 0xFF {
		konzole_2.MTisknout(([]byte)("Invalid Status"))
		return
	}

	if self.hlavní {
		self.zařízeníport.Zápis(0xA0)
	} else {
		self.zařízeníport.Zápis(0xB0)
	}
	self.sectorPočetport.Zápis(0)
	self.lbaNízkáport.Zápis(0)
	self.lbamidport.Zápis(0)
	self.lbahiport.Zápis(0)
	self.příkazport.Zápis(0xEC)

	stav = self.příkazport.Čtení()
	if stav == 0x00 {
		konzole_2.MTisknout(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stav&0x80) == 0x80 && (stav&0x01) != 0x01 {
		stav = self.příkazport.Čtení()
	}

	if (stav & 0x01) != 0 {
		konzole_2.MTisknout(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Čtení()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	konzole_2.MTisknoutxy(([]byte)("ata ok"), 10, 22)

}
func (self *TPokročiléTechnologieattachment) Čtení28(sector uint32, data *[]byte, počet int) {
	var konzole_2 = TKonzole{}
	if (sector & 0xF0000000) != 0 {
		konzole_2.MTisknout(([]byte)("ata read error "))
		return
	}
	if počet > Bytůpersector {
		konzole_2.MTisknout(([]byte)("ata read error "))
		return
	}

	if self.hlavní {
		self.zařízeníport.Zápis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.zařízeníport.Zápis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.chybaport.Zápis(0)
	self.sectorPočetport.Zápis(1)

	self.lbaNízkáport.Zápis(uint8(sector & 0x000000FF))
	self.lbamidport.Zápis(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Zápis(uint8((sector & 0x00FF0000) >> 16))
	self.příkazport.Zápis(0x20)

	var stav uint8 = self.příkazport.Čtení()
	for ((stav & 0x80) == 0x80) && ((stav & 0x01) != 0x01) {
		stav = self.příkazport.Čtení()
	}

	if (stav & 0x01) != 0 {
		konzole_2.MTisknout(([]byte)("ata read error "))
		return
	}

	konzole_2.MTisknoutxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < počet; i += 2 {
		var wdata uint16 = self.dataport.Čtení()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < počet {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (počet + (počet % 2)); i < Bytůpersector; i += 2 {
		self.dataport.Čtení()
	}
}
func (self *TPokročiléTechnologieattachment) Zápis28(sectorČíslo uint32, data []byte, počet uint32) {

	if sectorČíslo > 0x0FFFFFFF {
		return
	}

	if počet > 512 {
		return
	}

	if self.hlavní {
		self.zařízeníport.Zápis(uint8(0xE0 | uint8((sectorČíslo&0x0F000000)>>24)))
	} else {
		self.zařízeníport.Zápis(uint8(0xF0 | uint8((sectorČíslo&0x0F000000)>>24)))
	}

	self.chybaport.Zápis(0)
	self.sectorPočetport.Zápis(1)
	self.lbaNízkáport.Zápis(uint8(sectorČíslo & 0x000000FF))
	self.lbamidport.Zápis(uint8((sectorČíslo & 0x0000FF00) >> 8))
	self.lbahiport.Zápis(uint8((sectorČíslo & 0x00FF0000) >> 16))
	self.příkazport.Zápis(0x30)

	var konzole_2 = TKonzole{}
	konzole_2.MTisknout(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < počet; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < počet {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Zápis(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		konzole_2.MTisknout(text)
	}

	for i := (počet + (počet % 2)); i < 512; i += 2 {
		self.dataport.Zápis(0x0000)
	}

}

func (self *TPokročiléTechnologieattachment) Flush() {
	if self.hlavní {
		self.zařízeníport.Zápis(0xE0)
	} else {
		self.zařízeníport.Zápis(0xF0)
	}
	self.příkazport.Zápis(0xE7)

	var konzole_2 = TKonzole{}

	var stav uint8 = self.příkazport.Čtení()
	if stav == 0x00 {
		return
	}

	for ((stav & 0x80) == 0x80) && ((stav & 0x01) != 0x01) {
		stav = self.příkazport.Čtení()
	}
	if (stav & 0x01) != 0 {
		konzole_2.MTisknout(([]byte)(" ata flush error"))
		return
	}

}
