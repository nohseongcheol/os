package ata

import . "port"
import . "console"

const Bytepersector int = 512

type TLanjutanTeknologiattachment struct {
	master		bool
	dataport	TPort16bit
	galatport	TPort8bit
	sectorcountport	TPort8bit
	lbaRendahport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	perangkatport	TPort8bit
	perintahport	TPort8bit
	kontrolport	TPort8bit
}

func (dirisendiri *TLanjutanTeknologiattachment) Init(master bool, portbase uint16) {
	dirisendiri.master = master
	dirisendiri.dataport.Init(portbase)
	dirisendiri.galatport.Init(portbase + 0x1)
	dirisendiri.sectorcountport.Init(portbase + 0x2)
	dirisendiri.lbaRendahport.Init(portbase + 0x3)
	dirisendiri.lbamidport.Init(portbase + 0x4)
	dirisendiri.lbahiport.Init(portbase + 0x5)
	dirisendiri.perangkatport.Init(portbase + 0x6)
	dirisendiri.perintahport.Init(portbase + 0x7)
	dirisendiri.kontrolport.Init(portbase + 0x8)

}

func (dirisendiri *TLanjutanTeknologiattachment) Identify() {

	var console_2 = TConsole{}

	if dirisendiri.master {
		dirisendiri.perangkatport.Tulis(0xA0)
	} else {
		dirisendiri.perangkatport.Tulis(0xB0)
	}
	dirisendiri.kontrolport.Tulis(0)
	dirisendiri.perangkatport.Tulis(0xA0)

	var status uint8 = dirisendiri.perintahport.Baca()
	if status == 0xFF {
		console_2.MCetak(([]byte)("Invalid Status"))
		return
	}

	if dirisendiri.master {
		dirisendiri.perangkatport.Tulis(0xA0)
	} else {
		dirisendiri.perangkatport.Tulis(0xB0)
	}
	dirisendiri.sectorcountport.Tulis(0)
	dirisendiri.lbaRendahport.Tulis(0)
	dirisendiri.lbamidport.Tulis(0)
	dirisendiri.lbahiport.Tulis(0)
	dirisendiri.perintahport.Tulis(0xEC)

	status = dirisendiri.perintahport.Baca()
	if status == 0x00 {
		console_2.MCetak(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = dirisendiri.perintahport.Baca()
	}

	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = dirisendiri.dataport.Baca()
		teks := []byte("  ")
		teks[0] = uint8((data >> 8) & 0xFF)
		teks[1] = uint8(data & 0xFF)

	}
	console_2.MCetakxy(([]byte)("ata ok"), 10, 22)

}
func (dirisendiri *TLanjutanTeknologiattachment) Baca28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}
	if count > Bytepersector {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}

	if dirisendiri.master {
		dirisendiri.perangkatport.Tulis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		dirisendiri.perangkatport.Tulis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	dirisendiri.galatport.Tulis(0)
	dirisendiri.sectorcountport.Tulis(1)

	dirisendiri.lbaRendahport.Tulis(uint8(sector & 0x000000FF))
	dirisendiri.lbamidport.Tulis(uint8((sector & 0x0000FF00) >> 8))
	dirisendiri.lbahiport.Tulis(uint8((sector & 0x00FF0000) >> 16))
	dirisendiri.perintahport.Tulis(0x20)

	var status uint8 = dirisendiri.perintahport.Baca()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = dirisendiri.perintahport.Baca()
	}

	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}

	console_2.MCetakxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = dirisendiri.dataport.Baca()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bytepersector; i += 2 {
		dirisendiri.dataport.Baca()
	}
}
func (dirisendiri *TLanjutanTeknologiattachment) Tulis28(sectorNomor uint32, data []byte, count uint32) {

	if sectorNomor > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if dirisendiri.master {
		dirisendiri.perangkatport.Tulis(uint8(0xE0 | uint8((sectorNomor&0x0F000000)>>24)))
	} else {
		dirisendiri.perangkatport.Tulis(uint8(0xF0 | uint8((sectorNomor&0x0F000000)>>24)))
	}

	dirisendiri.galatport.Tulis(0)
	dirisendiri.sectorcountport.Tulis(1)
	dirisendiri.lbaRendahport.Tulis(uint8(sectorNomor & 0x000000FF))
	dirisendiri.lbamidport.Tulis(uint8((sectorNomor & 0x0000FF00) >> 8))
	dirisendiri.lbahiport.Tulis(uint8((sectorNomor & 0x00FF0000) >> 16))
	dirisendiri.perintahport.Tulis(0x30)

	var console_2 = TConsole{}
	console_2.MCetak(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		dirisendiri.dataport.Tulis(wdata)

		teks := []byte("  ")
		teks[0] = uint8((wdata >> 8) & 0xFF)
		teks[1] = uint8(wdata & 0xFF)

		console_2.MCetak(teks)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		dirisendiri.dataport.Tulis(0x0000)
	}

}

func (dirisendiri *TLanjutanTeknologiattachment) Flush() {
	if dirisendiri.master {
		dirisendiri.perangkatport.Tulis(0xE0)
	} else {
		dirisendiri.perangkatport.Tulis(0xF0)
	}
	dirisendiri.perintahport.Tulis(0xE7)

	var console_2 = TConsole{}

	var status uint8 = dirisendiri.perintahport.Baca()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = dirisendiri.perintahport.Baca()
	}
	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)(" ata flush error"))
		return
	}

}
