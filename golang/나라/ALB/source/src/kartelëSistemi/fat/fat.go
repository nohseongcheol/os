package fat

import . "util"
import . "konsolë"
import . "driver/ata"
import . "kartelëSistemi/msdospartition"
import . "memoriaManazhuesi"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softEmri		[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopjo		uint8
	rrënjëDosjeentry	uint16
	gjithsejsectors		uint16
	suportiLloji		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	padukshëmsectors	uint32
	gjithsejsectorcount	uint32

	tabelaMadhësia	uint32
	extFlamurka	uint16
	fatversion	uint16
	rrënjëcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	nisjasignature	uint8
	vëllimid	uint32
	vëllimEtiketë	[11]byte
	fatLlojiEtiketë	[8]byte
}

func (vetvetja *TBiosparameterblock32) Init(data []byte) {
	copy(vetvetja.jmp[:3], data[0:3])
	copy(vetvetja.softEmri[:8], data[3:11])

	vetvetja.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	vetvetja.sectorspercluster = data[13]
	vetvetja.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	vetvetja.fatKopjo = data[16]
	vetvetja.rrënjëDosjeentry = (uint16(data[17]) | uint16(data[18])<<8)
	vetvetja.gjithsejsectors = (uint16(data[19]) | uint16(data[20])<<8)
	vetvetja.suportiLloji = data[21]
	vetvetja.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	vetvetja.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	vetvetja.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	vetvetja.padukshëmsectors = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	vetvetja.gjithsejsectorcount = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	vetvetja.tabelaMadhësia = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	vetvetja.extFlamurka = (uint16(data[40]) | uint16(data[41])<<8)
	vetvetja.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	vetvetja.rrënjëcluster = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	vetvetja.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	vetvetja.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(vetvetja.reserved0[:12], data[52:64])

	vetvetja.drivenumber = data[64]
	vetvetja.reserved = data[65]
	vetvetja.nisjasignature = data[66]

	copy(buffer1[:4], data[67:71])
	vetvetja.vëllimid = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	copy(vetvetja.vëllimEtiketë[:11], data[71:82])
	copy(vetvetja.fatLlojiEtiketë[:8], data[82:90])

}

var konsolë_2 = TKonsolë{}

