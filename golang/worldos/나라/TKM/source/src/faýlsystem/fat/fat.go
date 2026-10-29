/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "faýlsystem/msdospartition"
import . "memorymanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softAd			[8]byte
	baýtlarpersector	uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatNusgala		uint8
	rootdirectoryentry	uint16
	totalsectors		uint16
	mediaHil		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	totalsectorcount	uint32

	tableUlulyk	uint32
	extflags	uint16
	fatversion	uint16
	rootcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	bootsignature	uint8
	volumeid	uint32
	volumelabel	[11]byte
	fatHillabel	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softAd[:8], data[3:11])

	self.baýtlarpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatNusgala = data[16]
	self.rootdirectoryentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaHil = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.totalsectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableUlulyk = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extflags = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.volumelabel[:11], data[71:82])
	copy(self.fatHillabel[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *TAdvancedtechnologyattachment, partentry TPartitiontableentry, faýlady []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbBaýtlar := GetBaýtlarfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Oka28(partitionoffset, &bpbBaýtlar, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBaýtlar)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatUlulyk = bpb.tableUlulyk

	var datastart = fatstart + fatUlulyk*uint32(bpb.fatNusgala)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntBaýtlar := GetBaýtlarfrompointer(uintptr(direntpointer), 512, 512)
	hd.Oka28(rootstart, &direntBaýtlar, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaýtlar[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ad[0] == 0x00 {
			break
		}

		if dirent[i].ululyk >= 0xFFFFFFFF {
			continue
		}

		if !EqualBaýtlar(faýlady, dirent[i].ad[:len(faýlady)]) {
			continue
		}

		memorymanager.Free(bpbpointer)
		memorymanager.Free(direntpointer)
		return dirent[i].ululyk
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) Oka(hd *TAdvancedtechnologyattachment, partentry TPartitiontableentry, faýlady []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbBaýtlar := GetBaýtlarfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Oka28(partitionoffset, &bpbBaýtlar, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBaýtlar)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatUlulyk = bpb.tableUlulyk

	var datastart = fatstart + fatUlulyk*uint32(bpb.fatNusgala)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntBaýtlar := GetBaýtlarfrompointer(uintptr(direntpointer), 512, 512)
	hd.Oka28(rootstart, &direntBaýtlar, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaýtlar[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ad[0] == 0x00 {
			break
		}

		if dirent[i].ululyk >= 0xFFFFFFFF {
			continue
		}

		if !EqualBaýtlar(faýlady, dirent[i].ad[:len(faýlady)]) {
			continue
		}

		var firstFaýlcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Ululyk = int32(dirent[i].ululyk)
		var nextFaýlcluster = int32(firstFaýlcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Ululyk > 0 {
			var faýlsector = datastart + uint32(bpb.sectorspercluster)*uint32(nextFaýlcluster-2)
			var sectoroffset int = 0

			for ; Ululyk > 0; Ululyk -= 512 {

				var buffer3 []byte

				if dirent[i].ululyk > 512 {
					buffer3 = buffer_2[:512]
					hd.Oka28(faýlsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].ululyk]
					hd.Oka28(faýlsector+uint32(sectoroffset), &buffer3, int(dirent[i].ululyk))
				}

				copy(data[int32(dirent[i].ululyk)-Ululyk:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(nextFaýlcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Oka28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetinsectorforcurrentcluster = nextFaýlcluster % 128
			var startoffset = fatoffsetinsectorforcurrentcluster * 4
			var endoffset = fatoffsetinsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			nextFaýlcluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
}

type TDirectoryentryfat32 struct {
	ad		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cZamantenth	uint8
	cZaman		uint16
	cTaryh		uint16
	aZaman		uint16
	firstclusterhi	uint16
	wZaman		uint16
	wTaryh		uint16
	firstclusterlow	uint16
	ululyk		uint32
}

func (self *TDirectoryentryfat32) Init(data [32]byte) {
	copy(self.ad[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cZamantenth = data[13]
	self.cZaman = uint16(data[14]) | uint16(data[15])<<8
	self.cTaryh = uint16(data[16]) | uint16(data[17])<<8
	self.aZaman = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wZaman = uint16(data[22]) | uint16(data[23])<<8
	self.wTaryh = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.ululyk = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
