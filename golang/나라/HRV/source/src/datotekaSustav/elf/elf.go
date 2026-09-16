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
	eVrsta		uint16
	emachine	uint16
	eInačica	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eZastavice	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shIme		uint32
	shVrsta		uint32
	shZastavice	uint32
	shaddress	uint32
	shoffset	uint32
	shVeličina	uint32
	shPoveznica	uint32
	shInformacije	uint32
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
	pZastavice	uint32
	pPoravnanje	uint32
}
type Elf32Bilješka struct {
	nnamesz	uint32
	ndescsz	uint32
	nVrsta	uint32
}
type Elf32dyn struct {
	dOznaka		uint32
	dvalPokazivač	uint32
}
type Elf32rel struct {
	roffset		uint32
	rInformacije	uint32
}
type Elf32rela struct {
	roffset		uint32
	rInformacije	uint32
	raddend		uint32
}
type Elf32sym struct {
	stIme		uint32
	stVrijednost	uint32
	stVeličina	uint32
	stInformacije	uint8
	stOstalo	uint8
	stshndx		uint16
}
type relocationTekst struct {
	offset		uint32
	bROJ		uint32
	oaddress	uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dinamično	uint32
}

func (sam *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (sam *Elf) Parse(data []byte, StranicaDirektorijentry uint32) {

	memorijamanager := TMemorijamanager{}
	var tekstPokazivač Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVeličina := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVeličina*i]))

			var sectIme []byte
			pokreni := uint32(strtab.shoffset + sectheader.shIme)
			kraj := pokreni
			for ; ; kraj++ {
				if data[kraj] == 0x0 || data[kraj] == ' ' {
					break
				}
			}
			sectIme = data[pokreni:kraj]

			var sectVrijednost []byte
			if sectheader.shVrsta != 8 {
				krajoffset := sectheader.shoffset + sectheader.shVeličina
				if krajoffset < sectheader.shoffset || krajoffset > uint32(len(data)) {
					continue
				}
				sectVrijednost = data[sectheader.shoffset:krajoffset]
			}

			if JednakoBajtova(sectIme, ([]byte)(".got.plt")) {
				console_2.MIspis("[")
				console_2.MIspis(sectIme)
				console_2.MIspis(":")
				sam.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Ispis(sam.Got)
				console_2.MIspis("]")
			}
			if JednakoBajtova(sectIme, ([]byte)(".dynamic")) {
				console_2.MIspis("[")
				console_2.MIspis(sectIme)
				console_2.MIspis(":")
				dinamično := sectheader.shaddress
				sam.Dinamično = dinamično
				console_2.MUnsignedinteger32Ispis(dinamično)
				console_2.MIspis("]")
			}

			if sectheader.shaddress > 0x1000 {
				veličina := sectheader.shVeličina
				if sectheader.shVrsta == 8 {
					ZeroBlokirajPovećajStranicaDirektorij(sectheader.shaddress, veličina, StranicaDirektorijentry)
				} else {
					odredište_2 := GetBajtovafromPokazivač(uintptr(sectheader.shaddress), int(veličina), int(veličina))
					PostaviBlokirajPovećajStranicaDirektorij(sectVrijednost, odredište_2, veličina, StranicaDirektorijentry)
				}
			}

			continue

			if JednakoBajtova(sectIme, ([]byte)(".text")) {
				console_2.MIspis(".text")
				console_2.MIspis("[")
				console_2.MUnsignedinteger32Ispis(sectheader.shaddress)
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(sectheader.shoffset)
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(sectheader.shVeličina)
				console_2.MIspis("]")
				copy(sam.tekst[:sectheader.shVeličina], sectVrijednost[:sectheader.shVeličina])
				sam.tekstlen = sectheader.shVeličina
			}
			if JednakoBajtova(sectIme, ([]byte)(".rel.text")) {
				console_2.MIspis(".rel.text")
				console_2.MIspis("[")
				console_2.MUnsignedinteger32Ispis(sectheader.shaddress)
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(sectheader.shVeličina)
				console_2.MIspis("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrijednost[rt*8]))
					sam.relTekst[rt].offset = offset
					sam.relTekst[rt].oaddress = *(*uint32)(Pointer(&sam.tekst[offset]))
					sam.relTekst[rt].bROJ = *(*uint32)(Pointer(&sectVrijednost[rt*8+4]))
					sam.relTekstlen++
				}
			}
			if JednakoBajtova(sectIme, ([]byte)(".dynsym")) {
				console_2.MIspis(".dynsym")
				console_2.MIspis("[")
				console_2.MUnsignedinteger32Ispis(sectheader.shaddress)
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(sectheader.shVeličina)
				console_2.MIspis("]")
				for rt := uint32(0); rt < sectheader.shVeličina/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrijednost[rt*8]))
					sam.relTekst[rt].offset = offset
					sam.relTekst[rt].oaddress = *(*uint32)(Pointer(&sam.tekst[offset]))
					sam.relTekst[rt].bROJ = *(*uint32)(Pointer(&sectVrijednost[rt*8+4]))
					sam.relTekstlen++
				}
			}
			if JednakoBajtova(sectIme, ([]byte)(".dynstr")) {
				console_2.MIspis(".dynstr")
				console_2.MIspis("[")
				console_2.MUnsignedinteger32Ispis(sectheader.shaddress)
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(sectheader.shVeličina)
				console_2.MIspis("]")
			}
			if JednakoBajtova(sectIme, ([]byte)(".strtab")) {
				console_2.MIspis(".strtab")
				console_2.MIspis("[")
				console_2.MUnsignedinteger32Ispis(sectheader.shaddress)
				console_2.MIspis("]")
				rt := uint32(0)
				pokreni := uint32(0)

				for st := uint32(1); st < sectheader.shVeličina; st++ {
					if sectVrijednost[st] == 0x0 || sectVrijednost[st] == ' ' {
						funcIme := sectVrijednost[pokreni+1 : st]
						console_2.MIspis("+")
						console_2.MIspis(funcIme)
						sam.strtab[rt] = BajtovatoZnakovniniz(funcIme)
						pokreni = st
						rt++
					}
				}

			}

		}

		console_2.MIspis(([]byte)("<------------"))
		for rt := uint32(0); rt < sam.relTekstlen; rt++ {
			console_2.MIspis("[")
			console_2.MIspis(([]byte)(sam.strtab[rt]))
			console_2.MIspis(":")
			console_2.MUnsignedinteger32Ispis(sam.relTekst[rt].bROJ)
			console_2.MIspis(":")

			console_2.MIspis(([]byte)("]"))
		}
		console_2.MIspis(([]byte)("------------>"))

		if tekstPokazivač != nil {
			memorijamanager.Slobodno(tekstPokazivač)
		}

	}

}
