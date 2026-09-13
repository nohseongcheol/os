package elf

import . "unsafe"

import . "консол"
import . "util"
import . "санахойЗохицуулагч"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТөрөл		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eТөлвүүд	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shНэр		uint32
	shТөрөл		uint32
	shТөлвүүд	uint32
	shaddress	uint32
	shoffset	uint32
	shХэмжээ	uint32
	shХолбоос	uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfПрограмheader struct {
	pТөрөл		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pТөлвүүд	uint32
	palign		uint32
}
type Elf32note struct {
	nnamesz	uint32
	ndescsz	uint32
	nТөрөл	uint32
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
	stНэр		uint32
	stУтга		uint32
	stХэмжээ	uint32
	stinfo		uint8
	stБусад		uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, ХУУДАСЛавлахentry uint32) {

	санахойЗохицуулагч := TСанахойЗохицуулагч{}
	var текстpointer Pointer = nil

	var консол_2 = TКонсол{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderХэмжээ := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderХэмжээ*i]))

			var sectНэр []byte
			эхлэл := uint32(strtab.shoffset + sectheader.shНэр)
			end := эхлэл
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectНэр = data[эхлэл:end]

			var sectУтга []byte
			if sectheader.shТөрөл != 8 {
				endoffset := sectheader.shoffset + sectheader.shХэмжээ
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectУтга = data[sectheader.shoffset:endoffset]
			}

			if EqualБайт(sectНэр, ([]byte)(".got.plt")) {
				консол_2.MХэвлэх("[")
				консол_2.MХэвлэх(sectНэр)
				консол_2.MХэвлэх(":")
				self.Got = sectheader.shaddress
				консол_2.MUnsignedinteger32Хэвлэх(self.Got)
				консол_2.MХэвлэх("]")
			}
			if EqualБайт(sectНэр, ([]byte)(".dynamic")) {
				консол_2.MХэвлэх("[")
				консол_2.MХэвлэх(sectНэр)
				консол_2.MХэвлэх(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				консол_2.MUnsignedinteger32Хэвлэх(dynamic)
				консол_2.MХэвлэх("]")
			}

			if sectheader.shaddress > 0x1000 {
				хэмжээ := sectheader.shХэмжээ
				if sectheader.shТөрөл == 8 {
					ZeroblockinХУУДАСЛавлах(sectheader.shaddress, хэмжээ, ХУУДАСЛавлахentry)
				} else {
					destination_2 := GetБайтfrompointer(uintptr(sectheader.shaddress), int(хэмжээ), int(хэмжээ))
					SetblockinХУУДАСЛавлах(sectУтга, destination_2, хэмжээ, ХУУДАСЛавлахentry)
				}
			}

			continue

			if EqualБайт(sectНэр, ([]byte)(".text")) {
				консол_2.MХэвлэх(".text")
				консол_2.MХэвлэх("[")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shaddress)
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shoffset)
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shХэмжээ)
				консол_2.MХэвлэх("]")
				copy(self.текст[:sectheader.shХэмжээ], sectУтга[:sectheader.shХэмжээ])
				self.текстlen = sectheader.shХэмжээ
			}
			if EqualБайт(sectНэр, ([]byte)(".rel.text")) {
				консол_2.MХэвлэх(".rel.text")
				консол_2.MХэвлэх("[")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shaddress)
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shХэмжээ)
				консол_2.MХэвлэх("]")
				for rt := uint32(0); rt < sectheader.shХэмжээ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectУтга[rt*8]))
					self.relТекст[rt].offset = offset
					self.relТекст[rt].oaddress = *(*uint32)(Pointer(&self.текст[offset]))
					self.relТекст[rt].number = *(*uint32)(Pointer(&sectУтга[rt*8+4]))
					self.relТекстlen++
				}
			}
			if EqualБайт(sectНэр, ([]byte)(".dynsym")) {
				консол_2.MХэвлэх(".dynsym")
				консол_2.MХэвлэх("[")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shaddress)
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shХэмжээ)
				консол_2.MХэвлэх("]")
				for rt := uint32(0); rt < sectheader.shХэмжээ/8; rt++ {
					offset := *(*uint32)(Pointer(&sectУтга[rt*8]))
					self.relТекст[rt].offset = offset
					self.relТекст[rt].oaddress = *(*uint32)(Pointer(&self.текст[offset]))
					self.relТекст[rt].number = *(*uint32)(Pointer(&sectУтга[rt*8+4]))
					self.relТекстlen++
				}
			}
			if EqualБайт(sectНэр, ([]byte)(".dynstr")) {
				консол_2.MХэвлэх(".dynstr")
				консол_2.MХэвлэх("[")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shaddress)
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shХэмжээ)
				консол_2.MХэвлэх("]")
			}
			if EqualБайт(sectНэр, ([]byte)(".strtab")) {
				консол_2.MХэвлэх(".strtab")
				консол_2.MХэвлэх("[")
				консол_2.MUnsignedinteger32Хэвлэх(sectheader.shaddress)
				консол_2.MХэвлэх("]")
				rt := uint32(0)
				эхлэл := uint32(0)

				for st := uint32(1); st < sectheader.shХэмжээ; st++ {
					if sectУтга[st] == 0x0 || sectУтга[st] == ' ' {
						funcНэр := sectУтга[эхлэл+1 : st]
						консол_2.MХэвлэх("+")
						консол_2.MХэвлэх(funcНэр)
						self.strtab[rt] = БайтtoБИЧВЭР(funcНэр)
						эхлэл = st
						rt++
					}
				}

			}

		}

		консол_2.MХэвлэх(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relТекстlen; rt++ {
			консол_2.MХэвлэх("[")
			консол_2.MХэвлэх(([]byte)(self.strtab[rt]))
			консол_2.MХэвлэх(":")
			консол_2.MUnsignedinteger32Хэвлэх(self.relТекст[rt].number)
			консол_2.MХэвлэх(":")

			консол_2.MХэвлэх(([]byte)("]"))
		}
		консол_2.MХэвлэх(([]byte)("------------>"))

		if текстpointer != nil {
			санахойЗохицуулагч.Чөлөөт(текстpointer)
		}

	}

}
