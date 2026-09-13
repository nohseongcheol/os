package fat

import . "util"
import . "console"
import . "driver/ata"
import . "faylTizim/msdospartition"
import . "xotiramanager"

type TBiosparameterBlok32 struct {
	jmp			[3]uint8
	softNomi		[8]byte
	baytlarpersector	uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatNusxaolish		uint8
	rootJildentry		uint16
	jamisectors		uint16
	mediaTuri		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	jamisectorcount		uint32

	tableHajmi	uint32
	extBayroqlar	uint16
	fatversion	uint16
	rootcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveRAQAM	uint8
	reserved	uint8
	bootsignature	uint8
	ovozid		uint32
	ovozYorliq	[11]byte
	fatTuriYorliq	[8]byte
}

func (self *TBiosparameterBlok32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softNomi[:8], data[3:11])

	self.baytlarpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatNusxaolish = data[16]
	self.rootJildentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.jamisectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaTuri = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.jamisectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableHajmi = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extBayroqlar = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveRAQAM = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.ovozid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.ovozYorliq[:11], data[71:82])
	copy(self.fatTuriYorliq[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterBlok32) Len(hd *TMurakkabTexnologiyaattachment, partentry TPartitiontableentry, faylnomi []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	xotiramanager := TXotiramanager{}
	bpbKorsatgich := xotiramanager.Malloc(90)
	bpbBaytlar := GetBaytlarfromKorsatgich(uintptr(bpbKorsatgich), 90, 90)
	var partitionoffset = partentry.Boshlashlba

	hd.Oʻqish28(partitionoffset, &bpbBaytlar, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBaytlar)

	var fatBoshlash = partitionoffset + uint32(bpb.reservedsectors)
	var fatHajmi = bpb.tableHajmi

	var dataBoshlash = fatBoshlash + fatHajmi*uint32(bpb.fatNusxaolish)

	var rootBoshlash = dataBoshlash + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntKorsatgich := xotiramanager.Malloc(512)
	direntBaytlar := GetBaytlarfromKorsatgich(uintptr(direntKorsatgich), 512, 512)
	hd.Oʻqish28(rootBoshlash, &direntBaytlar, 512)

	var dirent = [16]TJildentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaytlar[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nomi[0] == 0x00 {
			break
		}

		if dirent[i].hajmi >= 0xFFFFFFFF {
			continue
		}

		if !EqualBaytlar(faylnomi, dirent[i].nomi[:len(faylnomi)]) {
			continue
		}

		xotiramanager.Bosh(bpbKorsatgich)
		xotiramanager.Bosh(direntKorsatgich)
		return dirent[i].hajmi
	}
	xotiramanager.Bosh(bpbKorsatgich)
	xotiramanager.Bosh(direntKorsatgich)
	return 0
}
func (self *TBiosparameterBlok32) Oʻqish(hd *TMurakkabTexnologiyaattachment, partentry TPartitiontableentry, faylnomi []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	xotiramanager := TXotiramanager{}
	bpbKorsatgich := xotiramanager.Malloc(90)
	bpbBaytlar := GetBaytlarfromKorsatgich(uintptr(bpbKorsatgich), 90, 90)
	var partitionoffset = partentry.Boshlashlba

	hd.Oʻqish28(partitionoffset, &bpbBaytlar, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBaytlar)

	var fatBoshlash = partitionoffset + uint32(bpb.reservedsectors)
	var fatHajmi = bpb.tableHajmi

	var dataBoshlash = fatBoshlash + fatHajmi*uint32(bpb.fatNusxaolish)

	var rootBoshlash = dataBoshlash + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntKorsatgich := xotiramanager.Malloc(512)
	direntBaytlar := GetBaytlarfromKorsatgich(uintptr(direntKorsatgich), 512, 512)
	hd.Oʻqish28(rootBoshlash, &direntBaytlar, 512)

	var dirent = [16]TJildentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaytlar[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nomi[0] == 0x00 {
			break
		}

		if dirent[i].hajmi >= 0xFFFFFFFF {
			continue
		}

		if !EqualBaytlar(faylnomi, dirent[i].nomi[:len(faylnomi)]) {
			continue
		}

		var firstFaylcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterPast))

		var Hajmi = int32(dirent[i].hajmi)
		var keyingiFaylcluster = int32(firstFaylcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Hajmi > 0 {
			var faylsector = dataBoshlash + uint32(bpb.sectorspercluster)*uint32(keyingiFaylcluster-2)
			var sectoroffset int = 0

			for ; Hajmi > 0; Hajmi -= 512 {

				var buffer3 []byte

				if dirent[i].hajmi > 512 {
					buffer3 = buffer_2[:512]
					hd.Oʻqish28(faylsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].hajmi]
					hd.Oʻqish28(faylsector+uint32(sectoroffset), &buffer3, int(dirent[i].hajmi))
				}

				copy(data[int32(dirent[i].hajmi)-Hajmi:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(keyingiFaylcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Oʻqish28(fatBoshlash+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetYaqinlashtirishsectorforcurrentcluster = keyingiFaylcluster % 128
			var boshlashoffset = fatoffsetYaqinlashtirishsectorforcurrentcluster * 4
			var oxirgaoffset = fatoffsetYaqinlashtirishsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[boshlashoffset:oxirgaoffset])

			keyingiFaylcluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	xotiramanager.Bosh(bpbKorsatgich)
	xotiramanager.Bosh(direntKorsatgich)
}

type TJildentryfat32 struct {
	nomi			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cVaqttenth		uint8
	cVaqt			uint16
	cSana			uint16
	aVaqt			uint16
	firstclusterhi		uint16
	wVaqt			uint16
	wSana			uint16
	firstclusterPast	uint16
	hajmi			uint32
}

func (self *TJildentryfat32) Init(data [32]byte) {
	copy(self.nomi[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cVaqttenth = data[13]
	self.cVaqt = uint16(data[14]) | uint16(data[15])<<8
	self.cSana = uint16(data[16]) | uint16(data[17])<<8
	self.aVaqt = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wVaqt = uint16(data[22]) | uint16(data[23])<<8
	self.wSana = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterPast = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.hajmi = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
