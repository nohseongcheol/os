package fat

import . "util"
import . "konzola"
import . "driver/ata"
import . "súborSystém/msdospartition"
import . "pamäťmanager"

type TBiosparameterBlok32 struct {
	jmp			[3]uint8
	softNázov		[8]byte
	bajtypersector		uint16
	sectorspercluster	uint8
	rezervovanásectors	uint16
	fatKopírovať		uint8
	koreňAdresárpoložka	uint16
	celkomsectors		uint16
	médiáTyp		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	skrytésectors		uint32
	celkomsectorcount	uint32

	tabuľkaVeľkosť		uint32
	extPríznaky		uint16
	fatVerzia		uint16
	koreňcluster		uint32
	fatInformácie		uint16
	backupsector		uint16
	rezervovaná0		[12]uint8
	driveČíslo		uint8
	rezervovaná		uint8
	bootsignature		uint8
	hlasitosťIdentifikátor	uint32
	hlasitosťPopisok	[11]byte
	fatTypPopisok		[8]byte
}

func (vlastný *TBiosparameterBlok32) Init(data []byte) {
	copy(vlastný.jmp[:3], data[0:3])
	copy(vlastný.softNázov[:8], data[3:11])

	vlastný.bajtypersector = (uint16(data[11]) | uint16(data[12])<<8)
	vlastný.sectorspercluster = data[13]
	vlastný.rezervovanásectors = (uint16(data[14]) | uint16(data[15])<<8)
	vlastný.fatKopírovať = data[16]
	vlastný.koreňAdresárpoložka = (uint16(data[17]) | uint16(data[18])<<8)
	vlastný.celkomsectors = (uint16(data[19]) | uint16(data[20])<<8)
	vlastný.médiáTyp = data[21]
	vlastný.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	vlastný.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	vlastný.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	vlastný.skrytésectors = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	vlastný.celkomsectorcount = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	vlastný.tabuľkaVeľkosť = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	vlastný.extPríznaky = (uint16(data[40]) | uint16(data[41])<<8)
	vlastný.fatVerzia = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	vlastný.koreňcluster = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	vlastný.fatInformácie = (uint16(data[48]) | uint16(data[49])<<8)
	vlastný.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(vlastný.rezervovaná0[:12], data[52:64])

	vlastný.driveČíslo = data[64]
	vlastný.rezervovaná = data[65]
	vlastný.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	vlastný.hlasitosťIdentifikátor = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	copy(vlastný.hlasitosťPopisok[:11], data[71:82])
	copy(vlastný.fatTypPopisok[:8], data[82:90])

}

var konzola_2 = TKonzola{}

