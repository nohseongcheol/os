/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "konsoly"
import . "driver/ata"
import . "rakitraRafitra/msdospartition"
import . "arikaMpandrindra"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softAnarana		[8]byte
	octetpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatAdikao		uint8
	fakaLahatahiryentry	uint16
	tontalinysectors	uint16
	mediaKarazana		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	tontalinysectorcount	uint32

	fafanaHabe		uint32
	extSaina		uint16
	fatversion		uint16
	fakacluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	drivenumber		uint8
	reserved		uint8
	bootsignature		uint8
	volumeid		uint32
	volumeMaritsoratra	[11]byte
	fatKarazanaMaritsoratra	[8]byte
}

func (nytena *TBiosparameterblock32) Init(data []byte) {
	copy(nytena.jmp[:3], data[0:3])
	copy(nytena.softAnarana[:8], data[3:11])

	nytena.octetpersector = (uint16(data[11]) | uint16(data[12])<<8)
	nytena.sectorspercluster = data[13]
	nytena.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	nytena.fatAdikao = data[16]
	nytena.fakaLahatahiryentry = (uint16(data[17]) | uint16(data[18])<<8)
	nytena.tontalinysectors = (uint16(data[19]) | uint16(data[20])<<8)
	nytena.mediaKarazana = data[21]
	nytena.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	nytena.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	nytena.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	nytena.hiddensectors = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	nytena.tontalinysectorcount = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	nytena.fafanaHabe = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	nytena.extSaina = (uint16(data[40]) | uint16(data[41])<<8)
	nytena.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	nytena.fakacluster = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	nytena.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	nytena.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(nytena.reserved0[:12], data[52:64])

	nytena.drivenumber = data[64]
	nytena.reserved = data[65]
	nytena.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	nytena.volumeid = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	copy(nytena.volumeMaritsoratra[:11], data[71:82])
	copy(nytena.fatKarazanaMaritsoratra[:8], data[82:90])

}

var konsoly_2 = TKonsoly{}

func (nytena *TBiosparameterblock32) Len(hd *TAvolentatechnologyattachment, partentry TPartitionFafanaentry, anarandrakitra []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	arikaMpandrindra := TArikaMpandrindra{}
	bpbpointer := arikaMpandrindra.Malloc(90)
	bpbOctet := GetOctetfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Atomboylba

	hd.Mamaky28(partitionoffset, &bpbOctet, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbOctet)

	var fatAtomboy = partitionoffset + uint32(bpb.reservedsectors)
	var fatHabe = bpb.fafanaHabe

	var dataAtomboy = fatAtomboy + fatHabe*uint32(bpb.fatAdikao)

	var fakaAtomboy = dataAtomboy + uint32(bpb.sectorspercluster)*(bpb.fakacluster-2)

	direntpointer := arikaMpandrindra.Malloc(512)
	direntOctet := GetOctetfrompointer(uintptr(direntpointer), 512, 512)
	hd.Mamaky28(fakaAtomboy, &direntOctet, 512)

	var dirent = [16]TLahatahiryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOctet[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].anarana[0] == 0x00 {
			break
		}

		if dirent[i].habe >= 0xFFFFFFFF {
			continue
		}

		if !EqualOctet(anarandrakitra, dirent[i].anarana[:len(anarandrakitra)]) {
			continue
		}

		arikaMpandrindra.Malalaka(bpbpointer)
		arikaMpandrindra.Malalaka(direntpointer)
		return dirent[i].habe
	}
	arikaMpandrindra.Malalaka(bpbpointer)
	arikaMpandrindra.Malalaka(direntpointer)
	return 0
}
func (nytena *TBiosparameterblock32) Mamaky(hd *TAvolentatechnologyattachment, partentry TPartitionFafanaentry, anarandrakitra []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	arikaMpandrindra := TArikaMpandrindra{}
	bpbpointer := arikaMpandrindra.Malloc(90)
	bpbOctet := GetOctetfrompointer(uintptr(bpbpointer), 90, 90)
	var partitionoffset = partentry.Atomboylba

	hd.Mamaky28(partitionoffset, &bpbOctet, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbOctet)

	var fatAtomboy = partitionoffset + uint32(bpb.reservedsectors)
	var fatHabe = bpb.fafanaHabe

	var dataAtomboy = fatAtomboy + fatHabe*uint32(bpb.fatAdikao)

	var fakaAtomboy = dataAtomboy + uint32(bpb.sectorspercluster)*(bpb.fakacluster-2)

	direntpointer := arikaMpandrindra.Malloc(512)
	direntOctet := GetOctetfrompointer(uintptr(direntpointer), 512, 512)
	hd.Mamaky28(fakaAtomboy, &direntOctet, 512)

	var dirent = [16]TLahatahiryentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOctet[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].anarana[0] == 0x00 {
			break
		}

		if dirent[i].habe >= 0xFFFFFFFF {
			continue
		}

		if !EqualOctet(anarandrakitra, dirent[i].anarana[:len(anarandrakitra)]) {
			continue
		}

		var firstRakitracluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Habe = int32(dirent[i].habe)
		var manarakaRakitracluster = int32(firstRakitracluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Habe > 0 {
			var rakitrasector = dataAtomboy + uint32(bpb.sectorspercluster)*uint32(manarakaRakitracluster-2)
			var sectoroffset int = 0

			for ; Habe > 0; Habe -= 512 {

				var buffer3 []byte

				if dirent[i].habe > 512 {
					buffer3 = buffer_2[:512]
					hd.Mamaky28(rakitrasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].habe]
					hd.Mamaky28(rakitrasector+uint32(sectoroffset), &buffer3, int(dirent[i].habe))
				}

				copy(data[int32(dirent[i].habe)-Habe:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(manarakaRakitracluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Mamaky28(fatAtomboy+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetAnatysectorforcurrentcluster = manarakaRakitracluster % 128
			var atomboyoffset = fatoffsetAnatysectorforcurrentcluster * 4
			var endoffset = fatoffsetAnatysectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[atomboyoffset:endoffset])

			manarakaRakitracluster = int32(Unsignedinteger32r(Arraytounsignedinteger32(buffer4)))
		}
	}
	arikaMpandrindra.Malalaka(bpbpointer)
	arikaMpandrindra.Malalaka(direntpointer)
}

type TLahatahiryentryfat32 struct {
	anarana		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cFotoanatenth	uint8
	cFotoana	uint16
	cDaty		uint16
	aFotoana	uint16
	firstclusterhi	uint16
	wFotoana	uint16
	wDaty		uint16
	firstclusterlow	uint16
	habe		uint32
}

func (nytena *TLahatahiryentryfat32) Init(data [32]byte) {
	copy(nytena.anarana[:8], data[0:8])
	copy(nytena.ext[:3], data[8:11])
	nytena.attributes = data[11]
	nytena.reserved = data[12]
	nytena.cFotoanatenth = data[13]
	nytena.cFotoana = uint16(data[14]) | uint16(data[15])<<8
	nytena.cDaty = uint16(data[16]) | uint16(data[17])<<8
	nytena.aFotoana = uint16(data[18]) | uint16(data[19])<<8
	nytena.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	nytena.wFotoana = uint16(data[22]) | uint16(data[23])<<8
	nytena.wDaty = uint16(data[24]) | uint16(data[25])<<8
	nytena.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	nytena.habe = Unsignedinteger32r(Arraytounsignedinteger32(buffer))
}
