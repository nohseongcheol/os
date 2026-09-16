/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "konsoly"
import . "util"
import . "arikaMpandrindra"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eKarazana	uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eSaina		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shAnarana	uint32
	shKarazana	uint32
	shSaina		uint32
	shaddress	uint32
	shoffset	uint32
	shHabe		uint32
	shrohy		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfrindranasaheader struct {
	pKarazana	uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pSaina		uint32
	pampifanitsio	uint32
}
type Elf32Fanamarihana struct {
	nnamesz		uint32
	ndescsz		uint32
	nKarazana	uint32
}
type Elf32dyn struct {
	dtag		uint32
	dvalpointer	uint32
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
	stAnarana	uint32
	stSanda		uint32
	stHabe		uint32
	stinfo		uint8
	stHafa		uint8
	stshndx		uint16
}
type relocationSoratra struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	soratra		[]byte
	soratralen	uint32
	relSoratra	[100]relocationSoratra
	relSoratralen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (nytena *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (nytena *Elf) Parse(data []byte, PEJYLahatahiryentry uint32) {

	arikaMpandrindra := TArikaMpandrindra{}
	var soratrapointer Pointer = nil

	var konsoly_2 = TKonsoly{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderHabe := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderHabe*i]))

			var sectAnarana []byte
			atomboy := uint32(strtab.shoffset + sectheader.shAnarana)
			end := atomboy
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectAnarana = data[atomboy:end]

			var sectSanda []byte
			if sectheader.shKarazana != 8 {
				endoffset := sectheader.shoffset + sectheader.shHabe
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectSanda = data[sectheader.shoffset:endoffset]
			}

			if EqualOctet(sectAnarana, ([]byte)(".got.plt")) {
				konsoly_2.MAtontay("[")
				konsoly_2.MAtontay(sectAnarana)
				konsoly_2.MAtontay(":")
				nytena.Got = sectheader.shaddress
				konsoly_2.MUnsignedinteger32Atontay(nytena.Got)
				konsoly_2.MAtontay("]")
			}
			if EqualOctet(sectAnarana, ([]byte)(".dynamic")) {
				konsoly_2.MAtontay("[")
				konsoly_2.MAtontay(sectAnarana)
				konsoly_2.MAtontay(":")
				dynamic := sectheader.shaddress
				nytena.Dynamic = dynamic
				konsoly_2.MUnsignedinteger32Atontay(dynamic)
				konsoly_2.MAtontay("]")
			}

			if sectheader.shaddress > 0x1000 {
				habe := sectheader.shHabe
				if sectheader.shKarazana == 8 {
					ZeroblockAnatyPEJYLahatahiry(sectheader.shaddress, habe, PEJYLahatahiryentry)
				} else {
					destination_2 := GetOctetfrompointer(uintptr(sectheader.shaddress), int(habe), int(habe))
					SetblockAnatyPEJYLahatahiry(sectSanda, destination_2, habe, PEJYLahatahiryentry)
				}
			}

			continue

			if EqualOctet(sectAnarana, ([]byte)(".text")) {
				konsoly_2.MAtontay(".text")
				konsoly_2.MAtontay("[")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shaddress)
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shoffset)
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shHabe)
				konsoly_2.MAtontay("]")
				copy(nytena.soratra[:sectheader.shHabe], sectSanda[:sectheader.shHabe])
				nytena.soratralen = sectheader.shHabe
			}
			if EqualOctet(sectAnarana, ([]byte)(".rel.text")) {
				konsoly_2.MAtontay(".rel.text")
				konsoly_2.MAtontay("[")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shaddress)
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shHabe)
				konsoly_2.MAtontay("]")
				for rt := uint32(0); rt < sectheader.shHabe/8; rt++ {
					offset := *(*uint32)(Pointer(&sectSanda[rt*8]))
					nytena.relSoratra[rt].offset = offset
					nytena.relSoratra[rt].oaddress = *(*uint32)(Pointer(&nytena.soratra[offset]))
					nytena.relSoratra[rt].number = *(*uint32)(Pointer(&sectSanda[rt*8+4]))
					nytena.relSoratralen++
				}
			}
			if EqualOctet(sectAnarana, ([]byte)(".dynsym")) {
				konsoly_2.MAtontay(".dynsym")
				konsoly_2.MAtontay("[")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shaddress)
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shHabe)
				konsoly_2.MAtontay("]")
				for rt := uint32(0); rt < sectheader.shHabe/8; rt++ {
					offset := *(*uint32)(Pointer(&sectSanda[rt*8]))
					nytena.relSoratra[rt].offset = offset
					nytena.relSoratra[rt].oaddress = *(*uint32)(Pointer(&nytena.soratra[offset]))
					nytena.relSoratra[rt].number = *(*uint32)(Pointer(&sectSanda[rt*8+4]))
					nytena.relSoratralen++
				}
			}
			if EqualOctet(sectAnarana, ([]byte)(".dynstr")) {
				konsoly_2.MAtontay(".dynstr")
				konsoly_2.MAtontay("[")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shaddress)
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shHabe)
				konsoly_2.MAtontay("]")
			}
			if EqualOctet(sectAnarana, ([]byte)(".strtab")) {
				konsoly_2.MAtontay(".strtab")
				konsoly_2.MAtontay("[")
				konsoly_2.MUnsignedinteger32Atontay(sectheader.shaddress)
				konsoly_2.MAtontay("]")
				rt := uint32(0)
				atomboy := uint32(0)

				for st := uint32(1); st < sectheader.shHabe; st++ {
					if sectSanda[st] == 0x0 || sectSanda[st] == ' ' {
						funcAnarana := sectSanda[atomboy+1 : st]
						konsoly_2.MAtontay("+")
						konsoly_2.MAtontay(funcAnarana)
						nytena.strtab[rt] = Octettostring(funcAnarana)
						atomboy = st
						rt++
					}
				}

			}

		}

		konsoly_2.MAtontay(([]byte)("<------------"))
		for rt := uint32(0); rt < nytena.relSoratralen; rt++ {
			konsoly_2.MAtontay("[")
			konsoly_2.MAtontay(([]byte)(nytena.strtab[rt]))
			konsoly_2.MAtontay(":")
			konsoly_2.MUnsignedinteger32Atontay(nytena.relSoratra[rt].number)
			konsoly_2.MAtontay(":")

			konsoly_2.MAtontay(([]byte)("]"))
		}
		konsoly_2.MAtontay(([]byte)("------------>"))

		if soratrapointer != nil {
			arikaMpandrindra.Malalaka(soratrapointer)
		}

	}

}
