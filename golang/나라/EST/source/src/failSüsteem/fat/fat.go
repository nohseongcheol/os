package fat

import . "util"
import . "console"
import . "driver/ata"
import . "failSüsteem/msdospartition"
import . "mälumanager"

type TBiosparameterKast32 struct {
	jmp			[3]uint8
	softNimi		[8]byte
	baitipersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopeeri		uint8
	juurKataloogkirje	uint16
	kokkusectors		uint16
	meediumLiik		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	varjatudsectors		uint32
	kokkusectorcount	uint32

	tabelSuurus	uint32
	extLipud	uint16
	fatVersioon	uint16
	juurcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveArv	uint8
	reserved	uint8
	bootsignature	uint8
	valjusid	uint32
	valjusSilt	[11]byte
	fatLiikSilt	[8]byte
}

func (ise *TBiosparameterKast32) Init(data []byte) {
	copy(ise.jmp[:3], data[0:3])
	copy(ise.softNimi[:8], data[3:11])

	ise.baitipersector = (uint16(data[11]) | uint16(data[12])<<8)
	ise.sectorspercluster = data[13]
	ise.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	ise.fatKopeeri = data[16]
	ise.juurKataloogkirje = (uint16(data[17]) | uint16(data[18])<<8)
	ise.kokkusectors = (uint16(data[19]) | uint16(data[20])<<8)
	ise.meediumLiik = data[21]
	ise.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	ise.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	ise.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	ise.varjatudsectors = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	ise.kokkusectorcount = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	ise.tabelSuurus = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	ise.extLipud = (uint16(data[40]) | uint16(data[41])<<8)
	ise.fatVersioon = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	ise.juurcluster = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	ise.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	ise.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(ise.reserved0[:12], data[52:64])

	ise.driveArv = data[64]
	ise.reserved = data[65]
	ise.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	ise.valjusid = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	copy(ise.valjusSilt[:11], data[71:82])
	copy(ise.fatLiikSilt[:8], data[82:90])

}

var console_2 = TConsole{}

