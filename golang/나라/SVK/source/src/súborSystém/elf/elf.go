package elf

import . "unsafe"

import . "konzola"
import . "util"
import . "pamäťmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTyp		uint16
	emachine	uint16
	eVerzia		uint32
	epoložka	uint32
	ephoff		uint32
	eshoff		uint32
	ePríznaky	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNázov		uint32
	shTyp		uint32
	shPríznaky	uint32
	shaddress	uint32
	shPosunutie	uint32
	shVeľkosť	uint32
	shOdkaz		uint32
	shInformácie	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTyp		uint32
	pPosunutie	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pPríznaky	uint32
	pZarovnanie	uint32
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
	rPosunutie	uint32
	rInformácie	uint32
}
type Elf32rela struct {
	rPosunutie	uint32
	rInformácie	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNázov		uint32
	stHodnota	uint32
	stVeľkosť	uint32
	stInformácie	uint8
	stIné		uint8
	stshndx		uint16
}
type relocationSpracovanietextu struct {
	posunutie	uint32
	číslo		uint32
	oaddress	uint32
}
type Elf struct {
	spracovanietextu	[]byte
	spracovanietextulen	uint32
	relSpracovanietextu	[100]relocationSpracovanietextu
	relSpracovanietextulen	uint32
	strtab			[100]string
	Got			uint32
	Dynamická		uint32
}

func (vlastný *Elf) Getpoložka(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.epoložka
}

