/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "porta"
import . "console"

const Bytepersector int = 512

type TAvanzateTecnologiaattachment struct {
	principale		bool
	dataPorta		TPorta16bit
	errorePorta		TPorta8bit
	sectorConteggioPorta	TPorta8bit
	lbaBassoPorta		TPorta8bit
	lbamidPorta		TPorta8bit
	lbahiPorta		TPorta8bit
	dispositivoPorta	TPorta8bit
	comandoPorta		TPorta8bit
	ctrlPorta		TPorta8bit
}

func (séstesso *TAvanzateTecnologiaattachment) Init(principale bool, portabase uint16) {
	séstesso.principale = principale
	séstesso.dataPorta.Init(portabase)
	séstesso.errorePorta.Init(portabase + 0x1)
	séstesso.sectorConteggioPorta.Init(portabase + 0x2)
	séstesso.lbaBassoPorta.Init(portabase + 0x3)
	séstesso.lbamidPorta.Init(portabase + 0x4)
	séstesso.lbahiPorta.Init(portabase + 0x5)
	séstesso.dispositivoPorta.Init(portabase + 0x6)
	séstesso.comandoPorta.Init(portabase + 0x7)
	séstesso.ctrlPorta.Init(portabase + 0x8)

}

func (séstesso *TAvanzateTecnologiaattachment) Identify() {

	var console_2 = TConsole{}

	if séstesso.principale {
		séstesso.dispositivoPorta.Scrittura(0xA0)
	} else {
		séstesso.dispositivoPorta.Scrittura(0xB0)
	}
	séstesso.ctrlPorta.Scrittura(0)
	séstesso.dispositivoPorta.Scrittura(0xA0)

	var stato uint8 = séstesso.comandoPorta.Lettura()
	if stato == 0xFF {
		console_2.MStampa(([]byte)("Invalid Status"))
		return
	}

	if séstesso.principale {
		séstesso.dispositivoPorta.Scrittura(0xA0)
	} else {
		séstesso.dispositivoPorta.Scrittura(0xB0)
	}
	séstesso.sectorConteggioPorta.Scrittura(0)
	séstesso.lbaBassoPorta.Scrittura(0)
	séstesso.lbamidPorta.Scrittura(0)
	séstesso.lbahiPorta.Scrittura(0)
	séstesso.comandoPorta.Scrittura(0xEC)

	stato = séstesso.comandoPorta.Lettura()
	if stato == 0x00 {
		console_2.MStampa(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stato&0x80) == 0x80 && (stato&0x01) != 0x01 {
		stato = séstesso.comandoPorta.Lettura()
	}

	if (stato & 0x01) != 0 {
		console_2.MStampa(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = séstesso.dataPorta.Lettura()
		testo := []byte("  ")
		testo[0] = uint8((data >> 8) & 0xFF)
		testo[1] = uint8(data & 0xFF)

	}
	console_2.MStampaxy(([]byte)("ata ok"), 10, 22)

}
func (séstesso *TAvanzateTecnologiaattachment) Lettura28(sector uint32, data *[]byte, conteggio int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MStampa(([]byte)("ata read error "))
		return
	}
	if conteggio > Bytepersector {
		console_2.MStampa(([]byte)("ata read error "))
		return
	}

	if séstesso.principale {
		séstesso.dispositivoPorta.Scrittura(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		séstesso.dispositivoPorta.Scrittura(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	séstesso.errorePorta.Scrittura(0)
	séstesso.sectorConteggioPorta.Scrittura(1)

	séstesso.lbaBassoPorta.Scrittura(uint8(sector & 0x000000FF))
	séstesso.lbamidPorta.Scrittura(uint8((sector & 0x0000FF00) >> 8))
	séstesso.lbahiPorta.Scrittura(uint8((sector & 0x00FF0000) >> 16))
	séstesso.comandoPorta.Scrittura(0x20)

	var stato uint8 = séstesso.comandoPorta.Lettura()
	for ((stato & 0x80) == 0x80) && ((stato & 0x01) != 0x01) {
		stato = séstesso.comandoPorta.Lettura()
	}

	if (stato & 0x01) != 0 {
		console_2.MStampa(([]byte)("ata read error "))
		return
	}

	console_2.MStampaxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < conteggio; i += 2 {
		var wdata uint16 = séstesso.dataPorta.Lettura()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < conteggio {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (conteggio + (conteggio % 2)); i < Bytepersector; i += 2 {
		séstesso.dataPorta.Lettura()
	}
}
func (séstesso *TAvanzateTecnologiaattachment) Scrittura28(sectorNumero uint32, data []byte, conteggio uint32) {

	if sectorNumero > 0x0FFFFFFF {
		return
	}

	if conteggio > 512 {
		return
	}

	if séstesso.principale {
		séstesso.dispositivoPorta.Scrittura(uint8(0xE0 | uint8((sectorNumero&0x0F000000)>>24)))
	} else {
		séstesso.dispositivoPorta.Scrittura(uint8(0xF0 | uint8((sectorNumero&0x0F000000)>>24)))
	}

	séstesso.errorePorta.Scrittura(0)
	séstesso.sectorConteggioPorta.Scrittura(1)
	séstesso.lbaBassoPorta.Scrittura(uint8(sectorNumero & 0x000000FF))
	séstesso.lbamidPorta.Scrittura(uint8((sectorNumero & 0x0000FF00) >> 8))
	séstesso.lbahiPorta.Scrittura(uint8((sectorNumero & 0x00FF0000) >> 16))
	séstesso.comandoPorta.Scrittura(0x30)

	var console_2 = TConsole{}
	console_2.MStampa(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < conteggio; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < conteggio {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		séstesso.dataPorta.Scrittura(wdata)

		testo := []byte("  ")
		testo[0] = uint8((wdata >> 8) & 0xFF)
		testo[1] = uint8(wdata & 0xFF)

		console_2.MStampa(testo)
	}

	for i := (conteggio + (conteggio % 2)); i < 512; i += 2 {
		séstesso.dataPorta.Scrittura(0x0000)
	}

}

func (séstesso *TAvanzateTecnologiaattachment) Flush() {
	if séstesso.principale {
		séstesso.dispositivoPorta.Scrittura(0xE0)
	} else {
		séstesso.dispositivoPorta.Scrittura(0xF0)
	}
	séstesso.comandoPorta.Scrittura(0xE7)

	var console_2 = TConsole{}

	var stato uint8 = séstesso.comandoPorta.Lettura()
	if stato == 0x00 {
		return
	}

	for ((stato & 0x80) == 0x80) && ((stato & 0x01) != 0x01) {
		stato = séstesso.comandoPorta.Lettura()
	}
	if (stato & 0x01) != 0 {
		console_2.MStampa(([]byte)(" ata flush error"))
		return
	}

}
