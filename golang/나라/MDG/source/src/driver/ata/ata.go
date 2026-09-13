package ata

import . "irika"
import . "konsoly"

const Octetpersector int = 512

type TAvolentatechnologyattachment struct {
	master			bool
	dataIrika		TIrika16bit
	disoIrika		TIrika8bit
	sectorcountIrika	TIrika8bit
	lbalowIrika		TIrika8bit
	lbamidIrika		TIrika8bit
	lbahiIrika		TIrika8bit
	periferikaIrika		TIrika8bit
	baikoIrika		TIrika8bit
	controlIrika		TIrika8bit
}

func (nytena *TAvolentatechnologyattachment) Init(master bool, irikabase uint16) {
	nytena.master = master
	nytena.dataIrika.Init(irikabase)
	nytena.disoIrika.Init(irikabase + 0x1)
	nytena.sectorcountIrika.Init(irikabase + 0x2)
	nytena.lbalowIrika.Init(irikabase + 0x3)
	nytena.lbamidIrika.Init(irikabase + 0x4)
	nytena.lbahiIrika.Init(irikabase + 0x5)
	nytena.periferikaIrika.Init(irikabase + 0x6)
	nytena.baikoIrika.Init(irikabase + 0x7)
	nytena.controlIrika.Init(irikabase + 0x8)

}

func (nytena *TAvolentatechnologyattachment) Identify() {

	var konsoly_2 = TKonsoly{}

	if nytena.master {
		nytena.periferikaIrika.Manoratra(0xA0)
	} else {
		nytena.periferikaIrika.Manoratra(0xB0)
	}
	nytena.controlIrika.Manoratra(0)
	nytena.periferikaIrika.Manoratra(0xA0)

	var fivoarana uint8 = nytena.baikoIrika.Mamaky()
	if fivoarana == 0xFF {
		konsoly_2.MAtontay(([]byte)("Invalid Status"))
		return
	}

	if nytena.master {
		nytena.periferikaIrika.Manoratra(0xA0)
	} else {
		nytena.periferikaIrika.Manoratra(0xB0)
	}
	nytena.sectorcountIrika.Manoratra(0)
	nytena.lbalowIrika.Manoratra(0)
	nytena.lbamidIrika.Manoratra(0)
	nytena.lbahiIrika.Manoratra(0)
	nytena.baikoIrika.Manoratra(0xEC)

	fivoarana = nytena.baikoIrika.Mamaky()
	if fivoarana == 0x00 {
		konsoly_2.MAtontay(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (fivoarana&0x80) == 0x80 && (fivoarana&0x01) != 0x01 {
		fivoarana = nytena.baikoIrika.Mamaky()
	}

	if (fivoarana & 0x01) != 0 {
		konsoly_2.MAtontay(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = nytena.dataIrika.Mamaky()
		soratra := []byte("  ")
		soratra[0] = uint8((data >> 8) & 0xFF)
		soratra[1] = uint8(data & 0xFF)

	}
	konsoly_2.MAtontayxy(([]byte)("ata ok"), 10, 22)

}
func (nytena *TAvolentatechnologyattachment) Mamaky28(sector uint32, data *[]byte, count int) {
	var konsoly_2 = TKonsoly{}
	if (sector & 0xF0000000) != 0 {
		konsoly_2.MAtontay(([]byte)("ata read error "))
		return
	}
	if count > Octetpersector {
		konsoly_2.MAtontay(([]byte)("ata read error "))
		return
	}

	if nytena.master {
		nytena.periferikaIrika.Manoratra(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		nytena.periferikaIrika.Manoratra(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	nytena.disoIrika.Manoratra(0)
	nytena.sectorcountIrika.Manoratra(1)

	nytena.lbalowIrika.Manoratra(uint8(sector & 0x000000FF))
	nytena.lbamidIrika.Manoratra(uint8((sector & 0x0000FF00) >> 8))
	nytena.lbahiIrika.Manoratra(uint8((sector & 0x00FF0000) >> 16))
	nytena.baikoIrika.Manoratra(0x20)

	var fivoarana uint8 = nytena.baikoIrika.Mamaky()
	for ((fivoarana & 0x80) == 0x80) && ((fivoarana & 0x01) != 0x01) {
		fivoarana = nytena.baikoIrika.Mamaky()
	}

	if (fivoarana & 0x01) != 0 {
		konsoly_2.MAtontay(([]byte)("ata read error "))
		return
	}

	konsoly_2.MAtontayxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = nytena.dataIrika.Mamaky()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Octetpersector; i += 2 {
		nytena.dataIrika.Mamaky()
	}
}
func (nytena *TAvolentatechnologyattachment) Manoratra28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if nytena.master {
		nytena.periferikaIrika.Manoratra(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		nytena.periferikaIrika.Manoratra(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	nytena.disoIrika.Manoratra(0)
	nytena.sectorcountIrika.Manoratra(1)
	nytena.lbalowIrika.Manoratra(uint8(sectornumber & 0x000000FF))
	nytena.lbamidIrika.Manoratra(uint8((sectornumber & 0x0000FF00) >> 8))
	nytena.lbahiIrika.Manoratra(uint8((sectornumber & 0x00FF0000) >> 16))
	nytena.baikoIrika.Manoratra(0x30)

	var konsoly_2 = TKonsoly{}
	konsoly_2.MAtontay(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		nytena.dataIrika.Manoratra(wdata)

		soratra := []byte("  ")
		soratra[0] = uint8((wdata >> 8) & 0xFF)
		soratra[1] = uint8(wdata & 0xFF)

		konsoly_2.MAtontay(soratra)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		nytena.dataIrika.Manoratra(0x0000)
	}

}

func (nytena *TAvolentatechnologyattachment) Flush() {
	if nytena.master {
		nytena.periferikaIrika.Manoratra(0xE0)
	} else {
		nytena.periferikaIrika.Manoratra(0xF0)
	}
	nytena.baikoIrika.Manoratra(0xE7)

	var konsoly_2 = TKonsoly{}

	var fivoarana uint8 = nytena.baikoIrika.Mamaky()
	if fivoarana == 0x00 {
		return
	}

	for ((fivoarana & 0x80) == 0x80) && ((fivoarana & 0x01) != 0x01) {
		fivoarana = nytena.baikoIrika.Mamaky()
	}
	if (fivoarana & 0x01) != 0 {
		konsoly_2.MAtontay(([]byte)(" ata flush error"))
		return
	}

}
