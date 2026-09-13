package fat

import . "util"
import . "console"
import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "меморијаmanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softИме			[8]byte
	бајтиpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatКопирај		uint8
	коренДиректориумentry	uint16
	вкупноsectors		uint16
	медиумиТип		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	вкупноsectorcount	uint32

	табелаГолемина	uint32
	extАтрибути	uint16
	fatversion	uint16
	коренcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	bootsignature	uint8
	волуменИд	uint32
	волуменОзнака	[11]byte
	fatТипОзнака	[8]byte
}

func (само *TBiosparameterblock32) Init(data []byte) {
	copy(само.jmp[:3], data[0:3])
	copy(само.softИме[:8], data[3:11])

	само.бајтиpersector = (uint16(data[11]) | uint16(data[12])<<8)
	само.sectorspercluster = data[13]
	само.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	само.fatКопирај = data[16]
	само.коренДиректориумentry = (uint16(data[17]) | uint16(data[18])<<8)
	само.вкупноsectors = (uint16(data[19]) | uint16(data[20])<<8)
	само.медиумиТип = data[21]
	само.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	само.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	само.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	само.hiddensectors = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	само.вкупноsectorcount = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	само.табелаГолемина = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	само.extАтрибути = (uint16(data[40]) | uint16(data[41])<<8)
	само.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	само.коренcluster = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	само.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	само.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(само.reserved0[:12], data[52:64])

	само.drivenumber = data[64]
	само.reserved = data[65]
	само.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	само.волуменИд = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	copy(само.волуменОзнака[:11], data[71:82])
	copy(само.fatТипОзнака[:8], data[82:90])

}

var console_2 = TConsole{}

func (само *TBiosparameterblock32) Len(hd *TНапредноtechnologyattachment, partentry TPartitionТабелаentry, именадатотека []byte) uint32 {

	if partentry.PartitionИд == 0x00 {
		return 0
	}

	меморијаmanager := TМеморијаmanager{}
	bpbСтрелка := меморијаmanager.Malloc(90)
	bpbбајти := GetбајтиfromСтрелка(uintptr(bpbСтрелка), 90, 90)
	var partitionoffset = partentry.Пуштиlba

	hd.Читај28(partitionoffset, &bpbбајти, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbбајти)

	var fatПушти = partitionoffset + uint32(bpb.reservedsectors)
	var fatГолемина = bpb.табелаГолемина

	var dataПушти = fatПушти + fatГолемина*uint32(bpb.fatКопирај)

	var коренПушти = dataПушти + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntСтрелка := меморијаmanager.Malloc(512)
	direntбајти := GetбајтиfromСтрелка(uintptr(direntСтрелка), 512, 512)
	hd.Читај28(коренПушти, &direntбајти, 512)

	var dirent = [16]TДиректориумentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntбајти[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].име[0] == 0x00 {
			break
		}

		if dirent[i].големина >= 0xFFFFFFFF {
			continue
		}

		if !Equalбајти(именадатотека, dirent[i].име[:len(именадатотека)]) {
			continue
		}

		меморијаmanager.Слободни(bpbСтрелка)
		меморијаmanager.Слободни(direntСтрелка)
		return dirent[i].големина
	}
	меморијаmanager.Слободни(bpbСтрелка)
	меморијаmanager.Слободни(direntСтрелка)
	return 0
}
func (само *TBiosparameterblock32) Читај(hd *TНапредноtechnologyattachment, partentry TPartitionТабелаentry, именадатотека []byte, data []byte) {

	if partentry.PartitionИд == 0x00 {
		return
	}

	меморијаmanager := TМеморијаmanager{}
	bpbСтрелка := меморијаmanager.Malloc(90)
	bpbбајти := GetбајтиfromСтрелка(uintptr(bpbСтрелка), 90, 90)
	var partitionoffset = partentry.Пуштиlba

	hd.Читај28(partitionoffset, &bpbбајти, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbбајти)

	var fatПушти = partitionoffset + uint32(bpb.reservedsectors)
	var fatГолемина = bpb.табелаГолемина

	var dataПушти = fatПушти + fatГолемина*uint32(bpb.fatКопирај)

	var коренПушти = dataПушти + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntСтрелка := меморијаmanager.Malloc(512)
	direntбајти := GetбајтиfromСтрелка(uintptr(direntСтрелка), 512, 512)
	hd.Читај28(коренПушти, &direntбајти, 512)

	var dirent = [16]TДиректориумentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntбајти[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].име[0] == 0x00 {
			break
		}

		if dirent[i].големина >= 0xFFFFFFFF {
			continue
		}

		if !Equalбајти(именадатотека, dirent[i].име[:len(именадатотека)]) {
			continue
		}

		var firstДатотекаcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Големина = int32(dirent[i].големина)
		var следнаДатотекаcluster = int32(firstДатотекаcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Големина > 0 {
			var датотекаsector = dataПушти + uint32(bpb.sectorspercluster)*uint32(следнаДатотекаcluster-2)
			var sectoroffset int = 0

			for ; Големина > 0; Големина -= 512 {

				var buffer3 []byte

				if dirent[i].големина > 512 {
					buffer3 = buffer_2[:512]
					hd.Читај28(датотекаsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].големина]
					hd.Читај28(датотекаsector+uint32(sectoroffset), &buffer3, int(dirent[i].големина))
				}

				copy(data[int32(dirent[i].големина)-Големина:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(следнаДатотекаcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Читај28(fatПушти+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetвоsectorforcurrentcluster = следнаДатотекаcluster % 128
			var пуштиoffset = fatoffsetвоsectorforcurrentcluster * 4
			var endoffset = fatoffsetвоsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[пуштиoffset:endoffset])

			следнаДатотекаcluster = int32(Unsignedinteger32r(Построиtounsignedinteger32(buffer4)))
		}
	}
	меморијаmanager.Слободни(bpbСтрелка)
	меморијаmanager.Слободни(direntСтрелка)
}

type TДиректориумentryfat32 struct {
	име		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cВремеtenth	uint8
	cВреме		uint16
	cДатум		uint16
	aВреме		uint16
	firstclusterhi	uint16
	wВреме		uint16
	wДатум		uint16
	firstclusterlow	uint16
	големина	uint32
}

func (само *TДиректориумentryfat32) Init(data [32]byte) {
	copy(само.име[:8], data[0:8])
	copy(само.ext[:3], data[8:11])
	само.attributes = data[11]
	само.reserved = data[12]
	само.cВремеtenth = data[13]
	само.cВреме = uint16(data[14]) | uint16(data[15])<<8
	само.cДатум = uint16(data[16]) | uint16(data[17])<<8
	само.aВреме = uint16(data[18]) | uint16(data[19])<<8
	само.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	само.wВреме = uint16(data[22]) | uint16(data[23])<<8
	само.wДатум = uint16(data[24]) | uint16(data[25])<<8
	само.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	само.големина = Unsignedinteger32r(Построиtounsignedinteger32(buffer))
}
