/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "memorijamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTip		uint16
	emachine	uint16
	eVerzija	uint32
	eunos		uint32
	ephoff		uint32
	eshoff		uint32
	eZastave	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNaziv		uint32
	shTip		uint32
	shZastave	uint32
	shaddress	uint32
	shoffset	uint32
	shVeličina	uint32
	shVeza		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTip		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pZastave	uint32
	pPoravnaj	uint32
}
type Elf32Bilješka struct {
	nnamesz	uint32
	ndescsz	uint32
	nTip	uint32
}
type Elf32dyn struct {
	dOznaka		uint32
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
	stNaziv		uint32
	stVrijednost	uint32
	stVeličina	uint32
	stinfo		uint8
	stDrugo		uint8
	stshndx		uint16
}
type relocationTekst struct {
	offset		uint32
	broj		uint32
	oaddress	uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getunos(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eunos
}

func (self *Elf) Parse(data []byte, StranicaDirektorijunos uint32) {

	memorijamanager := TMemorijamanager{}
	var tekstpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVeličina := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVeličina*i]))

			var sectNaziv []byte
			start := uint32(strtab.shoffset + sectheader.shNaziv)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectNaziv = data[start:end]

			var sectVrijednost []byte
			if sectheader.shTip != 8 {
				endoffset := sectheader.shoffset + sectheader.shVeličina
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectVrijednost = data[sectheader.shoffset:endoffset]
			}

			if EqualBajtova(sectNaziv, ([]byte)(".got.plt")) {
				console_2.MŠtampaj("[")
				console_2.MŠtampaj(sectNaziv)
				console_2.MŠtampaj(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Štampaj(self.Got)
				console_2.MŠtampaj("]")
			}
			if EqualBajtova(sectNaziv, ([]byte)(".dynamic")) {
				console_2.MŠtampaj("[")
				console_2.MŠtampaj(sectNaziv)
				console_2.MŠtampaj(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Štampaj(dynamic)
				console_2.MŠtampaj("]")
			}

			if sectheader.shaddress > 0x1000 {
				veličina := sectheader.shVeličina
				if sectheader.shTip == 8 {
					ZeroblokPrimljenoStranicaDirektorij(sectheader.shaddress, veličina, StranicaDirektorijunos)
				} else {
					odredište_2 := GetBajtovafrompointer(uintptr(sectheader.shaddress), int(veličina), int(veličina))
					SkupblokPrimljenoStranicaDirektorij(sectVrijednost, odredište_2, veličina, StranicaDirektorijunos)
				}
			}

			continue

			if EqualBajtova(sectNaziv, ([]byte)(".text")) {
				console_2.MŠtampaj(".text")
				console_2.MŠtampaj("[")
				console_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(sectheader.shoffset)
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				console_2.MŠtampaj("]")
				copy(self.tekst[:sectheader.shVeličina], sectVrijednost[:sectheader.shVeličina])
				self.tekstlen = sectheader.shVeličina
			}
			if EqualBajtova(sectNaziv, ([]byte)(".rel.text")) {
				console_2.MŠtampaj(".rel.text")
				console_2.MŠtampaj("[")
				console_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				console_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrijednost[rt*8]))
					self.relTekst[rt].offset = offset
					self.relTekst[rt].oaddress = *(*uint32)(Pointer(&self.tekst[offset]))
					self.relTekst[rt].broj = *(*uint32)(Pointer(&sectVrijednost[rt*8+4]))
					self.relTekstlen++
				}
			}
			if EqualBajtova(sectNaziv, ([]byte)(".dynsym")) {
				console_2.MŠtampaj(".dynsym")
				console_2.MŠtampaj("[")
				console_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				console_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrijednost[rt*8]))
					self.relTekst[rt].offset = offset
					self.relTekst[rt].oaddress = *(*uint32)(Pointer(&self.tekst[offset]))
					self.relTekst[rt].broj = *(*uint32)(Pointer(&sectVrijednost[rt*8+4]))
					self.relTekstlen++
				}
			}
			if EqualBajtova(sectNaziv, ([]byte)(".dynstr")) {
				console_2.MŠtampaj(".dynstr")
				console_2.MŠtampaj("[")
				console_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				console_2.MŠtampaj("]")
			}
			if EqualBajtova(sectNaziv, ([]byte)(".strtab")) {
				console_2.MŠtampaj(".strtab")
				console_2.MŠtampaj("[")
				console_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				console_2.MŠtampaj("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shVeličina; st++ {
					if sectVrijednost[st] == 0x0 || sectVrijednost[st] == ' ' {
						funcNaziv := sectVrijednost[start+1 : st]
						console_2.MŠtampaj("+")
						console_2.MŠtampaj(funcNaziv)
						self.strtab[rt] = BajtovatoNIZ(funcNaziv)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MŠtampaj(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relTekstlen; rt++ {
			console_2.MŠtampaj("[")
			console_2.MŠtampaj(([]byte)(self.strtab[rt]))
			console_2.MŠtampaj(":")
			console_2.MUnsignedinteger32Štampaj(self.relTekst[rt].broj)
			console_2.MŠtampaj(":")

			console_2.MŠtampaj(([]byte)("]"))
		}
		console_2.MŠtampaj(([]byte)("------------>"))

		if tekstpointer != nil {
			memorijamanager.Slobodno(tekstpointer)
		}

	}

}
