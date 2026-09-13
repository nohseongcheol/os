package ata

import . "درگاه"
import . "console"

const Bبایتpersector int = 512

type Tپیشرفتهtechnologyattachment struct {
	اصلی			bool
	dataدرگاه		Tدرگاه16bit
	خطادرگاه		Tدرگاه8bit
	sectorcountدرگاه	Tدرگاه8bit
	lbaاندکدرگاه		Tدرگاه8bit
	lbamidدرگاه		Tدرگاه8bit
	lbahiدرگاه		Tدرگاه8bit
	دستگاهدرگاه		Tدرگاه8bit
	فرماندرگاه		Tدرگاه8bit
	مهاردرگاه		Tدرگاه8bit
}

func (خود *Tپیشرفتهtechnologyattachment) Init(اصلی bool, درگاهbase uint16) {
	خود.اصلی = اصلی
	خود.dataدرگاه.Init(درگاهbase)
	خود.خطادرگاه.Init(درگاهbase + 0x1)
	خود.sectorcountدرگاه.Init(درگاهbase + 0x2)
	خود.lbaاندکدرگاه.Init(درگاهbase + 0x3)
	خود.lbamidدرگاه.Init(درگاهbase + 0x4)
	خود.lbahiدرگاه.Init(درگاهbase + 0x5)
	خود.دستگاهدرگاه.Init(درگاهbase + 0x6)
	خود.فرماندرگاه.Init(درگاهbase + 0x7)
	خود.مهاردرگاه.Init(درگاهbase + 0x8)

}

func (خود *Tپیشرفتهtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if خود.اصلی {
		خود.دستگاهدرگاه.Wنوشتن(0xA0)
	} else {
		خود.دستگاهدرگاه.Wنوشتن(0xB0)
	}
	خود.مهاردرگاه.Wنوشتن(0)
	خود.دستگاهدرگاه.Wنوشتن(0xA0)

	var وضعیت uint8 = خود.فرماندرگاه.Rخواندن()
	if وضعیت == 0xFF {
		console_2.Mچاپ(([]byte)("Invalid Status"))
		return
	}

	if خود.اصلی {
		خود.دستگاهدرگاه.Wنوشتن(0xA0)
	} else {
		خود.دستگاهدرگاه.Wنوشتن(0xB0)
	}
	خود.sectorcountدرگاه.Wنوشتن(0)
	خود.lbaاندکدرگاه.Wنوشتن(0)
	خود.lbamidدرگاه.Wنوشتن(0)
	خود.lbahiدرگاه.Wنوشتن(0)
	خود.فرماندرگاه.Wنوشتن(0xEC)

	وضعیت = خود.فرماندرگاه.Rخواندن()
	if وضعیت == 0x00 {
		console_2.Mچاپ(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (وضعیت&0x80) == 0x80 && (وضعیت&0x01) != 0x01 {
		وضعیت = خود.فرماندرگاه.Rخواندن()
	}

	if (وضعیت & 0x01) != 0 {
		console_2.Mچاپ(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = خود.dataدرگاه.Rخواندن()
		متن := []byte("  ")
		متن[0] = uint8((data >> 8) & 0xFF)
		متن[1] = uint8(data & 0xFF)

	}
	console_2.Mچاپxy(([]byte)("ata ok"), 10, 22)

}
func (خود *Tپیشرفتهtechnologyattachment) Rخواندن28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.Mچاپ(([]byte)("ata read error "))
		return
	}
	if count > Bبایتpersector {
		console_2.Mچاپ(([]byte)("ata read error "))
		return
	}

	if خود.اصلی {
		خود.دستگاهدرگاه.Wنوشتن(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		خود.دستگاهدرگاه.Wنوشتن(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	خود.خطادرگاه.Wنوشتن(0)
	خود.sectorcountدرگاه.Wنوشتن(1)

	خود.lbaاندکدرگاه.Wنوشتن(uint8(sector & 0x000000FF))
	خود.lbamidدرگاه.Wنوشتن(uint8((sector & 0x0000FF00) >> 8))
	خود.lbahiدرگاه.Wنوشتن(uint8((sector & 0x00FF0000) >> 16))
	خود.فرماندرگاه.Wنوشتن(0x20)

	var وضعیت uint8 = خود.فرماندرگاه.Rخواندن()
	for ((وضعیت & 0x80) == 0x80) && ((وضعیت & 0x01) != 0x01) {
		وضعیت = خود.فرماندرگاه.Rخواندن()
	}

	if (وضعیت & 0x01) != 0 {
		console_2.Mچاپ(([]byte)("ata read error "))
		return
	}

	console_2.Mچاپxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = خود.dataدرگاه.Rخواندن()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bبایتpersector; i += 2 {
		خود.dataدرگاه.Rخواندن()
	}
}
func (خود *Tپیشرفتهtechnologyattachment) Wنوشتن28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if خود.اصلی {
		خود.دستگاهدرگاه.Wنوشتن(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		خود.دستگاهدرگاه.Wنوشتن(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	خود.خطادرگاه.Wنوشتن(0)
	خود.sectorcountدرگاه.Wنوشتن(1)
	خود.lbaاندکدرگاه.Wنوشتن(uint8(sectornumber & 0x000000FF))
	خود.lbamidدرگاه.Wنوشتن(uint8((sectornumber & 0x0000FF00) >> 8))
	خود.lbahiدرگاه.Wنوشتن(uint8((sectornumber & 0x00FF0000) >> 16))
	خود.فرماندرگاه.Wنوشتن(0x30)

	var console_2 = TConsole{}
	console_2.Mچاپ(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		خود.dataدرگاه.Wنوشتن(wdata)

		متن := []byte("  ")
		متن[0] = uint8((wdata >> 8) & 0xFF)
		متن[1] = uint8(wdata & 0xFF)

		console_2.Mچاپ(متن)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		خود.dataدرگاه.Wنوشتن(0x0000)
	}

}

func (خود *Tپیشرفتهtechnologyattachment) Flush() {
	if خود.اصلی {
		خود.دستگاهدرگاه.Wنوشتن(0xE0)
	} else {
		خود.دستگاهدرگاه.Wنوشتن(0xF0)
	}
	خود.فرماندرگاه.Wنوشتن(0xE7)

	var console_2 = TConsole{}

	var وضعیت uint8 = خود.فرماندرگاه.Rخواندن()
	if وضعیت == 0x00 {
		return
	}

	for ((وضعیت & 0x80) == 0x80) && ((وضعیت & 0x01) != 0x01) {
		وضعیت = خود.فرماندرگاه.Rخواندن()
	}
	if (وضعیت & 0x01) != 0 {
		console_2.Mچاپ(([]byte)(" ata flush error"))
		return
	}

}
