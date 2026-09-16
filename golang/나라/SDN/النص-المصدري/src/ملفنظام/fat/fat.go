/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "أداة"
import . "طرفية"
import . "مشغل/ata"
import . "ملفنظام/msdosتجزئة"
import . "ذاكرةمدير"

type Tمعلمات_نظام_الملفات32 struct {
	jmp			[3]uint8
	softالاسم		[8]byte
	بايتpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatنسخ			uint8
	الجذردليلentry		uint16
	المجموعsectors		uint16
	وسائطنوع		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	مخفيsectors		uint32
	المجموعsectorcount	uint32

	جدولالحجم	uint32
	extخيارات	uint16
	fatإصدار	uint16
	الجذرcluster	uint32
	fatمعلومات	uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveالأرقام	uint8
	reserved	uint8
	bootsignature	uint8
	الحجمالهوية	uint32
	الحجمتسمية	[11]byte
	fatنوعتسمية	[8]byte
}

func (نفسه *Tمعلمات_نظام_الملفات32) Init(بيانات []byte) {
	copy(نفسه.jmp[:3], بيانات[0:3])
	copy(نفسه.softالاسم[:8], بيانات[3:11])

	نفسه.بايتpersector = (uint16(بيانات[11]) | uint16(بيانات[12])<<8)
	نفسه.sectorspercluster = بيانات[13]
	نفسه.reservedsectors = (uint16(بيانات[14]) | uint16(بيانات[15])<<8)
	نفسه.fatنسخ = بيانات[16]
	نفسه.الجذردليلentry = (uint16(بيانات[17]) | uint16(بيانات[18])<<8)
	نفسه.المجموعsectors = (uint16(بيانات[19]) | uint16(بيانات[20])<<8)
	نفسه.وسائطنوع = بيانات[21]
	نفسه.fatsectorcount = (uint16(بيانات[22]) | uint16(بيانات[23])<<8)
	نفسه.sectorpertrack = (uint16(بيانات[24]) | uint16(بيانات[25])<<8)
	نفسه.headcount = (uint16(بيانات[26]) | uint16(بيانات[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], بيانات[28:32])
	نفسه.مخفيsectors = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	copy(buffer1[:4], بيانات[32:36])
	نفسه.المجموعsectorcount = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	copy(buffer1[:4], بيانات[36:40])
	نفسه.جدولالحجم = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	نفسه.extخيارات = (uint16(بيانات[40]) | uint16(بيانات[41])<<8)
	نفسه.fatإصدار = (uint16(بيانات[42]) | uint16(بيانات[43])<<8)

	copy(buffer1[:4], بيانات[44:48])
	نفسه.الجذرcluster = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	نفسه.fatمعلومات = (uint16(بيانات[48]) | uint16(بيانات[49])<<8)
	نفسه.backupsector = (uint16(بيانات[50]) | uint16(بيانات[51])<<8)

	copy(نفسه.reserved0[:12], بيانات[52:64])

	نفسه.driveالأرقام = بيانات[64]
	نفسه.reserved = بيانات[65]
	نفسه.bootsignature = بيانات[66]

	copy(buffer1[:4], بيانات[67:71])
	نفسه.الحجمالهوية = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer1))

	copy(نفسه.الحجمتسمية[:11], بيانات[71:82])
	copy(نفسه.fatنوعتسمية[:8], بيانات[82:90])

}

var طرفية_2 = Tطرفية{}

