package fat

import . "util"
import . "console"
import . "driver/ata"
import . "fílasystem/msdospartition"
import . "memorymanager"

type TBiosparameterBlokkur32 struct {
	jmp			[3]uint8
	softNavn		[8]byte
	býtpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatcopy			uint8
	rootFíluskráentry	uint16
	totalsectors		uint16
	mediatype		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	totalsectorcount	uint32

	tableStødd		uint32
	extflags		uint16
	fatversion		uint16
	rootcluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	drivenumber		uint8
	reserved		uint8
	bootsignature		uint8
	ljóðstyrkiid		uint32
	ljóðstyrkiSpjaldur	[11]byte
	fattypeSpjaldur		[8]byte
}

func (self *TBiosparameterBlokkur32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softNavn[:8], data[3:11])

	self.býtpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatcopy = data[16]
	self.rootFíluskráentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediatype = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.totalsectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableStødd = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

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
	self.ljóðstyrkiid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.ljóðstyrkiSpjaldur[:11], data[71:82])
	copy(self.fattypeSpjaldur[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterBlokkur32) Len(hd *TFramkomiðtechnologyattachment, partentry TPartitiontableentry, filename []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbbýt := Getbýtfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Lesa28(partitionoffset, &bpbbýt, 90)

	var bpb = TBiosparameterBlokkur32{}
	bpb.Init(bpbbýt)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatStødd = bpb.tableStødd

	var datastart = fatstart + fatStødd*uint32(bpb.fatcopy)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntbýt := Getbýtfrompointer(uintptr(direntpointer), 512, 512)
	hd.Lesa28(rootstart, &direntbýt, 512)

	var dirent = [16]TFíluskráentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbýt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].stødd >= 0xFFFFFFFF {
			continue
		}

		if !Equalbýt(filename, dirent[i].navn[:len(filename)]) {
			continue
		}

		memorymanager.Free(bpbpointer)
		memorymanager.Free(direntpointer)
		return dirent[i].stødd
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
	return 0
}
func (self *TBiosparameterBlokkur32) Lesa(hd *TFramkomiðtechnologyattachment, partentry TPartitiontableentry, filename []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	memorymanager := TMemorymanager{}
	bpbpointer := memorymanager.Malloc(90)
	bpbbýt := Getbýtfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Lesa28(partitionoffset, &bpbbýt, 90)

	var bpb = TBiosparameterBlokkur32{}
	bpb.Init(bpbbýt)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatStødd = bpb.tableStødd

	var datastart = fatstart + fatStødd*uint32(bpb.fatcopy)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := memorymanager.Malloc(512)
	direntbýt := Getbýtfrompointer(uintptr(direntpointer), 512, 512)
	hd.Lesa28(rootstart, &direntbýt, 512)

	var dirent = [16]TFíluskráentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbýt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].stødd >= 0xFFFFFFFF {
			continue
		}

		if !Equalbýt(filename, dirent[i].navn[:len(filename)]) {
			continue
		}

		var firstFílacluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLágur))

		var Stødd = int32(dirent[i].stødd)
		var næstaFílacluster = int32(firstFílacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Stødd > 0 {
			var fílasector = datastart + uint32(bpb.sectorspercluster)*uint32(næstaFílacluster-2)
			var sectoroffset int = 0

			for ; Stødd > 0; Stødd -= 512 {

				var buffer3 []byte

				if dirent[i].stødd > 512 {
					buffer3 = buffer_2[:512]
					hd.Lesa28(fílasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].stødd]
					hd.Lesa28(fílasector+uint32(sectoroffset), &buffer3, int(dirent[i].stødd))
				}

				copy(data[int32(dirent[i].stødd)-Stødd:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(næstaFílacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lesa28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetinsectorforcurrentcluster = næstaFílacluster % 128
			var startoffset = fatoffsetinsectorforcurrentcluster * 4
			var endoffset = fatoffsetinsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			næstaFílacluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	memorymanager.Free(bpbpointer)
	memorymanager.Free(direntpointer)
}

type TFíluskráentryfat32 struct {
	navn			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	ctimetenth		uint8
	ctime			uint16
	cdate			uint16
	atime			uint16
	firstclusterhi		uint16
	wtime			uint16
	wdate			uint16
	firstclusterLágur	uint16
	stødd			uint32
}

func (self *TFíluskráentryfat32) Init(data [32]byte) {
	copy(self.navn[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.ctimetenth = data[13]
	self.ctime = uint16(data[14]) | uint16(data[15])<<8
	self.cdate = uint16(data[16]) | uint16(data[17])<<8
	self.atime = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wtime = uint16(data[22]) | uint16(data[23])<<8
	self.wdate = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterLágur = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.stødd = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
