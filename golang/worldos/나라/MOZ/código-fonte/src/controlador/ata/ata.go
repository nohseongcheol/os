/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "porto"
import . "console"

const Bytespersector int = 512

type TAvançadoTecnologiaattachment struct {
	principal		bool
	dadosporto		TPorto16bit
	erroporto		TPorto8bit
	sectorContarporto	TPorto8bit
	lbaBaixoporto		TPorto8bit
	lbamidporto		TPorto8bit
	lbahiporto		TPorto8bit
	dispositivoporto	TPorto8bit
	comandoporto		TPorto8bit
	controloporto		TPorto8bit
}

func (próprio *TAvançadoTecnologiaattachment) Init(principal bool, portobase uint16) {
	próprio.principal = principal
	próprio.dadosporto.Init(portobase)
	próprio.erroporto.Init(portobase + 0x1)
	próprio.sectorContarporto.Init(portobase + 0x2)
	próprio.lbaBaixoporto.Init(portobase + 0x3)
	próprio.lbamidporto.Init(portobase + 0x4)
	próprio.lbahiporto.Init(portobase + 0x5)
	próprio.dispositivoporto.Init(portobase + 0x6)
	próprio.comandoporto.Init(portobase + 0x7)
	próprio.controloporto.Init(portobase + 0x8)

}

func (próprio *TAvançadoTecnologiaattachment) Identify() {

	var console_2 = TConsole{}

	if próprio.principal {
		próprio.dispositivoporto.Escrever(0xA0)
	} else {
		próprio.dispositivoporto.Escrever(0xB0)
	}
	próprio.controloporto.Escrever(0)
	próprio.dispositivoporto.Escrever(0xA0)

	var estado uint8 = próprio.comandoporto.Ler()
	if estado == 0xFF {
		console_2.MImprimir(([]byte)("Invalid Status"))
		return
	}

	if próprio.principal {
		próprio.dispositivoporto.Escrever(0xA0)
	} else {
		próprio.dispositivoporto.Escrever(0xB0)
	}
	próprio.sectorContarporto.Escrever(0)
	próprio.lbaBaixoporto.Escrever(0)
	próprio.lbamidporto.Escrever(0)
	próprio.lbahiporto.Escrever(0)
	próprio.comandoporto.Escrever(0xEC)

	estado = próprio.comandoporto.Ler()
	if estado == 0x00 {
		console_2.MImprimir(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (estado&0x80) == 0x80 && (estado&0x01) != 0x01 {
		estado = próprio.comandoporto.Ler()
	}

	if (estado & 0x01) != 0 {
		console_2.MImprimir(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var dados = próprio.dadosporto.Ler()
		texto := []byte("  ")
		texto[0] = uint8((dados >> 8) & 0xFF)
		texto[1] = uint8(dados & 0xFF)

	}
	console_2.MImprimirxy(([]byte)("ata ok"), 10, 22)

}
func (próprio *TAvançadoTecnologiaattachment) Ler28(sector uint32, dados *[]byte, contar int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MImprimir(([]byte)("ata read error "))
		return
	}
	if contar > Bytespersector {
		console_2.MImprimir(([]byte)("ata read error "))
		return
	}

	if próprio.principal {
		próprio.dispositivoporto.Escrever(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		próprio.dispositivoporto.Escrever(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	próprio.erroporto.Escrever(0)
	próprio.sectorContarporto.Escrever(1)

	próprio.lbaBaixoporto.Escrever(uint8(sector & 0x000000FF))
	próprio.lbamidporto.Escrever(uint8((sector & 0x0000FF00) >> 8))
	próprio.lbahiporto.Escrever(uint8((sector & 0x00FF0000) >> 16))
	próprio.comandoporto.Escrever(0x20)

	var estado uint8 = próprio.comandoporto.Ler()
	for ((estado & 0x80) == 0x80) && ((estado & 0x01) != 0x01) {
		estado = próprio.comandoporto.Ler()
	}

	if (estado & 0x01) != 0 {
		console_2.MImprimir(([]byte)("ata read error "))
		return
	}

	console_2.MImprimirxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < contar; i += 2 {
		var wdata uint16 = próprio.dadosporto.Ler()

		(*dados)[i] = uint8(wdata & 0x00FF)
		if i+1 < contar {

			(*dados)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (contar + (contar % 2)); i < Bytespersector; i += 2 {
		próprio.dadosporto.Ler()
	}
}
func (próprio *TAvançadoTecnologiaattachment) Escrever28(sectorNúmero uint32, dados []byte, contar uint32) {

	if sectorNúmero > 0x0FFFFFFF {
		return
	}

	if contar > 512 {
		return
	}

	if próprio.principal {
		próprio.dispositivoporto.Escrever(uint8(0xE0 | uint8((sectorNúmero&0x0F000000)>>24)))
	} else {
		próprio.dispositivoporto.Escrever(uint8(0xF0 | uint8((sectorNúmero&0x0F000000)>>24)))
	}

	próprio.erroporto.Escrever(0)
	próprio.sectorContarporto.Escrever(1)
	próprio.lbaBaixoporto.Escrever(uint8(sectorNúmero & 0x000000FF))
	próprio.lbamidporto.Escrever(uint8((sectorNúmero & 0x0000FF00) >> 8))
	próprio.lbahiporto.Escrever(uint8((sectorNúmero & 0x00FF0000) >> 16))
	próprio.comandoporto.Escrever(0x30)

	var console_2 = TConsole{}
	console_2.MImprimir(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < contar; i += 2 {

		var wdata uint16 = uint16(dados[i])

		if i+1 < contar {
			wdata = wdata | (uint16(dados[i+1]) << 8)
		}

		próprio.dadosporto.Escrever(wdata)

		texto := []byte("  ")
		texto[0] = uint8((wdata >> 8) & 0xFF)
		texto[1] = uint8(wdata & 0xFF)

		console_2.MImprimir(texto)
	}

	for i := (contar + (contar % 2)); i < 512; i += 2 {
		próprio.dadosporto.Escrever(0x0000)
	}

}

func (próprio *TAvançadoTecnologiaattachment) Flush() {
	if próprio.principal {
		próprio.dispositivoporto.Escrever(0xE0)
	} else {
		próprio.dispositivoporto.Escrever(0xF0)
	}
	próprio.comandoporto.Escrever(0xE7)

	var console_2 = TConsole{}

	var estado uint8 = próprio.comandoporto.Ler()
	if estado == 0x00 {
		return
	}

	for ((estado & 0x80) == 0x80) && ((estado & 0x01) != 0x01) {
		estado = próprio.comandoporto.Ler()
	}
	if (estado & 0x01) != 0 {
		console_2.MImprimir(([]byte)(" ata flush error"))
		return
	}

}
