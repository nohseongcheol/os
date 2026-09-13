package ata

import . "պորտ"
import . "console"

const Բայթերpersector int = 512

type TԸնդլայնվածՏեխնոլոգիաattachment struct {
	վարպետ		bool
	dataՊորտ	TՊորտ16bit
	սխալՊորտ	TՊորտ8bit
	sectorcountՊորտ	TՊորտ8bit
	lbaՑածրՊորտ	TՊորտ8bit
	lbamidՊորտ	TՊորտ8bit
	lbahiՊորտ	TՊորտ8bit
	սարքՊորտ	TՊորտ8bit
	հրահանգՊորտ	TՊորտ8bit
	controlՊորտ	TՊորտ8bit
}

func (ինքնուրույն *TԸնդլայնվածՏեխնոլոգիաattachment) Init(վարպետ bool, պորտbase uint16) {
	ինքնուրույն.վարպետ = վարպետ
	ինքնուրույն.dataՊորտ.Init(պորտbase)
	ինքնուրույն.սխալՊորտ.Init(պորտbase + 0x1)
	ինքնուրույն.sectorcountՊորտ.Init(պորտbase + 0x2)
	ինքնուրույն.lbaՑածրՊորտ.Init(պորտbase + 0x3)
	ինքնուրույն.lbamidՊորտ.Init(պորտbase + 0x4)
	ինքնուրույն.lbahiՊորտ.Init(պորտbase + 0x5)
	ինքնուրույն.սարքՊորտ.Init(պորտbase + 0x6)
	ինքնուրույն.հրահանգՊորտ.Init(պորտbase + 0x7)
	ինքնուրույն.controlՊորտ.Init(պորտbase + 0x8)

}

