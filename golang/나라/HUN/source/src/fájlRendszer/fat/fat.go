package fat

import . "util"
import . "konzol"
import . "driver/ata"
import . "fájlRendszer/msdospartition"
import . "memóriamanager"

type TBiosparameterBlokk32 struct {
	jmp				[3]uint8
	softNév				[8]byte
	bájtpersector			uint16
	sectorspercluster		uint8
	fenntartvasectors		uint16
	fatMásolás			uint8
	gyökérmappaKönyvtárbejegyzés	uint16
	összesensectors			uint16
	adathordozóTípus		uint8
	fatsectorSzámláló		uint16
	sectorpertrack			uint16
	headSzámláló			uint16
	rejtettsectors			uint32
	összesensectorSzámláló		uint32

	táblázatMéret		uint32
	extFlagek		uint16
	fatVerzió		uint16
	gyökérmappacluster	uint32
	fatInfó			uint16
	backupsector		uint16
	fenntartva0		[12]uint8
	driveSzám		uint8
	fenntartva		uint8
	bootsignature		uint8
	hangerőAzonosító	uint32
	hangerőcímke		[11]byte
	fatTípuscímke		[8]byte
}

func (self *TBiosparameterBlokk32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softNév[:8], data[3:11])

	self.bájtpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.fenntartvasectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatMásolás = data[16]
	self.gyökérmappaKönyvtárbejegyzés = (uint16(data[17]) | uint16(data[18])<<8)
	self.összesensectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.adathordozóTípus = data[21]
	self.fatsectorSzámláló = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headSzámláló = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.rejtettsectors = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.összesensectorSzámláló = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.táblázatMéret = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	self.extFlagek = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatVerzió = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.gyökérmappacluster = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	self.fatInfó = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.fenntartva0[:12], data[52:64])

	self.driveSzám = data[64]
	self.fenntartva = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.hangerőAzonosító = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	copy(self.hangerőcímke[:11], data[71:82])
	copy(self.fatTípuscímke[:8], data[82:90])

}

var konzol_2 = TKonzol{}

