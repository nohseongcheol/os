/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package spustitelný_a_spojitelný_formát

import . "unsafe"

import . "konzole"
import . "util"
import . "paměťmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTyp		uint16
	emachine	uint16
	eVerze		uint32
	eZáznam		uint32
	ephoff		uint32
	eshoff		uint32
	ePříznaky	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNázev		uint32
	shTyp		uint32
	shPříznaky	uint32
	shAdresa	uint32
	shoffset	uint32
	shVelikost	uint32
	shOdkaz		uint32
	shInformace	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTyp		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pPříznaky	uint32
	pZarovnání	uint32
}
type Elf32Poznámka struct {
	nnamesz	uint32
	ndescsz	uint32
	nTyp	uint32
}
type Elf32dyn struct {
	dZnačka		uint32
	dvalKurzor	uint32
}
type Elf32rel struct {
	roffset		uint32
	rInformace	uint32
}
type Elf32rela struct {
	roffset		uint32
	rInformace	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNázev		uint32
	stHodnota	uint32
	stVelikost	uint32
	stInformace	uint8
	stOstatní	uint8
	stshndx		uint16
}
type relocationtext struct {
	offset	uint32
	číslo	uint32
	oAdresa	uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	reltext		[100]relocationtext
	reltextlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamické	uint32
}

func (self *Elf) GetZáznam(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eZáznam
}

func (self *Elf) Parse(data []byte, StránkaadresářZáznam uint32) {

	paměťmanager := TPaměťmanager{}
	var textKurzor Pointer = nil

	var konzole_2 = TKonzole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVelikost := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVelikost*i]))

			var sectNázev []byte
			spustit := uint32(strtab.shoffset + sectheader.shNázev)
			konec := spustit
			for ; ; konec++ {
				if data[konec] == 0x0 || data[konec] == ' ' {
					break
				}
			}
			sectNázev = data[spustit:konec]

			var sectHodnota []byte
			if sectheader.shTyp != 8 {
				konecoffset := sectheader.shoffset + sectheader.shVelikost
				if konecoffset < sectheader.shoffset || konecoffset > uint32(len(data)) {
					continue
				}
				sectHodnota = data[sectheader.shoffset:konecoffset]
			}

			if TotožnéBytů(sectNázev, ([]byte)(".got.plt")) {
				konzole_2.MTisknout("[")
				konzole_2.MTisknout(sectNázev)
				konzole_2.MTisknout(":")
				self.Got = sectheader.shAdresa
				konzole_2.MUnsignedinteger32Tisknout(self.Got)
				konzole_2.MTisknout("]")
			}
			if TotožnéBytů(sectNázev, ([]byte)(".dynamic")) {
				konzole_2.MTisknout("[")
				konzole_2.MTisknout(sectNázev)
				konzole_2.MTisknout(":")
				dynamické := sectheader.shAdresa
				self.Dynamické = dynamické
				konzole_2.MUnsignedinteger32Tisknout(dynamické)
				konzole_2.MTisknout("]")
			}

			if sectheader.shAdresa > 0x1000 {
				velikost := sectheader.shVelikost
				if sectheader.shTyp == 8 {
					NulaBlokovýVstupStránkaadresář(sectheader.shAdresa, velikost, StránkaadresářZáznam)
				} else {
					cíl_2 := GetBytůzKurzor(uintptr(sectheader.shAdresa), int(velikost), int(velikost))
					NastavitBlokovýVstupStránkaadresář(sectHodnota, cíl_2, velikost, StránkaadresářZáznam)
				}
			}

			continue

			if TotožnéBytů(sectNázev, ([]byte)(".text")) {
				konzole_2.MTisknout(".text")
				konzole_2.MTisknout("[")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shAdresa)
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shoffset)
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shVelikost)
				konzole_2.MTisknout("]")
				copy(self.text[:sectheader.shVelikost], sectHodnota[:sectheader.shVelikost])
				self.textlen = sectheader.shVelikost
			}
			if TotožnéBytů(sectNázev, ([]byte)(".rel.text")) {
				konzole_2.MTisknout(".rel.text")
				konzole_2.MTisknout("[")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shAdresa)
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shVelikost)
				konzole_2.MTisknout("]")
				for rt := uint32(0); rt < sectheader.shVelikost/8; rt++ {
					offset := *(*uint32)(Pointer(&sectHodnota[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oAdresa = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].číslo = *(*uint32)(Pointer(&sectHodnota[rt*8+4]))
					self.reltextlen++
				}
			}
			if TotožnéBytů(sectNázev, ([]byte)(".dynsym")) {
				konzole_2.MTisknout(".dynsym")
				konzole_2.MTisknout("[")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shAdresa)
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shVelikost)
				konzole_2.MTisknout("]")
				for rt := uint32(0); rt < sectheader.shVelikost/8; rt++ {
					offset := *(*uint32)(Pointer(&sectHodnota[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oAdresa = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].číslo = *(*uint32)(Pointer(&sectHodnota[rt*8+4]))
					self.reltextlen++
				}
			}
			if TotožnéBytů(sectNázev, ([]byte)(".dynstr")) {
				konzole_2.MTisknout(".dynstr")
				konzole_2.MTisknout("[")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shAdresa)
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shVelikost)
				konzole_2.MTisknout("]")
			}
			if TotožnéBytů(sectNázev, ([]byte)(".strtab")) {
				konzole_2.MTisknout(".strtab")
				konzole_2.MTisknout("[")
				konzole_2.MUnsignedinteger32Tisknout(sectheader.shAdresa)
				konzole_2.MTisknout("]")
				rt := uint32(0)
				spustit := uint32(0)

				for st := uint32(1); st < sectheader.shVelikost; st++ {
					if sectHodnota[st] == 0x0 || sectHodnota[st] == ' ' {
						funcNázev := sectHodnota[spustit+1 : st]
						konzole_2.MTisknout("+")
						konzole_2.MTisknout(funcNázev)
						self.strtab[rt] = Bytůdořetězec(funcNázev)
						spustit = st
						rt++
					}
				}

			}

		}

		konzole_2.MTisknout(([]byte)("<------------"))
		for rt := uint32(0); rt < self.reltextlen; rt++ {
			konzole_2.MTisknout("[")
			konzole_2.MTisknout(([]byte)(self.strtab[rt]))
			konzole_2.MTisknout(":")
			konzole_2.MUnsignedinteger32Tisknout(self.reltext[rt].číslo)
			konzole_2.MTisknout(":")

			konzole_2.MTisknout(([]byte)("]"))
		}
		konzole_2.MTisknout(([]byte)("------------>"))

		if textKurzor != nil {
			paměťmanager.Volné(textKurzor)
		}

	}

}