func (ինքնուրույն *TԸնդլայնվածՏեխնոլոգիաattachment) Identify() {

	var console_2 = TConsole{}

	if ինքնուրույն.վարպետ {
		ինքնուրույն.սարքՊորտ.Գրել(0xA0)
	} else {
		ինքնուրույն.սարքՊորտ.Գրել(0xB0)
	}
	ինքնուրույն.controlՊորտ.Գրել(0)
	ինքնուրույն.սարքՊորտ.Գրել(0xA0)

	var կարգավիճակ uint8 = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	if կարգավիճակ == 0xFF {
		console_2.MՏպել(([]byte)("Invalid Status"))
		return
	}

	if ինքնուրույն.վարպետ {
		ինքնուրույն.սարքՊորտ.Գրել(0xA0)
	} else {
		ինքնուրույն.սարքՊորտ.Գրել(0xB0)
	}
	ինքնուրույն.sectorcountՊորտ.Գրել(0)
	ինքնուրույն.lbaՑածրՊորտ.Գրել(0)
	ինքնուրույն.lbamidՊորտ.Գրել(0)
	ինքնուրույն.lbahiՊորտ.Գրել(0)
	ինքնուրույն.հրահանգՊորտ.Գրել(0xEC)

	կարգավիճակ = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	if կարգավիճակ == 0x00 {
		console_2.MՏպել(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (կարգավիճակ&0x80) == 0x80 && (կարգավիճակ&0x01) != 0x01 {
		կարգավիճակ = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	}

	if (կարգավիճակ & 0x01) != 0 {
		console_2.MՏպել(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = ինքնուրույն.dataՊորտ.Ընթերցում()
		տեքստ := []byte("  ")
		տեքստ[0] = uint8((data >> 8) & 0xFF)
		տեքստ[1] = uint8(data & 0xFF)

	}
	console_2.MՏպելxy(([]byte)("ata ok"), 10, 22)

}
func (ինքնուրույն *TԸնդլայնվածՏեխնոլոգիաattachment) Ընթերցում28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MՏպել(([]byte)("ata read error "))
		return
	}
	if count > Բայթերpersector {
		console_2.MՏպել(([]byte)("ata read error "))
		return
	}

	if ինքնուրույն.վարպետ {
		ինքնուրույն.սարքՊորտ.Գրել(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		ինքնուրույն.սարքՊորտ.Գրել(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	ինքնուրույն.սխալՊորտ.Գրել(0)
	ինքնուրույն.sectorcountՊորտ.Գրել(1)

	ինքնուրույն.lbaՑածրՊորտ.Գրել(uint8(sector & 0x000000FF))
	ինքնուրույն.lbamidՊորտ.Գրել(uint8((sector & 0x0000FF00) >> 8))
	ինքնուրույն.lbahiՊորտ.Գրել(uint8((sector & 0x00FF0000) >> 16))
	ինքնուրույն.հրահանգՊորտ.Գրել(0x20)

	var կարգավիճակ uint8 = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	for ((կարգավիճակ & 0x80) == 0x80) && ((կարգավիճակ & 0x01) != 0x01) {
		կարգավիճակ = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	}

	if (կարգավիճակ & 0x01) != 0 {
		console_2.MՏպել(([]byte)("ata read error "))
		return
	}

	console_2.MՏպելxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = ինքնուրույն.dataՊորտ.Ընթերցում()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Բայթերpersector; i += 2 {
		ինքնուրույն.dataՊորտ.Ընթերցում()
	}
}
func (ինքնուրույն *TԸնդլայնվածՏեխնոլոգիաattachment) Գրել28(sectorՀԱՄԱՐ uint32, data []byte, count uint32) {

	if sectorՀԱՄԱՐ > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if ինքնուրույն.վարպետ {
		ինքնուրույն.սարքՊորտ.Գրել(uint8(0xE0 | uint8((sectorՀԱՄԱՐ&0x0F000000)>>24)))
	} else {
		ինքնուրույն.սարքՊորտ.Գրել(uint8(0xF0 | uint8((sectorՀԱՄԱՐ&0x0F000000)>>24)))
	}

	ինքնուրույն.սխալՊորտ.Գրել(0)
	ինքնուրույն.sectorcountՊորտ.Գրել(1)
	ինքնուրույն.lbaՑածրՊորտ.Գրել(uint8(sectorՀԱՄԱՐ & 0x000000FF))
	ինքնուրույն.lbamidՊորտ.Գրել(uint8((sectorՀԱՄԱՐ & 0x0000FF00) >> 8))
	ինքնուրույն.lbahiՊորտ.Գրել(uint8((sectorՀԱՄԱՐ & 0x00FF0000) >> 16))
	ինքնուրույն.հրահանգՊորտ.Գրել(0x30)

	var console_2 = TConsole{}
	console_2.MՏպել(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		ինքնուրույն.dataՊորտ.Գրել(wdata)

		տեքստ := []byte("  ")
		տեքստ[0] = uint8((wdata >> 8) & 0xFF)
		տեքստ[1] = uint8(wdata & 0xFF)

		console_2.MՏպել(տեքստ)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		ինքնուրույն.dataՊորտ.Գրել(0x0000)
	}

}

func (ինքնուրույն *TԸնդլայնվածՏեխնոլոգիաattachment) Flush() {
	if ինքնուրույն.վարպետ {
		ինքնուրույն.սարքՊորտ.Գրել(0xE0)
	} else {
		ինքնուրույն.սարքՊորտ.Գրել(0xF0)
	}
	ինքնուրույն.հրահանգՊորտ.Գրել(0xE7)

	var console_2 = TConsole{}

	var կարգավիճակ uint8 = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	if կարգավիճակ == 0x00 {
		return
	}

	for ((կարգավիճակ & 0x80) == 0x80) && ((կարգավիճակ & 0x01) != 0x01) {
		կարգավիճակ = ինքնուրույն.հրահանգՊորտ.Ընթերցում()
	}
	if (կարգավիճակ & 0x01) != 0 {
		console_2.MՏպել(([]byte)(" ata flush error"))
		return
	}

}
