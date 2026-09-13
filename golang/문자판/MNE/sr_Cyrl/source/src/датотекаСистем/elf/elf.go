package elf

import . "unsafe"

import . "конзола"
import . "util"
import . "меморијаmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eВрста		uint16
	emachine	uint16
	eИздање		uint32
	eунос		uint32
	ephoff		uint32
	eshoff		uint32
	eПараметри	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shНазив		uint32
	shВрста		uint32
	shПараметри	uint32
	shaddress	uint32
	shoffset	uint32
	shВеличина	uint32
	shВеза		uint32
	shПодаци	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограмheader struct {
	pВрста		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pПараметри	uint32
	pПоравнање	uint32
}
type Elf32Белешка struct {
	nnamesz	uint32
	ndescsz	uint32
	nВрста	uint32
}
type Elf32dyn struct {
	dознака		uint32
	dvalПоказивач	uint32
}
type Elf32rel struct {
	roffset	uint32
	rПодаци	uint32
}
type Elf32rela struct {
	roffset	uint32
	rПодаци	uint32
	raddend	uint32
}
type Elf32sym struct {
	stНазив		uint32
	stВредност	uint32
	stВеличина	uint32
	stПодаци	uint8
	stДруго		uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset		uint32
	број		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Растегљиво	uint32
}

func (исти *Elf) Getунос(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eунос
}

func (исти *Elf) Parse(data []byte, СТРАНАДиректоријумунос uint32) {

	меморијаmanager := TМеморијаmanager{}
	var текстПоказивач Pointer = nil

	var конзола_2 = TКонзола{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderВеличина := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderВеличина*i]))

			var sectНазив []byte
			покрени := uint32(strtab.shoffset + sectheader.shНазив)
			kraj := покрени
			for ; ; kraj++ {
				if data[kraj] == 0x0 || data[kraj] == ' ' {
					break
				}
			}
			sectНазив = data[покрени:kraj]

			var sectВредност []byte
			if sectheader.shВрста != 8 {
				krajoffset := sectheader.shoffset + sectheader.shВеличина
				if krajoffset < sectheader.shoffset || krajoffset > uint32(len(data)) {
					continue
				}
				sectВредност = data[sectheader.shoffset:krajoffset]
			}

			if ИстаБајтова(sectНазив, ([]byte)(".got.plt")) {
				конзола_2.MШтампај("[")
				конзола_2.MШтампај(sectНазив)
				конзола_2.MШтампај(":")
				исти.Got = sectheader.shaddress
				конзола_2.MUnsignedinteger32Штампај(исти.Got)
				конзола_2.MШтампај("]")
			}
			if ИстаБајтова(sectНазив, ([]byte)(".dynamic")) {
				конзола_2.MШтампај("[")
				конзола_2.MШтампај(sectНазив)
				конзола_2.MШтампај(":")
				растегљиво := sectheader.shaddress
				исти.Растегљиво = растегљиво
				конзола_2.MUnsignedinteger32Штампај(растегљиво)
				конзола_2.MШтампај("]")
			}

			if sectheader.shaddress > 0x1000 {
				величина := sectheader.shВеличина
				if sectheader.shВрста == 8 {
					ZeroБлокПримљеноСТРАНАДиректоријум(sectheader.shaddress, величина, СТРАНАДиректоријумунос)
				} else {
					одредиште_2 := GetБајтовасаПоказивач(uintptr(sectheader.shaddress), int(величина), int(величина))
					СкупБлокПримљеноСТРАНАДиректоријум(sectВредност, одредиште_2, величина, СТРАНАДиректоријумунос)
				}
			}

			continue

			if ИстаБајтова(sectНазив, ([]byte)(".text")) {
				конзола_2.MШтампај(".text")
				конзола_2.MШтампај("[")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shaddress)
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shoffset)
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shВеличина)
				конзола_2.MШтампај("]")
				copy(исти.текст[:sectheader.shВеличина], sectВредност[:sectheader.shВеличина])
				исти.текстlen = sectheader.shВеличина
			}
			if ИстаБајтова(sectНазив, ([]byte)(".rel.text")) {
				конзола_2.MШтампај(".rel.text")
				конзола_2.MШтампај("[")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shaddress)
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shВеличина)
				конзола_2.MШтампај("]")
				for rt := uint32(0); rt < sectheader.shВеличина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					исти.relТекст[rt].offset = offset
					исти.relТекст[rt].oaddress = *(*uint32)(Pointer(&исти.текст[offset]))
					исти.relТекст[rt].број = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					исти.relТекстlen++
				}
			}
			if ИстаБајтова(sectНазив, ([]byte)(".dynsym")) {
				конзола_2.MШтампај(".dynsym")
				конзола_2.MШтампај("[")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shaddress)
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shВеличина)
				конзола_2.MШтампај("]")
				for rt := uint32(0); rt < sectheader.shВеличина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					исти.relТекст[rt].offset = offset
					исти.relТекст[rt].oaddress = *(*uint32)(Pointer(&исти.текст[offset]))
					исти.relТекст[rt].број = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					исти.relТекстlen++
				}
			}
			if ИстаБајтова(sectНазив, ([]byte)(".dynstr")) {
				конзола_2.MШтампај(".dynstr")
				конзола_2.MШтампај("[")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shaddress)
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shВеличина)
				конзола_2.MШтампај("]")
			}
			if ИстаБајтова(sectНазив, ([]byte)(".strtab")) {
				конзола_2.MШтампај(".strtab")
				конзола_2.MШтампај("[")
				конзола_2.MUnsignedinteger32Штампај(sectheader.shaddress)
				конзола_2.MШтампај("]")
				rt := uint32(0)
				покрени := uint32(0)

				for st := uint32(1); st < sectheader.shВеличина; st++ {
					if sectВредност[st] == 0x0 || sectВредност[st] == ' ' {
						funcНазив := sectВредност[покрени+1 : st]
						конзола_2.MШтампај("+")
						конзола_2.MШтампај(funcНазив)
						исти.strtab[rt] = Бајтоваtoниска(funcНазив)
						покрени = st
						rt++
					}
				}

			}

		}

		конзола_2.MШтампај(([]byte)("<------------"))
		for rt := uint32(0); rt < исти.relТекстlen; rt++ {
			конзола_2.MШтампај("[")
			конзола_2.MШтампај(([]byte)(исти.strtab[rt]))
			конзола_2.MШтампај(":")
			конзола_2.MUnsignedinteger32Штампај(исти.relТекст[rt].број)
			конзола_2.MШтампај(":")

			конзола_2.MШтампај(([]byte)("]"))
		}
		конзола_2.MШтампај(([]byte)("------------>"))

		if текстПоказивач != nil {
			меморијаmanager.Слободно(текстПоказивач)
		}

	}

}
