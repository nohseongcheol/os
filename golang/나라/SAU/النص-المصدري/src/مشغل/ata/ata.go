/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "منفذ"
import . "طرفية"

const Bبايتpersector int = 512

type Tمتقدمالتقنيةattachment struct {
	رئيسي		bool
	بياناتمنفذ	Tمنفذ16bit
	خطأمنفذ		Tمنفذ8bit
	sectorcountمنفذ	Tمنفذ8bit
	lbaمنخفضمنفذ	Tمنفذ8bit
	lbamidمنفذ	Tمنفذ8bit
	lbahiمنفذ	Tمنفذ8bit
	الجهازمنفذ	Tمنفذ8bit
	أمرمنفذ		Tمنفذ8bit
	تحكممنفذ	Tمنفذ8bit
}

func (نفسه *Tمتقدمالتقنيةattachment) Init(رئيسي bool, منفذbase uint16) {
	نفسه.رئيسي = رئيسي
	نفسه.بياناتمنفذ.Init(منفذbase)
	نفسه.خطأمنفذ.Init(منفذbase + 0x1)
	نفسه.sectorcountمنفذ.Init(منفذbase + 0x2)
	نفسه.lbaمنخفضمنفذ.Init(منفذbase + 0x3)
	نفسه.lbamidمنفذ.Init(منفذbase + 0x4)
	نفسه.lbahiمنفذ.Init(منفذbase + 0x5)
	نفسه.الجهازمنفذ.Init(منفذbase + 0x6)
	نفسه.أمرمنفذ.Init(منفذbase + 0x7)
	نفسه.تحكممنفذ.Init(منفذbase + 0x8)

}

