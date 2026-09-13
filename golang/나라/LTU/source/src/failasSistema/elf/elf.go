package elf

import . "unsafe"

import . "console"
import . "util"
import . "atmintismanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTipas		uint16
	emachine	uint16
	eVersija	uint32
	eįrašas		uint32
	ephoff		uint32
	eshoff		uint32
	eParametrai	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shPavadinimas	uint32
	shTipas		uint32
	shParametrai	uint32
	shaddress	uint32
	shoffset	uint32
	shDydis		uint32
	shNuoroda	uint32
	shInformacija	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramaheader struct {
	pTipas		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pParametrai	uint32
	pLygiuotė	uint32
}
type Elf32Pastaba struct {
	nnamesz	uint32
	ndescsz	uint32
	nTipas	uint32
}
type Elf32dyn struct {
	dŽymė		uint32
	dvalRodyklė	uint32
}
type Elf32rel struct {
	roffset		uint32
	rInformacija	uint32
}
type Elf32rela struct {
	roffset		uint32
	rInformacija	uint32
	raddend		uint32
}
type Elf32sym struct {
	stPavadinimas	uint32
	stReikšmė	uint32
	stDydis		uint32
	stInformacija	uint8
	stKita		uint8
	stshndx		uint16
}
type relocationTekstas struct {
	offset		uint32
	skaičius	uint32
	oaddress	uint32
}
type Elf struct {
	tekstas		[]byte
	tekstaslen	uint32
	relTekstas	[100]relocationTekstas
	relTekstaslen	uint32
	strtab		[100]string
	Got		uint32
	Dinaminis	uint32
}

func (self *Elf) Getįrašas(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eįrašas
}

func (self *Elf) Parse(data []byte, Puslapiskatalogasįrašas uint32) {

	atmintismanager := TAtmintismanager{}
	var tekstasRodyklė Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderDydis := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderDydis*i]))

			var sectPavadinimas []byte
			paleisti := uint32(strtab.shoffset + sectheader.shPavadinimas)
			pab := paleisti
			for ; ; pab++ {
				if data[pab] == 0x0 || data[pab] == ' ' {
					break
				}
			}
			sectPavadinimas = data[paleisti:pab]

			var sectReikšmė []byte
			if sectheader.shTipas != 8 {
				paboffset := sectheader.shoffset + sectheader.shDydis
				if paboffset < sectheader.shoffset || paboffset > uint32(len(data)) {
					continue
				}
				sectReikšmė = data[sectheader.shoffset:paboffset]
			}

			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".got.plt")) {
				console_2.MSpausdinti("[")
				console_2.MSpausdinti(sectPavadinimas)
				console_2.MSpausdinti(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Spausdinti(self.Got)
				console_2.MSpausdinti("]")
			}
			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".dynamic")) {
				console_2.MSpausdinti("[")
				console_2.MSpausdinti(sectPavadinimas)
				console_2.MSpausdinti(":")
				dinaminis := sectheader.shaddress
				self.Dinaminis = dinaminis
				console_2.MUnsignedinteger32Spausdinti(dinaminis)
				console_2.MSpausdinti("]")
			}

			if sectheader.shaddress > 0x1000 {
				dydis := sectheader.shDydis
				if sectheader.shTipas == 8 {
					NulisBlokasĮPuslapiskatalogas(sectheader.shaddress, dydis, Puslapiskatalogasįrašas)
				} else {
					tikslas_2 := GetBaitųfromRodyklė(uintptr(sectheader.shaddress), int(dydis), int(dydis))
					NustatytaBlokasĮPuslapiskatalogas(sectReikšmė, tikslas_2, dydis, Puslapiskatalogasįrašas)
				}
			}

			continue

			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".text")) {
				console_2.MSpausdinti(".text")
				console_2.MSpausdinti("[")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shaddress)
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shoffset)
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shDydis)
				console_2.MSpausdinti("]")
				copy(self.tekstas[:sectheader.shDydis], sectReikšmė[:sectheader.shDydis])
				self.tekstaslen = sectheader.shDydis
			}
			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".rel.text")) {
				console_2.MSpausdinti(".rel.text")
				console_2.MSpausdinti("[")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shaddress)
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shDydis)
				console_2.MSpausdinti("]")
				for rt := uint32(0); rt < sectheader.shDydis/8; rt++ {
					offset := *(*uint32)(Pointer(&sectReikšmė[rt*8]))
					self.relTekstas[rt].offset = offset
					self.relTekstas[rt].oaddress = *(*uint32)(Pointer(&self.tekstas[offset]))
					self.relTekstas[rt].skaičius = *(*uint32)(Pointer(&sectReikšmė[rt*8+4]))
					self.relTekstaslen++
				}
			}
			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".dynsym")) {
				console_2.MSpausdinti(".dynsym")
				console_2.MSpausdinti("[")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shaddress)
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shDydis)
				console_2.MSpausdinti("]")
				for rt := uint32(0); rt < sectheader.shDydis/8; rt++ {
					offset := *(*uint32)(Pointer(&sectReikšmė[rt*8]))
					self.relTekstas[rt].offset = offset
					self.relTekstas[rt].oaddress = *(*uint32)(Pointer(&self.tekstas[offset]))
					self.relTekstas[rt].skaičius = *(*uint32)(Pointer(&sectReikšmė[rt*8+4]))
					self.relTekstaslen++
				}
			}
			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".dynstr")) {
				console_2.MSpausdinti(".dynstr")
				console_2.MSpausdinti("[")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shaddress)
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shDydis)
				console_2.MSpausdinti("]")
			}
			if SuvienodintiBaitų(sectPavadinimas, ([]byte)(".strtab")) {
				console_2.MSpausdinti(".strtab")
				console_2.MSpausdinti("[")
				console_2.MUnsignedinteger32Spausdinti(sectheader.shaddress)
				console_2.MSpausdinti("]")
				rt := uint32(0)
				paleisti := uint32(0)

				for st := uint32(1); st < sectheader.shDydis; st++ {
					if sectReikšmė[st] == 0x0 || sectReikšmė[st] == ' ' {
						funcPavadinimas := sectReikšmė[paleisti+1 : st]
						console_2.MSpausdinti("+")
						console_2.MSpausdinti(funcPavadinimas)
						self.strtab[rt] = BaitųtoEilutė(funcPavadinimas)
						paleisti = st
						rt++
					}
				}

			}

		}

		console_2.MSpausdinti(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relTekstaslen; rt++ {
			console_2.MSpausdinti("[")
			console_2.MSpausdinti(([]byte)(self.strtab[rt]))
			console_2.MSpausdinti(":")
			console_2.MUnsignedinteger32Spausdinti(self.relTekstas[rt].skaičius)
			console_2.MSpausdinti(":")

			console_2.MSpausdinti(([]byte)("]"))
		}
		console_2.MSpausdinti(([]byte)("------------>"))

		if tekstasRodyklė != nil {
			atmintismanager.Laisva(tekstasRodyklė)
		}

	}

}
