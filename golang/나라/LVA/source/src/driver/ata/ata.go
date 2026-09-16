/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "ports"
import . "console"

const Baitipersector int = 512

type TPaplašinātiTehnoloģijaattachment struct {
	master			bool
	dataPorts		TPorts16bit
	kļūdaPorts		TPorts8bit
	sectorcountPorts	TPorts8bit
	lbaKlusiPorts		TPorts8bit
	lbamidPorts		TPorts8bit
	lbahiPorts		TPorts8bit
	ierīcePorts		TPorts8bit
	komandaPorts		TPorts8bit
	ctrlPorts		TPorts8bit
}

func (pats *TPaplašinātiTehnoloģijaattachment) Init(master bool, portsbase uint16) {
	pats.master = master
	pats.dataPorts.Init(portsbase)
	pats.kļūdaPorts.Init(portsbase + 0x1)
	pats.sectorcountPorts.Init(portsbase + 0x2)
	pats.lbaKlusiPorts.Init(portsbase + 0x3)
	pats.lbamidPorts.Init(portsbase + 0x4)
	pats.lbahiPorts.Init(portsbase + 0x5)
	pats.ierīcePorts.Init(portsbase + 0x6)
	pats.komandaPorts.Init(portsbase + 0x7)
	pats.ctrlPorts.Init(portsbase + 0x8)

}

func (pats *TPaplašinātiTehnoloģijaattachment) Identify() {

	var console_2 = TConsole{}

	if pats.master {
		pats.ierīcePorts.Rakstīt(0xA0)
	} else {
		pats.ierīcePorts.Rakstīt(0xB0)
	}
	pats.ctrlPorts.Rakstīt(0)
	pats.ierīcePorts.Rakstīt(0xA0)

	var statuss uint8 = pats.komandaPorts.Lasīt()
	if statuss == 0xFF {
		console_2.MDrukāt(([]byte)("Invalid Status"))
		return
	}

	if pats.master {
		pats.ierīcePorts.Rakstīt(0xA0)
	} else {
		pats.ierīcePorts.Rakstīt(0xB0)
	}
	pats.sectorcountPorts.Rakstīt(0)
	pats.lbaKlusiPorts.Rakstīt(0)
	pats.lbamidPorts.Rakstīt(0)
	pats.lbahiPorts.Rakstīt(0)
	pats.komandaPorts.Rakstīt(0xEC)

	statuss = pats.komandaPorts.Lasīt()
	if statuss == 0x00 {
		console_2.MDrukāt(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (statuss&0x80) == 0x80 && (statuss&0x01) != 0x01 {
		statuss = pats.komandaPorts.Lasīt()
	}

	if (statuss & 0x01) != 0 {
		console_2.MDrukāt(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = pats.dataPorts.Lasīt()
		teksts := []byte("  ")
		teksts[0] = uint8((data >> 8) & 0xFF)
		teksts[1] = uint8(data & 0xFF)

	}
	console_2.MDrukātxy(([]byte)("ata ok"), 10, 22)

}
func (pats *TPaplašinātiTehnoloģijaattachment) Lasīt28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MDrukāt(([]byte)("ata read error "))
		return
	}
	if count > Baitipersector {
		console_2.MDrukāt(([]byte)("ata read error "))
		return
	}

	if pats.master {
		pats.ierīcePorts.Rakstīt(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		pats.ierīcePorts.Rakstīt(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	pats.kļūdaPorts.Rakstīt(0)
	pats.sectorcountPorts.Rakstīt(1)

	pats.lbaKlusiPorts.Rakstīt(uint8(sector & 0x000000FF))
	pats.lbamidPorts.Rakstīt(uint8((sector & 0x0000FF00) >> 8))
	pats.lbahiPorts.Rakstīt(uint8((sector & 0x00FF0000) >> 16))
	pats.komandaPorts.Rakstīt(0x20)

	var statuss uint8 = pats.komandaPorts.Lasīt()
	for ((statuss & 0x80) == 0x80) && ((statuss & 0x01) != 0x01) {
		statuss = pats.komandaPorts.Lasīt()
	}

	if (statuss & 0x01) != 0 {
		console_2.MDrukāt(([]byte)("ata read error "))
		return
	}

	console_2.MDrukātxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = pats.dataPorts.Lasīt()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baitipersector; i += 2 {
		pats.dataPorts.Lasīt()
	}
}
func (pats *TPaplašinātiTehnoloģijaattachment) Rakstīt28(sectorSkaitlis uint32, data []byte, count uint32) {

	if sectorSkaitlis > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if pats.master {
		pats.ierīcePorts.Rakstīt(uint8(0xE0 | uint8((sectorSkaitlis&0x0F000000)>>24)))
	} else {
		pats.ierīcePorts.Rakstīt(uint8(0xF0 | uint8((sectorSkaitlis&0x0F000000)>>24)))
	}

	pats.kļūdaPorts.Rakstīt(0)
	pats.sectorcountPorts.Rakstīt(1)
	pats.lbaKlusiPorts.Rakstīt(uint8(sectorSkaitlis & 0x000000FF))
	pats.lbamidPorts.Rakstīt(uint8((sectorSkaitlis & 0x0000FF00) >> 8))
	pats.lbahiPorts.Rakstīt(uint8((sectorSkaitlis & 0x00FF0000) >> 16))
	pats.komandaPorts.Rakstīt(0x30)

	var console_2 = TConsole{}
	console_2.MDrukāt(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		pats.dataPorts.Rakstīt(wdata)

		teksts := []byte("  ")
		teksts[0] = uint8((wdata >> 8) & 0xFF)
		teksts[1] = uint8(wdata & 0xFF)

		console_2.MDrukāt(teksts)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		pats.dataPorts.Rakstīt(0x0000)
	}

}

func (pats *TPaplašinātiTehnoloģijaattachment) Flush() {
	if pats.master {
		pats.ierīcePorts.Rakstīt(0xE0)
	} else {
		pats.ierīcePorts.Rakstīt(0xF0)
	}
	pats.komandaPorts.Rakstīt(0xE7)

	var console_2 = TConsole{}

	var statuss uint8 = pats.komandaPorts.Lasīt()
	if statuss == 0x00 {
		return
	}

	for ((statuss & 0x80) == 0x80) && ((statuss & 0x01) != 0x01) {
		statuss = pats.komandaPorts.Lasīt()
	}
	if (statuss & 0x01) != 0 {
		console_2.MDrukāt(([]byte)(" ata flush error"))
		return
	}

}
