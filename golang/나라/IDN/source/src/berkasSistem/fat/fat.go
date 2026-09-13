package fat

import . "util"
import . "console"
import . "driver/ata"
import . "berkasSistem/msdospartition"
import . "memorimanager"

type TParameter_sistem_berkas32 struct {
	jmp			[3]uint8
	softNama		[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatSalin		uint8
	akarDirektorientri	uint16
	totalsectors		uint16
	mediaTipe		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	tersembunyisectors	uint32
	totalsectorcount	uint32

	tabelUkuran	uint32
	extTanda	uint16
	fatVersi	uint16
	akarcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveNomor	uint8
	reserved	uint8
	bootsignature	uint8
	volumeid	uint32
	volumeNama	[11]byte
	fatTipeNama	[8]byte
}

func (dirisendiri *TParameter_sistem_berkas32) Init(data []byte) {
	copy(dirisendiri.jmp[:3], data[0:3])
	copy(dirisendiri.softNama[:8], data[3:11])

	dirisendiri.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	dirisendiri.sectorspercluster = data[13]
	dirisendiri.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	dirisendiri.fatSalin = data[16]
	dirisendiri.akarDirektorientri = (uint16(data[17]) | uint16(data[18])<<8)
	dirisendiri.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	dirisendiri.mediaTipe = data[21]
	dirisendiri.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	dirisendiri.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	dirisendiri.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	dirisendiri.tersembunyisectors = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	dirisendiri.totalsectorcount = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	dirisendiri.tabelUkuran = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	dirisendiri.extTanda = (uint16(data[40]) | uint16(data[41])<<8)
	dirisendiri.fatVersi = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	dirisendiri.akarcluster = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	dirisendiri.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	dirisendiri.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(dirisendiri.reserved0[:12], data[52:64])

	dirisendiri.driveNomor = data[64]
	dirisendiri.reserved = data[65]
	dirisendiri.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	dirisendiri.volumeid = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	copy(dirisendiri.volumeNama[:11], data[71:82])
	copy(dirisendiri.fatTipeNama[:8], data[82:90])

}

var console_2 = TConsole{}

func (dirisendiri *TParameter_sistem_berkas32) Len(hd *TLanjutanTeknologiattachment, partentri TPartitionTabelentri, namaberkas []byte) uint32 {

	if partentri.Partitionid == 0x00 {
		return 0
	}

	memorimanager := TMemorimanager{}
	bpbPenunjuk := memorimanager.Alokasikan_memori(90)
	bpbByte := GetBytefromPenunjuk(uintptr(bpbPenunjuk), 90, 90)
	var partitionoffset = partentri.Mulailba

	hd.Baca28(partitionoffset, &bpbByte, 90)

	var parameter_sistem_berkas = TParameter_sistem_berkas32{}
	parameter_sistem_berkas.Init(bpbByte)

	var fatMulai = partitionoffset + uint32(parameter_sistem_berkas.reservedsectors)
	var fatUkuran = parameter_sistem_berkas.tabelUkuran

	var dataMulai = fatMulai + fatUkuran*uint32(parameter_sistem_berkas.fatSalin)

	var akarMulai = dataMulai + uint32(parameter_sistem_berkas.sectorspercluster)*(parameter_sistem_berkas.akarcluster-2)

	direntPenunjuk := memorimanager.Alokasikan_memori(512)
	direntByte := GetBytefromPenunjuk(uintptr(direntPenunjuk), 512, 512)
	hd.Baca28(akarMulai, &direntByte, 512)

	var dirent = [16]TDirektorientrifat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nama[0] == 0x00 {
			break
		}

		if dirent[i].ukuran >= 0xFFFFFFFF {
			continue
		}

		if !SamaByte(namaberkas, dirent[i].nama[:len(namaberkas)]) {
			continue
		}

		memorimanager.Bebas(bpbPenunjuk)
		memorimanager.Bebas(direntPenunjuk)
		return dirent[i].ukuran
	}
	memorimanager.Bebas(bpbPenunjuk)
	memorimanager.Bebas(direntPenunjuk)
	return 0
}
func (dirisendiri *TParameter_sistem_berkas32) Baca(hd *TLanjutanTeknologiattachment, partentri TPartitionTabelentri, namaberkas []byte, data []byte) {

	if partentri.Partitionid == 0x00 {
		return
	}

	memorimanager := TMemorimanager{}
	bpbPenunjuk := memorimanager.Alokasikan_memori(90)
	bpbByte := GetBytefromPenunjuk(uintptr(bpbPenunjuk), 90, 90)
	var partitionoffset = partentri.Mulailba

	hd.Baca28(partitionoffset, &bpbByte, 90)

	var parameter_sistem_berkas = TParameter_sistem_berkas32{}
	parameter_sistem_berkas.Init(bpbByte)

	var fatMulai = partitionoffset + uint32(parameter_sistem_berkas.reservedsectors)
	var fatUkuran = parameter_sistem_berkas.tabelUkuran

	var dataMulai = fatMulai + fatUkuran*uint32(parameter_sistem_berkas.fatSalin)

	var akarMulai = dataMulai + uint32(parameter_sistem_berkas.sectorspercluster)*(parameter_sistem_berkas.akarcluster-2)

	direntPenunjuk := memorimanager.Alokasikan_memori(512)
	direntByte := GetBytefromPenunjuk(uintptr(direntPenunjuk), 512, 512)
	hd.Baca28(akarMulai, &direntByte, 512)

	var dirent = [16]TDirektorientrifat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nama[0] == 0x00 {
			break
		}

		if dirent[i].ukuran >= 0xFFFFFFFF {
			continue
		}

		if !SamaByte(namaberkas, dirent[i].nama[:len(namaberkas)]) {
			continue
		}

		var firstBerkascluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterRendah))

		var Ukuran = int32(dirent[i].ukuran)
		var berikutnyaBerkascluster = int32(firstBerkascluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Ukuran > 0 {
			var berkassector = dataMulai + uint32(parameter_sistem_berkas.sectorspercluster)*uint32(berikutnyaBerkascluster-2)
			var sectoroffset int = 0

			for ; Ukuran > 0; Ukuran -= 512 {

				var buffer3 []byte

				if dirent[i].ukuran > 512 {
					buffer3 = buffer_2[:512]
					hd.Baca28(berkassector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].ukuran]
					hd.Baca28(berkassector+uint32(sectoroffset), &buffer3, int(dirent[i].ukuran))
				}

				copy(data[int32(dirent[i].ukuran)-Ukuran:], buffer3)

				sectoroffset++

				if sectoroffset > int(parameter_sistem_berkas.sectorspercluster) {
					break
				}

			}

			var fatsectorforSekarangcluster = uint32(berikutnyaBerkascluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Baca28(fatMulai+fatsectorforSekarangcluster, &fatbuf, 512)

			var fatoffsetMasuksectorforSekarangcluster = berikutnyaBerkascluster % 128
			var mulaioffset = fatoffsetMasuksectorforSekarangcluster * 4
			var akhiroffset = fatoffsetMasuksectorforSekarangcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[mulaioffset:akhiroffset])

			berikutnyaBerkascluster = int32(Unsignedinteger32r(Jajarantounsignedinteger32(buffer4)))
		}
	}
	memorimanager.Bebas(bpbPenunjuk)
	memorimanager.Bebas(direntPenunjuk)
}

