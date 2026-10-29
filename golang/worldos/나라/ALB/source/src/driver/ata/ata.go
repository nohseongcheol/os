/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "porta"
import . "konsolë"

const Bytespersector int = 512

type TTëmëtejshmetechnologyattachment struct {
	master			bool
	dataPorta		TPorta16bit
	gabimPorta		TPorta8bit
	sectorcountPorta	TPorta8bit
	lbaUlëtPorta		TPorta8bit
	lbamidPorta		TPorta8bit
	lbahiPorta		TPorta8bit
	dispozitiviPorta	TPorta8bit
	urdhërPorta		TPorta8bit
	controlPorta		TPorta8bit
}

func (vetvetja *TTëmëtejshmetechnologyattachment) Init(master bool, portabase uint16) {
	vetvetja.master = master
	vetvetja.dataPorta.Init(portabase)
	vetvetja.gabimPorta.Init(portabase + 0x1)
	vetvetja.sectorcountPorta.Init(portabase + 0x2)
	vetvetja.lbaUlëtPorta.Init(portabase + 0x3)
	vetvetja.lbamidPorta.Init(portabase + 0x4)
	vetvetja.lbahiPorta.Init(portabase + 0x5)
	vetvetja.dispozitiviPorta.Init(portabase + 0x6)
	vetvetja.urdhërPorta.Init(portabase + 0x7)
	vetvetja.controlPorta.Init(portabase + 0x8)

}

func (vetvetja *TTëmëtejshmetechnologyattachment) Identify() {

	var konsolë_2 = TKonsolë{}

	if vetvetja.master {
		vetvetja.dispozitiviPorta.Shkrimi(0xA0)
	} else {
		vetvetja.dispozitiviPorta.Shkrimi(0xB0)
	}
	vetvetja.controlPorta.Shkrimi(0)
	vetvetja.dispozitiviPorta.Shkrimi(0xA0)

	var gjendja uint8 = vetvetja.urdhërPorta.Leximi()
	if gjendja == 0xFF {
		konsolë_2.MPrinto(([]byte)("Invalid Status"))
		return
	}

	if vetvetja.master {
		vetvetja.dispozitiviPorta.Shkrimi(0xA0)
	} else {
		vetvetja.dispozitiviPorta.Shkrimi(0xB0)
	}
	vetvetja.sectorcountPorta.Shkrimi(0)
	vetvetja.lbaUlëtPorta.Shkrimi(0)
	vetvetja.lbamidPorta.Shkrimi(0)
	vetvetja.lbahiPorta.Shkrimi(0)
	vetvetja.urdhërPorta.Shkrimi(0xEC)

	gjendja = vetvetja.urdhërPorta.Leximi()
	if gjendja == 0x00 {
		konsolë_2.MPrinto(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (gjendja&0x80) == 0x80 && (gjendja&0x01) != 0x01 {
		gjendja = vetvetja.urdhërPorta.Leximi()
	}

	if (gjendja & 0x01) != 0 {
		konsolë_2.MPrinto(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = vetvetja.dataPorta.Leximi()
		teksti := []byte("  ")
		teksti[0] = uint8((data >> 8) & 0xFF)
		teksti[1] = uint8(data & 0xFF)

	}
	konsolë_2.MPrintoxy(([]byte)("ata ok"), 10, 22)

}
func (vetvetja *TTëmëtejshmetechnologyattachment) Leximi28(sector uint32, data *[]byte, count int) {
	var konsolë_2 = TKonsolë{}
	if (sector & 0xF0000000) != 0 {
		konsolë_2.MPrinto(([]byte)("ata read error "))
		return
	}
	if count > Bytespersector {
		konsolë_2.MPrinto(([]byte)("ata read error "))
		return
	}

	if vetvetja.master {
		vetvetja.dispozitiviPorta.Shkrimi(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		vetvetja.dispozitiviPorta.Shkrimi(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	vetvetja.gabimPorta.Shkrimi(0)
	vetvetja.sectorcountPorta.Shkrimi(1)

	vetvetja.lbaUlëtPorta.Shkrimi(uint8(sector & 0x000000FF))
	vetvetja.lbamidPorta.Shkrimi(uint8((sector & 0x0000FF00) >> 8))
	vetvetja.lbahiPorta.Shkrimi(uint8((sector & 0x00FF0000) >> 16))
	vetvetja.urdhërPorta.Shkrimi(0x20)

	var gjendja uint8 = vetvetja.urdhërPorta.Leximi()
	for ((gjendja & 0x80) == 0x80) && ((gjendja & 0x01) != 0x01) {
		gjendja = vetvetja.urdhërPorta.Leximi()
	}

	if (gjendja & 0x01) != 0 {
		konsolë_2.MPrinto(([]byte)("ata read error "))
		return
	}

	konsolë_2.MPrintoxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = vetvetja.dataPorta.Leximi()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bytespersector; i += 2 {
		vetvetja.dataPorta.Leximi()
	}
}
func (vetvetja *TTëmëtejshmetechnologyattachment) Shkrimi28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if vetvetja.master {
		vetvetja.dispozitiviPorta.Shkrimi(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		vetvetja.dispozitiviPorta.Shkrimi(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	vetvetja.gabimPorta.Shkrimi(0)
	vetvetja.sectorcountPorta.Shkrimi(1)
	vetvetja.lbaUlëtPorta.Shkrimi(uint8(sectornumber & 0x000000FF))
	vetvetja.lbamidPorta.Shkrimi(uint8((sectornumber & 0x0000FF00) >> 8))
	vetvetja.lbahiPorta.Shkrimi(uint8((sectornumber & 0x00FF0000) >> 16))
	vetvetja.urdhërPorta.Shkrimi(0x30)

	var konsolë_2 = TKonsolë{}
	konsolë_2.MPrinto(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		vetvetja.dataPorta.Shkrimi(wdata)

		teksti := []byte("  ")
		teksti[0] = uint8((wdata >> 8) & 0xFF)
		teksti[1] = uint8(wdata & 0xFF)

		konsolë_2.MPrinto(teksti)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		vetvetja.dataPorta.Shkrimi(0x0000)
	}

}

func (vetvetja *TTëmëtejshmetechnologyattachment) Flush() {
	if vetvetja.master {
		vetvetja.dispozitiviPorta.Shkrimi(0xE0)
	} else {
		vetvetja.dispozitiviPorta.Shkrimi(0xF0)
	}
	vetvetja.urdhërPorta.Shkrimi(0xE7)

	var konsolë_2 = TKonsolë{}

	var gjendja uint8 = vetvetja.urdhërPorta.Leximi()
	if gjendja == 0x00 {
		return
	}

	for ((gjendja & 0x80) == 0x80) && ((gjendja & 0x01) != 0x01) {
		gjendja = vetvetja.urdhërPorta.Leximi()
	}
	if (gjendja & 0x01) != 0 {
		konsolë_2.MPrinto(([]byte)(" ata flush error"))
		return
	}

}
