package elf

import . "unsafe"

import . "console"
import . "util"
import . "ububikomanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eUbwoko		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eAmabendera	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shIzina		uint32
	shUbwoko	uint32
	shAmabendera	uint32
	shaddress	uint32
	shoffset	uint32
	shIngano	uint32
	shlink		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfPorogaramuheader struct {
	pUbwoko		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pAmabendera	uint32
	pItunganya	uint32
}
type Elf32Igisobanuro struct {
	nnamesz	uint32
	ndescsz	uint32
	nUbwoko	uint32
}
type Elf32dyn struct {
	dItagi		uint32
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
	stIzina		uint32
	stAgaciro	uint32
	stIngano	uint32
	stinfo		uint8
	stIkindi	uint8
	stshndx		uint16
}
type relocationUmwandiko struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	umwandiko	[]byte
	umwandikolen	uint32
	relUmwandiko	[100]relocationUmwandiko
	relUmwandikolen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, IpajiUbubikoentry uint32) {

	ububikomanager := TUbubikomanager{}
	var umwandikopointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderIngano := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderIngano*i]))

			var sectIzina []byte
			start := uint32(strtab.shoffset + sectheader.shIzina)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectIzina = data[start:end]

			var sectAgaciro []byte
			if sectheader.shUbwoko != 8 {
				endoffset := sectheader.shoffset + sectheader.shIngano
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectAgaciro = data[sectheader.shoffset:endoffset]
			}

			if EqualBayite(sectIzina, ([]byte)(".got.plt")) {
				console_2.MGucapa("[")
				console_2.MGucapa(sectIzina)
				console_2.MGucapa(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Gucapa(self.Got)
				console_2.MGucapa("]")
			}
			if EqualBayite(sectIzina, ([]byte)(".dynamic")) {
				console_2.MGucapa("[")
				console_2.MGucapa(sectIzina)
				console_2.MGucapa(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Gucapa(dynamic)
				console_2.MGucapa("]")
			}

			if sectheader.shaddress > 0x1000 {
				ingano := sectheader.shIngano
				if sectheader.shUbwoko == 8 {
					ZeroblockImbereIpajiUbubiko(sectheader.shaddress, ingano, IpajiUbubikoentry)
				} else {
					destination_2 := GetBayitefrompointer(uintptr(sectheader.shaddress), int(ingano), int(ingano))
					SetblockImbereIpajiUbubiko(sectAgaciro, destination_2, ingano, IpajiUbubikoentry)
				}
			}

			continue

			if EqualBayite(sectIzina, ([]byte)(".text")) {
				console_2.MGucapa(".text")
				console_2.MGucapa("[")
				console_2.MUnsignedinteger32Gucapa(sectheader.shaddress)
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(sectheader.shoffset)
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(sectheader.shIngano)
				console_2.MGucapa("]")
				copy(self.umwandiko[:sectheader.shIngano], sectAgaciro[:sectheader.shIngano])
				self.umwandikolen = sectheader.shIngano
			}
			if EqualBayite(sectIzina, ([]byte)(".rel.text")) {
				console_2.MGucapa(".rel.text")
				console_2.MGucapa("[")
				console_2.MUnsignedinteger32Gucapa(sectheader.shaddress)
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(sectheader.shIngano)
				console_2.MGucapa("]")
				for rt := uint32(0); rt < sectheader.shIngano/8; rt++ {
					offset := *(*uint32)(Pointer(&sectAgaciro[rt*8]))
					self.relUmwandiko[rt].offset = offset
					self.relUmwandiko[rt].oaddress = *(*uint32)(Pointer(&self.umwandiko[offset]))
					self.relUmwandiko[rt].number = *(*uint32)(Pointer(&sectAgaciro[rt*8+4]))
					self.relUmwandikolen++
				}
			}
			if EqualBayite(sectIzina, ([]byte)(".dynsym")) {
				console_2.MGucapa(".dynsym")
				console_2.MGucapa("[")
				console_2.MUnsignedinteger32Gucapa(sectheader.shaddress)
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(sectheader.shIngano)
				console_2.MGucapa("]")
				for rt := uint32(0); rt < sectheader.shIngano/8; rt++ {
					offset := *(*uint32)(Pointer(&sectAgaciro[rt*8]))
					self.relUmwandiko[rt].offset = offset
					self.relUmwandiko[rt].oaddress = *(*uint32)(Pointer(&self.umwandiko[offset]))
					self.relUmwandiko[rt].number = *(*uint32)(Pointer(&sectAgaciro[rt*8+4]))
					self.relUmwandikolen++
				}
			}
			if EqualBayite(sectIzina, ([]byte)(".dynstr")) {
				console_2.MGucapa(".dynstr")
				console_2.MGucapa("[")
				console_2.MUnsignedinteger32Gucapa(sectheader.shaddress)
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(sectheader.shIngano)
				console_2.MGucapa("]")
			}
			if EqualBayite(sectIzina, ([]byte)(".strtab")) {
				console_2.MGucapa(".strtab")
				console_2.MGucapa("[")
				console_2.MUnsignedinteger32Gucapa(sectheader.shaddress)
				console_2.MGucapa("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shIngano; st++ {
					if sectAgaciro[st] == 0x0 || sectAgaciro[st] == ' ' {
						funcIzina := sectAgaciro[start+1 : st]
						console_2.MGucapa("+")
						console_2.MGucapa(funcIzina)
						self.strtab[rt] = Bayitetostring(funcIzina)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MGucapa(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relUmwandikolen; rt++ {
			console_2.MGucapa("[")
			console_2.MGucapa(([]byte)(self.strtab[rt]))
			console_2.MGucapa(":")
			console_2.MUnsignedinteger32Gucapa(self.relUmwandiko[rt].number)
			console_2.MGucapa(":")

			console_2.MGucapa(([]byte)("]"))
		}
		console_2.MGucapa(([]byte)("------------>"))

		if umwandikopointer != nil {
			ububikomanager.Kigenga(umwandikopointer)
		}

	}

}
