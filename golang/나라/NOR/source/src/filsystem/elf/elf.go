package elf

import . "unsafe"

import . "console"
import . "util"
import . "minnemanager"
import . "paging"

type ElfTopptekst struct {
	eident		[16]byte
	eFiltype	uint16
	emachine	uint16
	eVersjon	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eFlagg		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type ElfsectionTopptekst struct {
	shNavn		uint32
	shFiltype	uint32
	shFlagg		uint32
	shaddress	uint32
	shAvstand	uint32
	shStørrelse	uint32
	shLenke		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfprogramTopptekst struct {
	pFiltype	uint32
	pAvstand	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlagg		uint32
	pJuster		uint32
}
type Elf32Merknad struct {
	nnamesz		uint32
	ndescsz		uint32
	nFiltype	uint32
}
type Elf32dyn struct {
	dMerke		uint32
	dvalPeker	uint32
}
type Elf32rel struct {
	rAvstand	uint32
	rinfo		uint32
}
type Elf32rela struct {
	rAvstand	uint32
	rinfo		uint32
	raddend		uint32
}
type Elf32sym struct {
	stNavn		uint32
	stVerdi		uint32
	stStørrelse	uint32
	stinfo		uint8
	stAndre		uint8
	stshndx		uint16
}
type relocationTekst struct {
	avstand		uint32
	tall		uint32
	oaddress	uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamisk	uint32
}

func (selv *Elf) Getentry(data []byte) uint32 {
	elfTopptekst := (*ElfTopptekst)(Pointer(&data[0]))
	return elfTopptekst.eentry
}

func (selv *Elf) Parse(data []byte, SideKatalogentry uint32) {

	minnemanager := TMinnemanager{}
	var tekstPeker Pointer = nil

	var console_2 = TConsole{}

	elfTopptekst := (*ElfTopptekst)(Pointer(&data[0]))

	if elfTopptekst.eshnum != 0 {
		strtab := (*ElfsectionTopptekst)(Pointer(&data[elfTopptekst.eshoff+uint32(elfTopptekst.eshentsize*elfTopptekst.eshstrndx)]))
		sectTopptekstStørrelse := uint32(Sizeof(ElfsectionTopptekst{}))

		for i := uint32(0); i < uint32(elfTopptekst.eshnum); i++ {
			sectTopptekst := (*ElfsectionTopptekst)(Pointer(&data[elfTopptekst.eshoff+sectTopptekstStørrelse*i]))

			var sectNavn []byte
			start := uint32(strtab.shAvstand + sectTopptekst.shNavn)
			slutt := start
			for ; ; slutt++ {
				if data[slutt] == 0x0 || data[slutt] == ' ' {
					break
				}
			}
			sectNavn = data[start:slutt]

			var sectVerdi []byte
			if sectTopptekst.shFiltype != 8 {
				sluttAvstand := sectTopptekst.shAvstand + sectTopptekst.shStørrelse
				if sluttAvstand < sectTopptekst.shAvstand || sluttAvstand > uint32(len(data)) {
					continue
				}
				sectVerdi = data[sectTopptekst.shAvstand:sluttAvstand]
			}

			if LikByte(sectNavn, ([]byte)(".got.plt")) {
				console_2.MSkrivut("[")
				console_2.MSkrivut(sectNavn)
				console_2.MSkrivut(":")
				selv.Got = sectTopptekst.shaddress
				console_2.MUnsignedinteger32Skrivut(selv.Got)
				console_2.MSkrivut("]")
			}
			if LikByte(sectNavn, ([]byte)(".dynamic")) {
				console_2.MSkrivut("[")
				console_2.MSkrivut(sectNavn)
				console_2.MSkrivut(":")
				dynamisk := sectTopptekst.shaddress
				selv.Dynamisk = dynamisk
				console_2.MUnsignedinteger32Skrivut(dynamisk)
				console_2.MSkrivut("]")
			}

			if sectTopptekst.shaddress > 0x1000 {
				størrelse := sectTopptekst.shStørrelse
				if sectTopptekst.shFiltype == 8 {
					ZeroBlokkInnSideKatalog(sectTopptekst.shaddress, størrelse, SideKatalogentry)
				} else {
					mål_2 := GetBytefromPeker(uintptr(sectTopptekst.shaddress), int(størrelse), int(størrelse))
					SettBlokkInnSideKatalog(sectVerdi, mål_2, størrelse, SideKatalogentry)
				}
			}

			continue

			if LikByte(sectNavn, ([]byte)(".text")) {
				console_2.MSkrivut(".text")
				console_2.MSkrivut("[")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shaddress)
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shAvstand)
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shStørrelse)
				console_2.MSkrivut("]")
				copy(selv.tekst[:sectTopptekst.shStørrelse], sectVerdi[:sectTopptekst.shStørrelse])
				selv.tekstlen = sectTopptekst.shStørrelse
			}
			if LikByte(sectNavn, ([]byte)(".rel.text")) {
				console_2.MSkrivut(".rel.text")
				console_2.MSkrivut("[")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shaddress)
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shStørrelse)
				console_2.MSkrivut("]")
				for rt := uint32(0); rt < sectTopptekst.shStørrelse/8; rt++ {
					avstand := *(*uint32)(Pointer(&sectVerdi[rt*8]))
					selv.relTekst[rt].avstand = avstand
					selv.relTekst[rt].oaddress = *(*uint32)(Pointer(&selv.tekst[avstand]))
					selv.relTekst[rt].tall = *(*uint32)(Pointer(&sectVerdi[rt*8+4]))
					selv.relTekstlen++
				}
			}
			if LikByte(sectNavn, ([]byte)(".dynsym")) {
				console_2.MSkrivut(".dynsym")
				console_2.MSkrivut("[")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shaddress)
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shStørrelse)
				console_2.MSkrivut("]")
				for rt := uint32(0); rt < sectTopptekst.shStørrelse/8; rt++ {
					avstand := *(*uint32)(Pointer(&sectVerdi[rt*8]))
					selv.relTekst[rt].avstand = avstand
					selv.relTekst[rt].oaddress = *(*uint32)(Pointer(&selv.tekst[avstand]))
					selv.relTekst[rt].tall = *(*uint32)(Pointer(&sectVerdi[rt*8+4]))
					selv.relTekstlen++
				}
			}
			if LikByte(sectNavn, ([]byte)(".dynstr")) {
				console_2.MSkrivut(".dynstr")
				console_2.MSkrivut("[")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shaddress)
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shStørrelse)
				console_2.MSkrivut("]")
			}
			if LikByte(sectNavn, ([]byte)(".strtab")) {
				console_2.MSkrivut(".strtab")
				console_2.MSkrivut("[")
				console_2.MUnsignedinteger32Skrivut(sectTopptekst.shaddress)
				console_2.MSkrivut("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectTopptekst.shStørrelse; st++ {
					if sectVerdi[st] == 0x0 || sectVerdi[st] == ' ' {
						funcNavn := sectVerdi[start+1 : st]
						console_2.MSkrivut("+")
						console_2.MSkrivut(funcNavn)
						selv.strtab[rt] = BytetoStreng(funcNavn)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MSkrivut(([]byte)("<------------"))
		for rt := uint32(0); rt < selv.relTekstlen; rt++ {
			console_2.MSkrivut("[")
			console_2.MSkrivut(([]byte)(selv.strtab[rt]))
			console_2.MSkrivut(":")
			console_2.MUnsignedinteger32Skrivut(selv.relTekst[rt].tall)
			console_2.MSkrivut(":")

			console_2.MSkrivut(([]byte)("]"))
		}
		console_2.MSkrivut(([]byte)("------------>"))

		if tekstPeker != nil {
			minnemanager.Ledig(tekstPeker)
		}

	}

}
