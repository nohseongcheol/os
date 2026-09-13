package elf

import . "unsafe"

import . "console"
import . "util"
import . "pomnilnikmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eVrsta		uint16
	emachine	uint16
	eRazličica	uint32
	evnos		uint32
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
	shVelikost	uint32
	shPovezava	uint32
	shPodatki	uint32
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
	pPoravnaj	uint32
}
type Elf32Opomba struct {
	nnamesz	uint32
	ndescsz	uint32
	nVrsta	uint32
}
type Elf32dyn struct {
	dOznaka		uint32
	dvalKazalnik	uint32
}
type Elf32rel struct {
	roffset		uint32
	rPodatki	uint32
}
type Elf32rela struct {
	roffset		uint32
	rPodatki	uint32
	raddend		uint32
}
type Elf32sym struct {
	stIme		uint32
	stVrednost	uint32
	stVelikost	uint32
	stPodatki	uint8
	stDrugo		uint8
	stshndx		uint16
}
type relocationBesedilo struct {
	offset		uint32
	številka	uint32
	oaddress	uint32
}
type Elf struct {
	besedilo	[]byte
	besedilolen	uint32
	relBesedilo	[100]relocationBesedilo
	relBesedilolen	uint32
	strtab		[100]string
	Got		uint32
	Dinamično	uint32
}

func (sam *Elf) Getvnos(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.evnos
}

func (sam *Elf) Parse(data []byte, StranMapavnos uint32) {

	pomnilnikmanager := TPomnilnikmanager{}
	var besediloKazalnik Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderVelikost := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderVelikost*i]))

			var sectIme []byte
			začni := uint32(strtab.shoffset + sectheader.shIme)
			end := začni
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectIme = data[začni:end]

			var sectVrednost []byte
			if sectheader.shVrsta != 8 {
				endoffset := sectheader.shoffset + sectheader.shVelikost
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectVrednost = data[sectheader.shoffset:endoffset]
			}

			if EqualBajtov(sectIme, ([]byte)(".got.plt")) {
				console_2.MNatisni("[")
				console_2.MNatisni(sectIme)
				console_2.MNatisni(":")
				sam.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Natisni(sam.Got)
				console_2.MNatisni("]")
			}
			if EqualBajtov(sectIme, ([]byte)(".dynamic")) {
				console_2.MNatisni("[")
				console_2.MNatisni(sectIme)
				console_2.MNatisni(":")
				dinamično := sectheader.shaddress
				sam.Dinamično = dinamično
				console_2.MUnsignedinteger32Natisni(dinamično)
				console_2.MNatisni("]")
			}

			if sectheader.shaddress > 0x1000 {
				velikost := sectheader.shVelikost
				if sectheader.shVrsta == 8 {
					ZeroBlokVhodnoStranMapa(sectheader.shaddress, velikost, StranMapavnos)
				} else {
					cilj_2 := GetBajtovfromKazalnik(uintptr(sectheader.shaddress), int(velikost), int(velikost))
					MnožicaBlokVhodnoStranMapa(sectVrednost, cilj_2, velikost, StranMapavnos)
				}
			}

			continue

			if EqualBajtov(sectIme, ([]byte)(".text")) {
				console_2.MNatisni(".text")
				console_2.MNatisni("[")
				console_2.MUnsignedinteger32Natisni(sectheader.shaddress)
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(sectheader.shoffset)
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(sectheader.shVelikost)
				console_2.MNatisni("]")
				copy(sam.besedilo[:sectheader.shVelikost], sectVrednost[:sectheader.shVelikost])
				sam.besedilolen = sectheader.shVelikost
			}
			if EqualBajtov(sectIme, ([]byte)(".rel.text")) {
				console_2.MNatisni(".rel.text")
				console_2.MNatisni("[")
				console_2.MUnsignedinteger32Natisni(sectheader.shaddress)
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(sectheader.shVelikost)
				console_2.MNatisni("]")
				for rt := uint32(0); rt < sectheader.shVelikost/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrednost[rt*8]))
					sam.relBesedilo[rt].offset = offset
					sam.relBesedilo[rt].oaddress = *(*uint32)(Pointer(&sam.besedilo[offset]))
					sam.relBesedilo[rt].številka = *(*uint32)(Pointer(&sectVrednost[rt*8+4]))
					sam.relBesedilolen++
				}
			}
			if EqualBajtov(sectIme, ([]byte)(".dynsym")) {
				console_2.MNatisni(".dynsym")
				console_2.MNatisni("[")
				console_2.MUnsignedinteger32Natisni(sectheader.shaddress)
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(sectheader.shVelikost)
				console_2.MNatisni("]")
				for rt := uint32(0); rt < sectheader.shVelikost/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVrednost[rt*8]))
					sam.relBesedilo[rt].offset = offset
					sam.relBesedilo[rt].oaddress = *(*uint32)(Pointer(&sam.besedilo[offset]))
					sam.relBesedilo[rt].številka = *(*uint32)(Pointer(&sectVrednost[rt*8+4]))
					sam.relBesedilolen++
				}
			}
			if EqualBajtov(sectIme, ([]byte)(".dynstr")) {
				console_2.MNatisni(".dynstr")
				console_2.MNatisni("[")
				console_2.MUnsignedinteger32Natisni(sectheader.shaddress)
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(sectheader.shVelikost)
				console_2.MNatisni("]")
			}
			if EqualBajtov(sectIme, ([]byte)(".strtab")) {
				console_2.MNatisni(".strtab")
				console_2.MNatisni("[")
				console_2.MUnsignedinteger32Natisni(sectheader.shaddress)
				console_2.MNatisni("]")
				rt := uint32(0)
				začni := uint32(0)

				for st := uint32(1); st < sectheader.shVelikost; st++ {
					if sectVrednost[st] == 0x0 || sectVrednost[st] == ' ' {
						funcIme := sectVrednost[začni+1 : st]
						console_2.MNatisni("+")
						console_2.MNatisni(funcIme)
						sam.strtab[rt] = BajtovtoNiz(funcIme)
						začni = st
						rt++
					}
				}

			}

		}

		console_2.MNatisni(([]byte)("<------------"))
		for rt := uint32(0); rt < sam.relBesedilolen; rt++ {
			console_2.MNatisni("[")
			console_2.MNatisni(([]byte)(sam.strtab[rt]))
			console_2.MNatisni(":")
			console_2.MUnsignedinteger32Natisni(sam.relBesedilo[rt].številka)
			console_2.MNatisni(":")

			console_2.MNatisni(([]byte)("]"))
		}
		console_2.MNatisni(([]byte)("------------>"))

		if besediloKazalnik != nil {
			pomnilnikmanager.Prosto(besediloKazalnik)
		}

	}

}
