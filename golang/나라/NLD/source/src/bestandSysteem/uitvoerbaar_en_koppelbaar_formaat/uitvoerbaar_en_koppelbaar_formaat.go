package uitvoerbaar_en_koppelbaar_formaat

import . "unsafe"

import . "console"
import . "util"
import . "geheugenmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eSoort		uint16
	emachine	uint16
	eVersie		uint32
	eItem		uint32
	ephoff		uint32
	eshoff		uint32
	eVlaggen	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNaam		uint32
	shSoort		uint32
	shVlaggen	uint32
	shaddress	uint32
	shVerschuiving	uint32
	shGrootte	uint32
	shKoppeling	uint32
	shInformatie	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogrammaheader struct {
	pSoort		uint32
	pVerschuiving	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pVlaggen	uint32
	pUitlijnen	uint32
}
type Elf32Notitie struct {
	nnamesz	uint32
	ndescsz	uint32
	nSoort	uint32
}
type Elf32dyn struct {
	dMarkering		uint32
	dvalMuisaanwijzer	uint32
}
type Elf32rel struct {
	rVerschuiving	uint32
	rInformatie	uint32
}
type Elf32rela struct {
	rVerschuiving	uint32
	rInformatie	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNaam		uint32
	stWaarde	uint32
	stGrootte	uint32
	stInformatie	uint8
	stOverig	uint8
	stshndx		uint16
}
type relocationTekst struct {
	verschuiving	uint32
	getal		uint32
	oaddress	uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamisch	uint32
}

func (zelf *Elf) GetItem(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eItem
}

func (zelf *Elf) Parse(data []byte, PaginaMapItem uint32) {

	geheugenmanager := TGeheugenmanager{}
	var tekstMuisaanwijzer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderGrootte := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderGrootte*i]))

			var sectNaam []byte
			starten := uint32(strtab.shVerschuiving + sectheader.shNaam)
			eind := starten
			for ; ; eind++ {
				if data[eind] == 0x0 || data[eind] == ' ' {
					break
				}
			}
			sectNaam = data[starten:eind]

			var sectWaarde []byte
			if sectheader.shSoort != 8 {
				eindVerschuiving := sectheader.shVerschuiving + sectheader.shGrootte
				if eindVerschuiving < sectheader.shVerschuiving || eindVerschuiving > uint32(len(data)) {
					continue
				}
				sectWaarde = data[sectheader.shVerschuiving:eindVerschuiving]
			}

			if Gelijkebytes(sectNaam, ([]byte)(".got.plt")) {
				console_2.MAfdrukken("[")
				console_2.MAfdrukken(sectNaam)
				console_2.MAfdrukken(":")
				zelf.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Afdrukken(zelf.Got)
				console_2.MAfdrukken("]")
			}
			if Gelijkebytes(sectNaam, ([]byte)(".dynamic")) {
				console_2.MAfdrukken("[")
				console_2.MAfdrukken(sectNaam)
				console_2.MAfdrukken(":")
				dynamisch := sectheader.shaddress
				zelf.Dynamisch = dynamisch
				console_2.MUnsignedinteger32Afdrukken(dynamisch)
				console_2.MAfdrukken("]")
			}

			if sectheader.shaddress > 0x1000 {
				grootte := sectheader.shGrootte
				if sectheader.shSoort == 8 {
					ZeroBlokinPaginaMap(sectheader.shaddress, grootte, PaginaMapItem)
				} else {
					bestemming_2 := GetbytesvanMuisaanwijzer(uintptr(sectheader.shaddress), int(grootte), int(grootte))
					InstellenBlokinPaginaMap(sectWaarde, bestemming_2, grootte, PaginaMapItem)
				}
			}

			continue

			if Gelijkebytes(sectNaam, ([]byte)(".text")) {
				console_2.MAfdrukken(".text")
				console_2.MAfdrukken("[")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shaddress)
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shVerschuiving)
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shGrootte)
				console_2.MAfdrukken("]")
				copy(zelf.tekst[:sectheader.shGrootte], sectWaarde[:sectheader.shGrootte])
				zelf.tekstlen = sectheader.shGrootte
			}
			if Gelijkebytes(sectNaam, ([]byte)(".rel.text")) {
				console_2.MAfdrukken(".rel.text")
				console_2.MAfdrukken("[")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shaddress)
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shGrootte)
				console_2.MAfdrukken("]")
				for rt := uint32(0); rt < sectheader.shGrootte/8; rt++ {
					verschuiving := *(*uint32)(Pointer(&sectWaarde[rt*8]))
					zelf.relTekst[rt].verschuiving = verschuiving
					zelf.relTekst[rt].oaddress = *(*uint32)(Pointer(&zelf.tekst[verschuiving]))
					zelf.relTekst[rt].getal = *(*uint32)(Pointer(&sectWaarde[rt*8+4]))
					zelf.relTekstlen++
				}
			}
			if Gelijkebytes(sectNaam, ([]byte)(".dynsym")) {
				console_2.MAfdrukken(".dynsym")
				console_2.MAfdrukken("[")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shaddress)
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shGrootte)
				console_2.MAfdrukken("]")
				for rt := uint32(0); rt < sectheader.shGrootte/8; rt++ {
					verschuiving := *(*uint32)(Pointer(&sectWaarde[rt*8]))
					zelf.relTekst[rt].verschuiving = verschuiving
					zelf.relTekst[rt].oaddress = *(*uint32)(Pointer(&zelf.tekst[verschuiving]))
					zelf.relTekst[rt].getal = *(*uint32)(Pointer(&sectWaarde[rt*8+4]))
					zelf.relTekstlen++
				}
			}
			if Gelijkebytes(sectNaam, ([]byte)(".dynstr")) {
				console_2.MAfdrukken(".dynstr")
				console_2.MAfdrukken("[")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shaddress)
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shGrootte)
				console_2.MAfdrukken("]")
			}
			if Gelijkebytes(sectNaam, ([]byte)(".strtab")) {
				console_2.MAfdrukken(".strtab")
				console_2.MAfdrukken("[")
				console_2.MUnsignedinteger32Afdrukken(sectheader.shaddress)
				console_2.MAfdrukken("]")
				rt := uint32(0)
				starten := uint32(0)

				for st := uint32(1); st < sectheader.shGrootte; st++ {
					if sectWaarde[st] == 0x0 || sectWaarde[st] == ' ' {
						funcNaam := sectWaarde[starten+1 : st]
						console_2.MAfdrukken("+")
						console_2.MAfdrukken(funcNaam)
						zelf.strtab[rt] = BytesnaarTekstsnoer(funcNaam)
						starten = st
						rt++
					}
				}

			}

		}

		console_2.MAfdrukken(([]byte)("<------------"))
		for rt := uint32(0); rt < zelf.relTekstlen; rt++ {
			console_2.MAfdrukken("[")
			console_2.MAfdrukken(([]byte)(zelf.strtab[rt]))
			console_2.MAfdrukken(":")
			console_2.MUnsignedinteger32Afdrukken(zelf.relTekst[rt].getal)
			console_2.MAfdrukken(":")

			console_2.MAfdrukken(([]byte)("]"))
		}
		console_2.MAfdrukken(([]byte)("------------>"))

		if tekstMuisaanwijzer != nil {
			geheugenmanager.Vrij(tekstMuisaanwijzer)
		}

	}

}