func (self *TBiosparameterBlokk32) Len(hd *THaladóTechnológiaattachment, partbejegyzés TPartitionTáblázatbejegyzés, fájlnév []byte) uint32 {

	if partbejegyzés.PartitionAzonosító == 0x00 {
		return 0
	}

	memóriamanager := TMemóriamanager{}
	bpbMutató := memóriamanager.Malloc(90)
	bpbBájt := GetBájtfromMutató(uintptr(bpbMutató), 90, 90)
	var partitionEltolás = partbejegyzés.Indításlba

	hd.Olvasás28(partitionEltolás, &bpbBájt, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbBájt)

	var fatIndítás = partitionEltolás + uint32(bpb.fenntartvasectors)
	var fatMéret = bpb.táblázatMéret

	var dataIndítás = fatIndítás + fatMéret*uint32(bpb.fatMásolás)

	var gyökérmappaIndítás = dataIndítás + uint32(bpb.sectorspercluster)*(bpb.gyökérmappacluster-2)

	direntMutató := memóriamanager.Malloc(512)
	direntBájt := GetBájtfromMutató(uintptr(direntMutató), 512, 512)
	hd.Olvasás28(gyökérmappaIndítás, &direntBájt, 512)

	var dirent = [16]TKönyvtárbejegyzésfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBájt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].név[0] == 0x00 {
			break
		}

		if dirent[i].méret >= 0xFFFFFFFF {
			continue
		}

		if !EgyenlőBájt(fájlnév, dirent[i].név[:len(fájlnév)]) {
			continue
		}

		memóriamanager.Szabad(bpbMutató)
		memóriamanager.Szabad(direntMutató)
		return dirent[i].méret
	}
	memóriamanager.Szabad(bpbMutató)
	memóriamanager.Szabad(direntMutató)
	return 0
}
func (self *TBiosparameterBlokk32) Olvasás(hd *THaladóTechnológiaattachment, partbejegyzés TPartitionTáblázatbejegyzés, fájlnév []byte, data []byte) {

	if partbejegyzés.PartitionAzonosító == 0x00 {
		return
	}

	memóriamanager := TMemóriamanager{}
	bpbMutató := memóriamanager.Malloc(90)
	bpbBájt := GetBájtfromMutató(uintptr(bpbMutató), 90, 90)
	var partitionEltolás = partbejegyzés.Indításlba

	hd.Olvasás28(partitionEltolás, &bpbBájt, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbBájt)

	var fatIndítás = partitionEltolás + uint32(bpb.fenntartvasectors)
	var fatMéret = bpb.táblázatMéret

	var dataIndítás = fatIndítás + fatMéret*uint32(bpb.fatMásolás)

	var gyökérmappaIndítás = dataIndítás + uint32(bpb.sectorspercluster)*(bpb.gyökérmappacluster-2)

	direntMutató := memóriamanager.Malloc(512)
	direntBájt := GetBájtfromMutató(uintptr(direntMutató), 512, 512)
	hd.Olvasás28(gyökérmappaIndítás, &direntBájt, 512)

	var dirent = [16]TKönyvtárbejegyzésfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBájt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].név[0] == 0x00 {
			break
		}

		if dirent[i].méret >= 0xFFFFFFFF {
			continue
		}

		if !EgyenlőBájt(fájlnév, dirent[i].név[:len(fájlnév)]) {
			continue
		}

		var firstFájlcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterAlacsony))

		var Méret = int32(dirent[i].méret)
		var következőFájlcluster = int32(firstFájlcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Méret > 0 {
			var fájlsector = dataIndítás + uint32(bpb.sectorspercluster)*uint32(következőFájlcluster-2)
			var sectorEltolás int = 0

			for ; Méret > 0; Méret -= 512 {

				var buffer3 []byte

				if dirent[i].méret > 512 {
					buffer3 = buffer_2[:512]
					hd.Olvasás28(fájlsector+uint32(sectorEltolás), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].méret]
					hd.Olvasás28(fájlsector+uint32(sectorEltolás), &buffer3, int(dirent[i].méret))
				}

				copy(data[int32(dirent[i].méret)-Méret:], buffer3)

				sectorEltolás++

				if sectorEltolás > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforJelenlegicluster = uint32(következőFájlcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Olvasás28(fatIndítás+fatsectorforJelenlegicluster, &fatbuf, 512)

			var fatEltolásBesectorforJelenlegicluster = következőFájlcluster % 128
			var indításEltolás = fatEltolásBesectorforJelenlegicluster * 4
			var végénEltolás = fatEltolásBesectorforJelenlegicluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[indításEltolás:végénEltolás])

			következőFájlcluster = int32(Unsignedinteger32r(Tömbtounsignedinteger32(buffer4)))
		}
	}
	memóriamanager.Szabad(bpbMutató)
	memóriamanager.Szabad(direntMutató)
}

type TKönyvtárbejegyzésfat32 struct {
	név			[8]byte
	ext			[3]byte
	attribútumok		uint8
	fenntartva		uint8
	cIdőtenth		uint8
	cIdő			uint16
	cDátum			uint16
	aIdő			uint16
	firstclusterhi		uint16
	wIdő			uint16
	wDátum			uint16
	firstclusterAlacsony	uint16
	méret			uint32
}

func (self *TKönyvtárbejegyzésfat32) Init(data [32]byte) {
	copy(self.név[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attribútumok = data[11]
	self.fenntartva = data[12]
	self.cIdőtenth = data[13]
	self.cIdő = uint16(data[14]) | uint16(data[15])<<8
	self.cDátum = uint16(data[16]) | uint16(data[17])<<8
	self.aIdő = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wIdő = uint16(data[22]) | uint16(data[23])<<8
	self.wDátum = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterAlacsony = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.méret = Unsignedinteger32r(Tömbtounsignedinteger32(buffer))
}
