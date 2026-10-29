/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "skráKerfis/msdospartition"
import . "minnimanager"

type TBiosparameterBlokk32 struct {
	jmp				[3]uint8
	softHeiti			[8]byte
	bætipersector			uint16
	sectorspercluster		uint8
	reservedsectors			uint16
	fatAfrita			uint8
	kerfisstjórirootmappaentry	uint16
	totalsectors			uint16
	miðillTegund			uint8
	fatsectorcount			uint16
	sectorpertrack			uint16
	headcount			uint16
	faliðsectors			uint32
	totalsectorcount		uint32

	taflaStærð		uint32
	extflags		uint16
	fatversion		uint16
	kerfisstjórirootcluster	uint32
	fatUpplýsingar		uint16
	backupsector		uint16
	reserved0		[12]uint8
	drivenumber		uint8
	reserved		uint8
	bootsignature		uint8
	hljóðstyrkurAuðkenni	uint32
	hljóðstyrkurSkýring	[11]byte
	fatTegundSkýring	[8]byte
}

func (sjálft *TBiosparameterBlokk32) Init(data []byte) {
	copy(sjálft.jmp[:3], data[0:3])
	copy(sjálft.softHeiti[:8], data[3:11])

	sjálft.bætipersector = (uint16(data[11]) | uint16(data[12])<<8)
	sjálft.sectorspercluster = data[13]
	sjálft.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	sjálft.fatAfrita = data[16]
	sjálft.kerfisstjórirootmappaentry = (uint16(data[17]) | uint16(data[18])<<8)
	sjálft.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	sjálft.miðillTegund = data[21]
	sjálft.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	sjálft.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	sjálft.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	sjálft.faliðsectors = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	sjálft.totalsectorcount = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	sjálft.taflaStærð = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	sjálft.extflags = (uint16(data[40]) | uint16(data[41])<<8)
	sjálft.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	sjálft.kerfisstjórirootcluster = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	sjálft.fatUpplýsingar = (uint16(data[48]) | uint16(data[49])<<8)
	sjálft.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(sjálft.reserved0[:12], data[52:64])

	sjálft.drivenumber = data[64]
	sjálft.reserved = data[65]
	sjálft.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	sjálft.hljóðstyrkurAuðkenni = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	copy(sjálft.hljóðstyrkurSkýring[:11], data[71:82])
	copy(sjálft.fatTegundSkýring[:8], data[82:90])

}

var console_2 = TConsole{}

