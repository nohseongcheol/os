package msdosتجزئة

import . "طرفية"
import . "أداة"

import . "مشغل/ata"

type Tتجزئةجدولentry struct {
	bootable	uint8

	ابدأhead	uint8
	ابدأsector	uint8
	ابدأcylinder	uint16

	Pتجزئةالهوية	uint8

	نهايةhead	uint8
	نهايةsector	uint8
	نهايةcylinder	uint16

	Sابدأlba	uint32
	المدة		uint32
}

func (نفسه *Tتجزئةجدولentry) Init(بيانات [16]byte) {
	نفسه.bootable = بيانات[0]

	نفسه.ابدأhead = بيانات[1]
	نفسه.ابدأsector = (بيانات[2] >> 2)
	نفسه.ابدأcylinder = Unsignedinteger16r(uint16(بيانات[2]&0x03) | uint16(بيانات[3]))

	نفسه.Pتجزئةالهوية = بيانات[4]

	نفسه.نهايةhead = بيانات[5]
	نفسه.نهايةsector = (بيانات[6] >> 2)
	نفسه.نهايةcylinder = Unsignedinteger16r(uint16(بيانات[6]&0x03) | uint16(بيانات[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], بيانات[8:12])
	نفسه.Sابدأlba = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], بيانات[12:16])
	نفسه.المدة = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer2))
}

type Tسجل_الإقلاع_الرئيسي struct {
	bootloader	[440]byte
	signature	uint32
	غيرمستخدمة	uint16

	Primaryتجزئة	[4]Tتجزئةجدولentry

	magicnumber	uint16
}
type Tmsdosتجزئةجدول struct {
	Mbr Tسجل_الإقلاع_الرئيسي
}

func (نفسه *Tmsdosتجزئةجدول) Rقراءةتجزئة(hd *Tمتقدمالتقنيةattachment) {

	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(([]byte)("Reading MBR"))

	var تجزئةبايت [512]byte
	var buffer_2 = تجزئةبايت[:]
	hd.Rقراءة28(0, &buffer_2, 512)

	نفسه.Mbr = Tسجل_الإقلاع_الرئيسي{}
	var i int = 0
	for ; i < 440; i++ {
		نفسه.Mbr.bootloader[i] = تجزئةبايت[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], تجزئةبايت[i:i+4])
	نفسه.Mbr.signature = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], تجزئةبايت[i:i+2])
	نفسه.Mbr.غيرمستخدمة = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], تجزئةبايت[i:i+16])
	نفسه.Mbr.Primaryتجزئة[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], تجزئةبايت[i:i+16])
	نفسه.Mbr.Primaryتجزئة[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], تجزئةبايت[i:i+16])
	نفسه.Mbr.Primaryتجزئة[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], تجزئةبايت[i:i+16])
	نفسه.Mbr.Primaryتجزئة[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], تجزئةبايت[i:i+2])
	نفسه.Mbr.magicnumber = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer6))

	if نفسه.Mbr.magicnumber != 0xAA55 {
		طرفية_2.Mاطبع(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if نفسه.Mbr.Primaryتجزئة[i].Pتجزئةالهوية == 0x00 {
			continue
		}

	}
}
