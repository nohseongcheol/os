package fat

import . "util"
import . "console"
import . "driver/ata"
import . "faylsystem/msdospartition"
import . "yaddaşmanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softAd			[8]byte
	baytpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKöçür		uint8
	rootCərgəentry		uint16
	cəmisectors		uint16
	mediaNöv		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	cəmisectorcount		uint32

	tableBöyüklük	uint32
	extBayraqlar	uint16
	fatversion	uint16
	rootcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	açılışsignature	uint8
	volumeid	uint32
	volumeEtiket	[11]byte
	fatNövEtiket	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softAd[:8], data[3:11])

	self.baytpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatKöçür = data[16]
	self.rootCərgəentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.cəmisectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaNöv = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.cəmisectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableBöyüklük = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extBayraqlar = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.açılışsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.volumeEtiket[:11], data[71:82])
	copy(self.fatNövEtiket[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *TƏtraflıtechnologyattachment, partentry TPartitiontableentry, fayladı []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	yaddaşmanager := TYaddaşmanager{}
	bpbpointer := yaddaşmanager.Malloc(90)
	bpbBayt := GetBaytfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Oxuma28(partitionoffset, &bpbBayt, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBayt)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatBöyüklük = bpb.tableBöyüklük

	var datastart = fatstart + fatBöyüklük*uint32(bpb.fatKöçür)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := yaddaşmanager.Malloc(512)
	direntBayt := GetBaytfrompointer(uintptr(direntpointer), 512, 512)
	hd.Oxuma28(rootstart, &direntBayt, 512)

	var dirent = [16]TCərgəentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ad[0] == 0x00 {
			break
		}

		if dirent[i].böyüklük >= 0xFFFFFFFF {
			continue
		}

		if !EqualBayt(fayladı, dirent[i].ad[:len(fayladı)]) {
			continue
		}

		yaddaşmanager.Boş(bpbpointer)
		yaddaşmanager.Boş(direntpointer)
		return dirent[i].böyüklük
	}
	yaddaşmanager.Boş(bpbpointer)
	yaddaşmanager.Boş(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) Oxuma(hd *TƏtraflıtechnologyattachment, partentry TPartitiontableentry, fayladı []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	yaddaşmanager := TYaddaşmanager{}
	bpbpointer := yaddaşmanager.Malloc(90)
	bpbBayt := GetBaytfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Oxuma28(partitionoffset, &bpbBayt, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBayt)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatBöyüklük = bpb.tableBöyüklük

	var datastart = fatstart + fatBöyüklük*uint32(bpb.fatKöçür)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := yaddaşmanager.Malloc(512)
	direntBayt := GetBaytfrompointer(uintptr(direntpointer), 512, 512)
	hd.Oxuma28(rootstart, &direntBayt, 512)

	var dirent = [16]TCərgəentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ad[0] == 0x00 {
			break
		}

		if dirent[i].böyüklük >= 0xFFFFFFFF {
			continue
		}

		if !EqualBayt(fayladı, dirent[i].ad[:len(fayladı)]) {
			continue
		}

		var firstFaylcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterAlçaq))

		var Böyüklük = int32(dirent[i].böyüklük)
		var sonrakıFaylcluster = int32(firstFaylcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Böyüklük > 0 {
			var faylsector = datastart + uint32(bpb.sectorspercluster)*uint32(sonrakıFaylcluster-2)
			var sectoroffset int = 0

			for ; Böyüklük > 0; Böyüklük -= 512 {

				var buffer3 []byte

				if dirent[i].böyüklük > 512 {
					buffer3 = buffer_2[:512]
					hd.Oxuma28(faylsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].böyüklük]
					hd.Oxuma28(faylsector+uint32(sectoroffset), &buffer3, int(dirent[i].böyüklük))
				}

				copy(data[int32(dirent[i].böyüklük)-Böyüklük:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(sonrakıFaylcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Oxuma28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetinsectorforcurrentcluster = sonrakıFaylcluster % 128
			var startoffset = fatoffsetinsectorforcurrentcluster * 4
			var endoffset = fatoffsetinsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			sonrakıFaylcluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	yaddaşmanager.Boş(bpbpointer)
	yaddaşmanager.Boş(direntpointer)
}

type TCərgəentryfat32 struct {
	ad			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cZamantenth		uint8
	cZaman			uint16
	cTarix			uint16
	aZaman			uint16
	firstclusterhi		uint16
	wZaman			uint16
	wTarix			uint16
	firstclusterAlçaq	uint16
	böyüklük		uint32
}

func (self *TCərgəentryfat32) Init(data [32]byte) {
	copy(self.ad[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cZamantenth = data[13]
	self.cZaman = uint16(data[14]) | uint16(data[15])<<8
	self.cTarix = uint16(data[16]) | uint16(data[17])<<8
	self.aZaman = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wZaman = uint16(data[22]) | uint16(data[23])<<8
	self.wTarix = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterAlçaq = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.böyüklük = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