func (sjálft *TBiosparameterBlokk32) Len(hd *TNánarTækniattachment, partentry TPartitionTaflaentry, skráarheiti []byte) uint32 {

	if partentry.PartitionAuðkenni == 0x00 {
		return 0
	}

	minnimanager := TMinnimanager{}
	bpbBendill := minnimanager.Malloc(90)
	bpbBæti := GetBætifromBendill(uintptr(bpbBendill), 90, 90)
	var partitionoffset = partentry.Ræsalba

	hd.Lestur28(partitionoffset, &bpbBæti, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbBæti)

	var fatRæsa = partitionoffset + uint32(bpb.reservedsectors)
	var fatStærð = bpb.taflaStærð

	var dataRæsa = fatRæsa + fatStærð*uint32(bpb.fatAfrita)

	var kerfisstjórirootRæsa = dataRæsa + uint32(bpb.sectorspercluster)*(bpb.kerfisstjórirootcluster-2)

	direntBendill := minnimanager.Malloc(512)
	direntBæti := GetBætifromBendill(uintptr(direntBendill), 512, 512)
	hd.Lestur28(kerfisstjórirootRæsa, &direntBæti, 512)

	var dirent = [16]TMappaentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBæti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].heiti[0] == 0x00 {
			break
		}

		if dirent[i].stærð >= 0xFFFFFFFF {
			continue
		}

		if !EqualBæti(skráarheiti, dirent[i].heiti[:len(skráarheiti)]) {
			continue
		}

		minnimanager.Laust(bpbBendill)
		minnimanager.Laust(direntBendill)
		return dirent[i].stærð
	}
	minnimanager.Laust(bpbBendill)
	minnimanager.Laust(direntBendill)
	return 0
}
func (sjálft *TBiosparameterBlokk32) Lestur(hd *TNánarTækniattachment, partentry TPartitionTaflaentry, skráarheiti []byte, data []byte) {

	if partentry.PartitionAuðkenni == 0x00 {
		return
	}

	minnimanager := TMinnimanager{}
	bpbBendill := minnimanager.Malloc(90)
	bpbBæti := GetBætifromBendill(uintptr(bpbBendill), 90, 90)
	var partitionoffset = partentry.Ræsalba

	hd.Lestur28(partitionoffset, &bpbBæti, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbBæti)

	var fatRæsa = partitionoffset + uint32(bpb.reservedsectors)
	var fatStærð = bpb.taflaStærð

	var dataRæsa = fatRæsa + fatStærð*uint32(bpb.fatAfrita)

	var kerfisstjórirootRæsa = dataRæsa + uint32(bpb.sectorspercluster)*(bpb.kerfisstjórirootcluster-2)

	direntBendill := minnimanager.Malloc(512)
	direntBæti := GetBætifromBendill(uintptr(direntBendill), 512, 512)
	hd.Lestur28(kerfisstjórirootRæsa, &direntBæti, 512)

	var dirent = [16]TMappaentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBæti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].heiti[0] == 0x00 {
			break
		}

		if dirent[i].stærð >= 0xFFFFFFFF {
			continue
		}

		if !EqualBæti(skráarheiti, dirent[i].heiti[:len(skráarheiti)]) {
			continue
		}

		var firstSkrácluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLágt))

		var Stærð = int32(dirent[i].stærð)
		var næstaSkrácluster = int32(firstSkrácluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Stærð > 0 {
			var skrásector = dataRæsa + uint32(bpb.sectorspercluster)*uint32(næstaSkrácluster-2)
			var sectoroffset int = 0

			for ; Stærð > 0; Stærð -= 512 {

				var buffer3 []byte

				if dirent[i].stærð > 512 {
					buffer3 = buffer_2[:512]
					hd.Lestur28(skrásector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].stærð]
					hd.Lestur28(skrásector+uint32(sectoroffset), &buffer3, int(dirent[i].stærð))
				}

				copy(data[int32(dirent[i].stærð)-Stærð:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforNúverandicluster = uint32(næstaSkrácluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lestur28(fatRæsa+fatsectorforNúverandicluster, &fatbuf, 512)

			var fatoffsetInnsectorforNúverandicluster = næstaSkrácluster % 128
			var ræsaoffset = fatoffsetInnsectorforNúverandicluster * 4
			var endoffset = fatoffsetInnsectorforNúverandicluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[ræsaoffset:endoffset])

			næstaSkrácluster = int32(Unsignedinteger32r(Fylkitounsignedinteger32(buffer4)))
		}
	}
	minnimanager.Laust(bpbBendill)
	minnimanager.Laust(direntBendill)
}

type TMappaentryfat32 struct {
	heiti			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cTímitenth		uint8
	cTími			uint16
	cDagsetning		uint16
	aTími			uint16
	firstclusterhi		uint16
	wTími			uint16
	wDagsetning		uint16
	firstclusterLágt	uint16
	stærð			uint32
}

func (sjálft *TMappaentryfat32) Init(data [32]byte) {
	copy(sjálft.heiti[:8], data[0:8])
	copy(sjálft.ext[:3], data[8:11])
	sjálft.attributes = data[11]
	sjálft.reserved = data[12]
	sjálft.cTímitenth = data[13]
	sjálft.cTími = uint16(data[14]) | uint16(data[15])<<8
	sjálft.cDagsetning = uint16(data[16]) | uint16(data[17])<<8
	sjálft.aTími = uint16(data[18]) | uint16(data[19])<<8
	sjálft.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	sjálft.wTími = uint16(data[22]) | uint16(data[23])<<8
	sjálft.wDagsetning = uint16(data[24]) | uint16(data[25])<<8
	sjálft.firstclusterLágt = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	sjálft.stærð = Unsignedinteger32r(Fylkitounsignedinteger32(buffer))
}
