/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "konzol"
import . "util"
import . "memóriamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTípus		uint16
	emachine	uint16
	eVerzió		uint32
	ebejegyzés	uint32
	ephoff		uint32
	eshoff		uint32
	eFlagek		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNév		uint32
	shTípus		uint32
	shFlagek	uint32
	shaddress	uint32
	shEltolás	uint32
	shMéret		uint32
	shHivatkozás	uint32
	shInfó		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTípus		uint32
	pEltolás	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlagek		uint32
	pIgazítás	uint32
}
type Elf32Megjegyzés struct {
	nnamesz	uint32
	ndescsz	uint32
	nTípus	uint32
}
type Elf32dyn struct {
	dCímke		uint32
	dvalMutató	uint32
}
type Elf32rel struct {
	rEltolás	uint32
	rInfó		uint32
}
type Elf32rela struct {
	rEltolás	uint32
	rInfó		uint32
	raddend		uint32
}
type Elf32sym struct {
	stNév	uint32
	stÉrték	uint32
	stMéret	uint32
	stInfó	uint8
	stEgyéb	uint8
	stshndx	uint16
}
type relocationSzöveg struct {
	eltolás		uint32
	szám		uint32
	oaddress	uint32
}
type Elf struct {
	szöveg		[]byte
	szöveglen	uint32
	relSzöveg	[100]relocationSzöveg
	relSzöveglen	uint32
	strtab		[100]string
	Got		uint32
	Dinamikus	uint32
}

func (self *Elf) Getbejegyzés(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.ebejegyzés
}

func (self *Elf) Parse(data []byte, OldalKönyvtárbejegyzés uint32) {

	memóriamanager := TMemóriamanager{}
	var szövegMutató Pointer = nil

	var konzol_2 = TKonzol{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderMéret := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderMéret*i]))

			var sectNév []byte
			indítás := uint32(strtab.shEltolás + sectheader.shNév)
			végén := indítás
			for ; ; végén++ {
				if data[végén] == 0x0 || data[végén] == ' ' {
					break
				}
			}
			sectNév = data[indítás:végén]

			var sectÉrték []byte
			if sectheader.shTípus != 8 {
				végénEltolás := sectheader.shEltolás + sectheader.shMéret
				if végénEltolás < sectheader.shEltolás || végénEltolás > uint32(len(data)) {
					continue
				}
				sectÉrték = data[sectheader.shEltolás:végénEltolás]
			}

			if EgyenlőBájt(sectNév, ([]byte)(".got.plt")) {
				konzol_2.MNyomtatás("[")
				konzol_2.MNyomtatás(sectNév)
				konzol_2.MNyomtatás(":")
				self.Got = sectheader.shaddress
				konzol_2.MUnsignedinteger32Nyomtatás(self.Got)
				konzol_2.MNyomtatás("]")
			}
			if EgyenlőBájt(sectNév, ([]byte)(".dynamic")) {
				konzol_2.MNyomtatás("[")
				konzol_2.MNyomtatás(sectNév)
				konzol_2.MNyomtatás(":")
				dinamikus := sectheader.shaddress
				self.Dinamikus = dinamikus
				konzol_2.MUnsignedinteger32Nyomtatás(dinamikus)
				konzol_2.MNyomtatás("]")
			}

			if sectheader.shaddress > 0x1000 {
				méret := sectheader.shMéret
				if sectheader.shTípus == 8 {
					NullaBlokkBeOldalKönyvtár(sectheader.shaddress, méret, OldalKönyvtárbejegyzés)
				} else {
					cél_2 := GetBájtfromMutató(uintptr(sectheader.shaddress), int(méret), int(méret))
					HalmazBlokkBeOldalKönyvtár(sectÉrték, cél_2, méret, OldalKönyvtárbejegyzés)
				}
			}

			continue

			if EgyenlőBájt(sectNév, ([]byte)(".text")) {
				konzol_2.MNyomtatás(".text")
				konzol_2.MNyomtatás("[")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shaddress)
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shEltolás)
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shMéret)
				konzol_2.MNyomtatás("]")
				copy(self.szöveg[:sectheader.shMéret], sectÉrték[:sectheader.shMéret])
				self.szöveglen = sectheader.shMéret
			}
			if EgyenlőBájt(sectNév, ([]byte)(".rel.text")) {
				konzol_2.MNyomtatás(".rel.text")
				konzol_2.MNyomtatás("[")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shaddress)
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shMéret)
				konzol_2.MNyomtatás("]")
				for rt := uint32(0); rt < sectheader.shMéret/8; rt++ {
					eltolás := *(*uint32)(Pointer(&sectÉrték[rt*8]))
					self.relSzöveg[rt].eltolás = eltolás
					self.relSzöveg[rt].oaddress = *(*uint32)(Pointer(&self.szöveg[eltolás]))
					self.relSzöveg[rt].szám = *(*uint32)(Pointer(&sectÉrték[rt*8+4]))
					self.relSzöveglen++
				}
			}
			if EgyenlőBájt(sectNév, ([]byte)(".dynsym")) {
				konzol_2.MNyomtatás(".dynsym")
				konzol_2.MNyomtatás("[")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shaddress)
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shMéret)
				konzol_2.MNyomtatás("]")
				for rt := uint32(0); rt < sectheader.shMéret/8; rt++ {
					eltolás := *(*uint32)(Pointer(&sectÉrték[rt*8]))
					self.relSzöveg[rt].eltolás = eltolás
					self.relSzöveg[rt].oaddress = *(*uint32)(Pointer(&self.szöveg[eltolás]))
					self.relSzöveg[rt].szám = *(*uint32)(Pointer(&sectÉrték[rt*8+4]))
					self.relSzöveglen++
				}
			}
			if EgyenlőBájt(sectNév, ([]byte)(".dynstr")) {
				konzol_2.MNyomtatás(".dynstr")
				konzol_2.MNyomtatás("[")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shaddress)
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shMéret)
				konzol_2.MNyomtatás("]")
			}
			if EgyenlőBájt(sectNév, ([]byte)(".strtab")) {
				konzol_2.MNyomtatás(".strtab")
				konzol_2.MNyomtatás("[")
				konzol_2.MUnsignedinteger32Nyomtatás(sectheader.shaddress)
				konzol_2.MNyomtatás("]")
				rt := uint32(0)
				indítás := uint32(0)

				for st := uint32(1); st < sectheader.shMéret; st++ {
					if sectÉrték[st] == 0x0 || sectÉrték[st] == ' ' {
						funcNév := sectÉrték[indítás+1 : st]
						konzol_2.MNyomtatás("+")
						konzol_2.MNyomtatás(funcNév)
						self.strtab[rt] = BájttoKarakterlánc(funcNév)
						indítás = st
						rt++
					}
				}

			}

		}

		konzol_2.MNyomtatás(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relSzöveglen; rt++ {
			konzol_2.MNyomtatás("[")
			konzol_2.MNyomtatás(([]byte)(self.strtab[rt]))
			konzol_2.MNyomtatás(":")
			konzol_2.MUnsignedinteger32Nyomtatás(self.relSzöveg[rt].szám)
			konzol_2.MNyomtatás(":")

			konzol_2.MNyomtatás(([]byte)("]"))
		}
		konzol_2.MNyomtatás(([]byte)("------------>"))

		if szövegMutató != nil {
			memóriamanager.Szabad(szövegMutató)
		}

	}

}
