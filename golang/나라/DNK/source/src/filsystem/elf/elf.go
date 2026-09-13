package elf

import . "unsafe"

import . "console"
import . "util"
import . "hukommelsemanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	etype		uint16
	emachine	uint16
	eversion	uint32
	eemne		uint32
	ephoff		uint32
	eshoff		uint32
	eFlag		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNavn		uint32
	shtype		uint32
	shFlag		uint32
	shaddress	uint32
	shForskydning	uint32
	shStørrelse	uint32
	shHenvisning	uint32
	shInformation	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	ptype		uint32
	pForskydning	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlag		uint32
	pJuster		uint32
}
type Elf32note struct {
	nnamesz	uint32
	ndescsz	uint32
	ntype	uint32
}
type Elf32dyn struct {
	dMærke		uint32
	dvalMarkør	uint32
}
type Elf32rel struct {
	rForskydning	uint32
	rInformation	uint32
}
type Elf32rela struct {
	rForskydning	uint32
	rInformation	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNavn		uint32
	stVærdi		uint32
	stStørrelse	uint32
	stInformation	uint8
	stAndet		uint8
	stshndx		uint16
}
type relocationTekst struct {
	forskydning	uint32
	tal		uint32
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

func (selv *Elf) Getemne(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eemne
}

func (selv *Elf) Parse(data []byte, SideMappeemne uint32) {

	hukommelsemanager := THukommelsemanager{}
	var tekstMarkør Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderStørrelse := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderStørrelse*i]))

			var sectNavn []byte
			begynd := uint32(strtab.shForskydning + sectheader.shNavn)
			slutningen := begynd
			for ; ; slutningen++ {
				if data[slutningen] == 0x0 || data[slutningen] == ' ' {
					break
				}
			}
			sectNavn = data[begynd:slutningen]

			var sectVærdi []byte
			if sectheader.shtype != 8 {
				slutningenForskydning := sectheader.shForskydning + sectheader.shStørrelse
				if slutningenForskydning < sectheader.shForskydning || slutningenForskydning > uint32(len(data)) {
					continue
				}
				sectVærdi = data[sectheader.shForskydning:slutningenForskydning]
			}

			if EqualByte(sectNavn, ([]byte)(".got.plt")) {
				console_2.MUdskriv("[")
				console_2.MUdskriv(sectNavn)
				console_2.MUdskriv(":")
				selv.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Udskriv(selv.Got)
				console_2.MUdskriv("]")
			}
			if EqualByte(sectNavn, ([]byte)(".dynamic")) {
				console_2.MUdskriv("[")
				console_2.MUdskriv(sectNavn)
				console_2.MUdskriv(":")
				dynamisk := sectheader.shaddress
				selv.Dynamisk = dynamisk
				console_2.MUnsignedinteger32Udskriv(dynamisk)
				console_2.MUdskriv("]")
			}

			if sectheader.shaddress > 0x1000 {
				størrelse := sectheader.shStørrelse
				if sectheader.shtype == 8 {
					ZeroBlokIndSideMappe(sectheader.shaddress, størrelse, SideMappeemne)
				} else {
					destination_2 := GetBytefraMarkør(uintptr(sectheader.shaddress), int(størrelse), int(størrelse))
					SatBlokIndSideMappe(sectVærdi, destination_2, størrelse, SideMappeemne)
				}
			}

			continue

			if EqualByte(sectNavn, ([]byte)(".text")) {
				console_2.MUdskriv(".text")
				console_2.MUdskriv("[")
				console_2.MUnsignedinteger32Udskriv(sectheader.shaddress)
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(sectheader.shForskydning)
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(sectheader.shStørrelse)
				console_2.MUdskriv("]")
				copy(selv.tekst[:sectheader.shStørrelse], sectVærdi[:sectheader.shStørrelse])
				selv.tekstlen = sectheader.shStørrelse
			}
			if EqualByte(sectNavn, ([]byte)(".rel.text")) {
				console_2.MUdskriv(".rel.text")
				console_2.MUdskriv("[")
				console_2.MUnsignedinteger32Udskriv(sectheader.shaddress)
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(sectheader.shStørrelse)
				console_2.MUdskriv("]")
				for rt := uint32(0); rt < sectheader.shStørrelse/8; rt++ {
					forskydning := *(*uint32)(Pointer(&sectVærdi[rt*8]))
					selv.relTekst[rt].forskydning = forskydning
					selv.relTekst[rt].oaddress = *(*uint32)(Pointer(&selv.tekst[forskydning]))
					selv.relTekst[rt].tal = *(*uint32)(Pointer(&sectVærdi[rt*8+4]))
					selv.relTekstlen++
				}
			}
			if EqualByte(sectNavn, ([]byte)(".dynsym")) {
				console_2.MUdskriv(".dynsym")
				console_2.MUdskriv("[")
				console_2.MUnsignedinteger32Udskriv(sectheader.shaddress)
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(sectheader.shStørrelse)
				console_2.MUdskriv("]")
				for rt := uint32(0); rt < sectheader.shStørrelse/8; rt++ {
					forskydning := *(*uint32)(Pointer(&sectVærdi[rt*8]))
					selv.relTekst[rt].forskydning = forskydning
					selv.relTekst[rt].oaddress = *(*uint32)(Pointer(&selv.tekst[forskydning]))
					selv.relTekst[rt].tal = *(*uint32)(Pointer(&sectVærdi[rt*8+4]))
					selv.relTekstlen++
				}
			}
			if EqualByte(sectNavn, ([]byte)(".dynstr")) {
				console_2.MUdskriv(".dynstr")
				console_2.MUdskriv("[")
				console_2.MUnsignedinteger32Udskriv(sectheader.shaddress)
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(sectheader.shStørrelse)
				console_2.MUdskriv("]")
			}
			if EqualByte(sectNavn, ([]byte)(".strtab")) {
				console_2.MUdskriv(".strtab")
				console_2.MUdskriv("[")
				console_2.MUnsignedinteger32Udskriv(sectheader.shaddress)
				console_2.MUdskriv("]")
				rt := uint32(0)
				begynd := uint32(0)

				for st := uint32(1); st < sectheader.shStørrelse; st++ {
					if sectVærdi[st] == 0x0 || sectVærdi[st] == ' ' {
						funcNavn := sectVærdi[begynd+1 : st]
						console_2.MUdskriv("+")
						console_2.MUdskriv(funcNavn)
						selv.strtab[rt] = BytetoStreng(funcNavn)
						begynd = st
						rt++
					}
				}

			}

		}

		console_2.MUdskriv(([]byte)("<------------"))
		for rt := uint32(0); rt < selv.relTekstlen; rt++ {
			console_2.MUdskriv("[")
			console_2.MUdskriv(([]byte)(selv.strtab[rt]))
			console_2.MUdskriv(":")
			console_2.MUnsignedinteger32Udskriv(selv.relTekst[rt].tal)
			console_2.MUdskriv(":")

			console_2.MUdskriv(([]byte)("]"))
		}
		console_2.MUdskriv(([]byte)("------------>"))

		if tekstMarkør != nil {
			hukommelsemanager.Fri(tekstMarkør)
		}

	}

}
