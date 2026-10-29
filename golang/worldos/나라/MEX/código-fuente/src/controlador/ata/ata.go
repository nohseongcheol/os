/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "puerto"
import . "consola"

const Bytespersector int = 512

type TAvanzadoTecnologíaattachment struct {
	maestro			bool
	datospuerto		TPuerto16bit
	errorpuerto		TPuerto8bit
	sectorRecuentopuerto	TPuerto8bit
	lbaBajapuerto		TPuerto8bit
	lbamidpuerto		TPuerto8bit
	lbahipuerto		TPuerto8bit
	dispositivopuerto	TPuerto8bit
	ordenpuerto		TPuerto8bit
	controlpuerto		TPuerto8bit
}

func (propio *TAvanzadoTecnologíaattachment) Init(maestro bool, puertobase uint16) {
	propio.maestro = maestro
	propio.datospuerto.Init(puertobase)
	propio.errorpuerto.Init(puertobase + 0x1)
	propio.sectorRecuentopuerto.Init(puertobase + 0x2)
	propio.lbaBajapuerto.Init(puertobase + 0x3)
	propio.lbamidpuerto.Init(puertobase + 0x4)
	propio.lbahipuerto.Init(puertobase + 0x5)
	propio.dispositivopuerto.Init(puertobase + 0x6)
	propio.ordenpuerto.Init(puertobase + 0x7)
	propio.controlpuerto.Init(puertobase + 0x8)

}

func (propio *TAvanzadoTecnologíaattachment) Identify() {

	var consola_2 = TConsola{}

	if propio.maestro {
		propio.dispositivopuerto.Escribir(0xA0)
	} else {
		propio.dispositivopuerto.Escribir(0xB0)
	}
	propio.controlpuerto.Escribir(0)
	propio.dispositivopuerto.Escribir(0xA0)

	var estado uint8 = propio.ordenpuerto.Leer()
	if estado == 0xFF {
		consola_2.MImprimir(([]byte)("Invalid Status"))
		return
	}

	if propio.maestro {
		propio.dispositivopuerto.Escribir(0xA0)
	} else {
		propio.dispositivopuerto.Escribir(0xB0)
	}
	propio.sectorRecuentopuerto.Escribir(0)
	propio.lbaBajapuerto.Escribir(0)
	propio.lbamidpuerto.Escribir(0)
	propio.lbahipuerto.Escribir(0)
	propio.ordenpuerto.Escribir(0xEC)

	estado = propio.ordenpuerto.Leer()
	if estado == 0x00 {
		consola_2.MImprimir(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (estado&0x80) == 0x80 && (estado&0x01) != 0x01 {
		estado = propio.ordenpuerto.Leer()
	}

	if (estado & 0x01) != 0 {
		consola_2.MImprimir(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var datos = propio.datospuerto.Leer()
		texto := []byte("  ")
		texto[0] = uint8((datos >> 8) & 0xFF)
		texto[1] = uint8(datos & 0xFF)

	}
	consola_2.MImprimirxy(([]byte)("ata ok"), 10, 22)

}
func (propio *TAvanzadoTecnologíaattachment) Leer28(sector uint32, datos *[]byte, recuento int) {
	var consola_2 = TConsola{}
	if (sector & 0xF0000000) != 0 {
		consola_2.MImprimir(([]byte)("ata read error "))
		return
	}
	if recuento > Bytespersector {
		consola_2.MImprimir(([]byte)("ata read error "))
		return
	}

	if propio.maestro {
		propio.dispositivopuerto.Escribir(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		propio.dispositivopuerto.Escribir(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	propio.errorpuerto.Escribir(0)
	propio.sectorRecuentopuerto.Escribir(1)

	propio.lbaBajapuerto.Escribir(uint8(sector & 0x000000FF))
	propio.lbamidpuerto.Escribir(uint8((sector & 0x0000FF00) >> 8))
	propio.lbahipuerto.Escribir(uint8((sector & 0x00FF0000) >> 16))
	propio.ordenpuerto.Escribir(0x20)

	var estado uint8 = propio.ordenpuerto.Leer()
	for ((estado & 0x80) == 0x80) && ((estado & 0x01) != 0x01) {
		estado = propio.ordenpuerto.Leer()
	}

	if (estado & 0x01) != 0 {
		consola_2.MImprimir(([]byte)("ata read error "))
		return
	}

	consola_2.MImprimirxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < recuento; i += 2 {
		var wdata uint16 = propio.datospuerto.Leer()

		(*datos)[i] = uint8(wdata & 0x00FF)
		if i+1 < recuento {

			(*datos)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (recuento + (recuento % 2)); i < Bytespersector; i += 2 {
		propio.datospuerto.Leer()
	}
}
func (propio *TAvanzadoTecnologíaattachment) Escribir28(sectorNúmero uint32, datos []byte, recuento uint32) {

	if sectorNúmero > 0x0FFFFFFF {
		return
	}

	if recuento > 512 {
		return
	}

	if propio.maestro {
		propio.dispositivopuerto.Escribir(uint8(0xE0 | uint8((sectorNúmero&0x0F000000)>>24)))
	} else {
		propio.dispositivopuerto.Escribir(uint8(0xF0 | uint8((sectorNúmero&0x0F000000)>>24)))
	}

	propio.errorpuerto.Escribir(0)
	propio.sectorRecuentopuerto.Escribir(1)
	propio.lbaBajapuerto.Escribir(uint8(sectorNúmero & 0x000000FF))
	propio.lbamidpuerto.Escribir(uint8((sectorNúmero & 0x0000FF00) >> 8))
	propio.lbahipuerto.Escribir(uint8((sectorNúmero & 0x00FF0000) >> 16))
	propio.ordenpuerto.Escribir(0x30)

	var consola_2 = TConsola{}
	consola_2.MImprimir(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < recuento; i += 2 {

		var wdata uint16 = uint16(datos[i])

		if i+1 < recuento {
			wdata = wdata | (uint16(datos[i+1]) << 8)
		}

		propio.datospuerto.Escribir(wdata)

		texto := []byte("  ")
		texto[0] = uint8((wdata >> 8) & 0xFF)
		texto[1] = uint8(wdata & 0xFF)

		consola_2.MImprimir(texto)
	}

	for i := (recuento + (recuento % 2)); i < 512; i += 2 {
		propio.datospuerto.Escribir(0x0000)
	}

}

func (propio *TAvanzadoTecnologíaattachment) Flush() {
	if propio.maestro {
		propio.dispositivopuerto.Escribir(0xE0)
	} else {
		propio.dispositivopuerto.Escribir(0xF0)
	}
	propio.ordenpuerto.Escribir(0xE7)

	var consola_2 = TConsola{}

	var estado uint8 = propio.ordenpuerto.Leer()
	if estado == 0x00 {
		return
	}

	for ((estado & 0x80) == 0x80) && ((estado & 0x01) != 0x01) {
		estado = propio.ordenpuerto.Leer()
	}
	if (estado & 0x01) != 0 {
		consola_2.MImprimir(([]byte)(" ata flush error"))
		return
	}

}
