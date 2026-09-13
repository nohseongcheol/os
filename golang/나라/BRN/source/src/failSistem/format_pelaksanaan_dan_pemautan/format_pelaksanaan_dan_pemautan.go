package format_pelaksanaan_dan_pemautan

import . "unsafe"

import . "console"
import . "util"
import . "ingatanmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eJenis		uint16
	emachine	uint16
	eVersi		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eBendera	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNama		uint32
	shJenis		uint32
	shBendera	uint32
	shaddress	uint32
	shoffset	uint32
	shSaiz		uint32
	shPautan	uint32
	shMaklumat	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pJenis		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pBendera	uint32
	pJajar		uint32
}
type Elf32Nota struct {
	nnamesz	uint32
	ndescsz	uint32
	nJenis	uint32
}
type Elf32dyn struct {
	dtag		uint32
	dvalPenuding	uint32
}
type Elf32rel struct {
	roffset		uint32
	rMaklumat	uint32
}
type Elf32rela struct {
	roffset		uint32
	rMaklumat	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNama		uint32
	stNilai		uint32
	stSaiz		uint32
	stMaklumat	uint8
	stLainlain	uint8
	stshndx		uint16
}
type relocationTeks struct {
	offset		uint32
	nOMBOR		uint32
	oaddress	uint32
}
type Elf struct {
	teks		[]byte
	tekslen		uint32
	relTeks		[100]relocationTeks
	relTekslen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (diri *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (diri *Elf) Parse(data []byte, Halamandirektorientry uint32) {

	ingatanmanager := TIngatanmanager{}
	var teksPenuding Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderSaiz := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderSaiz*i]))

			var sectNama []byte
			mula := uint32(strtab.shoffset + sectheader.shNama)
			tamat := mula
			for ; ; tamat++ {
				if data[tamat] == 0x0 || data[tamat] == ' ' {
					break
				}
			}
			sectNama = data[mula:tamat]

			var sectNilai []byte
			if sectheader.shJenis != 8 {
				tamatoffset := sectheader.shoffset + sectheader.shSaiz
				if tamatoffset < sectheader.shoffset || tamatoffset > uint32(len(data)) {
					continue
				}
				sectNilai = data[sectheader.shoffset:tamatoffset]
			}

			if SamaBait(sectNama, ([]byte)(".got.plt")) {
				console_2.MCetak("[")
				console_2.MCetak(sectNama)
				console_2.MCetak(":")
				diri.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Cetak(diri.Got)
				console_2.MCetak("]")
			}
			if SamaBait(sectNama, ([]byte)(".dynamic")) {
				console_2.MCetak("[")
				console_2.MCetak(sectNama)
				console_2.MCetak(":")
				dynamic := sectheader.shaddress
				diri.Dynamic = dynamic
				console_2.MUnsignedinteger32Cetak(dynamic)
				console_2.MCetak("]")
			}

			if sectheader.shaddress > 0x1000 {
				saiz := sectheader.shSaiz
				if sectheader.shJenis == 8 {
					ZeroBlokMasukHalamandirektori(sectheader.shaddress, saiz, Halamandirektorientry)
				} else {
					destination_2 := GetBaitfromPenuding(uintptr(sectheader.shaddress), int(saiz), int(saiz))
					TetapkanBlokMasukHalamandirektori(sectNilai, destination_2, saiz, Halamandirektorientry)
				}
			}

			continue

			if SamaBait(sectNama, ([]byte)(".text")) {
				console_2.MCetak(".text")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shoffset)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shSaiz)
				console_2.MCetak("]")
				copy(diri.teks[:sectheader.shSaiz], sectNilai[:sectheader.shSaiz])
				diri.tekslen = sectheader.shSaiz
			}
			if SamaBait(sectNama, ([]byte)(".rel.text")) {
				console_2.MCetak(".rel.text")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shSaiz)
				console_2.MCetak("]")
				for rt := uint32(0); rt < sectheader.shSaiz/8; rt++ {
					offset := *(*uint32)(Pointer(&sectNilai[rt*8]))
					diri.relTeks[rt].offset = offset
					diri.relTeks[rt].oaddress = *(*uint32)(Pointer(&diri.teks[offset]))
					diri.relTeks[rt].nOMBOR = *(*uint32)(Pointer(&sectNilai[rt*8+4]))
					diri.relTekslen++
				}
			}
			if SamaBait(sectNama, ([]byte)(".dynsym")) {
				console_2.MCetak(".dynsym")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shSaiz)
				console_2.MCetak("]")
				for rt := uint32(0); rt < sectheader.shSaiz/8; rt++ {
					offset := *(*uint32)(Pointer(&sectNilai[rt*8]))
					diri.relTeks[rt].offset = offset
					diri.relTeks[rt].oaddress = *(*uint32)(Pointer(&diri.teks[offset]))
					diri.relTeks[rt].nOMBOR = *(*uint32)(Pointer(&sectNilai[rt*8+4]))
					diri.relTekslen++
				}
			}
			if SamaBait(sectNama, ([]byte)(".dynstr")) {
				console_2.MCetak(".dynstr")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(sectheader.shSaiz)
				console_2.MCetak("]")
			}
			if SamaBait(sectNama, ([]byte)(".strtab")) {
				console_2.MCetak(".strtab")
				console_2.MCetak("[")
				console_2.MUnsignedinteger32Cetak(sectheader.shaddress)
				console_2.MCetak("]")
				rt := uint32(0)
				mula := uint32(0)

				for st := uint32(1); st < sectheader.shSaiz; st++ {
					if sectNilai[st] == 0x0 || sectNilai[st] == ' ' {
						funcNama := sectNilai[mula+1 : st]
						console_2.MCetak("+")
						console_2.MCetak(funcNama)
						diri.strtab[rt] = BaittoRentetan(funcNama)
						mula = st
						rt++
					}
				}

			}

		}

		console_2.MCetak(([]byte)("<------------"))
		for rt := uint32(0); rt < diri.relTekslen; rt++ {
			console_2.MCetak("[")
			console_2.MCetak(([]byte)(diri.strtab[rt]))
			console_2.MCetak(":")
			console_2.MUnsignedinteger32Cetak(diri.relTeks[rt].nOMBOR)
			console_2.MCetak(":")

			console_2.MCetak(([]byte)("]"))
		}
		console_2.MCetak(([]byte)("------------>"))

		if teksPenuding != nil {
			ingatanmanager.Bebas(teksPenuding)
		}

	}

}