func (ise *TBiosparameterKast32) Len(hd *TLaiendatudTehnoloogiaattachment, partkirje TPartitionTabelkirje, failinimi []byte) uint32 {

	if partkirje.Partitionid == 0x00 {
		return 0
	}

	mälumanager := TMälumanager{}
	bpbKursor := mälumanager.Malloc(90)
	bpbbaiti := GetbaitifromKursor(uintptr(bpbKursor), 90, 90)
	var partitionoffset = partkirje.Käivitalba

	hd.Lugemine28(partitionoffset, &bpbbaiti, 90)

	var bpb = TBiosparameterKast32{}
	bpb.Init(bpbbaiti)

	var fatKäivita = partitionoffset + uint32(bpb.reservedsectors)
	var fatSuurus = bpb.tabelSuurus

	var dataKäivita = fatKäivita + fatSuurus*uint32(bpb.fatKopeeri)

	var juurKäivita = dataKäivita + uint32(bpb.sectorspercluster)*(bpb.juurcluster-2)

	direntKursor := mälumanager.Malloc(512)
	direntbaiti := GetbaitifromKursor(uintptr(direntKursor), 512, 512)
	hd.Lugemine28(juurKäivita, &direntbaiti, 512)

	var dirent = [16]TKataloogkirjefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbaiti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nimi[0] == 0x00 {
			break
		}

		if dirent[i].suurus >= 0xFFFFFFFF {
			continue
		}

		if !Võrdnebaiti(failinimi, dirent[i].nimi[:len(failinimi)]) {
			continue
		}

		mälumanager.Vaba(bpbKursor)
		mälumanager.Vaba(direntKursor)
		return dirent[i].suurus
	}
	mälumanager.Vaba(bpbKursor)
	mälumanager.Vaba(direntKursor)
	return 0
}
func (ise *TBiosparameterKast32) Lugemine(hd *TLaiendatudTehnoloogiaattachment, partkirje TPartitionTabelkirje, failinimi []byte, data []byte) {

	if partkirje.Partitionid == 0x00 {
		return
	}

	mälumanager := TMälumanager{}
	bpbKursor := mälumanager.Malloc(90)
	bpbbaiti := GetbaitifromKursor(uintptr(bpbKursor), 90, 90)
	var partitionoffset = partkirje.Käivitalba

	hd.Lugemine28(partitionoffset, &bpbbaiti, 90)

	var bpb = TBiosparameterKast32{}
	bpb.Init(bpbbaiti)

	var fatKäivita = partitionoffset + uint32(bpb.reservedsectors)
	var fatSuurus = bpb.tabelSuurus

	var dataKäivita = fatKäivita + fatSuurus*uint32(bpb.fatKopeeri)

	var juurKäivita = dataKäivita + uint32(bpb.sectorspercluster)*(bpb.juurcluster-2)

	direntKursor := mälumanager.Malloc(512)
	direntbaiti := GetbaitifromKursor(uintptr(direntKursor), 512, 512)
	hd.Lugemine28(juurKäivita, &direntbaiti, 512)

	var dirent = [16]TKataloogkirjefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbaiti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nimi[0] == 0x00 {
			break
		}

		if dirent[i].suurus >= 0xFFFFFFFF {
			continue
		}

		if !Võrdnebaiti(failinimi, dirent[i].nimi[:len(failinimi)]) {
			continue
		}

		var firstFailcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterMadal))

		var Suurus = int32(dirent[i].suurus)
		var järgmineFailcluster = int32(firstFailcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Suurus > 0 {
			var failsector = dataKäivita + uint32(bpb.sectorspercluster)*uint32(järgmineFailcluster-2)
			var sectoroffset int = 0

			for ; Suurus > 0; Suurus -= 512 {

				var buffer3 []byte

				if dirent[i].suurus > 512 {
					buffer3 = buffer_2[:512]
					hd.Lugemine28(failsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].suurus]
					hd.Lugemine28(failsector+uint32(sectoroffset), &buffer3, int(dirent[i].suurus))
				}

				copy(data[int32(dirent[i].suurus)-Suurus:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforKäesolevcluster = uint32(järgmineFailcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lugemine28(fatKäivita+fatsectorforKäesolevcluster, &fatbuf, 512)

			var fatoffsetSissesectorforKäesolevcluster = järgmineFailcluster % 128
			var käivitaoffset = fatoffsetSissesectorforKäesolevcluster * 4
			var lõppoffset = fatoffsetSissesectorforKäesolevcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[käivitaoffset:lõppoffset])

			järgmineFailcluster = int32(Unsignedinteger32r(Massiivtounsignedinteger32(buffer4)))
		}
	}
	mälumanager.Vaba(bpbKursor)
	mälumanager.Vaba(direntKursor)
}

type TKataloogkirjefat32 struct {
	nimi			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cAegtenth		uint8
	cAeg			uint16
	cKuupäev		uint16
	aAeg			uint16
	firstclusterhi		uint16
	wAeg			uint16
	wKuupäev		uint16
	firstclusterMadal	uint16
	suurus			uint32
}

func (ise *TKataloogkirjefat32) Init(data [32]byte) {
	copy(ise.nimi[:8], data[0:8])
	copy(ise.ext[:3], data[8:11])
	ise.attributes = data[11]
	ise.reserved = data[12]
	ise.cAegtenth = data[13]
	ise.cAeg = uint16(data[14]) | uint16(data[15])<<8
	ise.cKuupäev = uint16(data[16]) | uint16(data[17])<<8
	ise.aAeg = uint16(data[18]) | uint16(data[19])<<8
	ise.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	ise.wAeg = uint16(data[22]) | uint16(data[23])<<8
	ise.wKuupäev = uint16(data[24]) | uint16(data[25])<<8
	ise.firstclusterMadal = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	ise.suurus = Unsignedinteger32r(Massiivtounsignedinteger32(buffer))
}
