/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "файлСистема/msdospartition"
import . "эсиmanager"

type TBiosparameterБлок32 struct {
	jmp			[3]uint8
	softАты			[8]byte
	байтpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatКөчүрүү		uint8
	тамыркаталогentry	uint16
	бардыгыsectors		uint16
	көтөргүчтөрТүрү		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	бардыгыsectorcount	uint32

	жадыбалӨлчөм		uint32
	extЖелектери		uint16
	fatversion		uint16
	тамырcluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveНОМЕР		uint8
	reserved		uint8
	bootsignature		uint8
	көлөмИДЕНТИФИКАТОР	uint32
	көлөмlabel		[11]byte
	fatТүрүlabel		[8]byte
}

func (self *TBiosparameterБлок32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softАты[:8], data[3:11])

	self.байтpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatКөчүрүү = data[16]
	self.тамыркаталогentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.бардыгыsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.көтөргүчтөрТүрү = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.бардыгыsectorcount = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.жадыбалӨлчөм = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	self.extЖелектери = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.тамырcluster = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveНОМЕР = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.көлөмИДЕНТИФИКАТОР = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	copy(self.көлөмlabel[:11], data[71:82])
	copy(self.fatТүрүlabel[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterБлок32) Len(hd *TКеңейтилгенТехнологияattachment, partentry TPartitionЖадыбалentry, файлаты []byte) uint32 {

	if partentry.PartitionИДЕНТИФИКАТОР == 0x00 {
		return 0
	}

	эсиmanager := TЭсиmanager{}
	bpbКөрсөткүч := эсиmanager.Malloc(90)
	bpbБайт := GetБайтfromКөрсөткүч(uintptr(bpbКөрсөткүч), 90, 90)
	var partitionoffset = partentry.Жүргүзүүlba

	hd.Окуу28(partitionoffset, &bpbБайт, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайт)

	var fatЖүргүзүү = partitionoffset + uint32(bpb.reservedsectors)
	var fatӨлчөм = bpb.жадыбалӨлчөм

	var dataЖүргүзүү = fatЖүргүзүү + fatӨлчөм*uint32(bpb.fatКөчүрүү)

	var тамырЖүргүзүү = dataЖүргүзүү + uint32(bpb.sectorspercluster)*(bpb.тамырcluster-2)

	direntКөрсөткүч := эсиmanager.Malloc(512)
	direntБайт := GetБайтfromКөрсөткүч(uintptr(direntКөрсөткүч), 512, 512)
	hd.Окуу28(тамырЖүргүзүү, &direntБайт, 512)

	var dirent = [16]TКаталогentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].аты[0] == 0x00 {
			break
		}

		if dirent[i].өлчөм >= 0xFFFFFFFF {
			continue
		}

		if !EqualБайт(файлаты, dirent[i].аты[:len(файлаты)]) {
			continue
		}

		эсиmanager.Бош(bpbКөрсөткүч)
		эсиmanager.Бош(direntКөрсөткүч)
		return dirent[i].өлчөм
	}
	эсиmanager.Бош(bpbКөрсөткүч)
	эсиmanager.Бош(direntКөрсөткүч)
	return 0
}
func (self *TBiosparameterБлок32) Окуу(hd *TКеңейтилгенТехнологияattachment, partentry TPartitionЖадыбалentry, файлаты []byte, data []byte) {

	if partentry.PartitionИДЕНТИФИКАТОР == 0x00 {
		return
	}

	эсиmanager := TЭсиmanager{}
	bpbКөрсөткүч := эсиmanager.Malloc(90)
	bpbБайт := GetБайтfromКөрсөткүч(uintptr(bpbКөрсөткүч), 90, 90)
	var partitionoffset = partentry.Жүргүзүүlba

	hd.Окуу28(partitionoffset, &bpbБайт, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайт)

	var fatЖүргүзүү = partitionoffset + uint32(bpb.reservedsectors)
	var fatӨлчөм = bpb.жадыбалӨлчөм

	var dataЖүргүзүү = fatЖүргүзүү + fatӨлчөм*uint32(bpb.fatКөчүрүү)

	var тамырЖүргүзүү = dataЖүргүзүү + uint32(bpb.sectorspercluster)*(bpb.тамырcluster-2)

	direntКөрсөткүч := эсиmanager.Malloc(512)
	direntБайт := GetБайтfromКөрсөткүч(uintptr(direntКөрсөткүч), 512, 512)
	hd.Окуу28(тамырЖүргүзүү, &direntБайт, 512)

	var dirent = [16]TКаталогentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].аты[0] == 0x00 {
			break
		}

		if dirent[i].өлчөм >= 0xFFFFFFFF {
			continue
		}

		if !EqualБайт(файлаты, dirent[i].аты[:len(файлаты)]) {
			continue
		}

		var firstФайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Өлчөм = int32(dirent[i].өлчөм)
		var кийинкиФайлcluster = int32(firstФайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Өлчөм > 0 {
			var файлsector = dataЖүргүзүү + uint32(bpb.sectorspercluster)*uint32(кийинкиФайлcluster-2)
			var sectoroffset int = 0

			for ; Өлчөм > 0; Өлчөм -= 512 {

				var buffer3 []byte

				if dirent[i].өлчөм > 512 {
					buffer3 = buffer_2[:512]
					hd.Окуу28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].өлчөм]
					hd.Окуу28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].өлчөм))
				}

				copy(data[int32(dirent[i].өлчөм)-Өлчөм:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(кийинкиФайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Окуу28(fatЖүргүзүү+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetЧоңойтууsectorforcurrentcluster = кийинкиФайлcluster % 128
			var жүргүзүүoffset = fatoffsetЧоңойтууsectorforcurrentcluster * 4
			var endoffset = fatoffsetЧоңойтууsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[жүргүзүүoffset:endoffset])

			кийинкиФайлcluster = int32(Unsignedinteger32r(Массивtounsignedinteger32(buffer4)))
		}
	}
	эсиmanager.Бош(bpbКөрсөткүч)
	эсиmanager.Бош(direntКөрсөткүч)
}

type TКаталогentryfat32 struct {
	аты		[8]byte
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
	өлчөм		uint32
}

func (self *TКаталогentryfat32) Init(data [32]byte) {
	copy(self.аты[:8], data[0:8])
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
	self.өлчөм = Unsignedinteger32r(Массивtounsignedinteger32(buffer))
}
