/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "failSistem/msdospartition"
import . "ingatanmanager"

type TParameter_sistem_fail32 struct {
	jmp			[3]uint8
	softNama		[8]byte
	baitpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatSalin		uint8
	rootdirektorientry	uint16
	jumlahsectors		uint16
	mediaJenis		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	sembunyisectors		uint32
	jumlahsectorcount	uint32

	jadualSaiz	uint32
	extBendera	uint16
	fatVersi	uint16
	rootcluster	uint32
	fatMaklumat	uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveNOMBOR	uint8
	reserved	uint8
	bootsignature	uint8
	volumid		uint32
	volumlabel	[11]byte
	fatJenislabel	[8]byte
}

func (diri *TParameter_sistem_fail32) Init(data []byte) {
	copy(diri.jmp[:3], data[0:3])
	copy(diri.softNama[:8], data[3:11])

	diri.baitpersector = (uint16(data[11]) | uint16(data[12])<<8)
	diri.sectorspercluster = data[13]
	diri.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	diri.fatSalin = data[16]
	diri.rootdirektorientry = (uint16(data[17]) | uint16(data[18])<<8)
	diri.jumlahsectors = (uint16(data[19]) | uint16(data[20])<<8)
	diri.mediaJenis = data[21]
	diri.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	diri.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	diri.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	diri.sembunyisectors = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	diri.jumlahsectorcount = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	diri.jadualSaiz = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	diri.extBendera = (uint16(data[40]) | uint16(data[41])<<8)
	diri.fatVersi = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	diri.rootcluster = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	diri.fatMaklumat = (uint16(data[48]) | uint16(data[49])<<8)
	diri.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(diri.reserved0[:12], data[52:64])

	diri.driveNOMBOR = data[64]
	diri.reserved = data[65]
	diri.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	diri.volumid = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	copy(diri.volumlabel[:11], data[71:82])
	copy(diri.fatJenislabel[:8], data[82:90])

}

var console_2 = TConsole{}

