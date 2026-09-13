package ata

import . "port"
import . "console"

const Bajtovapersector int = 512

type TNaprednotechnologyattachment struct {
	master		bool
	dataport	TPort16bit
	greškaport	TPort8bit
	sectorcountport	TPort8bit
	lbalowport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	uređajport	TPort8bit
	naredbaport	TPort8bit
	controlport	TPort8bit
}

func (self *TNaprednotechnologyattachment) Init(master bool, portbase uint16) {
	self.master = master
	self.dataport.Init(portbase)
	self.greškaport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbalowport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.uređajport.Init(portbase + 0x6)
	self.naredbaport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *TNaprednotechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.uređajport.Piši(0xA0)
	} else {
		self.uređajport.Piši(0xB0)
	}
	self.controlport.Piši(0)
	self.uređajport.Piši(0xA0)

	var status uint8 = self.naredbaport.Čitaj()
	if status == 0xFF {
		console_2.MŠtampaj(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.uređajport.Piši(0xA0)
	} else {
		self.uređajport.Piši(0xB0)
	}
	self.sectorcountport.Piši(0)
	self.lbalowport.Piši(0)
	self.lbamidport.Piši(0)
	self.lbahiport.Piši(0)
	self.naredbaport.Piši(0xEC)

	status = self.naredbaport.Čitaj()
	if status == 0x00 {
		console_2.MŠtampaj(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = self.naredbaport.Čitaj()
	}

	if (status & 0x01) != 0 {
		console_2.MŠtampaj(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Čitaj()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MŠtampajxy(([]byte)("ata ok"), 10, 22)

}
func (self *TNaprednotechnologyattachment) Čitaj28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MŠtampaj(([]byte)("ata read error "))
		return
	}
	if count > Bajtovapersector {
		console_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.uređajport.Piši(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.uređajport.Piši(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.greškaport.Piši(0)
	self.sectorcountport.Piši(1)

	self.lbalowport.Piši(uint8(sector & 0x000000FF))
	self.lbamidport.Piši(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Piši(uint8((sector & 0x00FF0000) >> 16))
	self.naredbaport.Piši(0x20)

	var status uint8 = self.naredbaport.Čitaj()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.naredbaport.Čitaj()
	}

	if (status & 0x01) != 0 {
		console_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	console_2.MŠtampajxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Čitaj()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtovapersector; i += 2 {
		self.dataport.Čitaj()
	}
}
func (self *TNaprednotechnologyattachment) Piši28(sectorBroj uint32, data []byte, count uint32) {

	if sectorBroj > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.uređajport.Piši(uint8(0xE0 | uint8((sectorBroj&0x0F000000)>>24)))
	} else {
		self.uređajport.Piši(uint8(0xF0 | uint8((sectorBroj&0x0F000000)>>24)))
	}

	self.greškaport.Piši(0)
	self.sectorcountport.Piši(1)
	self.lbalowport.Piši(uint8(sectorBroj & 0x000000FF))
	self.lbamidport.Piši(uint8((sectorBroj & 0x0000FF00) >> 8))
	self.lbahiport.Piši(uint8((sectorBroj & 0x00FF0000) >> 16))
	self.naredbaport.Piši(0x30)

	var console_2 = TConsole{}
	console_2.MŠtampaj(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Piši(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MŠtampaj(tekst)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Piši(0x0000)
	}

}

func (self *TNaprednotechnologyattachment) Flush() {
	if self.master {
		self.uređajport.Piši(0xE0)
	} else {
		self.uređajport.Piši(0xF0)
	}
	self.naredbaport.Piši(0xE7)

	var console_2 = TConsole{}

	var status uint8 = self.naredbaport.Čitaj()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.naredbaport.Čitaj()
	}
	if (status & 0x01) != 0 {
		console_2.MŠtampaj(([]byte)(" ata flush error"))
		return
	}

}
