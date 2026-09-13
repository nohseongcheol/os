package ata

import . "port"
import . "konsol"

const Bytepersector int = 512

type TAvanceratTeknikattachment struct {
	master		bool
	dataport	TPort16bit
	felport		TPort8bit
	sectorAntalport	TPort8bit
	lbaLågport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	enhetport	TPort8bit
	kommandoport	TPort8bit
	ctrlport	TPort8bit
}

func (själv *TAvanceratTeknikattachment) Init(master bool, portbase uint16) {
	själv.master = master
	själv.dataport.Init(portbase)
	själv.felport.Init(portbase + 0x1)
	själv.sectorAntalport.Init(portbase + 0x2)
	själv.lbaLågport.Init(portbase + 0x3)
	själv.lbamidport.Init(portbase + 0x4)
	själv.lbahiport.Init(portbase + 0x5)
	själv.enhetport.Init(portbase + 0x6)
	själv.kommandoport.Init(portbase + 0x7)
	själv.ctrlport.Init(portbase + 0x8)

}

func (själv *TAvanceratTeknikattachment) Identify() {

	var konsol_2 = TKonsol{}

	if själv.master {
		själv.enhetport.Skriv(0xA0)
	} else {
		själv.enhetport.Skriv(0xB0)
	}
	själv.ctrlport.Skriv(0)
	själv.enhetport.Skriv(0xA0)

	var status uint8 = själv.kommandoport.Läs()
	if status == 0xFF {
		konsol_2.MSkrivut(([]byte)("Invalid Status"))
		return
	}

	if själv.master {
		själv.enhetport.Skriv(0xA0)
	} else {
		själv.enhetport.Skriv(0xB0)
	}
	själv.sectorAntalport.Skriv(0)
	själv.lbaLågport.Skriv(0)
	själv.lbamidport.Skriv(0)
	själv.lbahiport.Skriv(0)
	själv.kommandoport.Skriv(0xEC)

	status = själv.kommandoport.Läs()
	if status == 0x00 {
		konsol_2.MSkrivut(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = själv.kommandoport.Läs()
	}

	if (status & 0x01) != 0 {
		konsol_2.MSkrivut(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = själv.dataport.Läs()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	konsol_2.MSkrivutxy(([]byte)("ata ok"), 10, 22)

}
func (själv *TAvanceratTeknikattachment) Läs28(sector uint32, data *[]byte, antal int) {
	var konsol_2 = TKonsol{}
	if (sector & 0xF0000000) != 0 {
		konsol_2.MSkrivut(([]byte)("ata read error "))
		return
	}
	if antal > Bytepersector {
		konsol_2.MSkrivut(([]byte)("ata read error "))
		return
	}

	if själv.master {
		själv.enhetport.Skriv(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		själv.enhetport.Skriv(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	själv.felport.Skriv(0)
	själv.sectorAntalport.Skriv(1)

	själv.lbaLågport.Skriv(uint8(sector & 0x000000FF))
	själv.lbamidport.Skriv(uint8((sector & 0x0000FF00) >> 8))
	själv.lbahiport.Skriv(uint8((sector & 0x00FF0000) >> 16))
	själv.kommandoport.Skriv(0x20)

	var status uint8 = själv.kommandoport.Läs()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = själv.kommandoport.Läs()
	}

	if (status & 0x01) != 0 {
		konsol_2.MSkrivut(([]byte)("ata read error "))
		return
	}

	konsol_2.MSkrivutxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < antal; i += 2 {
		var wdata uint16 = själv.dataport.Läs()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < antal {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (antal + (antal % 2)); i < Bytepersector; i += 2 {
		själv.dataport.Läs()
	}
}
func (själv *TAvanceratTeknikattachment) Skriv28(sectorNummer uint32, data []byte, antal uint32) {

	if sectorNummer > 0x0FFFFFFF {
		return
	}

	if antal > 512 {
		return
	}

	if själv.master {
		själv.enhetport.Skriv(uint8(0xE0 | uint8((sectorNummer&0x0F000000)>>24)))
	} else {
		själv.enhetport.Skriv(uint8(0xF0 | uint8((sectorNummer&0x0F000000)>>24)))
	}

	själv.felport.Skriv(0)
	själv.sectorAntalport.Skriv(1)
	själv.lbaLågport.Skriv(uint8(sectorNummer & 0x000000FF))
	själv.lbamidport.Skriv(uint8((sectorNummer & 0x0000FF00) >> 8))
	själv.lbahiport.Skriv(uint8((sectorNummer & 0x00FF0000) >> 16))
	själv.kommandoport.Skriv(0x30)

	var konsol_2 = TKonsol{}
	konsol_2.MSkrivut(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < antal; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < antal {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		själv.dataport.Skriv(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		konsol_2.MSkrivut(text)
	}

	for i := (antal + (antal % 2)); i < 512; i += 2 {
		själv.dataport.Skriv(0x0000)
	}

}

func (själv *TAvanceratTeknikattachment) Flush() {
	if själv.master {
		själv.enhetport.Skriv(0xE0)
	} else {
		själv.enhetport.Skriv(0xF0)
	}
	själv.kommandoport.Skriv(0xE7)

	var konsol_2 = TKonsol{}

	var status uint8 = själv.kommandoport.Läs()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = själv.kommandoport.Läs()
	}
	if (status & 0x01) != 0 {
		konsol_2.MSkrivut(([]byte)(" ata flush error"))
		return
	}

}
