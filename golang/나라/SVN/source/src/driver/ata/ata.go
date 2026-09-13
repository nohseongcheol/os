package ata

import . "vrata"
import . "console"

const Bajtovpersector int = 512

type TNaprednoTehnologijaattachment struct {
	glavni			bool
	dataVrata		TVrata16bit
	napakaVrata		TVrata8bit
	sectorcountVrata	TVrata8bit
	lbaNizkoVrata		TVrata8bit
	lbamidVrata		TVrata8bit
	lbahiVrata		TVrata8bit
	napravaVrata		TVrata8bit
	ukazVrata		TVrata8bit
	nadzorVrata		TVrata8bit
}

func (sam *TNaprednoTehnologijaattachment) Init(glavni bool, vratabase uint16) {
	sam.glavni = glavni
	sam.dataVrata.Init(vratabase)
	sam.napakaVrata.Init(vratabase + 0x1)
	sam.sectorcountVrata.Init(vratabase + 0x2)
	sam.lbaNizkoVrata.Init(vratabase + 0x3)
	sam.lbamidVrata.Init(vratabase + 0x4)
	sam.lbahiVrata.Init(vratabase + 0x5)
	sam.napravaVrata.Init(vratabase + 0x6)
	sam.ukazVrata.Init(vratabase + 0x7)
	sam.nadzorVrata.Init(vratabase + 0x8)

}

func (sam *TNaprednoTehnologijaattachment) Identify() {

	var console_2 = TConsole{}

	if sam.glavni {
		sam.napravaVrata.Pisanje(0xA0)
	} else {
		sam.napravaVrata.Pisanje(0xB0)
	}
	sam.nadzorVrata.Pisanje(0)
	sam.napravaVrata.Pisanje(0xA0)

	var stanje uint8 = sam.ukazVrata.Branje()
	if stanje == 0xFF {
		console_2.MNatisni(([]byte)("Invalid Status"))
		return
	}

	if sam.glavni {
		sam.napravaVrata.Pisanje(0xA0)
	} else {
		sam.napravaVrata.Pisanje(0xB0)
	}
	sam.sectorcountVrata.Pisanje(0)
	sam.lbaNizkoVrata.Pisanje(0)
	sam.lbamidVrata.Pisanje(0)
	sam.lbahiVrata.Pisanje(0)
	sam.ukazVrata.Pisanje(0xEC)

	stanje = sam.ukazVrata.Branje()
	if stanje == 0x00 {
		console_2.MNatisni(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stanje&0x80) == 0x80 && (stanje&0x01) != 0x01 {
		stanje = sam.ukazVrata.Branje()
	}

	if (stanje & 0x01) != 0 {
		console_2.MNatisni(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = sam.dataVrata.Branje()
		besedilo := []byte("  ")
		besedilo[0] = uint8((data >> 8) & 0xFF)
		besedilo[1] = uint8(data & 0xFF)

	}
	console_2.MNatisnixy(([]byte)("ata ok"), 10, 22)

}
func (sam *TNaprednoTehnologijaattachment) Branje28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MNatisni(([]byte)("ata read error "))
		return
	}
	if count > Bajtovpersector {
		console_2.MNatisni(([]byte)("ata read error "))
		return
	}

	if sam.glavni {
		sam.napravaVrata.Pisanje(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		sam.napravaVrata.Pisanje(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	sam.napakaVrata.Pisanje(0)
	sam.sectorcountVrata.Pisanje(1)

	sam.lbaNizkoVrata.Pisanje(uint8(sector & 0x000000FF))
	sam.lbamidVrata.Pisanje(uint8((sector & 0x0000FF00) >> 8))
	sam.lbahiVrata.Pisanje(uint8((sector & 0x00FF0000) >> 16))
	sam.ukazVrata.Pisanje(0x20)

	var stanje uint8 = sam.ukazVrata.Branje()
	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = sam.ukazVrata.Branje()
	}

	if (stanje & 0x01) != 0 {
		console_2.MNatisni(([]byte)("ata read error "))
		return
	}

	console_2.MNatisnixy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = sam.dataVrata.Branje()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtovpersector; i += 2 {
		sam.dataVrata.Branje()
	}
}
func (sam *TNaprednoTehnologijaattachment) Pisanje28(sectorŠtevilka uint32, data []byte, count uint32) {

	if sectorŠtevilka > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if sam.glavni {
		sam.napravaVrata.Pisanje(uint8(0xE0 | uint8((sectorŠtevilka&0x0F000000)>>24)))
	} else {
		sam.napravaVrata.Pisanje(uint8(0xF0 | uint8((sectorŠtevilka&0x0F000000)>>24)))
	}

	sam.napakaVrata.Pisanje(0)
	sam.sectorcountVrata.Pisanje(1)
	sam.lbaNizkoVrata.Pisanje(uint8(sectorŠtevilka & 0x000000FF))
	sam.lbamidVrata.Pisanje(uint8((sectorŠtevilka & 0x0000FF00) >> 8))
	sam.lbahiVrata.Pisanje(uint8((sectorŠtevilka & 0x00FF0000) >> 16))
	sam.ukazVrata.Pisanje(0x30)

	var console_2 = TConsole{}
	console_2.MNatisni(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		sam.dataVrata.Pisanje(wdata)

		besedilo := []byte("  ")
		besedilo[0] = uint8((wdata >> 8) & 0xFF)
		besedilo[1] = uint8(wdata & 0xFF)

		console_2.MNatisni(besedilo)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		sam.dataVrata.Pisanje(0x0000)
	}

}

func (sam *TNaprednoTehnologijaattachment) Flush() {
	if sam.glavni {
		sam.napravaVrata.Pisanje(0xE0)
	} else {
		sam.napravaVrata.Pisanje(0xF0)
	}
	sam.ukazVrata.Pisanje(0xE7)

	var console_2 = TConsole{}

	var stanje uint8 = sam.ukazVrata.Branje()
	if stanje == 0x00 {
		return
	}

	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = sam.ukazVrata.Branje()
	}
	if (stanje & 0x01) != 0 {
		console_2.MNatisni(([]byte)(" ata flush error"))
		return
	}

}
