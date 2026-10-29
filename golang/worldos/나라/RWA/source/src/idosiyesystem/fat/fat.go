/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "idosiyesystem/msdospartition"
import . "ububikomanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softIzina		[8]byte
	bayitepersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatGukoporora		uint8
	imiziUbubikoentry	uint16
	igiteranyosectors	uint16
	mediaUbwoko		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	igiteranyosectorcount	uint32

	imbonerahamweIngano	uint32
	extAmabendera		uint16
	fatversion		uint16
	imizicluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	drivenumber		uint8
	reserved		uint8
	bootsignature		uint8
	volumeid		uint32
	volumeAkarango		[11]byte
	fatUbwokoAkarango	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softIzina[:8], data[3:11])

	self.bayitepersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatGukoporora = data[16]
	self.imiziUbubikoentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.igiteranyosectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.mediaUbwoko = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.igiteranyosectorcount = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.imbonerahamweIngano = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer1))

	self.extAmabendera = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.imizicluster = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer1))

	copy(self.volumeAkarango[:11], data[71:82])
	copy(self.fatUbwokoAkarango[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *TUrwegorwohejurutechnologyattachment, partentry TPartitionImbonerahamweentry, izinaryidosiye []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	ububikomanager := TUbubikomanager{}
	bpbpointer := ububikomanager.Malloc(90)
	bpbBayite := GetBayitefrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Gusoma28(partitionoffset, &bpbBayite, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBayite)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatIngano = bpb.imbonerahamweIngano

	var datastart = fatstart + fatIngano*uint32(bpb.fatGukoporora)

	var imizistart = datastart + uint32(bpb.sectorspercluster)*(bpb.imizicluster-2)

	direntpointer := ububikomanager.Malloc(512)
	direntBayite := GetBayitefrompointer(uintptr(direntpointer), 512, 512)
	hd.Gusoma28(imizistart, &direntBayite, 512)

	var dirent = [16]TUbubikoentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayite[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].izina[0] == 0x00 {
			break
		}

		if dirent[i].ingano >= 0xFFFFFFFF {
			continue
		}

		if !EqualBayite(izinaryidosiye, dirent[i].izina[:len(izinaryidosiye)]) {
			continue
		}

		ububikomanager.Kigenga(bpbpointer)
		ububikomanager.Kigenga(direntpointer)
		return dirent[i].ingano
	}
	ububikomanager.Kigenga(bpbpointer)
	ububikomanager.Kigenga(direntpointer)
	return 0
}
func (self *TBiosparameterblock32) Gusoma(hd *TUrwegorwohejurutechnologyattachment, partentry TPartitionImbonerahamweentry, izinaryidosiye []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	ububikomanager := TUbubikomanager{}
	bpbpointer := ububikomanager.Malloc(90)
	bpbBayite := GetBayitefrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Gusoma28(partitionoffset, &bpbBayite, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbBayite)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatIngano = bpb.imbonerahamweIngano

	var datastart = fatstart + fatIngano*uint32(bpb.fatGukoporora)

	var imizistart = datastart + uint32(bpb.sectorspercluster)*(bpb.imizicluster-2)

	direntpointer := ububikomanager.Malloc(512)
	direntBayite := GetBayitefrompointer(uintptr(direntpointer), 512, 512)
	hd.Gusoma28(imizistart, &direntBayite, 512)

	var dirent = [16]TUbubikoentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayite[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].izina[0] == 0x00 {
			break
		}

		if dirent[i].ingano >= 0xFFFFFFFF {
			continue
		}

		if !EqualBayite(izinaryidosiye, dirent[i].izina[:len(izinaryidosiye)]) {
			continue
		}

		var firstIdosiyecluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Ingano = int32(dirent[i].ingano)
		var ikurikiraIdosiyecluster = int32(firstIdosiyecluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Ingano > 0 {
			var idosiyesector = datastart + uint32(bpb.sectorspercluster)*uint32(ikurikiraIdosiyecluster-2)
			var sectoroffset int = 0

			for ; Ingano > 0; Ingano -= 512 {

				var buffer3 []byte

				if dirent[i].ingano > 512 {
					buffer3 = buffer_2[:512]
					hd.Gusoma28(idosiyesector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].ingano]
					hd.Gusoma28(idosiyesector+uint32(sectoroffset), &buffer3, int(dirent[i].ingano))
				}

				copy(data[int32(dirent[i].ingano)-Ingano:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(ikurikiraIdosiyecluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Gusoma28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetImberesectorforcurrentcluster = ikurikiraIdosiyecluster % 128
			var startoffset = fatoffsetImberesectorforcurrentcluster * 4
			var endoffset = fatoffsetImberesectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			ikurikiraIdosiyecluster = int32(Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer4)))
		}
	}
	ububikomanager.Kigenga(bpbpointer)
	ububikomanager.Kigenga(direntpointer)
}

type TUbubikoentryfat32 struct {
	izina		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cIgihetenth	uint8
	cIgihe		uint16
	cItariki	uint16
	aIgihe		uint16
	firstclusterhi	uint16
	wIgihe		uint16
	wItariki	uint16
	firstclusterlow	uint16
	ingano		uint32
}

func (self *TUbubikoentryfat32) Init(data [32]byte) {
	copy(self.izina[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cIgihetenth = data[13]
	self.cIgihe = uint16(data[14]) | uint16(data[15])<<8
	self.cItariki = uint16(data[16]) | uint16(data[17])<<8
	self.aIgihe = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wIgihe = uint16(data[22]) | uint16(data[23])<<8
	self.wItariki = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.ingano = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer))
}