func (vlastný *Elf) Parse(data []byte, STRANAAdresárpoložka uint32) {

	pamäťmanager := TPamäťmanager{}
	var spracovanietextuKurzor Pointer = nil

	var konzola_2 = TKonzola{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVeľkosť := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVeľkosť*i]))

			var sectNázov []byte
			spustiť := uint32(strtab.shPosunutie + sectheader.shNázov)
			koniec := spustiť
			for ; ; koniec++ {
				if data[koniec] == 0x0 || data[koniec] == ' ' {
					break
				}
			}
			sectNázov = data[spustiť:koniec]

			var sectHodnota []byte
			if sectheader.shTyp != 8 {
				koniecPosunutie := sectheader.shPosunutie + sectheader.shVeľkosť
				if koniecPosunutie < sectheader.shPosunutie || koniecPosunutie > uint32(len(data)) {
					continue
				}
				sectHodnota = data[sectheader.shPosunutie:koniecPosunutie]
			}

			if RovnakáBajty(sectNázov, ([]byte)(".got.plt")) {
				konzola_2.MTlačiť("[")
				konzola_2.MTlačiť(sectNázov)
				konzola_2.MTlačiť(":")
				vlastný.Got = sectheader.shaddress
				konzola_2.MUnsignedinteger32Tlačiť(vlastný.Got)
				konzola_2.MTlačiť("]")
			}
			if RovnakáBajty(sectNázov, ([]byte)(".dynamic")) {
				konzola_2.MTlačiť("[")
				konzola_2.MTlačiť(sectNázov)
				konzola_2.MTlačiť(":")
				dynamická := sectheader.shaddress
				vlastný.Dynamická = dynamická
				konzola_2.MUnsignedinteger32Tlačiť(dynamická)
				konzola_2.MTlačiť("]")
			}

			if sectheader.shaddress > 0x1000 {
				veľkosť := sectheader.shVeľkosť
				if sectheader.shTyp == 8 {
					NulaBloknaSTRANAAdresár(sectheader.shaddress, veľkosť, STRANAAdresárpoložka)
				} else {
					cieľ_2 := GetBajtyzKurzor(uintptr(sectheader.shaddress), int(veľkosť), int(veľkosť))
					SadaBloknaSTRANAAdresár(sectHodnota, cieľ_2, veľkosť, STRANAAdresárpoložka)
				}
			}

			continue

			if RovnakáBajty(sectNázov, ([]byte)(".text")) {
				konzola_2.MTlačiť(".text")
				konzola_2.MTlačiť("[")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shaddress)
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shPosunutie)
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shVeľkosť)
				konzola_2.MTlačiť("]")
				copy(vlastný.spracovanietextu[:sectheader.shVeľkosť], sectHodnota[:sectheader.shVeľkosť])
				vlastný.spracovanietextulen = sectheader.shVeľkosť
			}
			if RovnakáBajty(sectNázov, ([]byte)(".rel.text")) {
				konzola_2.MTlačiť(".rel.text")
				konzola_2.MTlačiť("[")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shaddress)
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shVeľkosť)
				konzola_2.MTlačiť("]")
				for rt := uint32(0); rt < sectheader.shVeľkosť/8; rt++ {
					posunutie := *(*uint32)(Pointer(&sectHodnota[rt*8]))
					vlastný.relSpracovanietextu[rt].posunutie = posunutie
					vlastný.relSpracovanietextu[rt].oaddress = *(*uint32)(Pointer(&vlastný.spracovanietextu[posunutie]))
					vlastný.relSpracovanietextu[rt].číslo = *(*uint32)(Pointer(&sectHodnota[rt*8+4]))
					vlastný.relSpracovanietextulen++
				}
			}
			if RovnakáBajty(sectNázov, ([]byte)(".dynsym")) {
				konzola_2.MTlačiť(".dynsym")
				konzola_2.MTlačiť("[")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shaddress)
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shVeľkosť)
				konzola_2.MTlačiť("]")
				for rt := uint32(0); rt < sectheader.shVeľkosť/8; rt++ {
					posunutie := *(*uint32)(Pointer(&sectHodnota[rt*8]))
					vlastný.relSpracovanietextu[rt].posunutie = posunutie
					vlastný.relSpracovanietextu[rt].oaddress = *(*uint32)(Pointer(&vlastný.spracovanietextu[posunutie]))
					vlastný.relSpracovanietextu[rt].číslo = *(*uint32)(Pointer(&sectHodnota[rt*8+4]))
					vlastný.relSpracovanietextulen++
				}
			}
			if RovnakáBajty(sectNázov, ([]byte)(".dynstr")) {
				konzola_2.MTlačiť(".dynstr")
				konzola_2.MTlačiť("[")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shaddress)
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shVeľkosť)
				konzola_2.MTlačiť("]")
			}
			if RovnakáBajty(sectNázov, ([]byte)(".strtab")) {
				konzola_2.MTlačiť(".strtab")
				konzola_2.MTlačiť("[")
				konzola_2.MUnsignedinteger32Tlačiť(sectheader.shaddress)
				konzola_2.MTlačiť("]")
				rt := uint32(0)
				spustiť := uint32(0)

				for st := uint32(1); st < sectheader.shVeľkosť; st++ {
					if sectHodnota[st] == 0x0 || sectHodnota[st] == ' ' {
						funcNázov := sectHodnota[spustiť+1 : st]
						konzola_2.MTlačiť("+")
						konzola_2.MTlačiť(funcNázov)
						vlastný.strtab[rt] = Bajtytoreťazec(funcNázov)
						spustiť = st
						rt++
					}
				}

			}

		}

		konzola_2.MTlačiť(([]byte)("<------------"))
		for rt := uint32(0); rt < vlastný.relSpracovanietextulen; rt++ {
			konzola_2.MTlačiť("[")
			konzola_2.MTlačiť(([]byte)(vlastný.strtab[rt]))
			konzola_2.MTlačiť(":")
			konzola_2.MUnsignedinteger32Tlačiť(vlastný.relSpracovanietextu[rt].číslo)
			konzola_2.MTlačiť(":")

			konzola_2.MTlačiť(([]byte)("]"))
		}
		konzola_2.MTlačiť(([]byte)("------------>"))

		if spracovanietextuKurzor != nil {
			pamäťmanager.Voľné(spracovanietextuKurzor)
		}

	}

}
