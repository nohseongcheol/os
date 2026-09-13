package fat

import . "util"
import . "console"
import . "driver/ata"
import . "filesystem/msdospartition"
import . "මතකයmanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softනම			[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatcopy			uint8
	rootdirectoryentry	uint16
	totalsectors		uint16
	mediatype		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	totalsectorcount	uint32

	tablesize	uint32
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
	fattypelabel	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softනම[:8], data[3:11])

	self.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatcopy = data[16]
	self.rootdirectoryentry = (uint16(data[17]) | uint16(data[18])<<8)
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
	self.tablesize = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

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
	copy(self.fattypelabel[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *TAdvancedtechnologyattachment, partentry TPartitiontableentry, filename []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	මතකයmanager := Tමතකයmanager{}
	bpbpointer := මතකයmanager.Malloc(90)
	bpbbytes := Getbytesfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Kiyavima28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatsize = bpb.tablesize

	var datastart = fatstart + fatsize*uint32(bpb.fatcopy)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := මතකයmanager.Malloc(512)
	direntbytes := Getbytesfrompointer(uintptr(direntpointer), 512, 512)
	hd.Kiyavima28(rootstart, &direntbytes, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].නම[0] == 0x00 {
			break
		}

		if dirent[i].size >= 0xFFFFFFFF {
			continue
		}

		if !Equalbytes(filename, dirent[i].නම[:len(filename)]) {
			continue
		}

		මතකයmanager.Free(bpbpointer)
		මතකයmanager.Free(direntpointer)
		return dirent[i].size
	}
	මතකයmanager.Free(bpbpointer)
	මතකයmanager.Free(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) Kiyavima(hd *TAdvancedtechnologyattachment, partentry TPartitiontableentry, filename []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	මතකයmanager := Tමතකයmanager{}
	bpbpointer := මතකයmanager.Malloc(90)
	bpbbytes := Getbytesfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Kiyavima28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatsize = bpb.tablesize

	var datastart = fatstart + fatsize*uint32(bpb.fatcopy)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := මතකයmanager.Malloc(512)
	direntbytes := Getbytesfrompointer(uintptr(direntpointer), 512, 512)
	hd.Kiyavima28(rootstart, &direntbytes, 512)

	var dirent = [16]TDirectoryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].නම[0] == 0x00 {
			break
		}

		if dirent[i].size >= 0xFFFFFFFF {
			continue
		}

		if !Equalbytes(filename, dirent[i].නම[:len(filename)]) {
			continue
		}

		var firstfilecluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Size = int32(dirent[i].size)
		var ඊලඟfilecluster = int32(firstfilecluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Size > 0 {
			var filesector = datastart + uint32(bpb.sectorspercluster)*uint32(ඊලඟfilecluster-2)
			var sectoroffset int = 0

			for ; Size > 0; Size -= 512 {

				var buffer3 []byte

				if dirent[i].size > 512 {
					buffer3 = buffer_2[:512]
					hd.Kiyavima28(filesector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].size]
					hd.Kiyavima28(filesector+uint32(sectoroffset), &buffer3, int(dirent[i].size))
				}

				copy(data[int32(dirent[i].size)-Size:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(ඊලඟfilecluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Kiyavima28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetinsectorforcurrentcluster = ඊලඟfilecluster % 128
			var startoffset = fatoffsetinsectorforcurrentcluster * 4
			var endoffset = fatoffsetinsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			ඊලඟfilecluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	මතකයmanager.Free(bpbpointer)
	මතකයmanager.Free(direntpointer)
}

type TDirectoryentryfat32 struct {
	නම		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	ctimetenth	uint8
	ctime		uint16
	cdate		uint16
	atime		uint16
	firstclusterhi	uint16
	wtime		uint16
	wdate		uint16
	firstclusterlow	uint16
	size		uint32
}

func (self *TDirectoryentryfat32) Init(data [32]byte) {
	copy(self.නම[:8], data[0:8])
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
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.size = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
