package fat

import . "util"
import . "console"
import . "driver/ata"
import . "failsSistēma/msdospartition"
import . "atmiņamanager"

type TBiosparameterBloks32 struct {
	jmp			[3]uint8
	softNosaukums		[8]byte
	baitipersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopēt		uint8
	sakneMapeieraksts	uint16
	kopāsectors		uint16
	datunesējiTips		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	slēptssectors		uint32
	kopāsectorcount		uint32

	tabulaIzmērs	uint32
	extKarogi	uint16
	fatVersija	uint16
	saknecluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveSkaitlis	uint8
	reserved	uint8
	bootsignature	uint8
	tilpumsid	uint32
	tilpumsEtiķete	[11]byte
	fatTipsEtiķete	[8]byte
}

func (pats *TBiosparameterBloks32) Init(data []byte) {
	copy(pats.jmp[:3], data[0:3])
	copy(pats.softNosaukums[:8], data[3:11])

	pats.baitipersector = (uint16(data[11]) | uint16(data[12])<<8)
	pats.sectorspercluster = data[13]
	pats.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	pats.fatKopēt = data[16]
	pats.sakneMapeieraksts = (uint16(data[17]) | uint16(data[18])<<8)
	pats.kopāsectors = (uint16(data[19]) | uint16(data[20])<<8)
	pats.datunesējiTips = data[21]
	pats.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	pats.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	pats.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	pats.slēptssectors = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	pats.kopāsectorcount = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	pats.tabulaIzmērs = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	pats.extKarogi = (uint16(data[40]) | uint16(data[41])<<8)
	pats.fatVersija = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	pats.saknecluster = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	pats.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	pats.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(pats.reserved0[:12], data[52:64])

	pats.driveSkaitlis = data[64]
	pats.reserved = data[65]
	pats.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	pats.tilpumsid = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	copy(pats.tilpumsEtiķete[:11], data[71:82])
	copy(pats.fatTipsEtiķete[:8], data[82:90])

}

var console_2 = TConsole{}

