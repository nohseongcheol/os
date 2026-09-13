package elf

import . "unsafe"

import . "konsolë"
import . "util"
import . "memoriaManazhuesi"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eLloji		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eFlamurka	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shEmri		uint32
	shLloji		uint32
	shFlamurka	uint32
	shaddress	uint32
	shoffset	uint32
	shMadhësia	uint32
	shLidhje	uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfProgramiheader struct {
	pLloji		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlamurka	uint32
	pRreshtimi	uint32
}
type Elf32Shënim struct {
	nnamesz	uint32
	ndescsz	uint32
	nLloji	uint32
}
type Elf32dyn struct {
	dtag		uint32
	dvalKursori	uint32
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
	stEmri		uint32
	stVlera		uint32
	stMadhësia	uint32
	stinfo		uint8
	stTjetër	uint8
	stshndx		uint16
}
type relocationTeksti struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	teksti		[]byte
	tekstilen	uint32
	relTeksti	[100]relocationTeksti
	relTekstilen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (vetvetja *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (vetvetja *Elf) Parse(data []byte, FaqeDosjeentry uint32) {

	memoriaManazhuesi := TMemoriaManazhuesi{}
	var tekstiKursori Pointer = nil

	var konsolë_2 = TKonsolë{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderMadhësia := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderMadhësia*i]))

			var sectEmri []byte
			fillo := uint32(strtab.shoffset + sectheader.shEmri)
			fund := fillo
			for ; ; fund++ {
				if data[fund] == 0x0 || data[fund] == ' ' {
					break
				}
			}
			sectEmri = data[fillo:fund]

			var sectVlera []byte
			if sectheader.shLloji != 8 {
				fundoffset := sectheader.shoffset + sectheader.shMadhësia
				if fundoffset < sectheader.shoffset || fundoffset > uint32(len(data)) {
					continue
				}
				sectVlera = data[sectheader.shoffset:fundoffset]
			}

			if Barasbytes(sectEmri, ([]byte)(".got.plt")) {
				konsolë_2.MPrinto("[")
				konsolë_2.MPrinto(sectEmri)
				konsolë_2.MPrinto(":")
				vetvetja.Got = sectheader.shaddress
				konsolë_2.MUnsignedinteger32Printo(vetvetja.Got)
				konsolë_2.MPrinto("]")
			}
			if Barasbytes(sectEmri, ([]byte)(".dynamic")) {
				konsolë_2.MPrinto("[")
				konsolë_2.MPrinto(sectEmri)
				konsolë_2.MPrinto(":")
				dynamic := sectheader.shaddress
				vetvetja.Dynamic = dynamic
				konsolë_2.MUnsignedinteger32Printo(dynamic)
				konsolë_2.MPrinto("]")
			}

			if sectheader.shaddress > 0x1000 {
				madhësia := sectheader.shMadhësia
				if sectheader.shLloji == 8 {
					ZeroblockZmadhofaqeDosje(sectheader.shaddress, madhësia, FaqeDosjeentry)
				} else {
					destinacioni_2 := GetbytesfromKursori(uintptr(sectheader.shaddress), int(madhësia), int(madhësia))
					CaktoniblockZmadhofaqeDosje(sectVlera, destinacioni_2, madhësia, FaqeDosjeentry)
				}
			}

			continue

			if Barasbytes(sectEmri, ([]byte)(".text")) {
				konsolë_2.MPrinto(".text")
				konsolë_2.MPrinto("[")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shaddress)
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shoffset)
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shMadhësia)
				konsolë_2.MPrinto("]")
				copy(vetvetja.teksti[:sectheader.shMadhësia], sectVlera[:sectheader.shMadhësia])
				vetvetja.tekstilen = sectheader.shMadhësia
			}
			if Barasbytes(sectEmri, ([]byte)(".rel.text")) {
				konsolë_2.MPrinto(".rel.text")
				konsolë_2.MPrinto("[")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shaddress)
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shMadhësia)
				konsolë_2.MPrinto("]")
				for rt := uint32(0); rt < sectheader.shMadhësia/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVlera[rt*8]))
					vetvetja.relTeksti[rt].offset = offset
					vetvetja.relTeksti[rt].oaddress = *(*uint32)(Pointer(&vetvetja.teksti[offset]))
					vetvetja.relTeksti[rt].number = *(*uint32)(Pointer(&sectVlera[rt*8+4]))
					vetvetja.relTekstilen++
				}
			}
			if Barasbytes(sectEmri, ([]byte)(".dynsym")) {
				konsolë_2.MPrinto(".dynsym")
				konsolë_2.MPrinto("[")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shaddress)
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shMadhësia)
				konsolë_2.MPrinto("]")
				for rt := uint32(0); rt < sectheader.shMadhësia/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVlera[rt*8]))
					vetvetja.relTeksti[rt].offset = offset
					vetvetja.relTeksti[rt].oaddress = *(*uint32)(Pointer(&vetvetja.teksti[offset]))
					vetvetja.relTeksti[rt].number = *(*uint32)(Pointer(&sectVlera[rt*8+4]))
					vetvetja.relTekstilen++
				}
			}
			if Barasbytes(sectEmri, ([]byte)(".dynstr")) {
				konsolë_2.MPrinto(".dynstr")
				konsolë_2.MPrinto("[")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shaddress)
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shMadhësia)
				konsolë_2.MPrinto("]")
			}
			if Barasbytes(sectEmri, ([]byte)(".strtab")) {
				konsolë_2.MPrinto(".strtab")
				konsolë_2.MPrinto("[")
				konsolë_2.MUnsignedinteger32Printo(sectheader.shaddress)
				konsolë_2.MPrinto("]")
				rt := uint32(0)
				fillo := uint32(0)

				for st := uint32(1); st < sectheader.shMadhësia; st++ {
					if sectVlera[st] == 0x0 || sectVlera[st] == ' ' {
						funcEmri := sectVlera[fillo+1 : st]
						konsolë_2.MPrinto("+")
						konsolë_2.MPrinto(funcEmri)
						vetvetja.strtab[rt] = Bytestovarg(funcEmri)
						fillo = st
						rt++
					}
				}

			}

		}

		konsolë_2.MPrinto(([]byte)("<------------"))
		for rt := uint32(0); rt < vetvetja.relTekstilen; rt++ {
			konsolë_2.MPrinto("[")
			konsolë_2.MPrinto(([]byte)(vetvetja.strtab[rt]))
			konsolë_2.MPrinto(":")
			konsolë_2.MUnsignedinteger32Printo(vetvetja.relTeksti[rt].number)
			konsolë_2.MPrinto(":")

			konsolë_2.MPrinto(([]byte)("]"))
		}
		konsolë_2.MPrinto(([]byte)("------------>"))

		if tekstiKursori != nil {
			memoriaManazhuesi.Elirë(tekstiKursori)
		}

	}

}
