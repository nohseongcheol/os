package fat

import . "util"
import . "konsol"
import . "driver/ata"
import . "arkivsystem/msdospartition"
import . "minnemanager"

type TFilsystemsparametrar32 struct {
	jmp			[3]uint8
	softNamn		[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	reserveratsectors	uint16
	fatKopiera		uint8
	rotKatalogpost		uint16
	totaltsectors		uint16
	mediaTyp		uint8
	fatsectorAntal		uint16
	sectorpertrack		uint16
	headAntal		uint16
	doltsectors		uint32
	totaltsectorAntal	uint32

	tabellStorlek	uint32
	extFlaggor	uint16
	fatversion	uint16
	rotcluster	uint32
	fatInformation	uint16
	backupsector	uint16
	reserverat0	[12]uint8
	driveNummer	uint8
	reserverat	uint8
	bootsignature	uint8
	volymid		uint32
	volymetikett	[11]byte
	fatTypetikett	[8]byte
}

func (själv *TFilsystemsparametrar32) Init(data []byte) {
	copy(själv.jmp[:3], data[0:3])
	copy(själv.softNamn[:8], data[3:11])

	själv.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	själv.sectorspercluster = data[13]
	själv.reserveratsectors = (uint16(data[14]) | uint16(data[15])<<8)
	själv.fatKopiera = data[16]
	själv.rotKatalogpost = (uint16(data[17]) | uint16(data[18])<<8)
	själv.totaltsectors = (uint16(data[19]) | uint16(data[20])<<8)
	själv.mediaTyp = data[21]
	själv.fatsectorAntal = (uint16(data[22]) | uint16(data[23])<<8)
	själv.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	själv.headAntal = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	själv.doltsectors = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	själv.totaltsectorAntal = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	själv.tabellStorlek = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	själv.extFlaggor = (uint16(data[40]) | uint16(data[41])<<8)
	själv.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	själv.rotcluster = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	själv.fatInformation = (uint16(data[48]) | uint16(data[49])<<8)
	själv.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(själv.reserverat0[:12], data[52:64])

	själv.driveNummer = data[64]
	själv.reserverat = data[65]
	själv.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	själv.volymid = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	copy(själv.volymetikett[:11], data[71:82])
	copy(själv.fatTypetikett[:8], data[82:90])

}

var konsol_2 = TKonsol{}

func (själv *TFilsystemsparametrar32) Len(hd *TAvanceratTeknikattachment, partpost TPartitionTabellpost, filnamn []byte) uint32 {

	if partpost.Partitionid == 0x00 {
		return 0
	}

	minnemanager := TMinnemanager{}
	bpbMuspekare := minnemanager.Tilldela_minne(90)
	bpbByte := GetBytefromMuspekare(uintptr(bpbMuspekare), 90, 90)
	var partitionFörskjutning = partpost.Startalba

	hd.Läs28(partitionFörskjutning, &bpbByte, 90)

	var filsystemsparametrar = TFilsystemsparametrar32{}
	filsystemsparametrar.Init(bpbByte)

	var fatStarta = partitionFörskjutning + uint32(filsystemsparametrar.reserveratsectors)
	var fatStorlek = filsystemsparametrar.tabellStorlek

	var dataStarta = fatStarta + fatStorlek*uint32(filsystemsparametrar.fatKopiera)

	var rotStarta = dataStarta + uint32(filsystemsparametrar.sectorspercluster)*(filsystemsparametrar.rotcluster-2)

	direntMuspekare := minnemanager.Tilldela_minne(512)
	direntByte := GetBytefromMuspekare(uintptr(direntMuspekare), 512, 512)
	hd.Läs28(rotStarta, &direntByte, 512)

	var dirent = [16]TKatalogpostfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].namn[0] == 0x00 {
			break
		}

		if dirent[i].storlek >= 0xFFFFFFFF {
			continue
		}

		if !LikaByte(filnamn, dirent[i].namn[:len(filnamn)]) {
			continue
		}

		minnemanager.Ledigt(bpbMuspekare)
		minnemanager.Ledigt(direntMuspekare)
		return dirent[i].storlek
	}
	minnemanager.Ledigt(bpbMuspekare)
	minnemanager.Ledigt(direntMuspekare)
	return 0
}
func (själv *TFilsystemsparametrar32) Läs(hd *TAvanceratTeknikattachment, partpost TPartitionTabellpost, filnamn []byte, data []byte) {

	if partpost.Partitionid == 0x00 {
		return
	}

	minnemanager := TMinnemanager{}
	bpbMuspekare := minnemanager.Tilldela_minne(90)
	bpbByte := GetBytefromMuspekare(uintptr(bpbMuspekare), 90, 90)
	var partitionFörskjutning = partpost.Startalba

	hd.Läs28(partitionFörskjutning, &bpbByte, 90)

	var filsystemsparametrar = TFilsystemsparametrar32{}
	filsystemsparametrar.Init(bpbByte)

	var fatStarta = partitionFörskjutning + uint32(filsystemsparametrar.reserveratsectors)
	var fatStorlek = filsystemsparametrar.tabellStorlek

	var dataStarta = fatStarta + fatStorlek*uint32(filsystemsparametrar.fatKopiera)

	var rotStarta = dataStarta + uint32(filsystemsparametrar.sectorspercluster)*(filsystemsparametrar.rotcluster-2)

	direntMuspekare := minnemanager.Tilldela_minne(512)
	direntByte := GetBytefromMuspekare(uintptr(direntMuspekare), 512, 512)
	hd.Läs28(rotStarta, &direntByte, 512)

	var dirent = [16]TKatalogpostfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].namn[0] == 0x00 {
			break
		}

		if dirent[i].storlek >= 0xFFFFFFFF {
			continue
		}

		if !LikaByte(filnamn, dirent[i].namn[:len(filnamn)]) {
			continue
		}

		var firstArkivcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLåg))

		var Storlek = int32(dirent[i].storlek)
		var nästaArkivcluster = int32(firstArkivcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Storlek > 0 {
			var arkivsector = dataStarta + uint32(filsystemsparametrar.sectorspercluster)*uint32(nästaArkivcluster-2)
			var sectorFörskjutning int = 0

			for ; Storlek > 0; Storlek -= 512 {

				var buffer3 []byte

				if dirent[i].storlek > 512 {
					buffer3 = buffer_2[:512]
					hd.Läs28(arkivsector+uint32(sectorFörskjutning), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].storlek]
					hd.Läs28(arkivsector+uint32(sectorFörskjutning), &buffer3, int(dirent[i].storlek))
				}

				copy(data[int32(dirent[i].storlek)-Storlek:], buffer3)

				sectorFörskjutning++

				if sectorFörskjutning > int(filsystemsparametrar.sectorspercluster) {
					break
				}

			}

			var fatsectorforAktuellcluster = uint32(nästaArkivcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Läs28(fatStarta+fatsectorforAktuellcluster, &fatbuf, 512)

			var fatFörskjutningisectorforAktuellcluster = nästaArkivcluster % 128
			var startaFörskjutning = fatFörskjutningisectorforAktuellcluster * 4
			var slutFörskjutning = fatFörskjutningisectorforAktuellcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startaFörskjutning:slutFörskjutning])

			nästaArkivcluster = int32(Unsignedinteger32r(Vektortounsignedinteger32(buffer4)))
		}
	}
	minnemanager.Ledigt(bpbMuspekare)
	minnemanager.Ledigt(direntMuspekare)
}

type TKatalogpostfat32 struct {
	namn		[8]byte
	ext		[3]byte
	attribut_2	uint8
	reserverat	uint8
	cTidtenth	uint8
	cTid		uint16
	cDatum		uint16
	aTid		uint16
	firstclusterhi	uint16
	wTid		uint16
	wDatum		uint16
	firstclusterLåg	uint16
	storlek		uint32
}

func (själv *TKatalogpostfat32) Init(data [32]byte) {
	copy(själv.namn[:8], data[0:8])
	copy(själv.ext[:3], data[8:11])
	själv.attribut_2 = data[11]
	själv.reserverat = data[12]
	själv.cTidtenth = data[13]
	själv.cTid = uint16(data[14]) | uint16(data[15])<<8
	själv.cDatum = uint16(data[16]) | uint16(data[17])<<8
	själv.aTid = uint16(data[18]) | uint16(data[19])<<8
	själv.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	själv.wTid = uint16(data[22]) | uint16(data[23])<<8
	själv.wDatum = uint16(data[24]) | uint16(data[25])<<8
	själv.firstclusterLåg = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	själv.storlek = Unsignedinteger32r(Vektortounsignedinteger32(buffer))
}
