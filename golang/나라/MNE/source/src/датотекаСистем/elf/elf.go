package elf

import . "unsafe"

import . "конзола"
import . "util"
import . "memorijamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eВрста		uint16
	emachine	uint16
	eИздање		uint32
	eунос		uint32
	ephoff		uint32
	eshoff		uint32
	eParametri	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shНазив		uint32
	shВрста		uint32
	shParametri	uint32
	shaddress	uint32
	shoffset	uint32
	shВеличина	uint32
	shВеза		uint32
	shПодаци	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограмheader struct {
	pВрста		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pParametri	uint32
	pПоравнање	uint32
}
type Elf32Белешка struct {
	nnamesz	uint32
	ndescsz	uint32
	nВрста	uint32
}
type Elf32dyn struct {
	dознака		uint32
	dvalPokazivač	uint32
}
type Elf32rel struct {
	roffset	uint32
	rПодаци	uint32
}
type Elf32rela struct {
	roffset	uint32
	rПодаци	uint32
	raddend	uint32
}
type Elf32sym struct {
	stНазив		uint32
	stВредност	uint32
	stВеличина	uint32
	stПодаци	uint8
	stДруго		uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset		uint32
	број		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Rastegǉivo	uint32
}

func (isti *Elf) Getунос(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eунос
}

func (isti *Elf) Parse(data []byte, ListDirektorijumунос uint32) {

	memorijamanager := TMemorijamanager{}
	var текстPokazivač Pointer = nil

	var конзола_2 = TКонзола{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderВеличина := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderВеличина*i]))

			var sectНазив []byte
			pokreni := uint32(strtab.shoffset + sectheader.shНазив)
			kraj := pokreni
			for ; ; kraj++ {
				if data[kraj] == 0x0 || data[kraj] == ' ' {
					break
				}
			}
			sectНазив = data[pokreni:kraj]

			var sectВредност []byte
			if sectheader.shВрста != 8 {
				krajoffset := sectheader.shoffset + sectheader.shВеличина
				if krajoffset < sectheader.shoffset || krajoffset > uint32(len(data)) {
					continue
				}
				sectВредност = data[sectheader.shoffset:krajoffset]
			}

			if ИстаBajtova(sectНазив, ([]byte)(".got.plt")) {
				конзола_2.MŠtampaj("[")
				конзола_2.MŠtampaj(sectНазив)
				конзола_2.MŠtampaj(":")
				isti.Got = sectheader.shaddress
				конзола_2.MUnsignedinteger32Štampaj(isti.Got)
				конзола_2.MŠtampaj("]")
			}
			if ИстаBajtova(sectНазив, ([]byte)(".dynamic")) {
				конзола_2.MŠtampaj("[")
				конзола_2.MŠtampaj(sectНазив)
				конзола_2.MŠtampaj(":")
				rastegǉivo := sectheader.shaddress
				isti.Rastegǉivo = rastegǉivo
				конзола_2.MUnsignedinteger32Štampaj(rastegǉivo)
				конзола_2.MŠtampaj("]")
			}

			if sectheader.shaddress > 0x1000 {
				величина := sectheader.shВеличина
				if sectheader.shВрста == 8 {
					ZeroBlokПримљеноlistDirektorijum(sectheader.shaddress, величина, ListDirektorijumунос)
				} else {
					odredište_2 := GetBajtovasaPokazivač(uintptr(sectheader.shaddress), int(величина), int(величина))
					СкупBlokПримљеноlistDirektorijum(sectВредност, odredište_2, величина, ListDirektorijumунос)
				}
			}

			continue

			if ИстаBajtova(sectНазив, ([]byte)(".text")) {
				конзола_2.MŠtampaj(".text")
				конзола_2.MŠtampaj("[")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shoffset)
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shВеличина)
				конзола_2.MŠtampaj("]")
				copy(isti.текст[:sectheader.shВеличина], sectВредност[:sectheader.shВеличина])
				isti.текстlen = sectheader.shВеличина
			}
			if ИстаBajtova(sectНазив, ([]byte)(".rel.text")) {
				конзола_2.MŠtampaj(".rel.text")
				конзола_2.MŠtampaj("[")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shВеличина)
				конзола_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shВеличина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					isti.relТекст[rt].offset = offset
					isti.relТекст[rt].oaddress = *(*uint32)(Pointer(&isti.текст[offset]))
					isti.relТекст[rt].број = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					isti.relТекстlen++
				}
			}
			if ИстаBajtova(sectНазив, ([]byte)(".dynsym")) {
				конзола_2.MŠtampaj(".dynsym")
				конзола_2.MŠtampaj("[")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shВеличина)
				конзола_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shВеличина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					isti.relТекст[rt].offset = offset
					isti.relТекст[rt].oaddress = *(*uint32)(Pointer(&isti.текст[offset]))
					isti.relТекст[rt].број = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					isti.relТекстlen++
				}
			}
			if ИстаBajtova(sectНазив, ([]byte)(".dynstr")) {
				конзола_2.MŠtampaj(".dynstr")
				конзола_2.MŠtampaj("[")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shВеличина)
				конзола_2.MŠtampaj("]")
			}
			if ИстаBajtova(sectНазив, ([]byte)(".strtab")) {
				конзола_2.MŠtampaj(".strtab")
				конзола_2.MŠtampaj("[")
				конзола_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				конзола_2.MŠtampaj("]")
				rt := uint32(0)
				pokreni := uint32(0)

				for st := uint32(1); st < sectheader.shВеличина; st++ {
					if sectВредност[st] == 0x0 || sectВредност[st] == ' ' {
						funcНазив := sectВредност[pokreni+1 : st]
						конзола_2.MŠtampaj("+")
						конзола_2.MŠtampaj(funcНазив)
						isti.strtab[rt] = Bajtovatoниска(funcНазив)
						pokreni = st
						rt++
					}
				}

			}

		}

		конзола_2.MŠtampaj(([]byte)("<------------"))
		for rt := uint32(0); rt < isti.relТекстlen; rt++ {
			конзола_2.MŠtampaj("[")
			конзола_2.MŠtampaj(([]byte)(isti.strtab[rt]))
			конзола_2.MŠtampaj(":")
			конзола_2.MUnsignedinteger32Štampaj(isti.relТекст[rt].број)
			конзола_2.MŠtampaj(":")

			конзола_2.MŠtampaj(([]byte)("]"))
		}
		конзола_2.MŠtampaj(([]byte)("------------>"))

		if текстPokazivač != nil {
			memorijamanager.Slobodno(текстPokazivač)
		}

	}

}
