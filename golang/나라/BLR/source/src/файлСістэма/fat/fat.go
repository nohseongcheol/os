/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "файлСістэма/msdospartition"
import . "памяцьmanager"

type TBiosparameterБлок32 struct {
	jmp			[3]uint8
	softНазва		[8]byte
	байтаўpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatСкапіяваць		uint8
	кораньКаталогentry	uint16
	агуламsectors		uint16
	носьбітТып		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	схаванаsectors		uint32
	агуламsectorcount	uint32

	табліцаПамер		uint32
	extСцяжкі		uint16
	fatversion		uint16
	кораньcluster		uint32
	fatІнф			uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveНУМАР		uint8
	reserved		uint8
	bootsignature		uint8
	гучнасцьІДЭНТЫФІКАТАР	uint32
	гучнасцьМетка		[11]byte
	fatТыпМетка		[8]byte
}

func (self *TBiosparameterБлок32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softНазва[:8], data[3:11])

	self.байтаўpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatСкапіяваць = data[16]
	self.кораньКаталогentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.агуламsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.носьбітТып = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.схаванаsectors = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.агуламsectorcount = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.табліцаПамер = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	self.extСцяжкі = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.кораньcluster = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	self.fatІнф = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveНУМАР = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.гучнасцьІДЭНТЫФІКАТАР = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	copy(self.гучнасцьМетка[:11], data[71:82])
	copy(self.fatТыпМетка[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterБлок32) Len(hd *TДадатковаТэхналогіяattachment, partentry TPartitionТабліцаentry, назвафайла []byte) uint32 {

	if partentry.PartitionІДЭНТЫФІКАТАР == 0x00 {
		return 0
	}

	памяцьmanager := TПамяцьmanager{}
	bpbПаказальнік := памяцьmanager.Malloc(90)
	bpbБайтаў := GetБайтаўfromПаказальнік(uintptr(bpbПаказальнік), 90, 90)
	var partitionoffset = partentry.Уключыцьlba

	hd.Чытанне28(partitionoffset, &bpbБайтаў, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайтаў)

	var fatУключыць = partitionoffset + uint32(bpb.reservedsectors)
	var fatПамер = bpb.табліцаПамер

	var dataУключыць = fatУключыць + fatПамер*uint32(bpb.fatСкапіяваць)

	var кораньУключыць = dataУключыць + uint32(bpb.sectorspercluster)*(bpb.кораньcluster-2)

	direntПаказальнік := памяцьmanager.Malloc(512)
	direntБайтаў := GetБайтаўfromПаказальнік(uintptr(direntПаказальнік), 512, 512)
	hd.Чытанне28(кораньУключыць, &direntБайтаў, 512)

	var dirent = [16]TКаталогentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайтаў[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назва[0] == 0x00 {
			break
		}

		if dirent[i].памер >= 0xFFFFFFFF {
			continue
		}

		if !АднолькавыБайтаў(назвафайла, dirent[i].назва[:len(назвафайла)]) {
			continue
		}

		памяцьmanager.Вольна(bpbПаказальнік)
		памяцьmanager.Вольна(direntПаказальнік)
		return dirent[i].памер
	}
	памяцьmanager.Вольна(bpbПаказальнік)
	памяцьmanager.Вольна(direntПаказальнік)
	return 0
}
func (self *TBiosparameterБлок32) Чытанне(hd *TДадатковаТэхналогіяattachment, partentry TPartitionТабліцаentry, назвафайла []byte, data []byte) {

	if partentry.PartitionІДЭНТЫФІКАТАР == 0x00 {
		return
	}

	памяцьmanager := TПамяцьmanager{}
	bpbПаказальнік := памяцьmanager.Malloc(90)
	bpbБайтаў := GetБайтаўfromПаказальнік(uintptr(bpbПаказальнік), 90, 90)
	var partitionoffset = partentry.Уключыцьlba

	hd.Чытанне28(partitionoffset, &bpbБайтаў, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайтаў)

	var fatУключыць = partitionoffset + uint32(bpb.reservedsectors)
	var fatПамер = bpb.табліцаПамер

	var dataУключыць = fatУключыць + fatПамер*uint32(bpb.fatСкапіяваць)

	var кораньУключыць = dataУключыць + uint32(bpb.sectorspercluster)*(bpb.кораньcluster-2)

	direntПаказальнік := памяцьmanager.Malloc(512)
	direntБайтаў := GetБайтаўfromПаказальнік(uintptr(direntПаказальнік), 512, 512)
	hd.Чытанне28(кораньУключыць, &direntБайтаў, 512)

	var dirent = [16]TКаталогentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайтаў[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назва[0] == 0x00 {
			break
		}

		if dirent[i].памер >= 0xFFFFFFFF {
			continue
		}

		if !АднолькавыБайтаў(назвафайла, dirent[i].назва[:len(назвафайла)]) {
			continue
		}

		var firstФайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterНізкі))

		var Памер = int32(dirent[i].памер)
		var наступныФайлcluster = int32(firstФайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Памер > 0 {
			var файлsector = dataУключыць + uint32(bpb.sectorspercluster)*uint32(наступныФайлcluster-2)
			var sectoroffset int = 0

			for ; Памер > 0; Памер -= 512 {

				var buffer3 []byte

				if dirent[i].памер > 512 {
					buffer3 = buffer_2[:512]
					hd.Чытанне28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].памер]
					hd.Чытанне28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].памер))
				}

				copy(data[int32(dirent[i].памер)-Памер:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforДзейныcluster = uint32(наступныФайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Чытанне28(fatУключыць+fatsectorforДзейныcluster, &fatbuf, 512)

			var fatoffsetуsectorforДзейныcluster = наступныФайлcluster % 128
			var уключыцьoffset = fatoffsetуsectorforДзейныcluster * 4
			var канецoffset = fatoffsetуsectorforДзейныcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[уключыцьoffset:канецoffset])

			наступныФайлcluster = int32(Unsignedinteger32r(Масіўtounsignedinteger32(buffer4)))
		}
	}
	памяцьmanager.Вольна(bpbПаказальнік)
	памяцьmanager.Вольна(direntПаказальнік)
}

type TКаталогentryfat32 struct {
	назва			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cЧасtenth		uint8
	cЧас			uint16
	cДата			uint16
	aЧас			uint16
	firstclusterhi		uint16
	wЧас			uint16
	wДата			uint16
	firstclusterНізкі	uint16
	памер			uint32
}

func (self *TКаталогentryfat32) Init(data [32]byte) {
	copy(self.назва[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cЧасtenth = data[13]
	self.cЧас = uint16(data[14]) | uint16(data[15])<<8
	self.cДата = uint16(data[16]) | uint16(data[17])<<8
	self.aЧас = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wЧас = uint16(data[22]) | uint16(data[23])<<8
	self.wДата = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterНізкі = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.памер = Unsignedinteger32r(Масіўtounsignedinteger32(buffer))
}
