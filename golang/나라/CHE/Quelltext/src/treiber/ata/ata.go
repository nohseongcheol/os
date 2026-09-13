package ata

import . "anschluss"
import . "konsole"

const Bytepersector int = 512

type TErweitertTechnikattachment struct {
	haupt			bool
	datenAnschluss		TAnschluss16bit
	fehlerAnschluss		TAnschluss8bit
	sectorAnzahlAnschluss	TAnschluss8bit
	lbaNiedrigAnschluss	TAnschluss8bit
	lbamidAnschluss		TAnschluss8bit
	lbahiAnschluss		TAnschluss8bit
	gerätAnschluss		TAnschluss8bit
	befehlAnschluss		TAnschluss8bit
	strgAnschluss		TAnschluss8bit
}

func (selbst *TErweitertTechnikattachment) Init(haupt bool, anschlussbase uint16) {
	selbst.haupt = haupt
	selbst.datenAnschluss.Init(anschlussbase)
	selbst.fehlerAnschluss.Init(anschlussbase + 0x1)
	selbst.sectorAnzahlAnschluss.Init(anschlussbase + 0x2)
	selbst.lbaNiedrigAnschluss.Init(anschlussbase + 0x3)
	selbst.lbamidAnschluss.Init(anschlussbase + 0x4)
	selbst.lbahiAnschluss.Init(anschlussbase + 0x5)
	selbst.gerätAnschluss.Init(anschlussbase + 0x6)
	selbst.befehlAnschluss.Init(anschlussbase + 0x7)
	selbst.strgAnschluss.Init(anschlussbase + 0x8)

}

func (selbst *TErweitertTechnikattachment) Identify() {

	var konsole_2 = TKonsole{}

	if selbst.haupt {
		selbst.gerätAnschluss.Schreiben(0xA0)
	} else {
		selbst.gerätAnschluss.Schreiben(0xB0)
	}
	selbst.strgAnschluss.Schreiben(0)
	selbst.gerätAnschluss.Schreiben(0xA0)

	var status uint8 = selbst.befehlAnschluss.Lesen()
	if status == 0xFF {
		konsole_2.MDrucken(([]byte)("Invalid Status"))
		return
	}

	if selbst.haupt {
		selbst.gerätAnschluss.Schreiben(0xA0)
	} else {
		selbst.gerätAnschluss.Schreiben(0xB0)
	}
	selbst.sectorAnzahlAnschluss.Schreiben(0)
	selbst.lbaNiedrigAnschluss.Schreiben(0)
	selbst.lbamidAnschluss.Schreiben(0)
	selbst.lbahiAnschluss.Schreiben(0)
	selbst.befehlAnschluss.Schreiben(0xEC)

	status = selbst.befehlAnschluss.Lesen()
	if status == 0x00 {
		konsole_2.MDrucken(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = selbst.befehlAnschluss.Lesen()
	}

	if (status & 0x01) != 0 {
		konsole_2.MDrucken(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var daten = selbst.datenAnschluss.Lesen()
		text := []byte("  ")
		text[0] = uint8((daten >> 8) & 0xFF)
		text[1] = uint8(daten & 0xFF)

	}
	konsole_2.MDruckenxy(([]byte)("ata ok"), 10, 22)

}
func (selbst *TErweitertTechnikattachment) Lesen28(sector uint32, daten *[]byte, anzahl int) {
	var konsole_2 = TKonsole{}
	if (sector & 0xF0000000) != 0 {
		konsole_2.MDrucken(([]byte)("ata read error "))
		return
	}
	if anzahl > Bytepersector {
		konsole_2.MDrucken(([]byte)("ata read error "))
		return
	}

	if selbst.haupt {
		selbst.gerätAnschluss.Schreiben(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		selbst.gerätAnschluss.Schreiben(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	selbst.fehlerAnschluss.Schreiben(0)
	selbst.sectorAnzahlAnschluss.Schreiben(1)

	selbst.lbaNiedrigAnschluss.Schreiben(uint8(sector & 0x000000FF))
	selbst.lbamidAnschluss.Schreiben(uint8((sector & 0x0000FF00) >> 8))
	selbst.lbahiAnschluss.Schreiben(uint8((sector & 0x00FF0000) >> 16))
	selbst.befehlAnschluss.Schreiben(0x20)

	var status uint8 = selbst.befehlAnschluss.Lesen()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selbst.befehlAnschluss.Lesen()
	}

	if (status & 0x01) != 0 {
		konsole_2.MDrucken(([]byte)("ata read error "))
		return
	}

	konsole_2.MDruckenxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < anzahl; i += 2 {
		var wdata uint16 = selbst.datenAnschluss.Lesen()

		(*daten)[i] = uint8(wdata & 0x00FF)
		if i+1 < anzahl {

			(*daten)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (anzahl + (anzahl % 2)); i < Bytepersector; i += 2 {
		selbst.datenAnschluss.Lesen()
	}
}
func (selbst *TErweitertTechnikattachment) Schreiben28(sectorNummer uint32, daten []byte, anzahl uint32) {

	if sectorNummer > 0x0FFFFFFF {
		return
	}

	if anzahl > 512 {
		return
	}

	if selbst.haupt {
		selbst.gerätAnschluss.Schreiben(uint8(0xE0 | uint8((sectorNummer&0x0F000000)>>24)))
	} else {
		selbst.gerätAnschluss.Schreiben(uint8(0xF0 | uint8((sectorNummer&0x0F000000)>>24)))
	}

	selbst.fehlerAnschluss.Schreiben(0)
	selbst.sectorAnzahlAnschluss.Schreiben(1)
	selbst.lbaNiedrigAnschluss.Schreiben(uint8(sectorNummer & 0x000000FF))
	selbst.lbamidAnschluss.Schreiben(uint8((sectorNummer & 0x0000FF00) >> 8))
	selbst.lbahiAnschluss.Schreiben(uint8((sectorNummer & 0x00FF0000) >> 16))
	selbst.befehlAnschluss.Schreiben(0x30)

	var konsole_2 = TKonsole{}
	konsole_2.MDrucken(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < anzahl; i += 2 {

		var wdata uint16 = uint16(daten[i])

		if i+1 < anzahl {
			wdata = wdata | (uint16(daten[i+1]) << 8)
		}

		selbst.datenAnschluss.Schreiben(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		konsole_2.MDrucken(text)
	}

	for i := (anzahl + (anzahl % 2)); i < 512; i += 2 {
		selbst.datenAnschluss.Schreiben(0x0000)
	}

}

func (selbst *TErweitertTechnikattachment) Flush() {
	if selbst.haupt {
		selbst.gerätAnschluss.Schreiben(0xE0)
	} else {
		selbst.gerätAnschluss.Schreiben(0xF0)
	}
	selbst.befehlAnschluss.Schreiben(0xE7)

	var konsole_2 = TKonsole{}

	var status uint8 = selbst.befehlAnschluss.Lesen()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selbst.befehlAnschluss.Lesen()
	}
	if (status & 0x01) != 0 {
		konsole_2.MDrucken(([]byte)(" ata flush error"))
		return
	}

}