func (نفسه *Tمعلمات_نظام_الملفات32) Len(hd *Tمتقدمالتقنيةattachment, partentry Tتجزئةجدولentry, اسمالملف []byte) uint32 {

	if partentry.Pتجزئةالهوية == 0x00 {
		return 0
	}

	ذاكرةمدير := Tذاكرةمدير{}
	bpbالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(90)
	bpbبايت := Getبايتfromالمؤشر(uintptr(bpbالمؤشر), 90, 90)
	var تجزئةoffset = partentry.Sابدأlba

	hd.Rقراءة28(تجزئةoffset, &bpbبايت, 90)

	var معلمات_نظام_الملفات = Tمعلمات_نظام_الملفات32{}
	معلمات_نظام_الملفات.Init(bpbبايت)

	var fatابدأ = تجزئةoffset + uint32(معلمات_نظام_الملفات.reservedsectors)
	var fatالحجم = معلمات_نظام_الملفات.جدولالحجم

	var بياناتابدأ = fatابدأ + fatالحجم*uint32(معلمات_نظام_الملفات.fatنسخ)

	var الجذرابدأ = بياناتابدأ + uint32(معلمات_نظام_الملفات.sectorspercluster)*(معلمات_نظام_الملفات.الجذرcluster-2)

	direntالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(512)
	direntبايت := Getبايتfromالمؤشر(uintptr(direntالمؤشر), 512, 512)
	hd.Rقراءة28(الجذرابدأ, &direntبايت, 512)

	var dirent = [16]Tدليلentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبايت[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].الاسم[0] == 0x00 {
			break
		}

		if dirent[i].الحجم >= 0xFFFFFFFF {
			continue
		}

		if !Eمساويبايت(اسمالملف, dirent[i].الاسم[:len(اسمالملف)]) {
			continue
		}

		ذاكرةمدير.Fخالي(bpbالمؤشر)
		ذاكرةمدير.Fخالي(direntالمؤشر)
		return dirent[i].الحجم
	}
	ذاكرةمدير.Fخالي(bpbالمؤشر)
	ذاكرةمدير.Fخالي(direntالمؤشر)
	return 0
}
func (نفسه *Tمعلمات_نظام_الملفات32) Rقراءة(hd *Tمتقدمالتقنيةattachment, partentry Tتجزئةجدولentry, اسمالملف []byte, بيانات []byte) {

	if partentry.Pتجزئةالهوية == 0x00 {
		return
	}

	ذاكرةمدير := Tذاكرةمدير{}
	bpbالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(90)
	bpbبايت := Getبايتfromالمؤشر(uintptr(bpbالمؤشر), 90, 90)
	var تجزئةoffset = partentry.Sابدأlba

	hd.Rقراءة28(تجزئةoffset, &bpbبايت, 90)

	var معلمات_نظام_الملفات = Tمعلمات_نظام_الملفات32{}
	معلمات_نظام_الملفات.Init(bpbبايت)

	var fatابدأ = تجزئةoffset + uint32(معلمات_نظام_الملفات.reservedsectors)
	var fatالحجم = معلمات_نظام_الملفات.جدولالحجم

	var بياناتابدأ = fatابدأ + fatالحجم*uint32(معلمات_نظام_الملفات.fatنسخ)

	var الجذرابدأ = بياناتابدأ + uint32(معلمات_نظام_الملفات.sectorspercluster)*(معلمات_نظام_الملفات.الجذرcluster-2)

	direntالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(512)
	direntبايت := Getبايتfromالمؤشر(uintptr(direntالمؤشر), 512, 512)
	hd.Rقراءة28(الجذرابدأ, &direntبايت, 512)

	var dirent = [16]Tدليلentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبايت[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].الاسم[0] == 0x00 {
			break
		}

		if dirent[i].الحجم >= 0xFFFFFFFF {
			continue
		}

		if !Eمساويبايت(اسمالملف, dirent[i].الاسم[:len(اسمالملف)]) {
			continue
		}

		var firstملفcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterمنخفض))

		var Sالحجم = int32(dirent[i].الحجم)
		var التاليملفcluster = int32(firstملفcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sالحجم > 0 {
			var ملفsector = بياناتابدأ + uint32(معلمات_نظام_الملفات.sectorspercluster)*uint32(التاليملفcluster-2)
			var sectoroffset int = 0

			for ; Sالحجم > 0; Sالحجم -= 512 {

				var buffer3 []byte

				if dirent[i].الحجم > 512 {
					buffer3 = buffer_2[:512]
					hd.Rقراءة28(ملفsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].الحجم]
					hd.Rقراءة28(ملفsector+uint32(sectoroffset), &buffer3, int(dirent[i].الحجم))
				}

				copy(بيانات[int32(dirent[i].الحجم)-Sالحجم:], buffer3)

				sectoroffset++

				if sectoroffset > int(معلمات_نظام_الملفات.sectorspercluster) {
					break
				}

			}

			var fatsectorforالحاليcluster = uint32(التاليملفcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rقراءة28(fatابدأ+fatsectorforالحاليcluster, &fatbuf, 512)

			var fatoffsetداخلsectorforالحاليcluster = التاليملفcluster % 128
			var ابدأoffset = fatoffsetداخلsectorforالحاليcluster * 4
			var نهايةoffset = fatoffsetداخلsectorforالحاليcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[ابدأoffset:نهايةoffset])

			التاليملفcluster = int32(Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer4)))
		}
	}
	ذاكرةمدير.Fخالي(bpbالمؤشر)
	ذاكرةمدير.Fخالي(direntالمؤشر)
}

type Tدليلentryfat32 struct {
	الاسم			[8]byte
	ext			[3]byte
	سمات			uint8
	reserved		uint8
	cالوقتtenth		uint8
	cالوقت			uint16
	cالتاريخ		uint16
	aالوقت			uint16
	firstclusterhi		uint16
	wالوقت			uint16
	wالتاريخ		uint16
	firstclusterمنخفض	uint16
	الحجم			uint32
}

func (نفسه *Tدليلentryfat32) Init(بيانات [32]byte) {
	copy(نفسه.الاسم[:8], بيانات[0:8])
	copy(نفسه.ext[:3], بيانات[8:11])
	نفسه.سمات = بيانات[11]
	نفسه.reserved = بيانات[12]
	نفسه.cالوقتtenth = بيانات[13]
	نفسه.cالوقت = uint16(بيانات[14]) | uint16(بيانات[15])<<8
	نفسه.cالتاريخ = uint16(بيانات[16]) | uint16(بيانات[17])<<8
	نفسه.aالوقت = uint16(بيانات[18]) | uint16(بيانات[19])<<8
	نفسه.firstclusterhi = uint16(بيانات[20]) | uint16(بيانات[21])<<8
	نفسه.wالوقت = uint16(بيانات[22]) | uint16(بيانات[23])<<8
	نفسه.wالتاريخ = uint16(بيانات[24]) | uint16(بيانات[25])<<8
	نفسه.firstclusterمنخفض = uint16(بيانات[26]) | uint16(بيانات[27])<<8

	var buffer [4]byte
	copy(buffer[:4], بيانات[28:32])
	نفسه.الحجم = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer))
}