type TDirektorientrifat32 struct {
	nama			[8]byte
	ext			[3]byte
	atribut_2		uint8
	reserved		uint8
	cWaktutenth		uint8
	cWaktu			uint16
	cTanggal		uint16
	aWaktu			uint16
	firstclusterhi		uint16
	wWaktu			uint16
	wTanggal		uint16
	firstclusterRendah	uint16
	ukuran			uint32
}

func (dirisendiri *TDirektorientrifat32) Init(data [32]byte) {
	copy(dirisendiri.nama[:8], data[0:8])
	copy(dirisendiri.ext[:3], data[8:11])
	dirisendiri.atribut_2 = data[11]
	dirisendiri.reserved = data[12]
	dirisendiri.cWaktutenth = data[13]
	dirisendiri.cWaktu = uint16(data[14]) | uint16(data[15])<<8
	dirisendiri.cTanggal = uint16(data[16]) | uint16(data[17])<<8
	dirisendiri.aWaktu = uint16(data[18]) | uint16(data[19])<<8
	dirisendiri.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	dirisendiri.wWaktu = uint16(data[22]) | uint16(data[23])<<8
	dirisendiri.wTanggal = uint16(data[24]) | uint16(data[25])<<8
	dirisendiri.firstclusterRendah = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	dirisendiri.ukuran = Unsignedinteger32r(Jajarantounsignedinteger32(buffer))
}
