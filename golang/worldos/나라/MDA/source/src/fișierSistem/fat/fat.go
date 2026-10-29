/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "fișierSistem/msdospartition"
import . "memoriemanager"

type TBiosparameterBloc32 struct {
	jmp				[3]uint8
	softNume			[8]byte
	octețipersector			uint16
	sectorspercluster		uint8
	reservedsectors			uint16
	fatCopiază			uint8
	rădăcinăDirectorînregistrare	uint16
	totalsectors			uint16
	mediidestocareTip		uint8
	fatsectorcount			uint16
	sectorpertrack			uint16
	headcount			uint16
	ascunsesectors			uint32
	totalsectorcount		uint32

	tabelMărime	uint32
	extIndicatori	uint16
	fatVersiune	uint16
	rădăcinăcluster	uint32
	fatDetaliat	uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveNumăr	uint8
	reserved	uint8
	bootsignature	uint8
	volumid		uint32
	volumEtichetă	[11]byte
	fatTipEtichetă	[8]byte
}

func (sine *TBiosparameterBloc32) Init(data []byte) {
	copy(sine.jmp[:3], data[0:3])
	copy(sine.softNume[:8], data[3:11])

	sine.octețipersector = (uint16(data[11]) | uint16(data[12])<<8)
	sine.sectorspercluster = data[13]
	sine.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	sine.fatCopiază = data[16]
	sine.rădăcinăDirectorînregistrare = (uint16(data[17]) | uint16(data[18])<<8)
	sine.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	sine.mediidestocareTip = data[21]
	sine.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	sine.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	sine.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	sine.ascunsesectors = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	sine.totalsectorcount = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	sine.tabelMărime = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	sine.extIndicatori = (uint16(data[40]) | uint16(data[41])<<8)
	sine.fatVersiune = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	sine.rădăcinăcluster = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	sine.fatDetaliat = (uint16(data[48]) | uint16(data[49])<<8)
	sine.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(sine.reserved0[:12], data[52:64])

	sine.driveNumăr = data[64]
	sine.reserved = data[65]
	sine.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	sine.volumid = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	copy(sine.volumEtichetă[:11], data[71:82])
	copy(sine.fatTipEtichetă[:8], data[82:90])

}

var console_2 = TConsole{}

