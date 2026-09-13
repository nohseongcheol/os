package format_eksekusi_dan_penautan

import . "unsafe"

import . "console"
import . "util"
import . "memorimanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTipe		uint16
	emachine	uint16
	eVersi		uint32
	eentri		uint32
	ephoff		uint32
	eshoff		uint32
	eTanda		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNama		uint32
	shTipe		uint32
	shTanda		uint32
	shaddress	uint32
	shoffset	uint32
	shUkuran	uint32
	shTaut		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTipe	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pTanda	uint32
	pAlinea	uint32
}
type Elf32Catat struct {
	nnamesz	uint32
	ndescsz	uint32
	nTipe	uint32
}
type Elf32dyn struct {
	dTanda		uint32
	dvalPenunjuk	uint32
}
type Elf32rel struct {
	roffset	uint32
	rinfo	uint32
}
type Elf32rela struct {
	roffset	uint32
	rinfo	uint32
	raddend	uint32
}
type Elf32sym struct {
	stNama		uint32
	stNilai		uint32
	stUkuran	uint32
	stinfo		uint8
	stLainnya	uint8
	stshndx		uint16
}
type relocationTeks struct {
	offset		uint32
	nomor		uint32
	oaddress	uint32
}
type Elf struct {
	teks		[]byte
	tekslen		uint32
	relTeks		[100]relocationTeks
	relTekslen	uint32
	strtab		[100]string
	Got		uint32
	Dinamis		uint32
}

func (dirisendiri *Elf) Getentri(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentri
}

func (dirisendiri *Elf) Parse(data []byte, HalamanDirektorientri uint32) {

	memorimanager := TMemorimanager{}
	var teksPenunjuk Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderUkuran := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderUkuran*i]))

			var sectNama []byte
			mulai := uint32(strtab.shoffset + sectheader.shNama)
			akhir := mulai
			for ; ; akhir++ {
				if data[akhir] == 0x0 || data[akhir] == ' ' {
					break
				}
			}
			sectNama = data[mulai:akhir]

			var sectNilai []byte
			if sectheader.shTipe != 8 {
				akhiroffset := sectheader.shoffset + sectheader.shUkuran
				if akhiroffset < sectheader.shoffset || akhiroffset > uint32(len(data)) {
					continue
				}
				sectNilai = data[sectheader.shoffset:akhiroffset]
			}

			if SamaByte(sectNama, ([]byte)(".got.plt")) {
				console_2.MCetak("[")
				console_2.MCetak(sectNama)
				console_2.MCetak(":")
				dirisendiri.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Cetak(dirisendiri.Got)
				console_2.MCetak("]")
			}
			if SamaByte(sectNama, ([]byte)(".dynamic")) {
				console_2.MCetak("[")
				console_2.MCetak(sectNama)
				console_2.MCetak(":")
				dinamis := sectheader.shaddress
				dirisendiri.Dinamis = dinamis
				console_2.MUnsignedinteger32Cetak(dinamis)
				console_2.MCetak("]")
			}

			if sectheader.shaddress > 0x1000 {
				ukuran := sectheader.shUkuran
				if sectheader.shTipe == 8 {
					NolBlokMasukHalamanDirektori(sectheader.shaddress, ukuran, HalamanDirektorientri)
				} else {
					tujuan_2 := GetBytefromPenunjuk(uintptr(sectheader.shaddress), int(ukuran), int(ukuran))
					AturBlokMasukHalamanDirektori(sectNilai, tujuan_2, ukuran, HalamanDirektorientri)
				}
			}

			continue

			if SamaByte(sectNama, ([]byte)(".text")) {
				console_2.MCetak(".text")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shoffset)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shUkuran)
				console_2.MCetak("]")
				copy(dirisendiri.teks[:sectheader.shUkuran], sectNilai[:sectheader.shUkuran])
				dirisendiri.tekslen = sectheader.shUkuran
			}
			if SamaByte(sectNama, ([]byte)(".rel.text")) {
				console_2.MCetak(".rel.text")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shUkuran)
				console_2.MCetak("]")
				for rt := uint32(0); rt < sectheader.shUkuran/8; rt++ {
					offset := *(*uint32)(Pointer(&sectNilai[rt*8]))
					dirisendiri.relTeks[rt].offset = offset
					dirisendiri.relTeks[rt].oaddress = *(*uint32)(Pointer(&dirisendiri.teks[offset]))
					dirisendiri.relTeks[rt].nomor = *(*uint32)(Pointer(&sectNilai[rt*8+4]))
					dirisendiri.relTekslen++
				}
			}
			if SamaByte(sectNama, ([]byte)(".dynsym")) {
				console_2.MCetak(".dynsym")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shUkuran)
				console_2.MCetak("]")
				for rt := uint32(0); rt < sectheader.shUkuran/8; rt++ {
					offset := *(*uint32)(Pointer(&sectNilai[rt*8]))
					dirisendiri.relTeks[rt].offset = offset
					dirisendiri.relTeks[rt].oaddress = *(*uint32)(Pointer(&dirisendiri.teks[offset]))
					dirisendiri.relTeks[rt].nomor = *(*uint32)(Pointer(&sectNilai[rt*8+4]))
					dirisendiri.relTekslen++
				}
			}
			if SamaByte(sectNama, ([]byte)(".dynstr")) {
				console_2.MCetak(".dynstr")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shUkuran)
				console_2.MCetak("]")
			}
			if SamaByte(sectNama, ([]byte)(".strtab")) {
				console_2.MCetak(".strtab")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak("]")
				rt := uint32(0)
				mulai := uint32(0)

				for st := uint32(1); st < sectheader.shUkuran; st++ {
					if sectNilai[st] == 0x0 || sectNilai[st] == ' ' {
						funcNama := sectNilai[mulai+1 : st]
						console_2.MCetak("+")
						console_2.MCetak(funcNama)
						dirisendiri.strtab[rt] = BytetoBenang(funcNama)
						mulai = st
						rt++
					}
				}

			}

		}

		console_2.MCetak(([]byte)("<------------"))
		for rt := uint32(0); rt < dirisendiri.relTekslen; rt++ {
			console_2.MCetak("[")
			console_2.MCetak(([]byte)(dirisendiri.strtab[rt]))
			console_2.MCetak(":")
			console_2.MUnsignedinteger32Cetak(dirisendiri.relTeks[rt].nomor)
			console_2.MCetak(":")

			console_2.MCetak(([]byte)("]"))
		}
		console_2.MCetak(([]byte)("------------>"))

		if teksPenunjuk != nil {
			memorimanager.Bebas(teksPenunjuk)
		}

	}

}
