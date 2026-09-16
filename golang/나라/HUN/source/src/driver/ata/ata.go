/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "konzol"

const Bájtpersector int = 512

type THaladóTechnológiaattachment struct {
	fő			bool
	dataport		TPort16bit
	hibaport		TPort8bit
	sectorSzámlálóport	TPort8bit
	lbaAlacsonyport		TPort8bit
	lbamidport		TPort8bit
	lbahiport		TPort8bit
	eszközport		TPort8bit
	parancsport		TPort8bit
	vezérlésport		TPort8bit
}

func (self *THaladóTechnológiaattachment) Init(fő bool, portbase uint16) {
	self.fő = fő
	self.dataport.Init(portbase)
	self.hibaport.Init(portbase + 0x1)
	self.sectorSzámlálóport.Init(portbase + 0x2)
	self.lbaAlacsonyport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.eszközport.Init(portbase + 0x6)
	self.parancsport.Init(portbase + 0x7)
	self.vezérlésport.Init(portbase + 0x8)

}

func (self *THaladóTechnológiaattachment) Identify() {

	var konzol_2 = TKonzol{}

	if self.fő {
		self.eszközport.Írás(0xA0)
	} else {
		self.eszközport.Írás(0xB0)
	}
	self.vezérlésport.Írás(0)
	self.eszközport.Írás(0xA0)

	var állapot uint8 = self.parancsport.Olvasás()
	if állapot == 0xFF {
		konzol_2.MNyomtatás(([]byte)("Invalid Status"))
		return
	}

	if self.fő {
		self.eszközport.Írás(0xA0)
	} else {
		self.eszközport.Írás(0xB0)
	}
	self.sectorSzámlálóport.Írás(0)
	self.lbaAlacsonyport.Írás(0)
	self.lbamidport.Írás(0)
	self.lbahiport.Írás(0)
	self.parancsport.Írás(0xEC)

	állapot = self.parancsport.Olvasás()
	if állapot == 0x00 {
		konzol_2.MNyomtatás(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (állapot&0x80) == 0x80 && (állapot&0x01) != 0x01 {
		állapot = self.parancsport.Olvasás()
	}

	if (állapot & 0x01) != 0 {
		konzol_2.MNyomtatás(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Olvasás()
		szöveg := []byte("  ")
		szöveg[0] = uint8((data >> 8) & 0xFF)
		szöveg[1] = uint8(data & 0xFF)

	}
	konzol_2.MNyomtatásxy(([]byte)("ata ok"), 10, 22)

}
func (self *THaladóTechnológiaattachment) Olvasás28(sector uint32, data *[]byte, számláló int) {
	var konzol_2 = TKonzol{}
	if (sector & 0xF0000000) != 0 {
		konzol_2.MNyomtatás(([]byte)("ata read error "))
		return
	}
	if számláló > Bájtpersector {
		konzol_2.MNyomtatás(([]byte)("ata read error "))
		return
	}

	if self.fő {
		self.eszközport.Írás(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.eszközport.Írás(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.hibaport.Írás(0)
	self.sectorSzámlálóport.Írás(1)

	self.lbaAlacsonyport.Írás(uint8(sector & 0x000000FF))
	self.lbamidport.Írás(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Írás(uint8((sector & 0x00FF0000) >> 16))
	self.parancsport.Írás(0x20)

	var állapot uint8 = self.parancsport.Olvasás()
	for ((állapot & 0x80) == 0x80) && ((állapot & 0x01) != 0x01) {
		állapot = self.parancsport.Olvasás()
	}

	if (állapot & 0x01) != 0 {
		konzol_2.MNyomtatás(([]byte)("ata read error "))
		return
	}

	konzol_2.MNyomtatásxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < számláló; i += 2 {
		var wdata uint16 = self.dataport.Olvasás()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < számláló {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (számláló + (számláló % 2)); i < Bájtpersector; i += 2 {
		self.dataport.Olvasás()
	}
}
func (self *THaladóTechnológiaattachment) Írás28(sectorSzám uint32, data []byte, számláló uint32) {

	if sectorSzám > 0x0FFFFFFF {
		return
	}

	if számláló > 512 {
		return
	}

	if self.fő {
		self.eszközport.Írás(uint8(0xE0 | uint8((sectorSzám&0x0F000000)>>24)))
	} else {
		self.eszközport.Írás(uint8(0xF0 | uint8((sectorSzám&0x0F000000)>>24)))
	}

	self.hibaport.Írás(0)
	self.sectorSzámlálóport.Írás(1)
	self.lbaAlacsonyport.Írás(uint8(sectorSzám & 0x000000FF))
	self.lbamidport.Írás(uint8((sectorSzám & 0x0000FF00) >> 8))
	self.lbahiport.Írás(uint8((sectorSzám & 0x00FF0000) >> 16))
	self.parancsport.Írás(0x30)

	var konzol_2 = TKonzol{}
	konzol_2.MNyomtatás(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < számláló; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < számláló {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Írás(wdata)

		szöveg := []byte("  ")
		szöveg[0] = uint8((wdata >> 8) & 0xFF)
		szöveg[1] = uint8(wdata & 0xFF)

		konzol_2.MNyomtatás(szöveg)
	}

	for i := (számláló + (számláló % 2)); i < 512; i += 2 {
		self.dataport.Írás(0x0000)
	}

}

func (self *THaladóTechnológiaattachment) Flush() {
	if self.fő {
		self.eszközport.Írás(0xE0)
	} else {
		self.eszközport.Írás(0xF0)
	}
	self.parancsport.Írás(0xE7)

	var konzol_2 = TKonzol{}

	var állapot uint8 = self.parancsport.Olvasás()
	if állapot == 0x00 {
		return
	}

	for ((állapot & 0x80) == 0x80) && ((állapot & 0x01) != 0x01) {
		állapot = self.parancsport.Olvasás()
	}
	if (állapot & 0x01) != 0 {
		konzol_2.MNyomtatás(([]byte)(" ata flush error"))
		return
	}

}
