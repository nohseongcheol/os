/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "ማስታወሻmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eአይነት		uint16
	emachine	uint16
	eእትም		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eባንዲራዎች		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shስም		uint32
	shአይነት		uint32
	shባንዲራዎች	uint32
	shaddress	uint32
	shoffset	uint32
	shመጠን		uint32
	shአገናኝ		uint32
	shመረጃ		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfፕሮግራምheader struct {
	pአይነት	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pባንዲራዎች	uint32
	pማሰለፊያ	uint32
}
type Elf32ማስታወሻ struct {
	nnamesz	uint32
	ndescsz	uint32
	nአይነት	uint32
}
type Elf32dyn struct {
	dtag	uint32
	dvalጠቋሚ	uint32
}
type Elf32rel struct {
	roffset	uint32
	rመረጃ	uint32
}
type Elf32rela struct {
	roffset	uint32
	rመረጃ	uint32
	raddend	uint32
}
type Elf32sym struct {
	stስም	uint32
	stዋጋ	uint32
	stመጠን	uint32
	stመረጃ	uint8
	stሌላ	uint8
	stshndx	uint16
}
type relocationጽሁፍ struct {
	offset		uint32
	ቁጥር		uint32
	oaddress	uint32
}
type Elf struct {
	ጽሁፍ		[]byte
	ጽሁፍlen		uint32
	relጽሁፍ		[100]relocationጽሁፍ
	relጽሁፍlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, Pገጽዳይሬክቶሪentry uint32) {

	ማስታወሻmanager := Tማስታወሻmanager{}
	var ጽሁፍጠቋሚ Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderመጠን := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderመጠን*i]))

			var sectስም []byte
			ማስጀመሪያ := uint32(strtab.shoffset + sectheader.shስም)
			መጨረሻ := ማስጀመሪያ
			for ; ; መጨረሻ++ {
				if data[መጨረሻ] == 0x0 || data[መጨረሻ] == ' ' {
					break
				}
			}
			sectስም = data[ማስጀመሪያ:መጨረሻ]

			var sectዋጋ []byte
			if sectheader.shአይነት != 8 {
				መጨረሻoffset := sectheader.shoffset + sectheader.shመጠን
				if መጨረሻoffset < sectheader.shoffset || መጨረሻoffset > uint32(len(data)) {
					continue
				}
				sectዋጋ = data[sectheader.shoffset:መጨረሻoffset]
			}

			if Equalባይትስ(sectስም, ([]byte)(".got.plt")) {
				console_2.Mማተሚያ("[")
				console_2.Mማተሚያ(sectስም)
				console_2.Mማተሚያ(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32ማተሚያ(self.Got)
				console_2.Mማተሚያ("]")
			}
			if Equalባይትስ(sectስም, ([]byte)(".dynamic")) {
				console_2.Mማተሚያ("[")
				console_2.Mማተሚያ(sectስም)
				console_2.Mማተሚያ(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32ማተሚያ(dynamic)
				console_2.Mማተሚያ("]")
			}

			if sectheader.shaddress > 0x1000 {
				መጠን := sectheader.shመጠን
				if sectheader.shአይነት == 8 {
					Zeroመከልከያውስጥገጽዳይሬክቶሪ(sectheader.shaddress, መጠን, Pገጽዳይሬክቶሪentry)
				} else {
					destination_2 := Getባይትስfromጠቋሚ(uintptr(sectheader.shaddress), int(መጠን), int(መጠን))
					Setመከልከያውስጥገጽዳይሬክቶሪ(sectዋጋ, destination_2, መጠን, Pገጽዳይሬክቶሪentry)
				}
			}

			continue

			if Equalባይትስ(sectስም, ([]byte)(".text")) {
				console_2.Mማተሚያ(".text")
				console_2.Mማተሚያ("[")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shaddress)
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shoffset)
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shመጠን)
				console_2.Mማተሚያ("]")
				copy(self.ጽሁፍ[:sectheader.shመጠን], sectዋጋ[:sectheader.shመጠን])
				self.ጽሁፍlen = sectheader.shመጠን
			}
			if Equalባይትስ(sectስም, ([]byte)(".rel.text")) {
				console_2.Mማተሚያ(".rel.text")
				console_2.Mማተሚያ("[")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shaddress)
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shመጠን)
				console_2.Mማተሚያ("]")
				for rt := uint32(0); rt < sectheader.shመጠን/8; rt++ {
					offset := *(*uint32)(Pointer(&sectዋጋ[rt*8]))
					self.relጽሁፍ[rt].offset = offset
					self.relጽሁፍ[rt].oaddress = *(*uint32)(Pointer(&self.ጽሁፍ[offset]))
					self.relጽሁፍ[rt].ቁጥር = *(*uint32)(Pointer(&sectዋጋ[rt*8+4]))
					self.relጽሁፍlen++
				}
			}
			if Equalባይትስ(sectስም, ([]byte)(".dynsym")) {
				console_2.Mማተሚያ(".dynsym")
				console_2.Mማተሚያ("[")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shaddress)
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shመጠን)
				console_2.Mማተሚያ("]")
				for rt := uint32(0); rt < sectheader.shመጠን/8; rt++ {
					offset := *(*uint32)(Pointer(&sectዋጋ[rt*8]))
					self.relጽሁፍ[rt].offset = offset
					self.relጽሁፍ[rt].oaddress = *(*uint32)(Pointer(&self.ጽሁፍ[offset]))
					self.relጽሁፍ[rt].ቁጥር = *(*uint32)(Pointer(&sectዋጋ[rt*8+4]))
					self.relጽሁፍlen++
				}
			}
			if Equalባይትስ(sectስም, ([]byte)(".dynstr")) {
				console_2.Mማተሚያ(".dynstr")
				console_2.Mማተሚያ("[")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shaddress)
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shመጠን)
				console_2.Mማተሚያ("]")
			}
			if Equalባይትስ(sectስም, ([]byte)(".strtab")) {
				console_2.Mማተሚያ(".strtab")
				console_2.Mማተሚያ("[")
				console_2.MUnsignedinteger32ማተሚያ(sectheader.shaddress)
				console_2.Mማተሚያ("]")
				rt := uint32(0)
				ማስጀመሪያ := uint32(0)

				for st := uint32(1); st < sectheader.shመጠን; st++ {
					if sectዋጋ[st] == 0x0 || sectዋጋ[st] == ' ' {
						funcስም := sectዋጋ[ማስጀመሪያ+1 : st]
						console_2.Mማተሚያ("+")
						console_2.Mማተሚያ(funcስም)
						self.strtab[rt] = Bባይትስtoሐረግ(funcስም)
						ማስጀመሪያ = st
						rt++
					}
				}

			}

		}

		console_2.Mማተሚያ(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relጽሁፍlen; rt++ {
			console_2.Mማተሚያ("[")
			console_2.Mማተሚያ(([]byte)(self.strtab[rt]))
			console_2.Mማተሚያ(":")
			console_2.MUnsignedinteger32ማተሚያ(self.relጽሁፍ[rt].ቁጥር)
			console_2.Mማተሚያ(":")

			console_2.Mማተሚያ(([]byte)("]"))
		}
		console_2.Mማተሚያ(([]byte)("------------>"))

		if ጽሁፍጠቋሚ != nil {
			ማስታወሻmanager.Fነፃ(ጽሁፍጠቋሚ)
		}

	}

}
