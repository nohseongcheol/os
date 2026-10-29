/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package körbart_och_länkbart_format

import . "unsafe"

import . "konsol"
import . "util"
import . "minnemanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTyp		uint16
	emachine	uint16
	eversion	uint32
	epost		uint32
	ephoff		uint32
	eshoff		uint32
	eFlaggor	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNamn		uint32
	shTyp		uint32
	shFlaggor	uint32
	shAdress	uint32
	shFörskjutning	uint32
	shStorlek	uint32
	shLänk		uint32
	shInformation	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTyp		uint32
	pFörskjutning	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlaggor	uint32
	pJustera	uint32
}
type Elf32Anteckning struct {
	nnamesz	uint32
	ndescsz	uint32
	nTyp	uint32
}
type Elf32dyn struct {
	dTagg		uint32
	dvalMuspekare	uint32
}
type Elf32rel struct {
	rFörskjutning	uint32
	rInformation	uint32
}
type Elf32rela struct {
	rFörskjutning	uint32
	rInformation	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNamn		uint32
	stVärde		uint32
	stStorlek	uint32
	stInformation	uint8
	stAnnan		uint8
	stshndx		uint16
}
type relocationtext struct {
	förskjutning	uint32
	nummer		uint32
	oAdress		uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	reltext		[100]relocationtext
	reltextlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamisk	uint32
}

func (själv *Elf) Getpost(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.epost
}

func (själv *Elf) Parse(data []byte, SidaKatalogpost uint32) {

	minnemanager := TMinnemanager{}
	var textMuspekare Pointer = nil

	var konsol_2 = TKonsol{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderStorlek := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderStorlek*i]))

			var sectNamn []byte
			starta := uint32(strtab.shFörskjutning + sectheader.shNamn)
			slut := starta
			for ; ; slut++ {
				if data[slut] == 0x0 || data[slut] == ' ' {
					break
				}
			}
			sectNamn = data[starta:slut]

			var sectVärde []byte
			if sectheader.shTyp != 8 {
				slutFörskjutning := sectheader.shFörskjutning + sectheader.shStorlek
				if slutFörskjutning < sectheader.shFörskjutning || slutFörskjutning > uint32(len(data)) {
					continue
				}
				sectVärde = data[sectheader.shFörskjutning:slutFörskjutning]
			}

			if LikaByte(sectNamn, ([]byte)(".got.plt")) {
				konsol_2.MSkrivut("[")
				konsol_2.MSkrivut(sectNamn)
				konsol_2.MSkrivut(":")
				själv.Got = sectheader.shAdress
				konsol_2.MUnsignedinteger32Skrivut(själv.Got)
				konsol_2.MSkrivut("]")
			}
			if LikaByte(sectNamn, ([]byte)(".dynamic")) {
				konsol_2.MSkrivut("[")
				konsol_2.MSkrivut(sectNamn)
				konsol_2.MSkrivut(":")
				dynamisk := sectheader.shAdress
				själv.Dynamisk = dynamisk
				konsol_2.MUnsignedinteger32Skrivut(dynamisk)
				konsol_2.MSkrivut("]")
			}

			if sectheader.shAdress > 0x1000 {
				storlek := sectheader.shStorlek
				if sectheader.shTyp == 8 {
					NollblockiSidaKatalog(sectheader.shAdress, storlek, SidaKatalogpost)
				} else {
					mål_2 := GetBytefromMuspekare(uintptr(sectheader.shAdress), int(storlek), int(storlek))
					MängdblockiSidaKatalog(sectVärde, mål_2, storlek, SidaKatalogpost)
				}
			}

			continue

			if LikaByte(sectNamn, ([]byte)(".text")) {
				konsol_2.MSkrivut(".text")
				konsol_2.MSkrivut("[")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shAdress)
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shFörskjutning)
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shStorlek)
				konsol_2.MSkrivut("]")
				copy(själv.text[:sectheader.shStorlek], sectVärde[:sectheader.shStorlek])
				själv.textlen = sectheader.shStorlek
			}
			if LikaByte(sectNamn, ([]byte)(".rel.text")) {
				konsol_2.MSkrivut(".rel.text")
				konsol_2.MSkrivut("[")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shAdress)
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shStorlek)
				konsol_2.MSkrivut("]")
				for rt := uint32(0); rt < sectheader.shStorlek/8; rt++ {
					förskjutning := *(*uint32)(Pointer(&sectVärde[rt*8]))
					själv.reltext[rt].förskjutning = förskjutning
					själv.reltext[rt].oAdress = *(*uint32)(Pointer(&själv.text[förskjutning]))
					själv.reltext[rt].nummer = *(*uint32)(Pointer(&sectVärde[rt*8+4]))
					själv.reltextlen++
				}
			}
			if LikaByte(sectNamn, ([]byte)(".dynsym")) {
				konsol_2.MSkrivut(".dynsym")
				konsol_2.MSkrivut("[")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shAdress)
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shStorlek)
				konsol_2.MSkrivut("]")
				for rt := uint32(0); rt < sectheader.shStorlek/8; rt++ {
					förskjutning := *(*uint32)(Pointer(&sectVärde[rt*8]))
					själv.reltext[rt].förskjutning = förskjutning
					själv.reltext[rt].oAdress = *(*uint32)(Pointer(&själv.text[förskjutning]))
					själv.reltext[rt].nummer = *(*uint32)(Pointer(&sectVärde[rt*8+4]))
					själv.reltextlen++
				}
			}
			if LikaByte(sectNamn, ([]byte)(".dynstr")) {
				konsol_2.MSkrivut(".dynstr")
				konsol_2.MSkrivut("[")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shAdress)
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shStorlek)
				konsol_2.MSkrivut("]")
			}
			if LikaByte(sectNamn, ([]byte)(".strtab")) {
				konsol_2.MSkrivut(".strtab")
				konsol_2.MSkrivut("[")
				konsol_2.MUnsignedinteger32Skrivut(sectheader.shAdress)
				konsol_2.MSkrivut("]")
				rt := uint32(0)
				starta := uint32(0)

				for st := uint32(1); st < sectheader.shStorlek; st++ {
					if sectVärde[st] == 0x0 || sectVärde[st] == ' ' {
						funcNamn := sectVärde[starta+1 : st]
						konsol_2.MSkrivut("+")
						konsol_2.MSkrivut(funcNamn)
						själv.strtab[rt] = Bytetosträng(funcNamn)
						starta = st
						rt++
					}
				}

			}

		}

		konsol_2.MSkrivut(([]byte)("<------------"))
		for rt := uint32(0); rt < själv.reltextlen; rt++ {
			konsol_2.MSkrivut("[")
			konsol_2.MSkrivut(([]byte)(själv.strtab[rt]))
			konsol_2.MSkrivut(":")
			konsol_2.MUnsignedinteger32Skrivut(själv.reltext[rt].nummer)
			konsol_2.MSkrivut(":")

			konsol_2.MSkrivut(([]byte)("]"))
		}
		konsol_2.MSkrivut(([]byte)("------------>"))

		if textMuspekare != nil {
			minnemanager.Ledigt(textMuspekare)
		}

	}

}
