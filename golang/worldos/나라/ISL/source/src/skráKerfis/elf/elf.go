/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "minnimanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTegund		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eflags		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shHeiti		uint32
	shTegund	uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shStærð		uint32
	shTengill	uint32
	shUpplýsingar	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfforritheader struct {
	pTegund	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pflags	uint32
	pJafna	uint32
}
type Elf32Glósa struct {
	nnamesz	uint32
	ndescsz	uint32
	nTegund	uint32
}
type Elf32dyn struct {
	dMerki		uint32
	dvalBendill	uint32
}
type Elf32rel struct {
	roffset		uint32
	rUpplýsingar	uint32
}
type Elf32rela struct {
	roffset		uint32
	rUpplýsingar	uint32
	raddend		uint32
}
type Elf32sym struct {
	stHeiti		uint32
	stGildi		uint32
	stStærð		uint32
	stUpplýsingar	uint8
	stAnnað		uint8
	stshndx		uint16
}
type relocationTexti struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	texti		[]byte
	textilen	uint32
	relTexti	[100]relocationTexti
	relTextilen	uint32
	strtab		[100]string
	Got		uint32
	Breytilegt	uint32
}

func (sjálft *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (sjálft *Elf) Parse(data []byte, Síðamappaentry uint32) {

	minnimanager := TMinnimanager{}
	var textiBendill Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderStærð := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderStærð*i]))

			var sectHeiti []byte
			ræsa := uint32(strtab.shoffset + sectheader.shHeiti)
			end := ræsa
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectHeiti = data[ræsa:end]

			var sectGildi []byte
			if sectheader.shTegund != 8 {
				endoffset := sectheader.shoffset + sectheader.shStærð
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectGildi = data[sectheader.shoffset:endoffset]
			}

			if EqualBæti(sectHeiti, ([]byte)(".got.plt")) {
				console_2.MPrenta("[")
				console_2.MPrenta(sectHeiti)
				console_2.MPrenta(":")
				sjálft.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Prenta(sjálft.Got)
				console_2.MPrenta("]")
			}
			if EqualBæti(sectHeiti, ([]byte)(".dynamic")) {
				console_2.MPrenta("[")
				console_2.MPrenta(sectHeiti)
				console_2.MPrenta(":")
				breytilegt := sectheader.shaddress
				sjálft.Breytilegt = breytilegt
				console_2.MUnsignedinteger32Prenta(breytilegt)
				console_2.MPrenta("]")
			}

			if sectheader.shaddress > 0x1000 {
				stærð := sectheader.shStærð
				if sectheader.shTegund == 8 {
					ZeroBlokkInnsíðamappa(sectheader.shaddress, stærð, Síðamappaentry)
				} else {
					áfangastaður_2 := GetBætifromBendill(uintptr(sectheader.shaddress), int(stærð), int(stærð))
					SetjaBlokkInnsíðamappa(sectGildi, áfangastaður_2, stærð, Síðamappaentry)
				}
			}

			continue

			if EqualBæti(sectHeiti, ([]byte)(".text")) {
				console_2.MPrenta(".text")
				console_2.MPrenta("[")
				console_2.MUnsignedinteger32Prenta(sectheader.shaddress)
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(sectheader.shoffset)
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(sectheader.shStærð)
				console_2.MPrenta("]")
				copy(sjálft.texti[:sectheader.shStærð], sectGildi[:sectheader.shStærð])
				sjálft.textilen = sectheader.shStærð
			}
			if EqualBæti(sectHeiti, ([]byte)(".rel.text")) {
				console_2.MPrenta(".rel.text")
				console_2.MPrenta("[")
				console_2.MUnsignedinteger32Prenta(sectheader.shaddress)
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(sectheader.shStærð)
				console_2.MPrenta("]")
				for rt := uint32(0); rt < sectheader.shStærð/8; rt++ {
					offset := *(*uint32)(Pointer(&sectGildi[rt*8]))
					sjálft.relTexti[rt].offset = offset
					sjálft.relTexti[rt].oaddress = *(*uint32)(Pointer(&sjálft.texti[offset]))
					sjálft.relTexti[rt].number = *(*uint32)(Pointer(&sectGildi[rt*8+4]))
					sjálft.relTextilen++
				}
			}
			if EqualBæti(sectHeiti, ([]byte)(".dynsym")) {
				console_2.MPrenta(".dynsym")
				console_2.MPrenta("[")
				console_2.MUnsignedinteger32Prenta(sectheader.shaddress)
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(sectheader.shStærð)
				console_2.MPrenta("]")
				for rt := uint32(0); rt < sectheader.shStærð/8; rt++ {
					offset := *(*uint32)(Pointer(&sectGildi[rt*8]))
					sjálft.relTexti[rt].offset = offset
					sjálft.relTexti[rt].oaddress = *(*uint32)(Pointer(&sjálft.texti[offset]))
					sjálft.relTexti[rt].number = *(*uint32)(Pointer(&sectGildi[rt*8+4]))
					sjálft.relTextilen++
				}
			}
			if EqualBæti(sectHeiti, ([]byte)(".dynstr")) {
				console_2.MPrenta(".dynstr")
				console_2.MPrenta("[")
				console_2.MUnsignedinteger32Prenta(sectheader.shaddress)
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(sectheader.shStærð)
				console_2.MPrenta("]")
			}
			if EqualBæti(sectHeiti, ([]byte)(".strtab")) {
				console_2.MPrenta(".strtab")
				console_2.MPrenta("[")
				console_2.MUnsignedinteger32Prenta(sectheader.shaddress)
				console_2.MPrenta("]")
				rt := uint32(0)
				ræsa := uint32(0)

				for st := uint32(1); st < sectheader.shStærð; st++ {
					if sectGildi[st] == 0x0 || sectGildi[st] == ' ' {
						funcHeiti := sectGildi[ræsa+1 : st]
						console_2.MPrenta("+")
						console_2.MPrenta(funcHeiti)
						sjálft.strtab[rt] = BætitoStrengur(funcHeiti)
						ræsa = st
						rt++
					}
				}

			}

		}

		console_2.MPrenta(([]byte)("<------------"))
		for rt := uint32(0); rt < sjálft.relTextilen; rt++ {
			console_2.MPrenta("[")
			console_2.MPrenta(([]byte)(sjálft.strtab[rt]))
			console_2.MPrenta(":")
			console_2.MUnsignedinteger32Prenta(sjálft.relTexti[rt].number)
			console_2.MPrenta(":")

			console_2.MPrenta(([]byte)("]"))
		}
		console_2.MPrenta(([]byte)("------------>"))

		if textiBendill != nil {
			minnimanager.Laust(textiBendill)
		}

	}

}
