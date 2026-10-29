/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "konzola"
import . "util"
import . "memorijamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eVrsta		uint16
	emachine	uint16
	eIzdanje		uint32
	eunos		uint32
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
	shNaziv		uint32
	shVrsta		uint32
	shParametri	uint32
	shaddress	uint32
	shoffset	uint32
	shVeličina	uint32
	shVeza		uint32
	shPodaci	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pVrsta		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pParametri	uint32
	pPoravnanje	uint32
}
type Elf32Beleška struct {
	nnamesz	uint32
	ndescsz	uint32
	nVrsta	uint32
}
type Elf32dyn struct {
	doznaka		uint32
	dvalPokazivač	uint32
}
type Elf32rel struct {
	roffset	uint32
	rPodaci	uint32
}
type Elf32rela struct {
	roffset	uint32
	rPodaci	uint32
	raddend	uint32
}
type Elf32sym struct {
	stNaziv		uint32
	stVrednost	uint32
	stVeličina	uint32
	stPodaci	uint8
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
	Rastegljivo	uint32
}

func (isti *Elf) Getunos(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eunos
}

func (isti *Elf) Parse(data []byte, STRANADirektorijumunos uint32) {

	memorijamanager := TMemorijamanager{}
	var tekstPokazivač Pointer = nil

	var konzola_2 = TKonzola{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVeličina := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVeličina*i]))

			var sectNaziv []byte
			pokreni := uint32(strtab.shoffset + sectheader.shNaziv)
			kraj := pokreni
			for ; ; kraj++ {
				if data[kraj] == 0x0 || data[kraj] == ' ' {
					break
				}
			}
			sectNaziv = data[pokreni:kraj]

			var sectVrednost []byte
			if sectheader.shVrsta != 8 {
				krajoffset := sectheader.shoffset + sectheader.shVeličina
				if krajoffset < sectheader.shoffset || krajoffset > uint32(len(data)) {
					continue
				}
				sectVrednost = data[sectheader.shoffset:krajoffset]
			}

			if IstaBajtova(sectNaziv, ([]byte)(".got.plt")) {
				konzola_2.MŠtampaj("[")
				konzola_2.MŠtampaj(sectNaziv)
				konzola_2.MŠtampaj(":")
				isti.Got = sectheader.shaddress
				konzola_2.MUnsignedinteger32Štampaj(isti.Got)
				konzola_2.MŠtampaj("]")
			}
			if IstaBajtova(sectNaziv, ([]byte)(".dynamic")) {
				konzola_2.MŠtampaj("[")
				konzola_2.MŠtampaj(sectNaziv)
				konzola_2.MŠtampaj(":")
				rastegljivo := sectheader.shaddress
				isti.Rastegljivo = rastegljivo
				konzola_2.MUnsignedinteger32Štampaj(rastegljivo)
				konzola_2.MŠtampaj("]")
			}

			if sectheader.shaddress > 0x1000 {
				veličina := sectheader.shVeličina
				if sectheader.shVrsta == 8 {
					ZeroBlokPrimljenoSTRANADirektorijum(sectheader.shaddress, veličina, STRANADirektorijumunos)
				} else {
					odredište_2 := GetBajtovasaPokazivač(uintptr(sectheader.shaddress), int(veličina), int(veličina))
					SkupBlokPrimljenoSTRANADirektorijum(sectVrednost, odredište_2, veličina, STRANADirektorijumunos)
				}
			}

			continue

			if IstaBajtova(sectNaziv, ([]byte)(".text")) {
				konzola_2.MŠtampaj(".text")
				konzola_2.MŠtampaj("[")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shoffset)
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				konzola_2.MŠtampaj("]")
				copy(isti.tekst[:sectheader.shVeličina], sectVrednost[:sectheader.shVeličina])
				isti.tekstlen = sectheader.shVeličina
			}
			if IstaBajtova(sectNaziv, ([]byte)(".rel.text")) {
				konzola_2.MŠtampaj(".rel.text")
				konzola_2.MŠtampaj("[")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				konzola_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrednost[rt*8]))
					isti.relTekst[rt].offset = offset
					isti.relTekst[rt].oaddress = *(*uint32)(Pointer(&isti.tekst[offset]))
					isti.relTekst[rt].broj = *(*uint32)(Pointer(&sectVrednost[rt*8+4]))
					isti.relTekstlen++
				}
			}
			if IstaBajtova(sectNaziv, ([]byte)(".dynsym")) {
				konzola_2.MŠtampaj(".dynsym")
				konzola_2.MŠtampaj("[")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				konzola_2.MŠtampaj("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrednost[rt*8]))
					isti.relTekst[rt].offset = offset
					isti.relTekst[rt].oaddress = *(*uint32)(Pointer(&isti.tekst[offset]))
					isti.relTekst[rt].broj = *(*uint32)(Pointer(&sectVrednost[rt*8+4]))
					isti.relTekstlen++
				}
			}
			if IstaBajtova(sectNaziv, ([]byte)(".dynstr")) {
				konzola_2.MŠtampaj(".dynstr")
				konzola_2.MŠtampaj("[")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shVeličina)
				konzola_2.MŠtampaj("]")
			}
			if IstaBajtova(sectNaziv, ([]byte)(".strtab")) {
				konzola_2.MŠtampaj(".strtab")
				konzola_2.MŠtampaj("[")
				konzola_2.MUnsignedinteger32Štampaj(sectheader.shaddress)
				konzola_2.MŠtampaj("]")
				rt := uint32(0)
				pokreni := uint32(0)

				for st := uint32(1); st < sectheader.shVeličina; st++ {
					if sectVrednost[st] == 0x0 || sectVrednost[st] == ' ' {
						funcNaziv := sectVrednost[pokreni+1 : st]
						konzola_2.MŠtampaj("+")
						konzola_2.MŠtampaj(funcNaziv)
						isti.strtab[rt] = Bajtovatoniska(funcNaziv)
						pokreni = st
						rt++
					}
				}

			}

		}

		konzola_2.MŠtampaj(([]byte)("<------------"))
		for rt := uint32(0); rt < isti.relTekstlen; rt++ {
			konzola_2.MŠtampaj("[")
			konzola_2.MŠtampaj(([]byte)(isti.strtab[rt]))
			konzola_2.MŠtampaj(":")
			konzola_2.MUnsignedinteger32Štampaj(isti.relTekst[rt].broj)
			konzola_2.MŠtampaj(":")

			konzola_2.MŠtampaj(([]byte)("]"))
		}
		konzola_2.MŠtampaj(([]byte)("------------>"))

		if tekstPokazivač != nil {
			memorijamanager.Slobodno(tekstPokazivač)
		}

	}

}
