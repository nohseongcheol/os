package elf

import . "unsafe"

import . "console"
import . "util"
import . "memorymanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	etype		uint16
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
	shNavn		uint32
	shtype		uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shStødd		uint32
	shlink		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	ptype	uint32
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
	ntype	uint32
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
	stNavn	uint32
	stvalue	uint32
	stStødd	uint32
	stinfo	uint8
	stAðrir	uint8
	stshndx	uint16
}
type relocationtext struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	reltext		[100]relocationtext
	reltextlen	uint32
	strtab		[100]string
	Got		uint32
	Rakstrarmáttur	uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, PageFíluskráentry uint32) {

	memorymanager := TMemorymanager{}
	var textpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderStødd := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderStødd*i]))

			var sectNavn []byte
			start := uint32(strtab.shoffset + sectheader.shNavn)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectNavn = data[start:end]

			var sectvalue []byte
			if sectheader.shtype != 8 {
				endoffset := sectheader.shoffset + sectheader.shStødd
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectvalue = data[sectheader.shoffset:endoffset]
			}

			if Equalbýt(sectNavn, ([]byte)(".got.plt")) {
				console_2.MPrint("[")
				console_2.MPrint(sectNavn)
				console_2.MPrint(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32print(self.Got)
				console_2.MPrint("]")
			}
			if Equalbýt(sectNavn, ([]byte)(".dynamic")) {
				console_2.MPrint("[")
				console_2.MPrint(sectNavn)
				console_2.MPrint(":")
				rakstrarmáttur := sectheader.shaddress
				self.Rakstrarmáttur = rakstrarmáttur
				console_2.MUnsignedinteger32print(rakstrarmáttur)
				console_2.MPrint("]")
			}

			if sectheader.shaddress > 0x1000 {
				stødd := sectheader.shStødd
				if sectheader.shtype == 8 {
					ZeroBlokkurinpageFíluskrá(sectheader.shaddress, stødd, PageFíluskráentry)
				} else {
					destination_2 := Getbýtfrompointer(uintptr(sectheader.shaddress), int(stødd), int(stødd))
					SetBlokkurinpageFíluskrá(sectvalue, destination_2, stødd, PageFíluskráentry)
				}
			}

			continue

			if Equalbýt(sectNavn, ([]byte)(".text")) {
				console_2.MPrint(".text")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shoffset)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shStødd)
				console_2.MPrint("]")
				copy(self.text[:sectheader.shStødd], sectvalue[:sectheader.shStødd])
				self.textlen = sectheader.shStødd
			}
			if Equalbýt(sectNavn, ([]byte)(".rel.text")) {
				console_2.MPrint(".rel.text")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shStødd)
				console_2.MPrint("]")
				for rt := uint32(0); rt < sectheader.shStødd/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbýt(sectNavn, ([]byte)(".dynsym")) {
				console_2.MPrint(".dynsym")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shStødd)
				console_2.MPrint("]")
				for rt := uint32(0); rt < sectheader.shStødd/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbýt(sectNavn, ([]byte)(".dynstr")) {
				console_2.MPrint(".dynstr")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shStødd)
				console_2.MPrint("]")
			}
			if Equalbýt(sectNavn, ([]byte)(".strtab")) {
				console_2.MPrint(".strtab")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shStødd; st++ {
					if sectvalue[st] == 0x0 || sectvalue[st] == ' ' {
						funcNavn := sectvalue[start+1 : st]
						console_2.MPrint("+")
						console_2.MPrint(funcNavn)
						self.strtab[rt] = Býttostring(funcNavn)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MPrint(([]byte)("<------------"))
		for rt := uint32(0); rt < self.reltextlen; rt++ {
			console_2.MPrint("[")
			console_2.MPrint(([]byte)(self.strtab[rt]))
			console_2.MPrint(":")
			console_2.MUnsignedinteger32print(self.reltext[rt].number)
			console_2.MPrint(":")

			console_2.MPrint(([]byte)("]"))
		}
		console_2.MPrint(([]byte)("------------>"))

		if textpointer != nil {
			memorymanager.Free(textpointer)
		}

	}

}
