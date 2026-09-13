package elf

import . "unsafe"

import . "console"
import . "util"
import . "xotiramanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTuri		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eBayroqlar	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNomi		uint32
	shTuri		uint32
	shBayroqlar	uint32
	shaddress	uint32
	shoffset	uint32
	shHajmi		uint32
	shBogʻ		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfdasturheader struct {
	pTuri		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pBayroqlar	uint32
	pTekislash	uint32
}
type Elf32Qayd struct {
	nnamesz	uint32
	ndescsz	uint32
	nTuri	uint32
}
type Elf32dyn struct {
	dtag		uint32
	dvalKorsatgich	uint32
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
	stNomi		uint32
	stQiymat	uint32
	stHajmi		uint32
	stinfo		uint8
	stBoshqa	uint8
	stshndx		uint16
}
type relocationMatn struct {
	offset		uint32
	rAQAM		uint32
	oaddress	uint32
}
type Elf struct {
	matn		[]byte
	matnlen		uint32
	relMatn		[100]relocationMatn
	relMatnlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, SAHIFAJildentry uint32) {

	xotiramanager := TXotiramanager{}
	var matnKorsatgich Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderHajmi := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderHajmi*i]))

			var sectNomi []byte
			boshlash := uint32(strtab.shoffset + sectheader.shNomi)
			oxirga := boshlash
			for ; ; oxirga++ {
				if data[oxirga] == 0x0 || data[oxirga] == ' ' {
					break
				}
			}
			sectNomi = data[boshlash:oxirga]

			var sectQiymat []byte
			if sectheader.shTuri != 8 {
				oxirgaoffset := sectheader.shoffset + sectheader.shHajmi
				if oxirgaoffset < sectheader.shoffset || oxirgaoffset > uint32(len(data)) {
					continue
				}
				sectQiymat = data[sectheader.shoffset:oxirgaoffset]
			}

			if EqualBaytlar(sectNomi, ([]byte)(".got.plt")) {
				console_2.MChopetish("[")
				console_2.MChopetish(sectNomi)
				console_2.MChopetish(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Chopetish(self.Got)
				console_2.MChopetish("]")
			}
			if EqualBaytlar(sectNomi, ([]byte)(".dynamic")) {
				console_2.MChopetish("[")
				console_2.MChopetish(sectNomi)
				console_2.MChopetish(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Chopetish(dynamic)
				console_2.MChopetish("]")
			}

			if sectheader.shaddress > 0x1000 {
				hajmi := sectheader.shHajmi
				if sectheader.shTuri == 8 {
					ZeroBlokYaqinlashtirishSAHIFAJild(sectheader.shaddress, hajmi, SAHIFAJildentry)
				} else {
					destination_2 := GetBaytlarfromKorsatgich(uintptr(sectheader.shaddress), int(hajmi), int(hajmi))
					SetBlokYaqinlashtirishSAHIFAJild(sectQiymat, destination_2, hajmi, SAHIFAJildentry)
				}
			}

			continue

			if EqualBaytlar(sectNomi, ([]byte)(".text")) {
				console_2.MChopetish(".text")
				console_2.MChopetish("[")
				console_2.MUnsignedinteger32Chopetish(sectheader.shaddress)
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(sectheader.shoffset)
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(sectheader.shHajmi)
				console_2.MChopetish("]")
				copy(self.matn[:sectheader.shHajmi], sectQiymat[:sectheader.shHajmi])
				self.matnlen = sectheader.shHajmi
			}
			if EqualBaytlar(sectNomi, ([]byte)(".rel.text")) {
				console_2.MChopetish(".rel.text")
				console_2.MChopetish("[")
				console_2.MUnsignedinteger32Chopetish(sectheader.shaddress)
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(sectheader.shHajmi)
				console_2.MChopetish("]")
				for rt := uint32(0); rt < sectheader.shHajmi/8; rt++ {
					offset := *(*uint32)(Pointer(&sectQiymat[rt*8]))
					self.relMatn[rt].offset = offset
					self.relMatn[rt].oaddress = *(*uint32)(Pointer(&self.matn[offset]))
					self.relMatn[rt].rAQAM = *(*uint32)(Pointer(&sectQiymat[rt*8+4]))
					self.relMatnlen++
				}
			}
			if EqualBaytlar(sectNomi, ([]byte)(".dynsym")) {
				console_2.MChopetish(".dynsym")
				console_2.MChopetish("[")
				console_2.MUnsignedinteger32Chopetish(sectheader.shaddress)
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(sectheader.shHajmi)
				console_2.MChopetish("]")
				for rt := uint32(0); rt < sectheader.shHajmi/8; rt++ {
					offset := *(*uint32)(Pointer(&sectQiymat[rt*8]))
					self.relMatn[rt].offset = offset
					self.relMatn[rt].oaddress = *(*uint32)(Pointer(&self.matn[offset]))
					self.relMatn[rt].rAQAM = *(*uint32)(Pointer(&sectQiymat[rt*8+4]))
					self.relMatnlen++
				}
			}
			if EqualBaytlar(sectNomi, ([]byte)(".dynstr")) {
				console_2.MChopetish(".dynstr")
				console_2.MChopetish("[")
				console_2.MUnsignedinteger32Chopetish(sectheader.shaddress)
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(sectheader.shHajmi)
				console_2.MChopetish("]")
			}
			if EqualBaytlar(sectNomi, ([]byte)(".strtab")) {
				console_2.MChopetish(".strtab")
				console_2.MChopetish("[")
				console_2.MUnsignedinteger32Chopetish(sectheader.shaddress)
				console_2.MChopetish("]")
				rt := uint32(0)
				boshlash := uint32(0)

				for st := uint32(1); st < sectheader.shHajmi; st++ {
					if sectQiymat[st] == 0x0 || sectQiymat[st] == ' ' {
						funcNomi := sectQiymat[boshlash+1 : st]
						console_2.MChopetish("+")
						console_2.MChopetish(funcNomi)
						self.strtab[rt] = Baytlartostring(funcNomi)
						boshlash = st
						rt++
					}
				}

			}

		}

		console_2.MChopetish(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relMatnlen; rt++ {
			console_2.MChopetish("[")
			console_2.MChopetish(([]byte)(self.strtab[rt]))
			console_2.MChopetish(":")
			console_2.MUnsignedinteger32Chopetish(self.relMatn[rt].rAQAM)
			console_2.MChopetish(":")

			console_2.MChopetish(([]byte)("]"))
		}
		console_2.MChopetish(([]byte)("------------>"))

		if matnKorsatgich != nil {
			xotiramanager.Bosh(matnKorsatgich)
		}

	}

}
