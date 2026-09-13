package fat

import . "util"
import . "console"
import . "driver/ata"
import . "fileระบบ/msdospartition"
import . "memorymanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softname		[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatcopy			uint8
	รากdirectoryentry	uint16
	รวมsectors		uint16
	mediaประเภท		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	รวมsectorcount		uint32

	ตารางขนาด	uint32
	extflags	uint16
	fatversion	uint16
	รากcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	bootsignature	uint8
	volumeid	uint32
	volumeฉลาก	[11]byte
	fatประเภทฉลาก	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softname[:8], data[3:11])

	self.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatcopy = data[16]
	self.รากdirectoryentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.รวมsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaประเภท = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.รวมsectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.ตารางขนาด = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extflags = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.รากcluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.volumeฉลาก[:11], data[71:82])
	copy(self.fatประเภทฉลาก[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *TAdvancedtechnologyattachment, partentry TPartitionตารางentry, filename []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbbytes := Getbytesfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.An28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatขนาด = bpb.ตารางขนาด

	var datastart = fatstart + fatขนาด*uint32(bpb.fatcopy)

	var รากstart = datastart + uint32(bpb.sectorspercluster)*(bpb.รากcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntbytes := Getbytesfrompointer(uintptr(direntpointer), 512, 512)
	hd.An28(รากstart, &direntbytes, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].name[0] == 0x00 {
			break
		}

		if dirent[i].ขนาด >= 0xFFFFFFFF {
			continue
		}

		if !Equalbytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}

		memorymanager.Free(bpbpointer)
		memorymanager.Free(direntpointer)
		return dirent[i].ขนาด
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) An(hd *TAdvancedtechnologyattachment, partentry TPartitionตารางentry, filename []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbbytes := Getbytesfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.An28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatขนาด = bpb.ตารางขนาด

	var datastart = fatstart + fatขนาด*uint32(bpb.fatcopy)

	var รากstart = datastart + uint32(bpb.sectorspercluster)*(bpb.รากcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntbytes := Getbytesfrompointer(uintptr(direntpointer), 512, 512)
	hd.An28(รากstart, &direntbytes, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].name[0] == 0x00 {
			break
		}

		if dirent[i].ขนาด >= 0xFFFFFFFF {
			continue
		}

		if !Equalbytes(filename, dirent[i].name[:len(filename)]) {
			continue
		}

		var firstfilecluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Sขนาด = int32(dirent[i].ขนาด)
		var nextfilecluster = int32(firstfilecluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sขนาด > 0 {
			var filesector = datastart + uint32(bpb.sectorspercluster)*uint32(nextfilecluster-2)
			var sectoroffset int = 0

			for ; Sขนาด > 0; Sขนาด -= 512 {

				var buffer3 []byte

				if dirent[i].ขนาด > 512 {
					buffer3 = buffer_2[:512]
					hd.An28(filesector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].ขนาด]
					hd.An28(filesector+uint32(sectoroffset), &buffer3, int(dirent[i].ขนาด))
				}

				copy(data[int32(dirent[i].ขนาด)-Sขนาด:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(nextfilecluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.An28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetขยายsectorforcurrentcluster = nextfilecluster % 128
			var startoffset = fatoffsetขยายsectorforcurrentcluster * 4
			var endoffset = fatoffsetขยายsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			nextfilecluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
}

type TDirectoryentryfat32 struct {
	name		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cเวลาtenth	uint8
	cเวลา		uint16
	cdate		uint16
	aเวลา		uint16
	firstclusterhi	uint16
	wเวลา		uint16
	wdate		uint16
	firstclusterlow	uint16
	ขนาด		uint32
}

func (self *TDirectoryentryfat32) Init(data [32]byte) {
	copy(self.name[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cเวลาtenth = data[13]
	self.cเวลา = uint16(data[14]) | uint16(data[15])<<8
	self.cdate = uint16(data[16]) | uint16(data[17])<<8
	self.aเวลา = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wเวลา = uint16(data[22]) | uint16(data[23])<<8
	self.wdate = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.ขนาด = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
