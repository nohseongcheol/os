package ata

import . "port"
import . "console"

const Baitpersector int = 512

type TLanjutanTeknologiattachment struct {
	master		bool
	dataport	TPort16bit
	ralatport	TPort8bit
	sectorcountport	TPort8bit
	lbaRendahport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	perantiport	TPort8bit
	perintahport	TPort8bit
	kawalanport	TPort8bit
}

func (diri *TLanjutanTeknologiattachment) Init(master bool, portbase uint16) {
	diri.master = master
	diri.dataport.Init(portbase)
	diri.ralatport.Init(portbase + 0x1)
	diri.sectorcountport.Init(portbase + 0x2)
	diri.lbaRendahport.Init(portbase + 0x3)
	diri.lbamidport.Init(portbase + 0x4)
	diri.lbahiport.Init(portbase + 0x5)
	diri.perantiport.Init(portbase + 0x6)
	diri.perintahport.Init(portbase + 0x7)
	diri.kawalanport.Init(portbase + 0x8)

}

func (diri *TLanjutanTeknologiattachment) Identify() {

	var console_2 = TConsole{}

	if diri.master {
		diri.perantiport.Tulis(0xA0)
	} else {
		diri.perantiport.Tulis(0xB0)
	}
	diri.kawalanport.Tulis(0)
	diri.perantiport.Tulis(0xA0)

	var status uint8 = diri.perintahport.Baca()
	if status == 0xFF {
		console_2.MCetak(([]byte)("Invalid Status"))
		return
	}

	if diri.master {
		diri.perantiport.Tulis(0xA0)
	} else {
		diri.perantiport.Tulis(0xB0)
	}
	diri.sectorcountport.Tulis(0)
	diri.lbaRendahport.Tulis(0)
	diri.lbamidport.Tulis(0)
	diri.lbahiport.Tulis(0)
	diri.perintahport.Tulis(0xEC)

	status = diri.perintahport.Baca()
	if status == 0x00 {
		console_2.MCetak(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = diri.perintahport.Baca()
	}

	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = diri.dataport.Baca()
		teks := []byte("  ")
		teks[0] = uint8((data >> 8) & 0xFF)
		teks[1] = uint8(data & 0xFF)

	}
	console_2.MCetakxy(([]byte)("ata ok"), 10, 22)

}
func (diri *TLanjutanTeknologiattachment) Baca28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}
	if count > Baitpersector {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}

	if diri.master {
		diri.perantiport.Tulis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		diri.perantiport.Tulis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	diri.ralatport.Tulis(0)
	diri.sectorcountport.Tulis(1)

	diri.lbaRendahport.Tulis(uint8(sector & 0x000000FF))
	diri.lbamidport.Tulis(uint8((sector & 0x0000FF00) >> 8))
	diri.lbahiport.Tulis(uint8((sector & 0x00FF0000) >> 16))
	diri.perintahport.Tulis(0x20)

	var status uint8 = diri.perintahport.Baca()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = diri.perintahport.Baca()
	}

	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)("ata read error "))
		return
	}

	console_2.MCetakxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = diri.dataport.Baca()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baitpersector; i += 2 {
		diri.dataport.Baca()
	}
}
func (diri *TLanjutanTeknologiattachment) Tulis28(sectorNOMBOR uint32, data []byte, count uint32) {

	if sectorNOMBOR > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if diri.master {
		diri.perantiport.Tulis(uint8(0xE0 | uint8((sectorNOMBOR&0x0F000000)>>24)))
	} else {
		diri.perantiport.Tulis(uint8(0xF0 | uint8((sectorNOMBOR&0x0F000000)>>24)))
	}

	diri.ralatport.Tulis(0)
	diri.sectorcountport.Tulis(1)
	diri.lbaRendahport.Tulis(uint8(sectorNOMBOR & 0x000000FF))
	diri.lbamidport.Tulis(uint8((sectorNOMBOR & 0x0000FF00) >> 8))
	diri.lbahiport.Tulis(uint8((sectorNOMBOR & 0x00FF0000) >> 16))
	diri.perintahport.Tulis(0x30)

	var console_2 = TConsole{}
	console_2.MCetak(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		diri.dataport.Tulis(wdata)

		teks := []byte("  ")
		teks[0] = uint8((wdata >> 8) & 0xFF)
		teks[1] = uint8(wdata & 0xFF)

		console_2.MCetak(teks)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		diri.dataport.Tulis(0x0000)
	}

}

func (diri *TLanjutanTeknologiattachment) Flush() {
	if diri.master {
		diri.perantiport.Tulis(0xE0)
	} else {
		diri.perantiport.Tulis(0xF0)
	}
	diri.perintahport.Tulis(0xE7)

	var console_2 = TConsole{}

	var status uint8 = diri.perintahport.Baca()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = diri.perintahport.Baca()
	}
	if (status & 0x01) != 0 {
		console_2.MCetak(([]byte)(" ata flush error"))
		return
	}

}
