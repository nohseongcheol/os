package fat

import . "util"
import . "console"
import . "driver/ata"
import . "bestandSysteem/msdospartition"
import . "geheugenmanager"

type TBestandssysteemparameters32 struct {
	jmp			[3]uint8
	softNaam		[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	gereserveerdsectors	uint16
	fatKopiëren		uint8
	hoofdmapMapItem		uint16
	totaalsectors		uint16
	mediaSoort		uint8
	fatsectorAantal		uint16
	sectorpertrack		uint16
	headAantal		uint16
	verborgensectors	uint32
	totaalsectorAantal	uint32

	tabelGrootte	uint32
	extVlaggen	uint16
	fatVersie	uint16
	hoofdmapcluster	uint32
	fatInformatie	uint16
	backupsector	uint16
	gereserveerd0	[12]uint8
	driveGetal	uint8
	gereserveerd	uint8
	bootsignature	uint8
	inhoudid	uint32
	inhoudEtiket	[11]byte
	fatSoortEtiket	[8]byte
}

func (zelf *TBestandssysteemparameters32) Init(data []byte) {
	copy(zelf.jmp[:3], data[0:3])
	copy(zelf.softNaam[:8], data[3:11])

	zelf.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	zelf.sectorspercluster = data[13]
	zelf.gereserveerdsectors = (uint16(data[14]) | uint16(data[15])<<8)
	zelf.fatKopiëren = data[16]
	zelf.hoofdmapMapItem = (uint16(data[17]) | uint16(data[18])<<8)
	zelf.totaalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	zelf.mediaSoort = data[21]
	zelf.fatsectorAantal = (uint16(data[22]) | uint16(data[23])<<8)
	zelf.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	zelf.headAantal = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	zelf.verborgensectors = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	zelf.totaalsectorAantal = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	zelf.tabelGrootte = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	zelf.extVlaggen = (uint16(data[40]) | uint16(data[41])<<8)
	zelf.fatVersie = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	zelf.hoofdmapcluster = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	zelf.fatInformatie = (uint16(data[48]) | uint16(data[49])<<8)
	zelf.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(zelf.gereserveerd0[:12], data[52:64])

	zelf.driveGetal = data[64]
	zelf.gereserveerd = data[65]
	zelf.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	zelf.inhoudid = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	copy(zelf.inhoudEtiket[:11], data[71:82])
	copy(zelf.fatSoortEtiket[:8], data[82:90])

}

var console_2 = TConsole{}

func (zelf *TBestandssysteemparameters32) Len(hd *TGeavanceerdTechnologieattachment, partItem TPartitionTabelItem, bestandsnaam []byte) uint32 {

	if partItem.Partitionid == 0x00 {
		return 0
	}

	geheugenmanager := TGeheugenmanager{}
	bpbMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(90)
	bpbbytes := GetbytesvanMuisaanwijzer(uintptr(bpbMuisaanwijzer), 90, 90)
	var partitionVerschuiving = partItem.Startenlba

	hd.Lezen28(partitionVerschuiving, &bpbbytes, 90)

	var bestandssysteemparameters = TBestandssysteemparameters32{}
	bestandssysteemparameters.Init(bpbbytes)

	var fatStarten = partitionVerschuiving + uint32(bestandssysteemparameters.gereserveerdsectors)
	var fatGrootte = bestandssysteemparameters.tabelGrootte

	var dataStarten = fatStarten + fatGrootte*uint32(bestandssysteemparameters.fatKopiëren)

	var hoofdmapStarten = dataStarten + uint32(bestandssysteemparameters.sectorspercluster)*(bestandssysteemparameters.hoofdmapcluster-2)

	direntMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(512)
	direntbytes := GetbytesvanMuisaanwijzer(uintptr(direntMuisaanwijzer), 512, 512)
	hd.Lezen28(hoofdmapStarten, &direntbytes, 512)

	var dirent = [16]TMapItemfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naam[0] == 0x00 {
			break
		}

		if dirent[i].grootte >= 0xFFFFFFFF {
			continue
		}

		if !Gelijkebytes(bestandsnaam, dirent[i].naam[:len(bestandsnaam)]) {
			continue
		}

		geheugenmanager.Vrij(bpbMuisaanwijzer)
		geheugenmanager.Vrij(direntMuisaanwijzer)
		return dirent[i].grootte
	}
	geheugenmanager.Vrij(bpbMuisaanwijzer)
	geheugenmanager.Vrij(direntMuisaanwijzer)
	return 0
}
func (zelf *TBestandssysteemparameters32) Lezen(hd *TGeavanceerdTechnologieattachment, partItem TPartitionTabelItem, bestandsnaam []byte, data []byte) {

	if partItem.Partitionid == 0x00 {
		return
	}

	geheugenmanager := TGeheugenmanager{}
	bpbMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(90)
	bpbbytes := GetbytesvanMuisaanwijzer(uintptr(bpbMuisaanwijzer), 90, 90)
	var partitionVerschuiving = partItem.Startenlba

	hd.Lezen28(partitionVerschuiving, &bpbbytes, 90)

	var bestandssysteemparameters = TBestandssysteemparameters32{}
	bestandssysteemparameters.Init(bpbbytes)

	var fatStarten = partitionVerschuiving + uint32(bestandssysteemparameters.gereserveerdsectors)
	var fatGrootte = bestandssysteemparameters.tabelGrootte

	var dataStarten = fatStarten + fatGrootte*uint32(bestandssysteemparameters.fatKopiëren)

	var hoofdmapStarten = dataStarten + uint32(bestandssysteemparameters.sectorspercluster)*(bestandssysteemparameters.hoofdmapcluster-2)

	direntMuisaanwijzer := geheugenmanager.Geheugen_toewijzen(512)
	direntbytes := GetbytesvanMuisaanwijzer(uintptr(direntMuisaanwijzer), 512, 512)
	hd.Lezen28(hoofdmapStarten, &direntbytes, 512)

	var dirent = [16]TMapItemfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naam[0] == 0x00 {
			break
		}

		if dirent[i].grootte >= 0xFFFFFFFF {
			continue
		}

		if !Gelijkebytes(bestandsnaam, dirent[i].naam[:len(bestandsnaam)]) {
			continue
		}

		var firstBestandcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLaag))

		var Grootte = int32(dirent[i].grootte)
		var volgendeBestandcluster = int32(firstBestandcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Grootte > 0 {
			var bestandsector = dataStarten + uint32(bestandssysteemparameters.sectorspercluster)*uint32(volgendeBestandcluster-2)
			var sectorVerschuiving int = 0

			for ; Grootte > 0; Grootte -= 512 {

				var buffer3 []byte

				if dirent[i].grootte > 512 {
					buffer3 = buffer_2[:512]
					hd.Lezen28(bestandsector+uint32(sectorVerschuiving), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].grootte]
					hd.Lezen28(bestandsector+uint32(sectorVerschuiving), &buffer3, int(dirent[i].grootte))
				}

				copy(data[int32(dirent[i].grootte)-Grootte:], buffer3)

				sectorVerschuiving++

				if sectorVerschuiving > int(bestandssysteemparameters.sectorspercluster) {
					break
				}

			}

			var fatsectorforHuidigcluster = uint32(volgendeBestandcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lezen28(fatStarten+fatsectorforHuidigcluster, &fatbuf, 512)

			var fatVerschuivinginsectorforHuidigcluster = volgendeBestandcluster % 128
			var startenVerschuiving = fatVerschuivinginsectorforHuidigcluster * 4
			var eindVerschuiving = fatVerschuivinginsectorforHuidigcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startenVerschuiving:eindVerschuiving])

			volgendeBestandcluster = int32(Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer4)))
		}
	}
	geheugenmanager.Vrij(bpbMuisaanwijzer)
	geheugenmanager.Vrij(direntMuisaanwijzer)
}

type TMapItemfat32 struct {
	naam			[8]byte
	ext			[3]byte
	attributen		uint8
	gereserveerd		uint8
	cTijdtenth		uint8
	cTijd			uint16
	cDatum			uint16
	aTijd			uint16
	firstclusterhi		uint16
	wTijd			uint16
	wDatum			uint16
	firstclusterLaag	uint16
	grootte			uint32
}

func (zelf *TMapItemfat32) Init(data [32]byte) {
	copy(zelf.naam[:8], data[0:8])
	copy(zelf.ext[:3], data[8:11])
	zelf.attributen = data[11]
	zelf.gereserveerd = data[12]
	zelf.cTijdtenth = data[13]
	zelf.cTijd = uint16(data[14]) | uint16(data[15])<<8
	zelf.cDatum = uint16(data[16]) | uint16(data[17])<<8
	zelf.aTijd = uint16(data[18]) | uint16(data[19])<<8
	zelf.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	zelf.wTijd = uint16(data[22]) | uint16(data[23])<<8
	zelf.wDatum = uint16(data[24]) | uint16(data[25])<<8
	zelf.firstclusterLaag = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	zelf.grootte = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer))
}