func (نفسه *Tمتقدمالتقنيةattachment) Identify() {

	var طرفية_2 = Tطرفية{}

	if نفسه.رئيسي {
		نفسه.الجهازمنفذ.Wكتابة(0xA0)
	} else {
		نفسه.الجهازمنفذ.Wكتابة(0xB0)
	}
	نفسه.تحكممنفذ.Wكتابة(0)
	نفسه.الجهازمنفذ.Wكتابة(0xA0)

	var الحالة uint8 = نفسه.أمرمنفذ.Rقراءة()
	if الحالة == 0xFF {
		طرفية_2.Mاطبع(([]byte)("Invalid Status"))
		return
	}

	if نفسه.رئيسي {
		نفسه.الجهازمنفذ.Wكتابة(0xA0)
	} else {
		نفسه.الجهازمنفذ.Wكتابة(0xB0)
	}
	نفسه.sectorcountمنفذ.Wكتابة(0)
	نفسه.lbaمنخفضمنفذ.Wكتابة(0)
	نفسه.lbamidمنفذ.Wكتابة(0)
	نفسه.lbahiمنفذ.Wكتابة(0)
	نفسه.أمرمنفذ.Wكتابة(0xEC)

	الحالة = نفسه.أمرمنفذ.Rقراءة()
	if الحالة == 0x00 {
		طرفية_2.Mاطبع(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (الحالة&0x80) == 0x80 && (الحالة&0x01) != 0x01 {
		الحالة = نفسه.أمرمنفذ.Rقراءة()
	}

	if (الحالة & 0x01) != 0 {
		طرفية_2.Mاطبع(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var بيانات = نفسه.بياناتمنفذ.Rقراءة()
		نص := []byte("  ")
		نص[0] = uint8((بيانات >> 8) & 0xFF)
		نص[1] = uint8(بيانات & 0xFF)

	}
	طرفية_2.Mاطبعxy(([]byte)("ata ok"), 10, 22)

}
func (نفسه *Tمتقدمالتقنيةattachment) Rقراءة28(sector uint32, بيانات *[]byte, count int) {
	var طرفية_2 = Tطرفية{}
	if (sector & 0xF0000000) != 0 {
		طرفية_2.Mاطبع(([]byte)("ata read error "))
		return
	}
	if count > Bبايتpersector {
		طرفية_2.Mاطبع(([]byte)("ata read error "))
		return
	}

	if نفسه.رئيسي {
		نفسه.الجهازمنفذ.Wكتابة(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		نفسه.الجهازمنفذ.Wكتابة(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	نفسه.خطأمنفذ.Wكتابة(0)
	نفسه.sectorcountمنفذ.Wكتابة(1)

	نفسه.lbaمنخفضمنفذ.Wكتابة(uint8(sector & 0x000000FF))
	نفسه.lbamidمنفذ.Wكتابة(uint8((sector & 0x0000FF00) >> 8))
	نفسه.lbahiمنفذ.Wكتابة(uint8((sector & 0x00FF0000) >> 16))
	نفسه.أمرمنفذ.Wكتابة(0x20)

	var الحالة uint8 = نفسه.أمرمنفذ.Rقراءة()
	for ((الحالة & 0x80) == 0x80) && ((الحالة & 0x01) != 0x01) {
		الحالة = نفسه.أمرمنفذ.Rقراءة()
	}

	if (الحالة & 0x01) != 0 {
		طرفية_2.Mاطبع(([]byte)("ata read error "))
		return
	}

	طرفية_2.Mاطبعxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = نفسه.بياناتمنفذ.Rقراءة()

		(*بيانات)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*بيانات)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bبايتpersector; i += 2 {
		نفسه.بياناتمنفذ.Rقراءة()
	}
}
func (نفسه *Tمتقدمالتقنيةattachment) Wكتابة28(sectorالأرقام uint32, بيانات []byte, count uint32) {

	if sectorالأرقام > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if نفسه.رئيسي {
		نفسه.الجهازمنفذ.Wكتابة(uint8(0xE0 | uint8((sectorالأرقام&0x0F000000)>>24)))
	} else {
		نفسه.الجهازمنفذ.Wكتابة(uint8(0xF0 | uint8((sectorالأرقام&0x0F000000)>>24)))
	}

	نفسه.خطأمنفذ.Wكتابة(0)
	نفسه.sectorcountمنفذ.Wكتابة(1)
	نفسه.lbaمنخفضمنفذ.Wكتابة(uint8(sectorالأرقام & 0x000000FF))
	نفسه.lbamidمنفذ.Wكتابة(uint8((sectorالأرقام & 0x0000FF00) >> 8))
	نفسه.lbahiمنفذ.Wكتابة(uint8((sectorالأرقام & 0x00FF0000) >> 16))
	نفسه.أمرمنفذ.Wكتابة(0x30)

	var طرفية_2 = Tطرفية{}
	طرفية_2.Mاطبع(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(بيانات[i])

		if i+1 < count {
			wdata = wdata | (uint16(بيانات[i+1]) << 8)
		}

		نفسه.بياناتمنفذ.Wكتابة(wdata)

		نص := []byte("  ")
		نص[0] = uint8((wdata >> 8) & 0xFF)
		نص[1] = uint8(wdata & 0xFF)

		طرفية_2.Mاطبع(نص)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		نفسه.بياناتمنفذ.Wكتابة(0x0000)
	}

}

func (نفسه *Tمتقدمالتقنيةattachment) Flush() {
	if نفسه.رئيسي {
		نفسه.الجهازمنفذ.Wكتابة(0xE0)
	} else {
		نفسه.الجهازمنفذ.Wكتابة(0xF0)
	}
	نفسه.أمرمنفذ.Wكتابة(0xE7)

	var طرفية_2 = Tطرفية{}

	var الحالة uint8 = نفسه.أمرمنفذ.Rقراءة()
	if الحالة == 0x00 {
		return
	}

	for ((الحالة & 0x80) == 0x80) && ((الحالة & 0x01) != 0x01) {
		الحالة = نفسه.أمرمنفذ.Rقراءة()
	}
	if (الحالة & 0x01) != 0 {
		طرفية_2.Mاطبع(([]byte)(" ata flush error"))
		return
	}

}
