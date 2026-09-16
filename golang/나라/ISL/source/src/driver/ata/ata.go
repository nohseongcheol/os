/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Bætipersector int = 512

type TNánarTækniattachment struct {
	master		bool
	dataport	TPort16bit
	villaport	TPort8bit
	sectorcountport	TPort8bit
	lbaLágtport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	tækiport	TPort8bit
	skipunport	TPort8bit
	stýringport	TPort8bit
}

func (sjálft *TNánarTækniattachment) Init(master bool, portbase uint16) {
	sjálft.master = master
	sjálft.dataport.Init(portbase)
	sjálft.villaport.Init(portbase + 0x1)
	sjálft.sectorcountport.Init(portbase + 0x2)
	sjálft.lbaLágtport.Init(portbase + 0x3)
	sjálft.lbamidport.Init(portbase + 0x4)
	sjálft.lbahiport.Init(portbase + 0x5)
	sjálft.tækiport.Init(portbase + 0x6)
	sjálft.skipunport.Init(portbase + 0x7)
	sjálft.stýringport.Init(portbase + 0x8)

}

func (sjálft *TNánarTækniattachment) Identify() {

	var console_2 = TConsole{}

	if sjálft.master {
		sjálft.tækiport.Skrift(0xA0)
	} else {
		sjálft.tækiport.Skrift(0xB0)
	}
	sjálft.stýringport.Skrift(0)
	sjálft.tækiport.Skrift(0xA0)

	var staða_3 uint8 = sjálft.skipunport.Lestur()
	if staða_3 == 0xFF {
		console_2.MPrenta(([]byte)("Invalid Status"))
		return
	}

	if sjálft.master {
		sjálft.tækiport.Skrift(0xA0)
	} else {
		sjálft.tækiport.Skrift(0xB0)
	}
	sjálft.sectorcountport.Skrift(0)
	sjálft.lbaLágtport.Skrift(0)
	sjálft.lbamidport.Skrift(0)
	sjálft.lbahiport.Skrift(0)
	sjálft.skipunport.Skrift(0xEC)

	staða_3 = sjálft.skipunport.Lestur()
	if staða_3 == 0x00 {
		console_2.MPrenta(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (staða_3&0x80) == 0x80 && (staða_3&0x01) != 0x01 {
		staða_3 = sjálft.skipunport.Lestur()
	}

	if (staða_3 & 0x01) != 0 {
		console_2.MPrenta(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = sjálft.dataport.Lestur()
		texti := []byte("  ")
		texti[0] = uint8((data >> 8) & 0xFF)
		texti[1] = uint8(data & 0xFF)

	}
	console_2.MPrentaxy(([]byte)("ata ok"), 10, 22)

}
func (sjálft *TNánarTækniattachment) Lestur28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MPrenta(([]byte)("ata read error "))
		return
	}
	if count > Bætipersector {
		console_2.MPrenta(([]byte)("ata read error "))
		return
	}

	if sjálft.master {
		sjálft.tækiport.Skrift(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		sjálft.tækiport.Skrift(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	sjálft.villaport.Skrift(0)
	sjálft.sectorcountport.Skrift(1)

	sjálft.lbaLágtport.Skrift(uint8(sector & 0x000000FF))
	sjálft.lbamidport.Skrift(uint8((sector & 0x0000FF00) >> 8))
	sjálft.lbahiport.Skrift(uint8((sector & 0x00FF0000) >> 16))
	sjálft.skipunport.Skrift(0x20)

	var staða_3 uint8 = sjálft.skipunport.Lestur()
	for ((staða_3 & 0x80) == 0x80) && ((staða_3 & 0x01) != 0x01) {
		staða_3 = sjálft.skipunport.Lestur()
	}

	if (staða_3 & 0x01) != 0 {
		console_2.MPrenta(([]byte)("ata read error "))
		return
	}

	console_2.MPrentaxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = sjálft.dataport.Lestur()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bætipersector; i += 2 {
		sjálft.dataport.Lestur()
	}
}
func (sjálft *TNánarTækniattachment) Skrift28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if sjálft.master {
		sjálft.tækiport.Skrift(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		sjálft.tækiport.Skrift(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	sjálft.villaport.Skrift(0)
	sjálft.sectorcountport.Skrift(1)
	sjálft.lbaLágtport.Skrift(uint8(sectornumber & 0x000000FF))
	sjálft.lbamidport.Skrift(uint8((sectornumber & 0x0000FF00) >> 8))
	sjálft.lbahiport.Skrift(uint8((sectornumber & 0x00FF0000) >> 16))
	sjálft.skipunport.Skrift(0x30)

	var console_2 = TConsole{}
	console_2.MPrenta(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		sjálft.dataport.Skrift(wdata)

		texti := []byte("  ")
		texti[0] = uint8((wdata >> 8) & 0xFF)
		texti[1] = uint8(wdata & 0xFF)

		console_2.MPrenta(texti)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		sjálft.dataport.Skrift(0x0000)
	}

}

func (sjálft *TNánarTækniattachment) Flush() {
	if sjálft.master {
		sjálft.tækiport.Skrift(0xE0)
	} else {
		sjálft.tækiport.Skrift(0xF0)
	}
	sjálft.skipunport.Skrift(0xE7)

	var console_2 = TConsole{}

	var staða_3 uint8 = sjálft.skipunport.Lestur()
	if staða_3 == 0x00 {
		return
	}

	for ((staða_3 & 0x80) == 0x80) && ((staða_3 & 0x01) != 0x01) {
		staða_3 = sjálft.skipunport.Lestur()
	}
	if (staða_3 & 0x01) != 0 {
		console_2.MPrenta(([]byte)(" ata flush error"))
		return
	}

}
