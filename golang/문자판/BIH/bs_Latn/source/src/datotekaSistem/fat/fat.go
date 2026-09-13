package fat

import . "util"
import . "console"
import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "memorijamanager"

type TBiosparameterblok32 struct {
	jmp			[3]uint8
	softNaziv		[8]byte
	bajtovapersector	uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopiraj		uint8
	korijenDirektorijunos	uint16
	ukupnosectors		uint16
	mediaTip		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	ukupnosectorcount	uint32

	tableVeličina	uint32
	extZastave	uint16
	fatVerzija	uint16
	korijencluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveBroj	uint8
	reserved	uint8
	bootsignature	uint8
	volumeid	uint32
	volumeetiketa	[11]byte
	fatTipetiketa	[8]byte
}

func (self *TBiosparameterblok32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softNaziv[:8], data[3:11])

	self.bajtovapersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatKopiraj = data[16]
	self.korijenDirektorijunos = (uint16(data[17]) | uint16(data[18])<<8)
	self.ukupnosectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaTip = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.ukupnosectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableVeličina = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extZastave = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatVerzija = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.korijencluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveBroj = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.volumeetiketa[:11], data[71:82])
	copy(self.fatTipetiketa[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblok32) Len(hd *TNaprednotechnologyattachment, partunos TPartitiontableunos, imedatoteke []byte) uint32 {

	if partunos.Partitionid == 0x00 {
		return 0
	}

	memorijamanager := TMemorijamanager{}
	bpbpointer := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovafrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partunos.Startlba

	hd.Čitaj28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterblok32{}
	bpb.Init(bpbBajtova)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatVeličina = bpb.tableVeličina

	var datastart = fatstart + fatVeličina*uint32(bpb.fatKopiraj)

	var korijenstart = datastart + uint32(bpb.sectorspercluster)*(bpb.korijencluster-2)

	direntpointer := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovafrompointer(uintptr(direntpointer), 512, 512)
	hd.Čitaj28(korijenstart, &direntBajtova, 512)

	var dirent = [16]TDirektorijunosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naziv[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !EqualBajtova(imedatoteke, dirent[i].naziv[:len(imedatoteke)]) {
			continue
		}

		memorijamanager.Slobodno(bpbpointer)
		memorijamanager.Slobodno(direntpointer)
		return dirent[i].veličina
	}
	memorijamanager.Slobodno(bpbpointer)
	memorijamanager.Slobodno(direntpointer)
	return 0
}
func (self *TBiosparameterblok32) Čitaj(hd *TNaprednotechnologyattachment, partunos TPartitiontableunos, imedatoteke []byte, data []byte) {

	if partunos.Partitionid == 0x00 {
		return
	}

	memorijamanager := TMemorijamanager{}
	bpbpointer := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovafrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partunos.Startlba

	hd.Čitaj28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterblok32{}
	bpb.Init(bpbBajtova)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatVeličina = bpb.tableVeličina

	var datastart = fatstart + fatVeličina*uint32(bpb.fatKopiraj)

	var korijenstart = datastart + uint32(bpb.sectorspercluster)*(bpb.korijencluster-2)

	direntpointer := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovafrompointer(uintptr(direntpointer), 512, 512)
	hd.Čitaj28(korijenstart, &direntBajtova, 512)

	var dirent = [16]TDirektorijunosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naziv[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !EqualBajtova(imedatoteke, dirent[i].naziv[:len(imedatoteke)]) {
			continue
		}

		var firstDatotekacluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Veličina = int32(dirent[i].veličina)
		var sljedećeDatotekacluster = int32(firstDatotekacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Veličina > 0 {
			var datotekasector = datastart + uint32(bpb.sectorspercluster)*uint32(sljedećeDatotekacluster-2)
			var sectoroffset int = 0

			for ; Veličina > 0; Veličina -= 512 {

				var buffer3 []byte

				if dirent[i].veličina > 512 {
					buffer3 = buffer_2[:512]
					hd.Čitaj28(datotekasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].veličina]
					hd.Čitaj28(datotekasector+uint32(sectoroffset), &buffer3, int(dirent[i].veličina))
				}

				copy(data[int32(dirent[i].veličina)-Veličina:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(sljedećeDatotekacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Čitaj28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetPrimljenosectorforcurrentcluster = sljedećeDatotekacluster % 128
			var startoffset = fatoffsetPrimljenosectorforcurrentcluster * 4
			var endoffset = fatoffsetPrimljenosectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			sljedećeDatotekacluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	memorijamanager.Slobodno(bpbpointer)
	memorijamanager.Slobodno(direntpointer)
}

type TDirektorijunosfat32 struct {
	naziv		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cVrijemetenth	uint8
	cVrijeme	uint16
	cdatum		uint16
	aVrijeme	uint16
	firstclusterhi	uint16
	wVrijeme	uint16
	wdatum		uint16
	firstclusterlow	uint16
	veličina	uint32
}

func (self *TDirektorijunosfat32) Init(data [32]byte) {
	copy(self.naziv[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cVrijemetenth = data[13]
	self.cVrijeme = uint16(data[14]) | uint16(data[15])<<8
	self.cdatum = uint16(data[16]) | uint16(data[17])<<8
	self.aVrijeme = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wVrijeme = uint16(data[22]) | uint16(data[23])<<8
	self.wdatum = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.veličina = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
