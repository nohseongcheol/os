package ata

import . "port"
import . "konsola"

const Bajtypersector int = 512

type TZaawansowaneTechnologiaattachment struct {
	główny			bool
	dataport		TPort16bit
	błądport		TPort8bit
	sectorLiczbaport	TPort8bit
	lbaNiskiport		TPort8bit
	lbamidport		TPort8bit
	lbahiport		TPort8bit
	urządzenieport		TPort8bit
	polecenieport		TPort8bit
	sterowanieport		TPort8bit
}

func (bieżący *TZaawansowaneTechnologiaattachment) Init(główny bool, portbase uint16) {
	bieżący.główny = główny
	bieżący.dataport.Init(portbase)
	bieżący.błądport.Init(portbase + 0x1)
	bieżący.sectorLiczbaport.Init(portbase + 0x2)
	bieżący.lbaNiskiport.Init(portbase + 0x3)
	bieżący.lbamidport.Init(portbase + 0x4)
	bieżący.lbahiport.Init(portbase + 0x5)
	bieżący.urządzenieport.Init(portbase + 0x6)
	bieżący.polecenieport.Init(portbase + 0x7)
	bieżący.sterowanieport.Init(portbase + 0x8)

}

func (bieżący *TZaawansowaneTechnologiaattachment) Identify() {

	var konsola_2 = TKonsola{}

	if bieżący.główny {
		bieżący.urządzenieport.Zapis(0xA0)
	} else {
		bieżący.urządzenieport.Zapis(0xB0)
	}
	bieżący.sterowanieport.Zapis(0)
	bieżący.urządzenieport.Zapis(0xA0)

	var stan uint8 = bieżący.polecenieport.Odczyt()
	if stan == 0xFF {
		konsola_2.MWydrukuj(([]byte)("Invalid Status"))
		return
	}

	if bieżący.główny {
		bieżący.urządzenieport.Zapis(0xA0)
	} else {
		bieżący.urządzenieport.Zapis(0xB0)
	}
	bieżący.sectorLiczbaport.Zapis(0)
	bieżący.lbaNiskiport.Zapis(0)
	bieżący.lbamidport.Zapis(0)
	bieżący.lbahiport.Zapis(0)
	bieżący.polecenieport.Zapis(0xEC)

	stan = bieżący.polecenieport.Odczyt()
	if stan == 0x00 {
		konsola_2.MWydrukuj(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stan&0x80) == 0x80 && (stan&0x01) != 0x01 {
		stan = bieżący.polecenieport.Odczyt()
	}

	if (stan & 0x01) != 0 {
		konsola_2.MWydrukuj(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = bieżący.dataport.Odczyt()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	konsola_2.MWydrukujxy(([]byte)("ata ok"), 10, 22)

}
func (bieżący *TZaawansowaneTechnologiaattachment) Odczyt28(sector uint32, data *[]byte, liczba int) {
	var konsola_2 = TKonsola{}
	if (sector & 0xF0000000) != 0 {
		konsola_2.MWydrukuj(([]byte)("ata read error "))
		return
	}
	if liczba > Bajtypersector {
		konsola_2.MWydrukuj(([]byte)("ata read error "))
		return
	}

	if bieżący.główny {
		bieżący.urządzenieport.Zapis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		bieżący.urządzenieport.Zapis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	bieżący.błądport.Zapis(0)
	bieżący.sectorLiczbaport.Zapis(1)

	bieżący.lbaNiskiport.Zapis(uint8(sector & 0x000000FF))
	bieżący.lbamidport.Zapis(uint8((sector & 0x0000FF00) >> 8))
	bieżący.lbahiport.Zapis(uint8((sector & 0x00FF0000) >> 16))
	bieżący.polecenieport.Zapis(0x20)

	var stan uint8 = bieżący.polecenieport.Odczyt()
	for ((stan & 0x80) == 0x80) && ((stan & 0x01) != 0x01) {
		stan = bieżący.polecenieport.Odczyt()
	}

	if (stan & 0x01) != 0 {
		konsola_2.MWydrukuj(([]byte)("ata read error "))
		return
	}

	konsola_2.MWydrukujxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < liczba; i += 2 {
		var wdata uint16 = bieżący.dataport.Odczyt()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < liczba {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (liczba + (liczba % 2)); i < Bajtypersector; i += 2 {
		bieżący.dataport.Odczyt()
	}
}
func (bieżący *TZaawansowaneTechnologiaattachment) Zapis28(sectorLiczba uint32, data []byte, liczba uint32) {

	if sectorLiczba > 0x0FFFFFFF {
		return
	}

	if liczba > 512 {
		return
	}

	if bieżący.główny {
		bieżący.urządzenieport.Zapis(uint8(0xE0 | uint8((sectorLiczba&0x0F000000)>>24)))
	} else {
		bieżący.urządzenieport.Zapis(uint8(0xF0 | uint8((sectorLiczba&0x0F000000)>>24)))
	}

	bieżący.błądport.Zapis(0)
	bieżący.sectorLiczbaport.Zapis(1)
	bieżący.lbaNiskiport.Zapis(uint8(sectorLiczba & 0x000000FF))
	bieżący.lbamidport.Zapis(uint8((sectorLiczba & 0x0000FF00) >> 8))
	bieżący.lbahiport.Zapis(uint8((sectorLiczba & 0x00FF0000) >> 16))
	bieżący.polecenieport.Zapis(0x30)

	var konsola_2 = TKonsola{}
	konsola_2.MWydrukuj(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < liczba; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < liczba {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		bieżący.dataport.Zapis(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		konsola_2.MWydrukuj(tekst)
	}

	for i := (liczba + (liczba % 2)); i < 512; i += 2 {
		bieżący.dataport.Zapis(0x0000)
	}

}

func (bieżący *TZaawansowaneTechnologiaattachment) Flush() {
	if bieżący.główny {
		bieżący.urządzenieport.Zapis(0xE0)
	} else {
		bieżący.urządzenieport.Zapis(0xF0)
	}
	bieżący.polecenieport.Zapis(0xE7)

	var konsola_2 = TKonsola{}

	var stan uint8 = bieżący.polecenieport.Odczyt()
	if stan == 0x00 {
		return
	}

	for ((stan & 0x80) == 0x80) && ((stan & 0x01) != 0x01) {
		stan = bieżący.polecenieport.Odczyt()
	}
	if (stan & 0x01) != 0 {
		konsola_2.MWydrukuj(([]byte)(" ata flush error"))
		return
	}

}
