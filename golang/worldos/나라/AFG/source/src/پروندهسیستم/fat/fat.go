/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "پروندهسیستم/msdospartition"
import . "حافظهmanager"

type TBiosparameterقطعه32 struct {
	jmp			[3]uint8
	softنام			[8]byte
	بایتpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatکپی			uint8
	ریشهشاخهentry		uint16
	totalsectors		uint16
	mediaنوع		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	totalsectorcount	uint32

	جدولاندازه	uint32
	extflags	uint16
	fatversion	uint16
	ریشهcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	bootsignature	uint8
	حجمشناسه	uint32
	حجمبرچسب	[11]byte
	fatنوعبرچسب	[8]byte
}

func (خود *TBiosparameterقطعه32) Init(data []byte) {
	copy(خود.jmp[:3], data[0:3])
	copy(خود.softنام[:8], data[3:11])

	خود.بایتpersector = (uint16(data[11]) | uint16(data[12])<<8)
	خود.sectorspercluster = data[13]
	خود.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	خود.fatکپی = data[16]
	خود.ریشهشاخهentry = (uint16(data[17]) | uint16(data[18])<<8)
	خود.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	خود.mediaنوع = data[21]
	خود.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	خود.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	خود.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	خود.hiddensectors = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	خود.totalsectorcount = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	خود.جدولاندازه = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	خود.extflags = (uint16(data[40]) | uint16(data[41])<<8)
	خود.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	خود.ریشهcluster = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	خود.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	خود.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(خود.reserved0[:12], data[52:64])

	خود.drivenumber = data[64]
	خود.reserved = data[65]
	خود.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	خود.حجمشناسه = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	copy(خود.حجمبرچسب[:11], data[71:82])
	copy(خود.fatنوعبرچسب[:8], data[82:90])

}

var console_2 = TConsole{}

func (خود *TBiosparameterقطعه32) Len(hd *Tپیشرفتهtechnologyattachment, partentry TPartitionجدولentry, نامپرونده []byte) uint32 {

	if partentry.Partitionشناسه == 0x00 {
		return 0
	}

	حافظهmanager := Tحافظهmanager{}
	bpbpointer := حافظهmanager.Malloc(90)
	bpbبایت := Getبایتfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Rخواندن28(partitionoffset, &bpbبایت, 90)

	var bpb = TBiosparameterقطعه32{}
	bpb.Init(bpbبایت)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatاندازه = bpb.جدولاندازه

	var datastart = fatstart + fatاندازه*uint32(bpb.fatکپی)

	var ریشهstart = datastart + uint32(bpb.sectorspercluster)*(bpb.ریشهcluster-2)

	direntpointer := حافظهmanager.Malloc(512)
	direntبایت := Getبایتfrompointer(uintptr(direntpointer), 512, 512)
	hd.Rخواندن28(ریشهstart, &direntبایت, 512)

	var dirent = [16]Tشاخهentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبایت[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].نام[0] == 0x00 {
			break
		}

		if dirent[i].اندازه >= 0xFFFFFFFF {
			continue
		}

		if !Equalبایت(نامپرونده, dirent[i].نام[:len(نامپرونده)]) {
			continue
		}

		حافظهmanager.Fآزاد(bpbpointer)
		حافظهmanager.Fآزاد(direntpointer)
		return dirent[i].اندازه
	}
	حافظهmanager.Fآزاد(bpbpointer)
	حافظهmanager.Fآزاد(direntpointer)
	return 0
}
func (خود *TBiosparameterقطعه32) Rخواندن(hd *Tپیشرفتهtechnologyattachment, partentry TPartitionجدولentry, نامپرونده []byte, data []byte) {

	if partentry.Partitionشناسه == 0x00 {
		return
	}

	حافظهmanager := Tحافظهmanager{}
	bpbpointer := حافظهmanager.Malloc(90)
	bpbبایت := Getبایتfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Rخواندن28(partitionoffset, &bpbبایت, 90)

	var bpb = TBiosparameterقطعه32{}
	bpb.Init(bpbبایت)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatاندازه = bpb.جدولاندازه

	var datastart = fatstart + fatاندازه*uint32(bpb.fatکپی)

	var ریشهstart = datastart + uint32(bpb.sectorspercluster)*(bpb.ریشهcluster-2)

	direntpointer := حافظهmanager.Malloc(512)
	direntبایت := Getبایتfrompointer(uintptr(direntpointer), 512, 512)
	hd.Rخواندن28(ریشهstart, &direntبایت, 512)

	var dirent = [16]Tشاخهentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبایت[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].نام[0] == 0x00 {
			break
		}

		if dirent[i].اندازه >= 0xFFFFFFFF {
			continue
		}

		if !Equalبایت(نامپرونده, dirent[i].نام[:len(نامپرونده)]) {
			continue
		}

		var firstپروندهcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterاندک))

		var Sاندازه = int32(dirent[i].اندازه)
		var بعدیپروندهcluster = int32(firstپروندهcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sاندازه > 0 {
			var پروندهsector = datastart + uint32(bpb.sectorspercluster)*uint32(بعدیپروندهcluster-2)
			var sectoroffset int = 0

			for ; Sاندازه > 0; Sاندازه -= 512 {

				var buffer3 []byte

				if dirent[i].اندازه > 512 {
					buffer3 = buffer_2[:512]
					hd.Rخواندن28(پروندهsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].اندازه]
					hd.Rخواندن28(پروندهsector+uint32(sectoroffset), &buffer3, int(dirent[i].اندازه))
				}

				copy(data[int32(dirent[i].اندازه)-Sاندازه:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(بعدیپروندهcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rخواندن28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetداخلsectorforcurrentcluster = بعدیپروندهcluster % 128
			var startoffset = fatoffsetداخلsectorforcurrentcluster * 4
			var پایانoffset = fatoffsetداخلsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:پایانoffset])

			بعدیپروندهcluster = int32(Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer4)))
		}
	}
	حافظهmanager.Fآزاد(bpbpointer)
	حافظهmanager.Fآزاد(direntpointer)
}

type Tشاخهentryfat32 struct {
	نام			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cزمانtenth		uint8
	cزمان			uint16
	cتاریخ			uint16
	aزمان			uint16
	firstclusterhi		uint16
	wزمان			uint16
	wتاریخ			uint16
	firstclusterاندک	uint16
	اندازه			uint32
}

func (خود *Tشاخهentryfat32) Init(data [32]byte) {
	copy(خود.نام[:8], data[0:8])
	copy(خود.ext[:3], data[8:11])
	خود.attributes = data[11]
	خود.reserved = data[12]
	خود.cزمانtenth = data[13]
	خود.cزمان = uint16(data[14]) | uint16(data[15])<<8
	خود.cتاریخ = uint16(data[16]) | uint16(data[17])<<8
	خود.aزمان = uint16(data[18]) | uint16(data[19])<<8
	خود.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	خود.wزمان = uint16(data[22]) | uint16(data[23])<<8
	خود.wتاریخ = uint16(data[24]) | uint16(data[25])<<8
	خود.firstclusterاندک = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	خود.اندازه = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer))
}
