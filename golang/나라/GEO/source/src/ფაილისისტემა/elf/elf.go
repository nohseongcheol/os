package elf

import . "unsafe"

import . "console"
import . "util"
import . "მეხსიერებაmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eტიპი		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eალმები		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shსახელი	uint32
	shტიპი		uint32
	shალმები	uint32
	shaddress	uint32
	shoffset	uint32
	shზომა		uint32
	shბმული		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfპროგრამაheader struct {
	pტიპი		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pალმები		uint32
	pგანთავსება	uint32
}
type Elf32შენიშვნა struct {
	nnamesz	uint32
	ndescsz	uint32
	nტიპი	uint32
}
type Elf32dyn struct {
	dიარლიყი	uint32
	dvalკურსორი	uint32
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
	stსახელი	uint32
	stმნიშვნელობა	uint32
	stზომა		uint32
	stinfo		uint8
	stსხვა		uint8
	stshndx		uint16
}
type relocationტექსტი struct {
	offset		uint32
	რიცხვი		uint32
	oaddress	uint32
}
type Elf struct {
	ტექსტი		[]byte
	ტექსტიlen	uint32
	relტექსტი	[100]relocationტექსტი
	relტექსტიlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, Pგვერდიდასტაentry uint32) {

	მეხსიერებაmanager := Tმეხსიერებაmanager{}
	var ტექსტიკურსორი Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderზომა := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderზომა*i]))

			var sectსახელი []byte
			start := uint32(strtab.shoffset + sectheader.shსახელი)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectსახელი = data[start:end]

			var sectმნიშვნელობა []byte
			if sectheader.shტიპი != 8 {
				endoffset := sectheader.shoffset + sectheader.shზომა
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectმნიშვნელობა = data[sectheader.shoffset:endoffset]
			}

			if Equalბაიტი(sectსახელი, ([]byte)(".got.plt")) {
				console_2.Mბეჭდვა("[")
				console_2.Mბეჭდვა(sectსახელი)
				console_2.Mბეჭდვა(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32ბეჭდვა(self.Got)
				console_2.Mბეჭდვა("]")
			}
			if Equalბაიტი(sectსახელი, ([]byte)(".dynamic")) {
				console_2.Mბეჭდვა("[")
				console_2.Mბეჭდვა(sectსახელი)
				console_2.Mბეჭდვა(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32ბეჭდვა(dynamic)
				console_2.Mბეჭდვა("]")
			}

			if sectheader.shaddress > 0x1000 {
				ზომა := sectheader.shზომა
				if sectheader.shტიპი == 8 {
					Zeroblockგადიდებაგვერდიდასტა(sectheader.shaddress, ზომა, Pგვერდიდასტაentry)
				} else {
					destination_2 := Getბაიტიfromკურსორი(uintptr(sectheader.shaddress), int(ზომა), int(ზომა))
					Setblockგადიდებაგვერდიდასტა(sectმნიშვნელობა, destination_2, ზომა, Pგვერდიდასტაentry)
				}
			}

			continue

			if Equalბაიტი(sectსახელი, ([]byte)(".text")) {
				console_2.Mბეჭდვა(".text")
				console_2.Mბეჭდვა("[")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shaddress)
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shoffset)
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shზომა)
				console_2.Mბეჭდვა("]")
				copy(self.ტექსტი[:sectheader.shზომა], sectმნიშვნელობა[:sectheader.shზომა])
				self.ტექსტიlen = sectheader.shზომა
			}
			if Equalბაიტი(sectსახელი, ([]byte)(".rel.text")) {
				console_2.Mბეჭდვა(".rel.text")
				console_2.Mბეჭდვა("[")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shaddress)
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shზომა)
				console_2.Mბეჭდვა("]")
				for rt := uint32(0); rt < sectheader.shზომა/8; rt++ {
					offset := *(*uint32)(Pointer(&sectმნიშვნელობა[rt*8]))
					self.relტექსტი[rt].offset = offset
					self.relტექსტი[rt].oaddress = *(*uint32)(Pointer(&self.ტექსტი[offset]))
					self.relტექსტი[rt].რიცხვი = *(*uint32)(Pointer(&sectმნიშვნელობა[rt*8+4]))
					self.relტექსტიlen++
				}
			}
			if Equalბაიტი(sectსახელი, ([]byte)(".dynsym")) {
				console_2.Mბეჭდვა(".dynsym")
				console_2.Mბეჭდვა("[")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shaddress)
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shზომა)
				console_2.Mბეჭდვა("]")
				for rt := uint32(0); rt < sectheader.shზომა/8; rt++ {
					offset := *(*uint32)(Pointer(&sectმნიშვნელობა[rt*8]))
					self.relტექსტი[rt].offset = offset
					self.relტექსტი[rt].oaddress = *(*uint32)(Pointer(&self.ტექსტი[offset]))
					self.relტექსტი[rt].რიცხვი = *(*uint32)(Pointer(&sectმნიშვნელობა[rt*8+4]))
					self.relტექსტიlen++
				}
			}
			if Equalბაიტი(sectსახელი, ([]byte)(".dynstr")) {
				console_2.Mბეჭდვა(".dynstr")
				console_2.Mბეჭდვა("[")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shaddress)
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shზომა)
				console_2.Mბეჭდვა("]")
			}
			if Equalბაიტი(sectსახელი, ([]byte)(".strtab")) {
				console_2.Mბეჭდვა(".strtab")
				console_2.Mბეჭდვა("[")
				console_2.MUnsignedinteger32ბეჭდვა(sectheader.shaddress)
				console_2.Mბეჭდვა("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shზომა; st++ {
					if sectმნიშვნელობა[st] == 0x0 || sectმნიშვნელობა[st] == ' ' {
						funcსახელი := sectმნიშვნელობა[start+1 : st]
						console_2.Mბეჭდვა("+")
						console_2.Mბეჭდვა(funcსახელი)
						self.strtab[rt] = Bბაიტიtostring(funcსახელი)
						start = st
						rt++
					}
				}

			}

		}

		console_2.Mბეჭდვა(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relტექსტიlen; rt++ {
			console_2.Mბეჭდვა("[")
			console_2.Mბეჭდვა(([]byte)(self.strtab[rt]))
			console_2.Mბეჭდვა(":")
			console_2.MUnsignedinteger32ბეჭდვა(self.relტექსტი[rt].რიცხვი)
			console_2.Mბეჭდვა(":")

			console_2.Mბეჭდვა(([]byte)("]"))
		}
		console_2.Mბეჭდვა(([]byte)("------------>"))

		if ტექსტიკურსორი != nil {
			მეხსიერებაmanager.Fთავისუფალი(ტექსტიკურსორი)
		}

	}

}