func (vlastný *TBiosparameterBlok32) Len(hd *TPokročiléTechnológiaattachment, partpoložka TPartitionTabuľkapoložka, názovsúboru []byte) uint32 {

	if partpoložka.PartitionIdentifikátor == 0x00 {
		return 0
	}

	pamäťmanager := TPamäťmanager{}
	bpbKurzor := pamäťmanager.Malloc(90)
	bpbBajty := GetBajtyzKurzor(uintptr(bpbKurzor), 90, 90)
	var partitionPosunutie = partpoložka.Spustiťlba

	hd.Čítanie28(partitionPosunutie, &bpbBajty, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajty)

	var fatSpustiť = partitionPosunutie + uint32(bpb.rezervovanásectors)
	var fatVeľkosť = bpb.tabuľkaVeľkosť

	var dataSpustiť = fatSpustiť + fatVeľkosť*uint32(bpb.fatKopírovať)

	var koreňSpustiť = dataSpustiť + uint32(bpb.sectorspercluster)*(bpb.koreňcluster-2)

	direntKurzor := pamäťmanager.Malloc(512)
	direntBajty := GetBajtyzKurzor(uintptr(direntKurzor), 512, 512)
	hd.Čítanie28(koreňSpustiť, &direntBajty, 512)

	var dirent = [16]TAdresárpoložkafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajty[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].názov[0] == 0x00 {
			break
		}

		if dirent[i].veľkosť >= 0xFFFFFFFF {
			continue
		}

		if !RovnakáBajty(názovsúboru, dirent[i].názov[:len(názovsúboru)]) {
			continue
		}

		pamäťmanager.Voľné(bpbKurzor)
		pamäťmanager.Voľné(direntKurzor)
		return dirent[i].veľkosť
	}
	pamäťmanager.Voľné(bpbKurzor)
	pamäťmanager.Voľné(direntKurzor)
	return 0
}
func (vlastný *TBiosparameterBlok32) Čítanie(hd *TPokročiléTechnológiaattachment, partpoložka TPartitionTabuľkapoložka, názovsúboru []byte, data []byte) {

	if partpoložka.PartitionIdentifikátor == 0x00 {
		return
	}

	pamäťmanager := TPamäťmanager{}
	bpbKurzor := pamäťmanager.Malloc(90)
	bpbBajty := GetBajtyzKurzor(uintptr(bpbKurzor), 90, 90)
	var partitionPosunutie = partpoložka.Spustiťlba

	hd.Čítanie28(partitionPosunutie, &bpbBajty, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajty)

	var fatSpustiť = partitionPosunutie + uint32(bpb.rezervovanásectors)
	var fatVeľkosť = bpb.tabuľkaVeľkosť

	var dataSpustiť = fatSpustiť + fatVeľkosť*uint32(bpb.fatKopírovať)

	var koreňSpustiť = dataSpustiť + uint32(bpb.sectorspercluster)*(bpb.koreňcluster-2)

	direntKurzor := pamäťmanager.Malloc(512)
	direntBajty := GetBajtyzKurzor(uintptr(direntKurzor), 512, 512)
	hd.Čítanie28(koreňSpustiť, &direntBajty, 512)

	var dirent = [16]TAdresárpoložkafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajty[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].názov[0] == 0x00 {
			break
		}

		if dirent[i].veľkosť >= 0xFFFFFFFF {
			continue
		}

		if !RovnakáBajty(názovsúboru, dirent[i].názov[:len(názovsúboru)]) {
			continue
		}

		var firstSúborcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterNízka))

		var Veľkosť = int32(dirent[i].veľkosť)
		var nasledujúciSúborcluster = int32(firstSúborcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Veľkosť > 0 {
			var súborsector = dataSpustiť + uint32(bpb.sectorspercluster)*uint32(nasledujúciSúborcluster-2)
			var sectorPosunutie int = 0

			for ; Veľkosť > 0; Veľkosť -= 512 {

				var buffer3 []byte

				if dirent[i].veľkosť > 512 {
					buffer3 = buffer_2[:512]
					hd.Čítanie28(súborsector+uint32(sectorPosunutie), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].veľkosť]
					hd.Čítanie28(súborsector+uint32(sectorPosunutie), &buffer3, int(dirent[i].veľkosť))
				}

				copy(data[int32(dirent[i].veľkosť)-Veľkosť:], buffer3)

				sectorPosunutie++

				if sectorPosunutie > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforAktuálnycluster = uint32(nasledujúciSúborcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Čítanie28(fatSpustiť+fatsectorforAktuálnycluster, &fatbuf, 512)

			var fatPosunutienasectorforAktuálnycluster = nasledujúciSúborcluster % 128
			var spustiťPosunutie = fatPosunutienasectorforAktuálnycluster * 4
			var koniecPosunutie = fatPosunutienasectorforAktuálnycluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[spustiťPosunutie:koniecPosunutie])

			nasledujúciSúborcluster = int32(Unsignedinteger32r(Poletounsignedinteger32(buffer4)))
		}
	}
	pamäťmanager.Voľné(bpbKurzor)
	pamäťmanager.Voľné(direntKurzor)
}

type TAdresárpoložkafat32 struct {
	názov			[8]byte
	ext			[3]byte
	atribúty		uint8
	rezervovaná		uint8
	cČastenth		uint8
	cČas			uint16
	cDátum			uint16
	aČas			uint16
	firstclusterhi		uint16
	wČas			uint16
	wDátum			uint16
	firstclusterNízka	uint16
	veľkosť			uint32
}

func (vlastný *TAdresárpoložkafat32) Init(data [32]byte) {
	copy(vlastný.názov[:8], data[0:8])
	copy(vlastný.ext[:3], data[8:11])
	vlastný.atribúty = data[11]
	vlastný.rezervovaná = data[12]
	vlastný.cČastenth = data[13]
	vlastný.cČas = uint16(data[14]) | uint16(data[15])<<8
	vlastný.cDátum = uint16(data[16]) | uint16(data[17])<<8
	vlastný.aČas = uint16(data[18]) | uint16(data[19])<<8
	vlastný.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	vlastný.wČas = uint16(data[22]) | uint16(data[23])<<8
	vlastný.wDátum = uint16(data[24]) | uint16(data[25])<<8
	vlastný.firstclusterNízka = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	vlastný.veľkosť = Unsignedinteger32r(Poletounsignedinteger32(buffer))
}
