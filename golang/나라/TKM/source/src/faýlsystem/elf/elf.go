package elf

import . "unsafe"

import . "console"
import . "util"
import . "memorymanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eHil		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eflags		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shAd		uint32
	shHil		uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shUlulyk	uint32
	shbaglaýyş	uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pHil	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pflags	uint32
	palign	uint32
}
type Elf32note struct {
	nnamesz	uint32
	ndescsz	uint32
	nHil	uint32
}
type Elf32dyn struct {
	dtag		uint32
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
	stAd		uint32
	stMykdar	uint32
	stUlulyk	uint32
	stinfo		uint8
	stother		uint8
	stshndx		uint16
}
type relocationMetin struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	metin		[]byte
	metinlen	uint32
	relMetin	[100]relocationMetin
	relMetinlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, Pagedirectoryentry uint32) {

	memorymanager := TMemorymanager{}
	var metinpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderUlulyk := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderUlulyk*i]))

			var sectAd []byte
			start := uint32(strtab.shoffset + sectheader.shAd)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectAd = data[start:end]

			var sectMykdar []byte
			if sectheader.shHil != 8 {
				endoffset := sectheader.shoffset + sectheader.shUlulyk
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectMykdar = data[sectheader.shoffset:endoffset]
			}

			if EqualBaýtlar(sectAd, ([]byte)(".got.plt")) {
				console_2.MÇap("[")
				console_2.MÇap(sectAd)
				console_2.MÇap(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Çap(self.Got)
				console_2.MÇap("]")
			}
			if EqualBaýtlar(sectAd, ([]byte)(".dynamic")) {
				console_2.MÇap("[")
				console_2.MÇap(sectAd)
				console_2.MÇap(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Çap(dynamic)
				console_2.MÇap("]")
			}

			if sectheader.shaddress > 0x1000 {
				ululyk := sectheader.shUlulyk
				if sectheader.shHil == 8 {
					Zeroblockinpagedirectory(sectheader.shaddress, ululyk, Pagedirectoryentry)
				} else {
					destination_2 := GetBaýtlarfrompointer(uintptr(sectheader.shaddress), int(ululyk), int(ululyk))
					Setblockinpagedirectory(sectMykdar, destination_2, ululyk, Pagedirectoryentry)
				}
			}

			continue

			if EqualBaýtlar(sectAd, ([]byte)(".text")) {
				console_2.MÇap(".text")
				console_2.MÇap("[")
				console_2.MUnsignedinteger32Çap(sectheader.shaddress)
				console_2.MÇap(":")
				console_2.MUnsignedinteger32Çap(sectheader.shoffset)
				console_2.MÇap(":")
				console_2.MUnsignedinteger32Çap(sectheader.shUlulyk)
				console_2.MÇap("]")
				copy(self.metin[:sectheader.shUlulyk], sectMykdar[:sectheader.shUlulyk])
				self.metinlen = sectheader.shUlulyk
			}
			if EqualBaýtlar(sectAd, ([]byte)(".rel.text")) {
				console_2.MÇap(".rel.text")
				console_2.MÇap("[")
				console_2.MUnsignedinteger32Çap(sectheader.shaddress)
				console_2.MÇap(":")
				console_2.MUnsignedinteger32Çap(sectheader.shUlulyk)
				console_2.MÇap("]")
				for rt := uint32(0); rt < sectheader.shUlulyk/8; rt++ {
					offset := *(*uint32)(Pointer(&sectMykdar[rt*8]))
					self.relMetin[rt].offset = offset
					self.relMetin[rt].oaddress = *(*uint32)(Pointer(&self.metin[offset]))
					self.relMetin[rt].number = *(*uint32)(Pointer(&sectMykdar[rt*8+4]))
					self.relMetinlen++
				}
			}
			if EqualBaýtlar(sectAd, ([]byte)(".dynsym")) {
				console_2.MÇap(".dynsym")
				console_2.MÇap("[")
				console_2.MUnsignedinteger32Çap(sectheader.shaddress)
				console_2.MÇap(":")
				console_2.MUnsignedinteger32Çap(sectheader.shUlulyk)
				console_2.MÇap("]")
				for rt := uint32(0); rt < sectheader.shUlulyk/8; rt++ {
					offset := *(*uint32)(Pointer(&sectMykdar[rt*8]))
					self.relMetin[rt].offset = offset
					self.relMetin[rt].oaddress = *(*uint32)(Pointer(&self.metin[offset]))
					self.relMetin[rt].number = *(*uint32)(Pointer(&sectMykdar[rt*8+4]))
					self.relMetinlen++
				}
			}
			if EqualBaýtlar(sectAd, ([]byte)(".dynstr")) {
				console_2.MÇap(".dynstr")
				console_2.MÇap("[")
				console_2.MUnsignedinteger32Çap(sectheader.shaddress)
				console_2.MÇap(":")
				console_2.MUnsignedinteger32Çap(sectheader.shUlulyk)
				console_2.MÇap("]")
			}
			if EqualBaýtlar(sectAd, ([]byte)(".strtab")) {
				console_2.MÇap(".strtab")
				console_2.MÇap("[")
				console_2.MUnsignedinteger32Çap(sectheader.shaddress)
				console_2.MÇap("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shUlulyk; st++ {
					if sectMykdar[st] == 0x0 || sectMykdar[st] == ' ' {
						funcAd := sectMykdar[start+1 : st]
						console_2.MÇap("+")
						console_2.MÇap(funcAd)
						self.strtab[rt] = Baýtlartostring(funcAd)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MÇap(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relMetinlen; rt++ {
			console_2.MÇap("[")
			console_2.MÇap(([]byte)(self.strtab[rt]))
			console_2.MÇap(":")
			console_2.MUnsignedinteger32Çap(self.relMetin[rt].number)
			console_2.MÇap(":")

			console_2.MÇap(([]byte)("]"))
		}
		console_2.MÇap(([]byte)("------------>"))

		if metinpointer != nil {
			memorymanager.Free(metinpointer)
		}

	}

}