func (sine *TBiosparameterBloc32) Len(hd *TAvansateTehnologieattachment, partînregistrare TPartitionTabelînregistrare, numefișier []byte) uint32 {

	if partînregistrare.Partitionid == 0x00 {
		return 0
	}

	memoriemanager := TMemoriemanager{}
	bpbIndicator := memoriemanager.Malloc(90)
	bpbOcteți := GetOctețifromIndicator(uintptr(bpbIndicator), 90, 90)
	var partitionoffset = partînregistrare.Porneștelba

	hd.Citire28(partitionoffset, &bpbOcteți, 90)

	var bpb = TBiosparameterBloc32{}
	bpb.Init(bpbOcteți)

	var fatPornește = partitionoffset + uint32(bpb.reservedsectors)
	var fatMărime = bpb.tabelMărime

	var dataPornește = fatPornește + fatMărime*uint32(bpb.fatCopiază)

	var rădăcinăPornește = dataPornește + uint32(bpb.sectorspercluster)*(bpb.rădăcinăcluster-2)

	direntIndicator := memoriemanager.Malloc(512)
	direntOcteți := GetOctețifromIndicator(uintptr(direntIndicator), 512, 512)
	hd.Citire28(rădăcinăPornește, &direntOcteți, 512)

	var dirent = [16]TDirectorînregistrarefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOcteți[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nume[0] == 0x00 {
			break
		}

		if dirent[i].mărime >= 0xFFFFFFFF {
			continue
		}

		if !EqualOcteți(numefișier, dirent[i].nume[:len(numefișier)]) {
			continue
		}

		memoriemanager.Liber(bpbIndicator)
		memoriemanager.Liber(direntIndicator)
		return dirent[i].mărime
	}
	memoriemanager.Liber(bpbIndicator)
	memoriemanager.Liber(direntIndicator)
	return 0
}
func (sine *TBiosparameterBloc32) Citire(hd *TAvansateTehnologieattachment, partînregistrare TPartitionTabelînregistrare, numefișier []byte, data []byte) {

	if partînregistrare.Partitionid == 0x00 {
		return
	}

	memoriemanager := TMemoriemanager{}
	bpbIndicator := memoriemanager.Malloc(90)
	bpbOcteți := GetOctețifromIndicator(uintptr(bpbIndicator), 90, 90)
	var partitionoffset = partînregistrare.Porneștelba

	hd.Citire28(partitionoffset, &bpbOcteți, 90)

	var bpb = TBiosparameterBloc32{}
	bpb.Init(bpbOcteți)

	var fatPornește = partitionoffset + uint32(bpb.reservedsectors)
	var fatMărime = bpb.tabelMărime

	var dataPornește = fatPornește + fatMărime*uint32(bpb.fatCopiază)

	var rădăcinăPornește = dataPornește + uint32(bpb.sectorspercluster)*(bpb.rădăcinăcluster-2)

	direntIndicator := memoriemanager.Malloc(512)
	direntOcteți := GetOctețifromIndicator(uintptr(direntIndicator), 512, 512)
	hd.Citire28(rădăcinăPornește, &direntOcteți, 512)

	var dirent = [16]TDirectorînregistrarefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOcteți[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nume[0] == 0x00 {
			break
		}

		if dirent[i].mărime >= 0xFFFFFFFF {
			continue
		}

		if !EqualOcteți(numefișier, dirent[i].nume[:len(numefișier)]) {
			continue
		}

		var firstFișiercluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterScăzută))

		var Mărime = int32(dirent[i].mărime)
		var înainteFișiercluster = int32(firstFișiercluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Mărime > 0 {
			var fișiersector = dataPornește + uint32(bpb.sectorspercluster)*uint32(înainteFișiercluster-2)
			var sectoroffset int = 0

			for ; Mărime > 0; Mărime -= 512 {

				var buffer3 []byte

				if dirent[i].mărime > 512 {
					buffer3 = buffer_2[:512]
					hd.Citire28(fișiersector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].mărime]
					hd.Citire28(fișiersector+uint32(sectoroffset), &buffer3, int(dirent[i].mărime))
				}

				copy(data[int32(dirent[i].mărime)-Mărime:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforCurentăcluster = uint32(înainteFișiercluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Citire28(fatPornește+fatsectorforCurentăcluster, &fatbuf, 512)

			var fatoffsetIntraresectorforCurentăcluster = înainteFișiercluster % 128
			var porneșteoffset = fatoffsetIntraresectorforCurentăcluster * 4
			var sfârșitoffset = fatoffsetIntraresectorforCurentăcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[porneșteoffset:sfârșitoffset])

			înainteFișiercluster = int32(Unsignedinteger32r(Vectortounsignedinteger32(buffer4)))
		}
	}
	memoriemanager.Liber(bpbIndicator)
	memoriemanager.Liber(direntIndicator)
}

type TDirectorînregistrarefat32 struct {
	nume			[8]byte
	ext			[3]byte
	atribute		uint8
	reserved		uint8
	cOrătenth		uint8
	cOră			uint16
	cDată			uint16
	aOră			uint16
	firstclusterhi		uint16
	wOră			uint16
	wDată			uint16
	firstclusterScăzută	uint16
	mărime			uint32
}

func (sine *TDirectorînregistrarefat32) Init(data [32]byte) {
	copy(sine.nume[:8], data[0:8])
	copy(sine.ext[:3], data[8:11])
	sine.atribute = data[11]
	sine.reserved = data[12]
	sine.cOrătenth = data[13]
	sine.cOră = uint16(data[14]) | uint16(data[15])<<8
	sine.cDată = uint16(data[16]) | uint16(data[17])<<8
	sine.aOră = uint16(data[18]) | uint16(data[19])<<8
	sine.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	sine.wOră = uint16(data[22]) | uint16(data[23])<<8
	sine.wDată = uint16(data[24]) | uint16(data[25])<<8
	sine.firstclusterScăzută = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	sine.mărime = Unsignedinteger32r(Vectortounsignedinteger32(buffer))
}
