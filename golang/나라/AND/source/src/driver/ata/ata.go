package ata

import . "port"
import . "consola"

const Bytespersector int = 512

type TAvançatTecnologiaattachment struct {
	mestre			bool
	dataport		TPort16bit
	shaproduïtunerrorport	TPort8bit
	sectorRecompteport	TPort8bit
	lbaBaixaport		TPort8bit
	lbamidport		TPort8bit
	lbahiport		TPort8bit
	dispositiuport		TPort8bit
	ordreport		TPort8bit
	controlport		TPort8bit
}

func (unmateix *TAvançatTecnologiaattachment) Init(mestre bool, portbase uint16) {
	unmateix.mestre = mestre
	unmateix.dataport.Init(portbase)
	unmateix.shaproduïtunerrorport.Init(portbase + 0x1)
	unmateix.sectorRecompteport.Init(portbase + 0x2)
	unmateix.lbaBaixaport.Init(portbase + 0x3)
	unmateix.lbamidport.Init(portbase + 0x4)
	unmateix.lbahiport.Init(portbase + 0x5)
	unmateix.dispositiuport.Init(portbase + 0x6)
	unmateix.ordreport.Init(portbase + 0x7)
	unmateix.controlport.Init(portbase + 0x8)

}

func (unmateix *TAvançatTecnologiaattachment) Identify() {

	var consola_2 = TConsola{}

	if unmateix.mestre {
		unmateix.dispositiuport.Escriptura(0xA0)
	} else {
		unmateix.dispositiuport.Escriptura(0xB0)
	}
	unmateix.controlport.Escriptura(0)
	unmateix.dispositiuport.Escriptura(0xA0)

	var estat uint8 = unmateix.ordreport.Lectura()
	if estat == 0xFF {
		consola_2.MImprimeix(([]byte)("Invalid Status"))
		return
	}

	if unmateix.mestre {
		unmateix.dispositiuport.Escriptura(0xA0)
	} else {
		unmateix.dispositiuport.Escriptura(0xB0)
	}
	unmateix.sectorRecompteport.Escriptura(0)
	unmateix.lbaBaixaport.Escriptura(0)
	unmateix.lbamidport.Escriptura(0)
	unmateix.lbahiport.Escriptura(0)
	unmateix.ordreport.Escriptura(0xEC)

	estat = unmateix.ordreport.Lectura()
	if estat == 0x00 {
		consola_2.MImprimeix(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (estat&0x80) == 0x80 && (estat&0x01) != 0x01 {
		estat = unmateix.ordreport.Lectura()
	}

	if (estat & 0x01) != 0 {
		consola_2.MImprimeix(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = unmateix.dataport.Lectura()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	consola_2.MImprimeixxy(([]byte)("ata ok"), 10, 22)

}
func (unmateix *TAvançatTecnologiaattachment) Lectura28(sector uint32, data *[]byte, recompte int) {
	var consola_2 = TConsola{}
	if (sector & 0xF0000000) != 0 {
		consola_2.MImprimeix(([]byte)("ata read error "))
		return
	}
	if recompte > Bytespersector {
		consola_2.MImprimeix(([]byte)("ata read error "))
		return
	}

	if unmateix.mestre {
		unmateix.dispositiuport.Escriptura(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		unmateix.dispositiuport.Escriptura(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	unmateix.shaproduïtunerrorport.Escriptura(0)
	unmateix.sectorRecompteport.Escriptura(1)

	unmateix.lbaBaixaport.Escriptura(uint8(sector & 0x000000FF))
	unmateix.lbamidport.Escriptura(uint8((sector & 0x0000FF00) >> 8))
	unmateix.lbahiport.Escriptura(uint8((sector & 0x00FF0000) >> 16))
	unmateix.ordreport.Escriptura(0x20)

	var estat uint8 = unmateix.ordreport.Lectura()
	for ((estat & 0x80) == 0x80) && ((estat & 0x01) != 0x01) {
		estat = unmateix.ordreport.Lectura()
	}

	if (estat & 0x01) != 0 {
		consola_2.MImprimeix(([]byte)("ata read error "))
		return
	}

	consola_2.MImprimeixxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < recompte; i += 2 {
		var wdata uint16 = unmateix.dataport.Lectura()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < recompte {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (recompte + (recompte % 2)); i < Bytespersector; i += 2 {
		unmateix.dataport.Lectura()
	}
}
func (unmateix *TAvançatTecnologiaattachment) Escriptura28(sectorNombre uint32, data []byte, recompte uint32) {

	if sectorNombre > 0x0FFFFFFF {
		return
	}

	if recompte > 512 {
		return
	}

	if unmateix.mestre {
		unmateix.dispositiuport.Escriptura(uint8(0xE0 | uint8((sectorNombre&0x0F000000)>>24)))
	} else {
		unmateix.dispositiuport.Escriptura(uint8(0xF0 | uint8((sectorNombre&0x0F000000)>>24)))
	}

	unmateix.shaproduïtunerrorport.Escriptura(0)
	unmateix.sectorRecompteport.Escriptura(1)
	unmateix.lbaBaixaport.Escriptura(uint8(sectorNombre & 0x000000FF))
	unmateix.lbamidport.Escriptura(uint8((sectorNombre & 0x0000FF00) >> 8))
	unmateix.lbahiport.Escriptura(uint8((sectorNombre & 0x00FF0000) >> 16))
	unmateix.ordreport.Escriptura(0x30)

	var consola_2 = TConsola{}
	consola_2.MImprimeix(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < recompte; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < recompte {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		unmateix.dataport.Escriptura(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		consola_2.MImprimeix(text)
	}

	for i := (recompte + (recompte % 2)); i < 512; i += 2 {
		unmateix.dataport.Escriptura(0x0000)
	}

}

func (unmateix *TAvançatTecnologiaattachment) Flush() {
	if unmateix.mestre {
		unmateix.dispositiuport.Escriptura(0xE0)
	} else {
		unmateix.dispositiuport.Escriptura(0xF0)
	}
	unmateix.ordreport.Escriptura(0xE7)

	var consola_2 = TConsola{}

	var estat uint8 = unmateix.ordreport.Lectura()
	if estat == 0x00 {
		return
	}

	for ((estat & 0x80) == 0x80) && ((estat & 0x01) != 0x01) {
		estat = unmateix.ordreport.Lectura()
	}
	if (estat & 0x01) != 0 {
		consola_2.MImprimeix(([]byte)(" ata flush error"))
		return
	}

}