func (pats *TBiosparameterBloks32) Len(hd *TPaplašinātiTehnoloģijaattachment, partieraksts TPartitionTabulaieraksts, failanosaukums []byte) uint32 {

	if partieraksts.Partitionid == 0x00 {
		return 0
	}

	atmiņamanager := TAtmiņamanager{}
	bpbKursors := atmiņamanager.Malloc(90)
	bpbBaiti := GetBaitifromKursors(uintptr(bpbKursors), 90, 90)
	var partitionoffset = partieraksts.Startētlba

	hd.Lasīt28(partitionoffset, &bpbBaiti, 90)

	var bpb = TBiosparameterBloks32{}
	bpb.Init(bpbBaiti)

	var fatStartēt = partitionoffset + uint32(bpb.reservedsectors)
	var fatIzmērs = bpb.tabulaIzmērs

	var dataStartēt = fatStartēt + fatIzmērs*uint32(bpb.fatKopēt)

	var sakneStartēt = dataStartēt + uint32(bpb.sectorspercluster)*(bpb.saknecluster-2)

	direntKursors := atmiņamanager.Malloc(512)
	direntBaiti := GetBaitifromKursors(uintptr(direntKursors), 512, 512)
	hd.Lasīt28(sakneStartēt, &direntBaiti, 512)

	var dirent = [16]TMapeierakstsfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaiti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nosaukums[0] == 0x00 {
			break
		}

		if dirent[i].izmērs >= 0xFFFFFFFF {
			continue
		}

		if !VienādsBaiti(failanosaukums, dirent[i].nosaukums[:len(failanosaukums)]) {
			continue
		}

		atmiņamanager.Brīvs(bpbKursors)
		atmiņamanager.Brīvs(direntKursors)
		return dirent[i].izmērs
	}
	atmiņamanager.Brīvs(bpbKursors)
	atmiņamanager.Brīvs(direntKursors)
	return 0
}
func (pats *TBiosparameterBloks32) Lasīt(hd *TPaplašinātiTehnoloģijaattachment, partieraksts TPartitionTabulaieraksts, failanosaukums []byte, data []byte) {

	if partieraksts.Partitionid == 0x00 {
		return
	}

	atmiņamanager := TAtmiņamanager{}
	bpbKursors := atmiņamanager.Malloc(90)
	bpbBaiti := GetBaitifromKursors(uintptr(bpbKursors), 90, 90)
	var partitionoffset = partieraksts.Startētlba

	hd.Lasīt28(partitionoffset, &bpbBaiti, 90)

	var bpb = TBiosparameterBloks32{}
	bpb.Init(bpbBaiti)

	var fatStartēt = partitionoffset + uint32(bpb.reservedsectors)
	var fatIzmērs = bpb.tabulaIzmērs

	var dataStartēt = fatStartēt + fatIzmērs*uint32(bpb.fatKopēt)

	var sakneStartēt = dataStartēt + uint32(bpb.sectorspercluster)*(bpb.saknecluster-2)

	direntKursors := atmiņamanager.Malloc(512)
	direntBaiti := GetBaitifromKursors(uintptr(direntKursors), 512, 512)
	hd.Lasīt28(sakneStartēt, &direntBaiti, 512)

	var dirent = [16]TMapeierakstsfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaiti[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nosaukums[0] == 0x00 {
			break
		}

		if dirent[i].izmērs >= 0xFFFFFFFF {
			continue
		}

		if !VienādsBaiti(failanosaukums, dirent[i].nosaukums[:len(failanosaukums)]) {
			continue
		}

		var pirmaisFailscluster = (uint32(dirent[i].pirmaisclusterhi)<<16 | uint32(dirent[i].pirmaisclusterKlusi))

		var Izmērs = int32(dirent[i].izmērs)
		var nākamaisFailscluster = int32(pirmaisFailscluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Izmērs > 0 {
			var failssector = dataStartēt + uint32(bpb.sectorspercluster)*uint32(nākamaisFailscluster-2)
			var sectoroffset int = 0

			for ; Izmērs > 0; Izmērs -= 512 {

				var buffer3 []byte

				if dirent[i].izmērs > 512 {
					buffer3 = buffer_2[:512]
					hd.Lasīt28(failssector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].izmērs]
					hd.Lasīt28(failssector+uint32(sectoroffset), &buffer3, int(dirent[i].izmērs))
				}

				copy(data[int32(dirent[i].izmērs)-Izmērs:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforPašreizējaiscluster = uint32(nākamaisFailscluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lasīt28(fatStartēt+fatsectorforPašreizējaiscluster, &fatbuf, 512)

			var fatoffsetIenākošāsectorforPašreizējaiscluster = nākamaisFailscluster % 128
			var startētoffset = fatoffsetIenākošāsectorforPašreizējaiscluster * 4
			var beigasoffset = fatoffsetIenākošāsectorforPašreizējaiscluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startētoffset:beigasoffset])

			nākamaisFailscluster = int32(Unsignedinteger32r(Masīvstounsignedinteger32(buffer4)))
		}
	}
	atmiņamanager.Brīvs(bpbKursors)
	atmiņamanager.Brīvs(direntKursors)
}

type TMapeierakstsfat32 struct {
	nosaukums		[8]byte
	ext			[3]byte
	atribūti		uint8
	reserved		uint8
	cLaikstenth		uint8
	cLaiks			uint16
	cDatums			uint16
	aLaiks			uint16
	pirmaisclusterhi	uint16
	wLaiks			uint16
	wDatums			uint16
	pirmaisclusterKlusi	uint16
	izmērs			uint32
}

func (pats *TMapeierakstsfat32) Init(data [32]byte) {
	copy(pats.nosaukums[:8], data[0:8])
	copy(pats.ext[:3], data[8:11])
	pats.atribūti = data[11]
	pats.reserved = data[12]
	pats.cLaikstenth = data[13]
	pats.cLaiks = uint16(data[14]) | uint16(data[15])<<8
	pats.cDatums = uint16(data[16]) | uint16(data[17])<<8
	pats.aLaiks = uint16(data[18]) | uint16(data[19])<<8
	pats.pirmaisclusterhi = uint16(data[20]) | uint16(data[21])<<8
	pats.wLaiks = uint16(data[22]) | uint16(data[23])<<8
	pats.wDatums = uint16(data[24]) | uint16(data[25])<<8
	pats.pirmaisclusterKlusi = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	pats.izmērs = Unsignedinteger32r(Masīvstounsignedinteger32(buffer))
}
