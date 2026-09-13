package ata

import . "prievadas"
import . "console"

const Baitųpersector int = 512

type TIšsamiauTechnologijaattachment struct {
	pagrindinis		bool
	dataPrievadas		TPrievadas16bit
	klaidaPrievadas		TPrievadas8bit
	sectorcountPrievadas	TPrievadas8bit
	lbaŽemasPrievadas	TPrievadas8bit
	lbamidPrievadas		TPrievadas8bit
	lbahiPrievadas		TPrievadas8bit
	įrenginysPrievadas	TPrievadas8bit
	komandaPrievadas	TPrievadas8bit
	valdymasPrievadas	TPrievadas8bit
}

func (self *TIšsamiauTechnologijaattachment) Init(pagrindinis bool, prievadasbase uint16) {
	self.pagrindinis = pagrindinis
	self.dataPrievadas.Init(prievadasbase)
	self.klaidaPrievadas.Init(prievadasbase + 0x1)
	self.sectorcountPrievadas.Init(prievadasbase + 0x2)
	self.lbaŽemasPrievadas.Init(prievadasbase + 0x3)
	self.lbamidPrievadas.Init(prievadasbase + 0x4)
	self.lbahiPrievadas.Init(prievadasbase + 0x5)
	self.įrenginysPrievadas.Init(prievadasbase + 0x6)
	self.komandaPrievadas.Init(prievadasbase + 0x7)
	self.valdymasPrievadas.Init(prievadasbase + 0x8)

}

func (self *TIšsamiauTechnologijaattachment) Identify() {

	var console_2 = TConsole{}

	if self.pagrindinis {
		self.įrenginysPrievadas.Rašymas(0xA0)
	} else {
		self.įrenginysPrievadas.Rašymas(0xB0)
	}
	self.valdymasPrievadas.Rašymas(0)
	self.įrenginysPrievadas.Rašymas(0xA0)

	var būsena uint8 = self.komandaPrievadas.Skaitymas()
	if būsena == 0xFF {
		console_2.MSpausdinti(([]byte)("Invalid Status"))
		return
	}

	if self.pagrindinis {
		self.įrenginysPrievadas.Rašymas(0xA0)
	} else {
		self.įrenginysPrievadas.Rašymas(0xB0)
	}
	self.sectorcountPrievadas.Rašymas(0)
	self.lbaŽemasPrievadas.Rašymas(0)
	self.lbamidPrievadas.Rašymas(0)
	self.lbahiPrievadas.Rašymas(0)
	self.komandaPrievadas.Rašymas(0xEC)

	būsena = self.komandaPrievadas.Skaitymas()
	if būsena == 0x00 {
		console_2.MSpausdinti(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (būsena&0x80) == 0x80 && (būsena&0x01) != 0x01 {
		būsena = self.komandaPrievadas.Skaitymas()
	}

	if (būsena & 0x01) != 0 {
		console_2.MSpausdinti(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataPrievadas.Skaitymas()
		tekstas := []byte("  ")
		tekstas[0] = uint8((data >> 8) & 0xFF)
		tekstas[1] = uint8(data & 0xFF)

	}
	console_2.MSpausdintixy(([]byte)("ata ok"), 10, 22)

}
func (self *TIšsamiauTechnologijaattachment) Skaitymas28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MSpausdinti(([]byte)("ata read error "))
		return
	}
	if count > Baitųpersector {
		console_2.MSpausdinti(([]byte)("ata read error "))
		return
	}

	if self.pagrindinis {
		self.įrenginysPrievadas.Rašymas(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.įrenginysPrievadas.Rašymas(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.klaidaPrievadas.Rašymas(0)
	self.sectorcountPrievadas.Rašymas(1)

	self.lbaŽemasPrievadas.Rašymas(uint8(sector & 0x000000FF))
	self.lbamidPrievadas.Rašymas(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiPrievadas.Rašymas(uint8((sector & 0x00FF0000) >> 16))
	self.komandaPrievadas.Rašymas(0x20)

	var būsena uint8 = self.komandaPrievadas.Skaitymas()
	for ((būsena & 0x80) == 0x80) && ((būsena & 0x01) != 0x01) {
		būsena = self.komandaPrievadas.Skaitymas()
	}

	if (būsena & 0x01) != 0 {
		console_2.MSpausdinti(([]byte)("ata read error "))
		return
	}

	console_2.MSpausdintixy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataPrievadas.Skaitymas()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baitųpersector; i += 2 {
		self.dataPrievadas.Skaitymas()
	}
}
func (self *TIšsamiauTechnologijaattachment) Rašymas28(sectorSkaičius uint32, data []byte, count uint32) {

	if sectorSkaičius > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.pagrindinis {
		self.įrenginysPrievadas.Rašymas(uint8(0xE0 | uint8((sectorSkaičius&0x0F000000)>>24)))
	} else {
		self.įrenginysPrievadas.Rašymas(uint8(0xF0 | uint8((sectorSkaičius&0x0F000000)>>24)))
	}

	self.klaidaPrievadas.Rašymas(0)
	self.sectorcountPrievadas.Rašymas(1)
	self.lbaŽemasPrievadas.Rašymas(uint8(sectorSkaičius & 0x000000FF))
	self.lbamidPrievadas.Rašymas(uint8((sectorSkaičius & 0x0000FF00) >> 8))
	self.lbahiPrievadas.Rašymas(uint8((sectorSkaičius & 0x00FF0000) >> 16))
	self.komandaPrievadas.Rašymas(0x30)

	var console_2 = TConsole{}
	console_2.MSpausdinti(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataPrievadas.Rašymas(wdata)

		tekstas := []byte("  ")
		tekstas[0] = uint8((wdata >> 8) & 0xFF)
		tekstas[1] = uint8(wdata & 0xFF)

		console_2.MSpausdinti(tekstas)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataPrievadas.Rašymas(0x0000)
	}

}

func (self *TIšsamiauTechnologijaattachment) Flush() {
	if self.pagrindinis {
		self.įrenginysPrievadas.Rašymas(0xE0)
	} else {
		self.įrenginysPrievadas.Rašymas(0xF0)
	}
	self.komandaPrievadas.Rašymas(0xE7)

	var console_2 = TConsole{}

	var būsena uint8 = self.komandaPrievadas.Skaitymas()
	if būsena == 0x00 {
		return
	}

	for ((būsena & 0x80) == 0x80) && ((būsena & 0x01) != 0x01) {
		būsena = self.komandaPrievadas.Skaitymas()
	}
	if (būsena & 0x01) != 0 {
		console_2.MSpausdinti(([]byte)(" ata flush error"))
		return
	}

}
