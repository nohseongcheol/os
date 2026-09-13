package ata

import . "portti"
import . "konsoli"

const Tavuapersector int = 512

type TLisäasetuksetTekniikkaattachment struct {
	master			bool
	dataPortti		TPortti16bit
	virhePortti		TPortti8bit
	sectorcountPortti	TPortti8bit
	lbaMatalaPortti		TPortti8bit
	lbamidPortti		TPortti8bit
	lbahiPortti		TPortti8bit
	laitePortti		TPortti8bit
	komentoPortti		TPortti8bit
	ctrlPortti		TPortti8bit
}

func (itse *TLisäasetuksetTekniikkaattachment) Init(master bool, porttibase uint16) {
	itse.master = master
	itse.dataPortti.Init(porttibase)
	itse.virhePortti.Init(porttibase + 0x1)
	itse.sectorcountPortti.Init(porttibase + 0x2)
	itse.lbaMatalaPortti.Init(porttibase + 0x3)
	itse.lbamidPortti.Init(porttibase + 0x4)
	itse.lbahiPortti.Init(porttibase + 0x5)
	itse.laitePortti.Init(porttibase + 0x6)
	itse.komentoPortti.Init(porttibase + 0x7)
	itse.ctrlPortti.Init(porttibase + 0x8)

}

func (itse *TLisäasetuksetTekniikkaattachment) Identify() {

	var konsoli_2 = TKonsoli{}

	if itse.master {
		itse.laitePortti.Kirjoitus(0xA0)
	} else {
		itse.laitePortti.Kirjoitus(0xB0)
	}
	itse.ctrlPortti.Kirjoitus(0)
	itse.laitePortti.Kirjoitus(0xA0)

	var tila uint8 = itse.komentoPortti.Luku()
	if tila == 0xFF {
		konsoli_2.MTulosta(([]byte)("Invalid Status"))
		return
	}

	if itse.master {
		itse.laitePortti.Kirjoitus(0xA0)
	} else {
		itse.laitePortti.Kirjoitus(0xB0)
	}
	itse.sectorcountPortti.Kirjoitus(0)
	itse.lbaMatalaPortti.Kirjoitus(0)
	itse.lbamidPortti.Kirjoitus(0)
	itse.lbahiPortti.Kirjoitus(0)
	itse.komentoPortti.Kirjoitus(0xEC)

	tila = itse.komentoPortti.Luku()
	if tila == 0x00 {
		konsoli_2.MTulosta(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (tila&0x80) == 0x80 && (tila&0x01) != 0x01 {
		tila = itse.komentoPortti.Luku()
	}

	if (tila & 0x01) != 0 {
		konsoli_2.MTulosta(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = itse.dataPortti.Luku()
		teksti := []byte("  ")
		teksti[0] = uint8((data >> 8) & 0xFF)
		teksti[1] = uint8(data & 0xFF)

	}
	konsoli_2.MTulostaxy(([]byte)("ata ok"), 10, 22)

}
func (itse *TLisäasetuksetTekniikkaattachment) Luku28(sector uint32, data *[]byte, count int) {
	var konsoli_2 = TKonsoli{}
	if (sector & 0xF0000000) != 0 {
		konsoli_2.MTulosta(([]byte)("ata read error "))
		return
	}
	if count > Tavuapersector {
		konsoli_2.MTulosta(([]byte)("ata read error "))
		return
	}

	if itse.master {
		itse.laitePortti.Kirjoitus(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		itse.laitePortti.Kirjoitus(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	itse.virhePortti.Kirjoitus(0)
	itse.sectorcountPortti.Kirjoitus(1)

	itse.lbaMatalaPortti.Kirjoitus(uint8(sector & 0x000000FF))
	itse.lbamidPortti.Kirjoitus(uint8((sector & 0x0000FF00) >> 8))
	itse.lbahiPortti.Kirjoitus(uint8((sector & 0x00FF0000) >> 16))
	itse.komentoPortti.Kirjoitus(0x20)

	var tila uint8 = itse.komentoPortti.Luku()
	for ((tila & 0x80) == 0x80) && ((tila & 0x01) != 0x01) {
		tila = itse.komentoPortti.Luku()
	}

	if (tila & 0x01) != 0 {
		konsoli_2.MTulosta(([]byte)("ata read error "))
		return
	}

	konsoli_2.MTulostaxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = itse.dataPortti.Luku()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Tavuapersector; i += 2 {
		itse.dataPortti.Luku()
	}
}
func (itse *TLisäasetuksetTekniikkaattachment) Kirjoitus28(sectorNumero uint32, data []byte, count uint32) {

	if sectorNumero > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if itse.master {
		itse.laitePortti.Kirjoitus(uint8(0xE0 | uint8((sectorNumero&0x0F000000)>>24)))
	} else {
		itse.laitePortti.Kirjoitus(uint8(0xF0 | uint8((sectorNumero&0x0F000000)>>24)))
	}

	itse.virhePortti.Kirjoitus(0)
	itse.sectorcountPortti.Kirjoitus(1)
	itse.lbaMatalaPortti.Kirjoitus(uint8(sectorNumero & 0x000000FF))
	itse.lbamidPortti.Kirjoitus(uint8((sectorNumero & 0x0000FF00) >> 8))
	itse.lbahiPortti.Kirjoitus(uint8((sectorNumero & 0x00FF0000) >> 16))
	itse.komentoPortti.Kirjoitus(0x30)

	var konsoli_2 = TKonsoli{}
	konsoli_2.MTulosta(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		itse.dataPortti.Kirjoitus(wdata)

		teksti := []byte("  ")
		teksti[0] = uint8((wdata >> 8) & 0xFF)
		teksti[1] = uint8(wdata & 0xFF)

		konsoli_2.MTulosta(teksti)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		itse.dataPortti.Kirjoitus(0x0000)
	}

}

func (itse *TLisäasetuksetTekniikkaattachment) Flush() {
	if itse.master {
		itse.laitePortti.Kirjoitus(0xE0)
	} else {
		itse.laitePortti.Kirjoitus(0xF0)
	}
	itse.komentoPortti.Kirjoitus(0xE7)

	var konsoli_2 = TKonsoli{}

	var tila uint8 = itse.komentoPortti.Luku()
	if tila == 0x00 {
		return
	}

	for ((tila & 0x80) == 0x80) && ((tila & 0x01) != 0x01) {
		tila = itse.komentoPortti.Luku()
	}
	if (tila & 0x01) != 0 {
		konsoli_2.MTulosta(([]byte)(" ata flush error"))
		return
	}

}
