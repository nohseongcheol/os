/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "filsystem/msdospartition"
import . "minnemanager"

type TBiosparameterBlokk32 struct {
	jmp			[3]uint8
	softNavn		[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopier		uint8
	rotKatalogentry		uint16
	totaltsectors		uint16
	medierFiltype		uint8
	fatsectorAntall		uint16
	sectorpertrack		uint16
	headAntall		uint16
	skjultsectors		uint32
	totaltsectorAntall	uint32

	tabellStørrelse		uint32
	extFlagg		uint16
	fatVersjon		uint16
	rotcluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveTall		uint8
	reserved		uint8
	bootsignature		uint8
	volumid			uint32
	volumEtikett		[11]byte
	fatFiltypeEtikett	[8]byte
}

func (selv *TBiosparameterBlokk32) Init(data []byte) {
	copy(selv.jmp[:3], data[0:3])
	copy(selv.softNavn[:8], data[3:11])

	selv.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	selv.sectorspercluster = data[13]
	selv.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	selv.fatKopier = data[16]
	selv.rotKatalogentry = (uint16(data[17]) | uint16(data[18])<<8)
	selv.totaltsectors = (uint16(data[19]) | uint16(data[20])<<8)
	selv.medierFiltype = data[21]
	selv.fatsectorAntall = (uint16(data[22]) | uint16(data[23])<<8)
	selv.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	selv.headAntall = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	selv.skjultsectors = Unsignedinteger32r(Tabelltounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	selv.totaltsectorAntall = Unsignedinteger32r(Tabelltounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	selv.tabellStørrelse = Unsignedinteger32r(Tabelltounsignedinteger32(buffer1))

	selv.extFlagg = (uint16(data[40]) | uint16(data[41])<<8)
	selv.fatVersjon = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	selv.rotcluster = Unsignedinteger32r(Tabelltounsignedinteger32(buffer1))

	selv.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	selv.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(selv.reserved0[:12], data[52:64])

	selv.driveTall = data[64]
	selv.reserved = data[65]
	selv.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	selv.volumid = Unsignedinteger32r(Tabelltounsignedinteger32(buffer1))

	copy(selv.volumEtikett[:11], data[71:82])
	copy(selv.fatFiltypeEtikett[:8], data[82:90])

}

var console_2 = TConsole{}

func (selv *TBiosparameterBlokk32) Len(hd *TAvansertTeknologiattachment, partentry TPartitionTabellentry, filnavn []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	minnemanager := TMinnemanager{}
	bpbPeker := minnemanager.Malloc(90)
	bpbByte := GetBytefromPeker(uintptr(bpbPeker), 90, 90)
	var partitionAvstand = partentry.Startlba

	hd.Les28(partitionAvstand, &bpbByte, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbByte)

	var fatstart = partitionAvstand + uint32(bpb.reservedsectors)
	var fatStørrelse = bpb.tabellStørrelse

	var datastart = fatstart + fatStørrelse*uint32(bpb.fatKopier)

	var rotstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rotcluster-2)

	direntPeker := minnemanager.Malloc(512)
	direntByte := GetBytefromPeker(uintptr(direntPeker), 512, 512)
	hd.Les28(rotstart, &direntByte, 512)

	var dirent = [16]TKatalogentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].størrelse >= 0xFFFFFFFF {
			continue
		}

		if !LikByte(filnavn, dirent[i].navn[:len(filnavn)]) {
			continue
		}

		minnemanager.Ledig(bpbPeker)
		minnemanager.Ledig(direntPeker)
		return dirent[i].størrelse
	}
	minnemanager.Ledig(bpbPeker)
	minnemanager.Ledig(direntPeker)
	return 0
}
func (selv *TBiosparameterBlokk32) Les(hd *TAvansertTeknologiattachment, partentry TPartitionTabellentry, filnavn []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	minnemanager := TMinnemanager{}
	bpbPeker := minnemanager.Malloc(90)
	bpbByte := GetBytefromPeker(uintptr(bpbPeker), 90, 90)
	var partitionAvstand = partentry.Startlba

	hd.Les28(partitionAvstand, &bpbByte, 90)

	var bpb = TBiosparameterBlokk32{}
	bpb.Init(bpbByte)

	var fatstart = partitionAvstand + uint32(bpb.reservedsectors)
	var fatStørrelse = bpb.tabellStørrelse

	var datastart = fatstart + fatStørrelse*uint32(bpb.fatKopier)

	var rotstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rotcluster-2)

	direntPeker := minnemanager.Malloc(512)
	direntByte := GetBytefromPeker(uintptr(direntPeker), 512, 512)
	hd.Les28(rotstart, &direntByte, 512)

	var dirent = [16]TKatalogentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].størrelse >= 0xFFFFFFFF {
			continue
		}

		if !LikByte(filnavn, dirent[i].navn[:len(filnavn)]) {
			continue
		}

		var firstFilcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLav))

		var Størrelse = int32(dirent[i].størrelse)
		var nesteFilcluster = int32(firstFilcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Størrelse > 0 {
			var filsector = datastart + uint32(bpb.sectorspercluster)*uint32(nesteFilcluster-2)
			var sectorAvstand int = 0

			for ; Størrelse > 0; Størrelse -= 512 {

				var buffer3 []byte

				if dirent[i].størrelse > 512 {
					buffer3 = buffer_2[:512]
					hd.Les28(filsector+uint32(sectorAvstand), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].størrelse]
					hd.Les28(filsector+uint32(sectorAvstand), &buffer3, int(dirent[i].størrelse))
				}

				copy(data[int32(dirent[i].størrelse)-Størrelse:], buffer3)

				sectorAvstand++

				if sectorAvstand > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforGjeldendecluster = uint32(nesteFilcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Les28(fatstart+fatsectorforGjeldendecluster, &fatbuf, 512)

			var fatAvstandInnsectorforGjeldendecluster = nesteFilcluster % 128
			var startAvstand = fatAvstandInnsectorforGjeldendecluster * 4
			var sluttAvstand = fatAvstandInnsectorforGjeldendecluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startAvstand:sluttAvstand])

			nesteFilcluster = int32(Unsignedinteger32r(Tabelltounsignedinteger32(buffer4)))
		}
	}
	minnemanager.Ledig(bpbPeker)
	minnemanager.Ledig(direntPeker)
}

type TKatalogentryfat32 struct {
	navn		[8]byte
	ext		[3]byte
	egenskaper	uint8
	reserved	uint8
	cTidtenth	uint8
	cTid		uint16
	cDato		uint16
	aTid		uint16
	firstclusterhi	uint16
	wTid		uint16
	wDato		uint16
	firstclusterLav	uint16
	størrelse	uint32
}

func (selv *TKatalogentryfat32) Init(data [32]byte) {
	copy(selv.navn[:8], data[0:8])
	copy(selv.ext[:3], data[8:11])
	selv.egenskaper = data[11]
	selv.reserved = data[12]
	selv.cTidtenth = data[13]
	selv.cTid = uint16(data[14]) | uint16(data[15])<<8
	selv.cDato = uint16(data[16]) | uint16(data[17])<<8
	selv.aTid = uint16(data[18]) | uint16(data[19])<<8
	selv.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	selv.wTid = uint16(data[22]) | uint16(data[23])<<8
	selv.wDato = uint16(data[24]) | uint16(data[25])<<8
	selv.firstclusterLav = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	selv.størrelse = Unsignedinteger32r(Tabelltounsignedinteger32(buffer))
}