func (vetvetja *TBiosparameterblock32) Len(hd *TTëmëtejshmetechnologyattachment, partentry TPartitionTabelaentry, emriifile []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	memoriaManazhuesi := TMemoriaManazhuesi{}
	bpbKursori := memoriaManazhuesi.Malloc(90)
	bpbbytes := GetbytesfromKursori(uintptr(bpbKursori), 90, 90)
	var partitionoffset = partentry.Fillolba

	hd.Leximi28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatFillo = partitionoffset + uint32(bpb.reservedsectors)
	var fatMadhësia = bpb.tabelaMadhësia

	var dataFillo = fatFillo + fatMadhësia*uint32(bpb.fatKopjo)

	var rrënjëFillo = dataFillo + uint32(bpb.sectorspercluster)*(bpb.rrënjëcluster-2)

	direntKursori := memoriaManazhuesi.Malloc(512)
	direntbytes := GetbytesfromKursori(uintptr(direntKursori), 512, 512)
	hd.Leximi28(rrënjëFillo, &direntbytes, 512)

	var dirent = [16]TDosjeentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].emri[0] == 0x00 {
			break
		}

		if dirent[i].madhësia >= 0xFFFFFFFF {
			continue
		}

		if !Barasbytes(emriifile, dirent[i].emri[:len(emriifile)]) {
			continue
		}

		memoriaManazhuesi.Elirë(bpbKursori)
		memoriaManazhuesi.Elirë(direntKursori)
		return dirent[i].madhësia
	}
	memoriaManazhuesi.Elirë(bpbKursori)
	memoriaManazhuesi.Elirë(direntKursori)
	return 0
}
func (vetvetja *TBiosparameterblock32) Leximi(hd *TTëmëtejshmetechnologyattachment, partentry TPartitionTabelaentry, emriifile []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	memoriaManazhuesi := TMemoriaManazhuesi{}
	bpbKursori := memoriaManazhuesi.Malloc(90)
	bpbbytes := GetbytesfromKursori(uintptr(bpbKursori), 90, 90)
	var partitionoffset = partentry.Fillolba

	hd.Leximi28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbbytes)

	var fatFillo = partitionoffset + uint32(bpb.reservedsectors)
	var fatMadhësia = bpb.tabelaMadhësia

	var dataFillo = fatFillo + fatMadhësia*uint32(bpb.fatKopjo)

	var rrënjëFillo = dataFillo + uint32(bpb.sectorspercluster)*(bpb.rrënjëcluster-2)

	direntKursori := memoriaManazhuesi.Malloc(512)
	direntbytes := GetbytesfromKursori(uintptr(direntKursori), 512, 512)
	hd.Leximi28(rrënjëFillo, &direntbytes, 512)

	var dirent = [16]TDosjeentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].emri[0] == 0x00 {
			break
		}

		if dirent[i].madhësia >= 0xFFFFFFFF {
			continue
		}

		if !Barasbytes(emriifile, dirent[i].emri[:len(emriifile)]) {
			continue
		}

		var firstKartelëcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterUlët))

		var Madhësia = int32(dirent[i].madhësia)
		var pasuesenKartelëcluster = int32(firstKartelëcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Madhësia > 0 {
			var kartelësector = dataFillo + uint32(bpb.sectorspercluster)*uint32(pasuesenKartelëcluster-2)
			var sectoroffset int = 0

			for ; Madhësia > 0; Madhësia -= 512 {

				var buffer3 []byte

				if dirent[i].madhësia > 512 {
					buffer3 = buffer_2[:512]
					hd.Leximi28(kartelësector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].madhësia]
					hd.Leximi28(kartelësector+uint32(sectoroffset), &buffer3, int(dirent[i].madhësia))
				}

				copy(data[int32(dirent[i].madhësia)-Madhësia:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforEtanishmecluster = uint32(pasuesenKartelëcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Leximi28(fatFillo+fatsectorforEtanishmecluster, &fatbuf, 512)

			var fatoffsetZmadhosectorforEtanishmecluster = pasuesenKartelëcluster % 128
			var fillooffset = fatoffsetZmadhosectorforEtanishmecluster * 4
			var fundoffset = fatoffsetZmadhosectorforEtanishmecluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[fillooffset:fundoffset])

			pasuesenKartelëcluster = int32(Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer4)))
		}
	}
	memoriaManazhuesi.Elirë(bpbKursori)
	memoriaManazhuesi.Elirë(direntKursori)
}

type TDosjeentryfat32 struct {
	emri			[8]byte
	ext			[3]byte
	veti			uint8
	reserved		uint8
	cOratenth		uint8
	cOra			uint16
	cData			uint16
	aOra			uint16
	firstclusterhi		uint16
	wOra			uint16
	wData			uint16
	firstclusterUlët	uint16
	madhësia		uint32
}

func (vetvetja *TDosjeentryfat32) Init(data [32]byte) {
	copy(vetvetja.emri[:8], data[0:8])
	copy(vetvetja.ext[:3], data[8:11])
	vetvetja.veti = data[11]
	vetvetja.reserved = data[12]
	vetvetja.cOratenth = data[13]
	vetvetja.cOra = uint16(data[14]) | uint16(data[15])<<8
	vetvetja.cData = uint16(data[16]) | uint16(data[17])<<8
	vetvetja.aOra = uint16(data[18]) | uint16(data[19])<<8
	vetvetja.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	vetvetja.wOra = uint16(data[22]) | uint16(data[23])<<8
	vetvetja.wData = uint16(data[24]) | uint16(data[25])<<8
	vetvetja.firstclusterUlët = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	vetvetja.madhësia = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer))
}
