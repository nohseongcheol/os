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
	shНом		uint32
	shtype		uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shsize		uint32
	shАлоқа		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	ptype		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pflags		uint32
	pСафкашидан	uint32
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
	stНом	uint32
	stvalue	uint32
	stsize	uint32
	stinfo	uint8
	stДигар	uint8
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
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, PageФеҳрастentry uint32) {

	memorymanager := TMemorymanager{}
	var textpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheadersize := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheadersize*i]))

			var sectНом []byte
			start := uint32(strtab.shoffset + sectheader.shНом)
			охириҳуҷҷат := start
			for ; ; охириҳуҷҷат++ {
				if data[охириҳуҷҷат] == 0x0 || data[охириҳуҷҷат] == ' ' {
					break
				}
			}
			sectНом = data[start:охириҳуҷҷат]

			var sectvalue []byte
			if sectheader.shtype != 8 {
				охириҳуҷҷатoffset := sectheader.shoffset + sectheader.shsize
				if охириҳуҷҷатoffset < sectheader.shoffset || охириҳуҷҷатoffset > uint32(len(data)) {
					continue
				}
				sectvalue = data[sectheader.shoffset:охириҳуҷҷатoffset]
			}

			if Equalbytes(sectНом, ([]byte)(".got.plt")) {
				console_2.MЧопкардан("[")
				console_2.MЧопкардан(sectНом)
				console_2.MЧопкардан(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Чопкардан(self.Got)
				console_2.MЧопкардан("]")
			}
			if Equalbytes(sectНом, ([]byte)(".dynamic")) {
				console_2.MЧопкардан("[")
				console_2.MЧопкардан(sectНом)
				console_2.MЧопкардан(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Чопкардан(dynamic)
				console_2.MЧопкардан("]")
			}

			if sectheader.shaddress > 0x1000 {
				size := sectheader.shsize
				if sectheader.shtype == 8 {
					ZeroblockinpageФеҳраст(sectheader.shaddress, size, PageФеҳрастentry)
				} else {
					destination_2 := Getbytesfrompointer(uintptr(sectheader.shaddress), int(size), int(size))
					SetblockinpageФеҳраст(sectvalue, destination_2, size, PageФеҳрастentry)
				}
			}

			continue

			if Equalbytes(sectНом, ([]byte)(".text")) {
				console_2.MЧопкардан(".text")
				console_2.MЧопкардан("[")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shaddress)
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shoffset)
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shsize)
				console_2.MЧопкардан("]")
				copy(self.text[:sectheader.shsize], sectvalue[:sectheader.shsize])
				self.textlen = sectheader.shsize
			}
			if Equalbytes(sectНом, ([]byte)(".rel.text")) {
				console_2.MЧопкардан(".rel.text")
				console_2.MЧопкардан("[")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shaddress)
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shsize)
				console_2.MЧопкардан("]")
				for rt := uint32(0); rt < sectheader.shsize/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbytes(sectНом, ([]byte)(".dynsym")) {
				console_2.MЧопкардан(".dynsym")
				console_2.MЧопкардан("[")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shaddress)
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shsize)
				console_2.MЧопкардан("]")
				for rt := uint32(0); rt < sectheader.shsize/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbytes(sectНом, ([]byte)(".dynstr")) {
				console_2.MЧопкардан(".dynstr")
				console_2.MЧопкардан("[")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shaddress)
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shsize)
				console_2.MЧопкардан("]")
			}
			if Equalbytes(sectНом, ([]byte)(".strtab")) {
				console_2.MЧопкардан(".strtab")
				console_2.MЧопкардан("[")
				console_2.MUnsignedinteger32Чопкардан(sectheader.shaddress)
				console_2.MЧопкардан("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shsize; st++ {
					if sectvalue[st] == 0x0 || sectvalue[st] == ' ' {
						funcНом := sectvalue[start+1 : st]
						console_2.MЧопкардан("+")
						console_2.MЧопкардан(funcНом)
						self.strtab[rt] = Bytestostring(funcНом)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MЧопкардан(([]byte)("<------------"))
		for rt := uint32(0); rt < self.reltextlen; rt++ {
			console_2.MЧопкардан("[")
			console_2.MЧопкардан(([]byte)(self.strtab[rt]))
			console_2.MЧопкардан(":")
			console_2.MUnsignedinteger32Чопкардан(self.reltext[rt].number)
			console_2.MЧопкардан(":")

			console_2.MЧопкардан(([]byte)("]"))
		}
		console_2.MЧопкардан(([]byte)("------------>"))

		if textpointer != nil {
			memorymanager.Free(textpointer)
		}

	}

}
