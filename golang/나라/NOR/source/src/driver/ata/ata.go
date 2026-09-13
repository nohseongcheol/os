package ata

import . "port"
import . "console"

const Bytepersector int = 512

type TAvansertTeknologiattachment struct {
	hovedinnstilling	bool
	dataport		TPort16bit
	feilport		TPort8bit
	sectorAntallport	TPort8bit
	lbaLavport		TPort8bit
	lbamidport		TPort8bit
	lbahiport		TPort8bit
	enhetport		TPort8bit
	kommandoport		TPort8bit
	kontrollport		TPort8bit
}

func (selv *TAvansertTeknologiattachment) Init(hovedinnstilling bool, portbase uint16) {
	selv.hovedinnstilling = hovedinnstilling
	selv.dataport.Init(portbase)
	selv.feilport.Init(portbase + 0x1)
	selv.sectorAntallport.Init(portbase + 0x2)
	selv.lbaLavport.Init(portbase + 0x3)
	selv.lbamidport.Init(portbase + 0x4)
	selv.lbahiport.Init(portbase + 0x5)
	selv.enhetport.Init(portbase + 0x6)
	selv.kommandoport.Init(portbase + 0x7)
	selv.kontrollport.Init(portbase + 0x8)

}

func (selv *TAvansertTeknologiattachment) Identify() {

	var console_2 = TConsole{}

	if selv.hovedinnstilling {
		selv.enhetport.Skriv(0xA0)
	} else {
		selv.enhetport.Skriv(0xB0)
	}
	selv.kontrollport.Skriv(0)
	selv.enhetport.Skriv(0xA0)

	var status uint8 = selv.kommandoport.Les()
	if status == 0xFF {
		console_2.MSkrivut(([]byte)("Invalid Status"))
		return
	}

	if selv.hovedinnstilling {
		selv.enhetport.Skriv(0xA0)
	} else {
		selv.enhetport.Skriv(0xB0)
	}
	selv.sectorAntallport.Skriv(0)
	selv.lbaLavport.Skriv(0)
	selv.lbamidport.Skriv(0)
	selv.lbahiport.Skriv(0)
	selv.kommandoport.Skriv(0xEC)

	status = selv.kommandoport.Les()
	if status == 0x00 {
		console_2.MSkrivut(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = selv.kommandoport.Les()
	}

	if (status & 0x01) != 0 {
		console_2.MSkrivut(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = selv.dataport.Les()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MSkrivutxy(([]byte)("ata ok"), 10, 22)

}
func (selv *TAvansertTeknologiattachment) Les28(sector uint32, data *[]byte, antall int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MSkrivut(([]byte)("ata read error "))
		return
	}
	if antall > Bytepersector {
		console_2.MSkrivut(([]byte)("ata read error "))
		return
	}

	if selv.hovedinnstilling {
		selv.enhetport.Skriv(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		selv.enhetport.Skriv(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	selv.feilport.Skriv(0)
	selv.sectorAntallport.Skriv(1)

	selv.lbaLavport.Skriv(uint8(sector & 0x000000FF))
	selv.lbamidport.Skriv(uint8((sector & 0x0000FF00) >> 8))
	selv.lbahiport.Skriv(uint8((sector & 0x00FF0000) >> 16))
	selv.kommandoport.Skriv(0x20)

	var status uint8 = selv.kommandoport.Les()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selv.kommandoport.Les()
	}

	if (status & 0x01) != 0 {
		console_2.MSkrivut(([]byte)("ata read error "))
		return
	}

	console_2.MSkrivutxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < antall; i += 2 {
		var wdata uint16 = selv.dataport.Les()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < antall {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (antall + (antall % 2)); i < Bytepersector; i += 2 {
		selv.dataport.Les()
	}
}
func (selv *TAvansertTeknologiattachment) Skriv28(sectorTall uint32, data []byte, antall uint32) {

	if sectorTall > 0x0FFFFFFF {
		return
	}

	if antall > 512 {
		return
	}

	if selv.hovedinnstilling {
		selv.enhetport.Skriv(uint8(0xE0 | uint8((sectorTall&0x0F000000)>>24)))
	} else {
		selv.enhetport.Skriv(uint8(0xF0 | uint8((sectorTall&0x0F000000)>>24)))
	}

	selv.feilport.Skriv(0)
	selv.sectorAntallport.Skriv(1)
	selv.lbaLavport.Skriv(uint8(sectorTall & 0x000000FF))
	selv.lbamidport.Skriv(uint8((sectorTall & 0x0000FF00) >> 8))
	selv.lbahiport.Skriv(uint8((sectorTall & 0x00FF0000) >> 16))
	selv.kommandoport.Skriv(0x30)

	var console_2 = TConsole{}
	console_2.MSkrivut(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < antall; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < antall {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		selv.dataport.Skriv(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MSkrivut(tekst)
	}

	for i := (antall + (antall % 2)); i < 512; i += 2 {
		selv.dataport.Skriv(0x0000)
	}

}

func (selv *TAvansertTeknologiattachment) Flush() {
	if selv.hovedinnstilling {
		selv.enhetport.Skriv(0xE0)
	} else {
		selv.enhetport.Skriv(0xF0)
	}
	selv.kommandoport.Skriv(0xE7)

	var console_2 = TConsole{}

	var status uint8 = selv.kommandoport.Les()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selv.kommandoport.Les()
	}
	if (status & 0x01) != 0 {
		console_2.MSkrivut(([]byte)(" ata flush error"))
		return
	}

}
