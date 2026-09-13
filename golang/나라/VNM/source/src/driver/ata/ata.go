package ata

import . "cổng"
import . "console"

const Bytepersector int = 512

type TNângcaoCôngnghệattachment struct {
	master			bool
	dataCổng		TCổng16bit
	lỗiCổng			TCổng8bit
	sectorSốlượngCổng	TCổng8bit
	lbaThấpCổng		TCổng8bit
	lbamidCổng		TCổng8bit
	lbahiCổng		TCổng8bit
	thiếtbịCổng		TCổng8bit
	lệnhCổng		TCổng8bit
	điềukhiểnCổng		TCổng8bit
}

func (mình *TNângcaoCôngnghệattachment) Init(master bool, cổngbase uint16) {
	mình.master = master
	mình.dataCổng.Init(cổngbase)
	mình.lỗiCổng.Init(cổngbase + 0x1)
	mình.sectorSốlượngCổng.Init(cổngbase + 0x2)
	mình.lbaThấpCổng.Init(cổngbase + 0x3)
	mình.lbamidCổng.Init(cổngbase + 0x4)
	mình.lbahiCổng.Init(cổngbase + 0x5)
	mình.thiếtbịCổng.Init(cổngbase + 0x6)
	mình.lệnhCổng.Init(cổngbase + 0x7)
	mình.điềukhiểnCổng.Init(cổngbase + 0x8)

}

func (mình *TNângcaoCôngnghệattachment) Identify() {

	var console_2 = TConsole{}

	if mình.master {
		mình.thiếtbịCổng.Ghi(0xA0)
	} else {
		mình.thiếtbịCổng.Ghi(0xB0)
	}
	mình.điềukhiểnCổng.Ghi(0)
	mình.thiếtbịCổng.Ghi(0xA0)

	var trạngthái uint8 = mình.lệnhCổng.Đọc()
	if trạngthái == 0xFF {
		console_2.MIn(([]byte)("Invalid Status"))
		return
	}

	if mình.master {
		mình.thiếtbịCổng.Ghi(0xA0)
	} else {
		mình.thiếtbịCổng.Ghi(0xB0)
	}
	mình.sectorSốlượngCổng.Ghi(0)
	mình.lbaThấpCổng.Ghi(0)
	mình.lbamidCổng.Ghi(0)
	mình.lbahiCổng.Ghi(0)
	mình.lệnhCổng.Ghi(0xEC)

	trạngthái = mình.lệnhCổng.Đọc()
	if trạngthái == 0x00 {
		console_2.MIn(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (trạngthái&0x80) == 0x80 && (trạngthái&0x01) != 0x01 {
		trạngthái = mình.lệnhCổng.Đọc()
	}

	if (trạngthái & 0x01) != 0 {
		console_2.MIn(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = mình.dataCổng.Đọc()
		nhãn := []byte("  ")
		nhãn[0] = uint8((data >> 8) & 0xFF)
		nhãn[1] = uint8(data & 0xFF)

	}
	console_2.MInxy(([]byte)("ata ok"), 10, 22)

}
func (mình *TNângcaoCôngnghệattachment) Đọc28(sector uint32, data *[]byte, sốlượng int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MIn(([]byte)("ata read error "))
		return
	}
	if sốlượng > Bytepersector {
		console_2.MIn(([]byte)("ata read error "))
		return
	}

	if mình.master {
		mình.thiếtbịCổng.Ghi(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		mình.thiếtbịCổng.Ghi(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	mình.lỗiCổng.Ghi(0)
	mình.sectorSốlượngCổng.Ghi(1)

	mình.lbaThấpCổng.Ghi(uint8(sector & 0x000000FF))
	mình.lbamidCổng.Ghi(uint8((sector & 0x0000FF00) >> 8))
	mình.lbahiCổng.Ghi(uint8((sector & 0x00FF0000) >> 16))
	mình.lệnhCổng.Ghi(0x20)

	var trạngthái uint8 = mình.lệnhCổng.Đọc()
	for ((trạngthái & 0x80) == 0x80) && ((trạngthái & 0x01) != 0x01) {
		trạngthái = mình.lệnhCổng.Đọc()
	}

	if (trạngthái & 0x01) != 0 {
		console_2.MIn(([]byte)("ata read error "))
		return
	}

	console_2.MInxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < sốlượng; i += 2 {
		var wdata uint16 = mình.dataCổng.Đọc()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < sốlượng {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (sốlượng + (sốlượng % 2)); i < Bytepersector; i += 2 {
		mình.dataCổng.Đọc()
	}
}
func (mình *TNângcaoCôngnghệattachment) Ghi28(sectorSỐ uint32, data []byte, sốlượng uint32) {

	if sectorSỐ > 0x0FFFFFFF {
		return
	}

	if sốlượng > 512 {
		return
	}

	if mình.master {
		mình.thiếtbịCổng.Ghi(uint8(0xE0 | uint8((sectorSỐ&0x0F000000)>>24)))
	} else {
		mình.thiếtbịCổng.Ghi(uint8(0xF0 | uint8((sectorSỐ&0x0F000000)>>24)))
	}

	mình.lỗiCổng.Ghi(0)
	mình.sectorSốlượngCổng.Ghi(1)
	mình.lbaThấpCổng.Ghi(uint8(sectorSỐ & 0x000000FF))
	mình.lbamidCổng.Ghi(uint8((sectorSỐ & 0x0000FF00) >> 8))
	mình.lbahiCổng.Ghi(uint8((sectorSỐ & 0x00FF0000) >> 16))
	mình.lệnhCổng.Ghi(0x30)

	var console_2 = TConsole{}
	console_2.MIn(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < sốlượng; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < sốlượng {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		mình.dataCổng.Ghi(wdata)

		nhãn := []byte("  ")
		nhãn[0] = uint8((wdata >> 8) & 0xFF)
		nhãn[1] = uint8(wdata & 0xFF)

		console_2.MIn(nhãn)
	}

	for i := (sốlượng + (sốlượng % 2)); i < 512; i += 2 {
		mình.dataCổng.Ghi(0x0000)
	}

}

func (mình *TNângcaoCôngnghệattachment) Flush() {
	if mình.master {
		mình.thiếtbịCổng.Ghi(0xE0)
	} else {
		mình.thiếtbịCổng.Ghi(0xF0)
	}
	mình.lệnhCổng.Ghi(0xE7)

	var console_2 = TConsole{}

	var trạngthái uint8 = mình.lệnhCổng.Đọc()
	if trạngthái == 0x00 {
		return
	}

	for ((trạngthái & 0x80) == 0x80) && ((trạngthái & 0x01) != 0x01) {
		trạngthái = mình.lệnhCổng.Đọc()
	}
	if (trạngthái & 0x01) != 0 {
		console_2.MIn(([]byte)(" ata flush error"))
		return
	}

}
