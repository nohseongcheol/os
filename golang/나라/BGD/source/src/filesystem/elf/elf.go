package elf

import . "unsafe"

import . "console"
import . "util"
import . "memorymanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eধরণ		uint16
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
	shname		uint32
	shধরণ		uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shsize		uint32
	shlink		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pধরণ	uint32
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
	nধরণ	uint32
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
	stname	uint32
	stvalue	uint32
	stsize	uint32
	stinfo	uint8
	stother	uint8
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

func (self *Elf) Parse(data []byte, Pagedirectoryentry uint32) {

	memorymanager := TMemorymanager{}
	var textpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheadersize := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheadersize*i]))

			var sectname []byte
			start := uint32(strtab.shoffset + sectheader.shname)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectname = data[start:end]

			var sectvalue []byte
			if sectheader.shধরণ != 8 {
				endoffset := sectheader.shoffset + sectheader.shsize
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectvalue = data[sectheader.shoffset:endoffset]
			}

			if Equalbytes(sectname, ([]byte)(".got.plt")) {
				console_2.MPrint("[")
				console_2.MPrint(sectname)
				console_2.MPrint(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32print(self.Got)
				console_2.MPrint("]")
			}
			if Equalbytes(sectname, ([]byte)(".dynamic")) {
				console_2.MPrint("[")
				console_2.MPrint(sectname)
				console_2.MPrint(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32print(dynamic)
				console_2.MPrint("]")
			}

			if sectheader.shaddress > 0x1000 {
				size := sectheader.shsize
				if sectheader.shধরণ == 8 {
					Zeroblockinpagedirectory(sectheader.shaddress, size, Pagedirectoryentry)
				} else {
					destination_2 := Getbytesfrompointer(uintptr(sectheader.shaddress), int(size), int(size))
					Setblockinpagedirectory(sectvalue, destination_2, size, Pagedirectoryentry)
				}
			}

			continue

			if Equalbytes(sectname, ([]byte)(".text")) {
				console_2.MPrint(".text")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shoffset)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shsize)
				console_2.MPrint("]")
				copy(self.text[:sectheader.shsize], sectvalue[:sectheader.shsize])
				self.textlen = sectheader.shsize
			}
			if Equalbytes(sectname, ([]byte)(".rel.text")) {
				console_2.MPrint(".rel.text")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shsize)
				console_2.MPrint("]")
				for rt := uint32(0); rt < sectheader.shsize/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbytes(sectname, ([]byte)(".dynsym")) {
				console_2.MPrint(".dynsym")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shsize)
				console_2.MPrint("]")
				for rt := uint32(0); rt < sectheader.shsize/8; rt++ {
					offset := *(*uint32)(Pointer(&sectvalue[rt*8]))
					self.reltext[rt].offset = offset
					self.reltext[rt].oaddress = *(*uint32)(Pointer(&self.text[offset]))
					self.reltext[rt].number = *(*uint32)(Pointer(&sectvalue[rt*8+4]))
					self.reltextlen++
				}
			}
			if Equalbytes(sectname, ([]byte)(".dynstr")) {
				console_2.MPrint(".dynstr")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(sectheader.shsize)
				console_2.MPrint("]")
			}
			if Equalbytes(sectname, ([]byte)(".strtab")) {
				console_2.MPrint(".strtab")
				console_2.MPrint("[")
				console_2.MUnsignedinteger32print(sectheader.shaddress)
				console_2.MPrint("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shsize; st++ {
					if sectvalue[st] == 0x0 || sectvalue[st] == ' ' {
						funcname := sectvalue[start+1 : st]
						console_2.MPrint("+")
						console_2.MPrint(funcname)
						self.strtab[rt] = Bytestostring(funcname)
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