func (diri *TParameter_sistem_fail32) Len(hd *TLanjutanTeknologiattachment, partentry TPartitionJadualentry, namafail []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	ingatanmanager := TIngatanmanager{}
	bpbPenuding := ingatanmanager.Peruntukkan_ingatan(90)
	bpbBait := GetBaitfromPenuding(uintptr(bpbPenuding), 90, 90)
	var partitionoffset = partentry.Mulalba

	hd.Baca28(partitionoffset, &bpbBait, 90)

	var parameter_sistem_fail = TParameter_sistem_fail32{}
	parameter_sistem_fail.Init(bpbBait)

	var fatMula = partitionoffset + uint32(parameter_sistem_fail.reservedsectors)
	var fatSaiz = parameter_sistem_fail.jadualSaiz

	var dataMula = fatMula + fatSaiz*uint32(parameter_sistem_fail.fatSalin)

	var rootMula = dataMula + uint32(parameter_sistem_fail.sectorspercluster)*(parameter_sistem_fail.rootcluster-2)

	direntPenuding := ingatanmanager.Peruntukkan_ingatan(512)
	direntBait := GetBaitfromPenuding(uintptr(direntPenuding), 512, 512)
	hd.Baca28(rootMula, &direntBait, 512)

	var dirent = [16]TDirektorientryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBait[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nama[0] == 0x00 {
			break
		}

		if dirent[i].saiz >= 0xFFFFFFFF {
			continue
		}

		if !SamaBait(namafail, dirent[i].nama[:len(namafail)]) {
			continue
		}

		ingatanmanager.Bebas(bpbPenuding)
		ingatanmanager.Bebas(direntPenuding)
		return dirent[i].saiz
	}
	ingatanmanager.Bebas(bpbPenuding)
	ingatanmanager.Bebas(direntPenuding)
	return 0
}
func (diri *TParameter_sistem_fail32) Baca(hd *TLanjutanTeknologiattachment, partentry TPartitionJadualentry, namafail []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	ingatanmanager := TIngatanmanager{}
	bpbPenuding := ingatanmanager.Peruntukkan_ingatan(90)
	bpbBait := GetBaitfromPenuding(uintptr(bpbPenuding), 90, 90)
	var partitionoffset = partentry.Mulalba

	hd.Baca28(partitionoffset, &bpbBait, 90)

	var parameter_sistem_fail = TParameter_sistem_fail32{}
	parameter_sistem_fail.Init(bpbBait)

	var fatMula = partitionoffset + uint32(parameter_sistem_fail.reservedsectors)
	var fatSaiz = parameter_sistem_fail.jadualSaiz

	var dataMula = fatMula + fatSaiz*uint32(parameter_sistem_fail.fatSalin)

	var rootMula = dataMula + uint32(parameter_sistem_fail.sectorspercluster)*(parameter_sistem_fail.rootcluster-2)

	direntPenuding := ingatanmanager.Peruntukkan_ingatan(512)
	direntBait := GetBaitfromPenuding(uintptr(direntPenuding), 512, 512)
	hd.Baca28(rootMula, &direntBait, 512)

	var dirent = [16]TDirektorientryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBait[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nama[0] == 0x00 {
			break
		}

		if dirent[i].saiz >= 0xFFFFFFFF {
			continue
		}

		if !SamaBait(namafail, dirent[i].nama[:len(namafail)]) {
			continue
		}

		var firstFailcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterRendah))

		var Saiz = int32(dirent[i].saiz)
		var berikutnyaFailcluster = int32(firstFailcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Saiz > 0 {
			var failsector = dataMula + uint32(parameter_sistem_fail.sectorspercluster)*uint32(berikutnyaFailcluster-2)
			var sectoroffset int = 0

			for ; Saiz > 0; Saiz -= 512 {

				var buffer3 []byte

				if dirent[i].saiz > 512 {
					buffer3 = buffer_2[:512]
					hd.Baca28(failsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].saiz]
					hd.Baca28(failsector+uint32(sectoroffset), &buffer3, int(dirent[i].saiz))
				}

				copy(data[int32(dirent[i].saiz)-Saiz:], buffer3)

				sectoroffset++

				if sectoroffset > int(parameter_sistem_fail.sectorspercluster) {
					break
				}

			}

			var fatsectorforSemasacluster = uint32(berikutnyaFailcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Baca28(fatMula+fatsectorforSemasacluster, &fatbuf, 512)

			var fatoffsetMasuksectorforSemasacluster = berikutnyaFailcluster % 128
			var mulaoffset = fatoffsetMasuksectorforSemasacluster * 4
			var tamatoffset = fatoffsetMasuksectorforSemasacluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[mulaoffset:tamatoffset])

			berikutnyaFailcluster = int32(Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer4)))
		}
	}
	ingatanmanager.Bebas(bpbPenuding)
	ingatanmanager.Bebas(direntPenuding)
}

type TDirektorientryfat32 struct {
	nama			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cMasatenth		uint8
	cMasa			uint16
	cTarikh			uint16
	aMasa			uint16
	firstclusterhi		uint16
	wMasa			uint16
	wTarikh			uint16
	firstclusterRendah	uint16
	saiz			uint32
}

func (diri *TDirektorientryfat32) Init(data [32]byte) {
	copy(diri.nama[:8], data[0:8])
	copy(diri.ext[:3], data[8:11])
	diri.attributes = data[11]
	diri.reserved = data[12]
	diri.cMasatenth = data[13]
	diri.cMasa = uint16(data[14]) | uint16(data[15])<<8
	diri.cTarikh = uint16(data[16]) | uint16(data[17])<<8
	diri.aMasa = uint16(data[18]) | uint16(data[19])<<8
	diri.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	diri.wMasa = uint16(data[22]) | uint16(data[23])<<8
	diri.wTarikh = uint16(data[24]) | uint16(data[25])<<8
	diri.firstclusterRendah = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	diri.saiz = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer))
}
