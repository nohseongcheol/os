/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "консол"
import . "driver/ata"
import . "файлСистем/msdospartition"
import . "санахойЗохицуулагч"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softНэр			[8]byte
	байтpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatХуулах		uint8
	rootЛавлахentry		uint16
	нийтsectors		uint16
	mediaТөрөл		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	нийтsectorcount		uint32

	tableХэмжээ		uint32
	extТөлвүүд		uint16
	fatversion		uint16
	rootcluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	drivenumber		uint8
	reserved		uint8
	эхлүүлэлsignature	uint8
	эзэлхүүнДугаар		uint32
	эзэлхүүнТэмдэг		[11]byte
	fatТөрөлТэмдэг		[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softНэр[:8], data[3:11])

	self.байтpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatХуулах = data[16]
	self.rootЛавлахentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.нийтsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaТөрөл = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.нийтsectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableХэмжээ = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.extТөлвүүд = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.эхлүүлэлsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.эзэлхүүнДугаар = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(self.эзэлхүүнТэмдэг[:11], data[71:82])
	copy(self.fatТөрөлТэмдэг[:8], data[82:90])

}

var консол_2 = TКонсол{}

func (self *TBiosparameterblock32) Len(hd *TӨргөтгөсөнtechnologyattachment, partentry TPartitiontableentry, файлыннэр []byte) uint32 {

	if partentry.PartitionДугаар == 0x00 {
		return 0
	}

	санахойЗохицуулагч := TСанахойЗохицуулагч{}
	bpbpointer := санахойЗохицуулагч.Malloc(90)
	bpbБайт := GetБайтfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Эхлэлlba

	hd.Унших28(partitionoffset, &bpbБайт, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbБайт)

	var fatЭхлэл = partitionoffset + uint32(bpb.reservedsectors)
	var fatХэмжээ = bpb.tableХэмжээ

	var dataЭхлэл = fatЭхлэл + fatХэмжээ*uint32(bpb.fatХуулах)

	var rootЭхлэл = dataЭхлэл + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := санахойЗохицуулагч.Malloc(512)
	direntБайт := GetБайтfrompointer(uintptr(direntpointer), 512, 512)
	hd.Унших28(rootЭхлэл, &direntБайт, 512)

	var dirent = [16]TЛавлахentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].нэр[0] == 0x00 {
			break
		}

		if dirent[i].хэмжээ >= 0xFFFFFFFF {
			continue
		}

		if !EqualБайт(файлыннэр, dirent[i].нэр[:len(файлыннэр)]) {
			continue
		}

		санахойЗохицуулагч.Чөлөөт(bpbpointer)
		санахойЗохицуулагч.Чөлөөт(direntpointer)
		return dirent[i].хэмжээ
	}
	санахойЗохицуулагч.Чөлөөт(bpbpointer)
	санахойЗохицуулагч.Чөлөөт(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) Унших(hd *TӨргөтгөсөнtechnologyattachment, partentry TPartitiontableentry, файлыннэр []byte, data []byte) {

	if partentry.PartitionДугаар == 0x00 {
		return
	}

	санахойЗохицуулагч := TСанахойЗохицуулагч{}
	bpbpointer := санахойЗохицуулагч.Malloc(90)
	bpbБайт := GetБайтfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Эхлэлlba

	hd.Унших28(partitionoffset, &bpbБайт, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbБайт)

	var fatЭхлэл = partitionoffset + uint32(bpb.reservedsectors)
	var fatХэмжээ = bpb.tableХэмжээ

	var dataЭхлэл = fatЭхлэл + fatХэмжээ*uint32(bpb.fatХуулах)

	var rootЭхлэл = dataЭхлэл + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntpointer := санахойЗохицуулагч.Malloc(512)
	direntБайт := GetБайтfrompointer(uintptr(direntpointer), 512, 512)
	hd.Унших28(rootЭхлэл, &direntБайт, 512)

	var dirent = [16]TЛавлахentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].нэр[0] == 0x00 {
			break
		}

		if dirent[i].хэмжээ >= 0xFFFFFFFF {
			continue
		}

		if !EqualБайт(файлыннэр, dirent[i].нэр[:len(файлыннэр)]) {
			continue
		}

		var firstФайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterБага))

		var Хэмжээ = int32(dirent[i].хэмжээ)
		var дараахФайлcluster = int32(firstФайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Хэмжээ > 0 {
			var файлsector = dataЭхлэл + uint32(bpb.sectorspercluster)*uint32(дараахФайлcluster-2)
			var sectoroffset int = 0

			for ; Хэмжээ > 0; Хэмжээ -= 512 {

				var buffer3 []byte

				if dirent[i].хэмжээ > 512 {
					buffer3 = buffer_2[:512]
					hd.Унших28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].хэмжээ]
					hd.Унших28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].хэмжээ))
				}

				copy(data[int32(dirent[i].хэмжээ)-Хэмжээ:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(дараахФайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Унших28(fatЭхлэл+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetinsectorforcurrentcluster = дараахФайлcluster % 128
			var эхлэлoffset = fatoffsetinsectorforcurrentcluster * 4
			var endoffset = fatoffsetinsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[эхлэлoffset:endoffset])

			дараахФайлcluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	санахойЗохицуулагч.Чөлөөт(bpbpointer)
	санахойЗохицуулагч.Чөлөөт(direntpointer)
}

type TЛавлахentryfat32 struct {
	нэр			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cЦагtenth		uint8
	cЦаг			uint16
	cОгноо			uint16
	aЦаг			uint16
	firstclusterhi		uint16
	wЦаг			uint16
	wОгноо			uint16
	firstclusterБага	uint16
	хэмжээ			uint32
}

func (self *TЛавлахentryfat32) Init(data [32]byte) {
	copy(self.нэр[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cЦагtenth = data[13]
	self.cЦаг = uint16(data[14]) | uint16(data[15])<<8
	self.cОгноо = uint16(data[16]) | uint16(data[17])<<8
	self.aЦаг = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wЦаг = uint16(data[22]) | uint16(data[23])<<8
	self.wОгноо = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterБага = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.хэмжээ = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
