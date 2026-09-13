package ata

import . "port"
import . "console"

const Bytepersector int = 512

type TAvanceretTeknologiattachment struct {
	master		bool
	dataport	TPort16bit
	fejlport	TPort8bit
	sectorAntalport	TPort8bit
	lbaLavport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	enhedport	TPort8bit
	kommandoport	TPort8bit
	kontrolport	TPort8bit
}

func (selv *TAvanceretTeknologiattachment) Init(master bool, portbase uint16) {
	selv.master = master
	selv.dataport.Init(portbase)
	selv.fejlport.Init(portbase + 0x1)
	selv.sectorAntalport.Init(portbase + 0x2)
	selv.lbaLavport.Init(portbase + 0x3)
	selv.lbamidport.Init(portbase + 0x4)
	selv.lbahiport.Init(portbase + 0x5)
	selv.enhedport.Init(portbase + 0x6)
	selv.kommandoport.Init(portbase + 0x7)
	selv.kontrolport.Init(portbase + 0x8)

}

func (selv *TAvanceretTeknologiattachment) Identify() {

	var console_2 = TConsole{}

	if selv.master {
		selv.enhedport.Skrive(0xA0)
	} else {
		selv.enhedport.Skrive(0xB0)
	}
	selv.kontrolport.Skrive(0)
	selv.enhedport.Skrive(0xA0)

	var status uint8 = selv.kommandoport.Læse()
	if status == 0xFF {
		console_2.MUdskriv(([]byte)("Invalid Status"))
		return
	}

	if selv.master {
		selv.enhedport.Skrive(0xA0)
	} else {
		selv.enhedport.Skrive(0xB0)
	}
	selv.sectorAntalport.Skrive(0)
	selv.lbaLavport.Skrive(0)
	selv.lbamidport.Skrive(0)
	selv.lbahiport.Skrive(0)
	selv.kommandoport.Skrive(0xEC)

	status = selv.kommandoport.Læse()
	if status == 0x00 {
		console_2.MUdskriv(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = selv.kommandoport.Læse()
	}

	if (status & 0x01) != 0 {
		console_2.MUdskriv(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = selv.dataport.Læse()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MUdskrivxy(([]byte)("ata ok"), 10, 22)

}
func (selv *TAvanceretTeknologiattachment) Læse28(sector uint32, data *[]byte, antal int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MUdskriv(([]byte)("ata read error "))
		return
	}
	if antal > Bytepersector {
		console_2.MUdskriv(([]byte)("ata read error "))
		return
	}

	if selv.master {
		selv.enhedport.Skrive(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		selv.enhedport.Skrive(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	selv.fejlport.Skrive(0)
	selv.sectorAntalport.Skrive(1)

	selv.lbaLavport.Skrive(uint8(sector & 0x000000FF))
	selv.lbamidport.Skrive(uint8((sector & 0x0000FF00) >> 8))
	selv.lbahiport.Skrive(uint8((sector & 0x00FF0000) >> 16))
	selv.kommandoport.Skrive(0x20)

	var status uint8 = selv.kommandoport.Læse()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selv.kommandoport.Læse()
	}

	if (status & 0x01) != 0 {
		console_2.MUdskriv(([]byte)("ata read error "))
		return
	}

	console_2.MUdskrivxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < antal; i += 2 {
		var wdata uint16 = selv.dataport.Læse()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < antal {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (antal + (antal % 2)); i < Bytepersector; i += 2 {
		selv.dataport.Læse()
	}
}
func (selv *TAvanceretTeknologiattachment) Skrive28(sectorTal uint32, data []byte, antal uint32) {

	if sectorTal > 0x0FFFFFFF {
		return
	}

	if antal > 512 {
		return
	}

	if selv.master {
		selv.enhedport.Skrive(uint8(0xE0 | uint8((sectorTal&0x0F000000)>>24)))
	} else {
		selv.enhedport.Skrive(uint8(0xF0 | uint8((sectorTal&0x0F000000)>>24)))
	}

	selv.fejlport.Skrive(0)
	selv.sectorAntalport.Skrive(1)
	selv.lbaLavport.Skrive(uint8(sectorTal & 0x000000FF))
	selv.lbamidport.Skrive(uint8((sectorTal & 0x0000FF00) >> 8))
	selv.lbahiport.Skrive(uint8((sectorTal & 0x00FF0000) >> 16))
	selv.kommandoport.Skrive(0x30)

	var console_2 = TConsole{}
	console_2.MUdskriv(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < antal; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < antal {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		selv.dataport.Skrive(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MUdskriv(tekst)
	}

	for i := (antal + (antal % 2)); i < 512; i += 2 {
		selv.dataport.Skrive(0x0000)
	}

}

func (selv *TAvanceretTeknologiattachment) Flush() {
	if selv.master {
		selv.enhedport.Skrive(0xE0)
	} else {
		selv.enhedport.Skrive(0xF0)
	}
	selv.kommandoport.Skrive(0xE7)

	var console_2 = TConsole{}

	var status uint8 = selv.kommandoport.Læse()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = selv.kommandoport.Læse()
	}
	if (status & 0x01) != 0 {
		console_2.MUdskriv(([]byte)(" ata flush error"))
		return
	}

}
