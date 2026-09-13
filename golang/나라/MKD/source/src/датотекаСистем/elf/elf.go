package elf

import . "unsafe"

import . "console"
import . "util"
import . "меморијаmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТип		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eАтрибути	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shИме		uint32
	shТип		uint32
	shАтрибути	uint32
	shaddress	uint32
	shoffset	uint32
	shГолемина	uint32
	shВрска		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограмаheader struct {
	pТип		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pАтрибути	uint32
	pПодреди	uint32
}
type Elf32Белешка struct {
	nnamesz	uint32
	ndescsz	uint32
	nТип	uint32
}
type Elf32dyn struct {
	dЕтикета	uint32
	dvalСтрелка	uint32
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
	stИме		uint32
	stВредност	uint32
	stГолемина	uint32
	stinfo		uint8
	stДруги		uint8
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

func (само *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (само *Elf) Parse(data []byte, СтраницаДиректориумentry uint32) {

	меморијаmanager := TМеморијаmanager{}
	var текстСтрелка Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderГолемина := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderГолемина*i]))

			var sectИме []byte
			пушти := uint32(strtab.shoffset + sectheader.shИме)
			end := пушти
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectИме = data[пушти:end]

			var sectВредност []byte
			if sectheader.shТип != 8 {
				endoffset := sectheader.shoffset + sectheader.shГолемина
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectВредност = data[sectheader.shoffset:endoffset]
			}

			if Equalбајти(sectИме, ([]byte)(".got.plt")) {
				console_2.MПечати("[")
				console_2.MПечати(sectИме)
				console_2.MПечати(":")
				само.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Печати(само.Got)
				console_2.MПечати("]")
			}
			if Equalбајти(sectИме, ([]byte)(".dynamic")) {
				console_2.MПечати("[")
				console_2.MПечати(sectИме)
				console_2.MПечати(":")
				dynamic := sectheader.shaddress
				само.Dynamic = dynamic
				console_2.MUnsignedinteger32Печати(dynamic)
				console_2.MПечати("]")
			}

			if sectheader.shaddress > 0x1000 {
				големина := sectheader.shГолемина
				if sectheader.shТип == 8 {
					ZeroblockвоСтраницаДиректориум(sectheader.shaddress, големина, СтраницаДиректориумentry)
				} else {
					одредиште_2 := GetбајтиfromСтрелка(uintptr(sectheader.shaddress), int(големина), int(големина))
					ПоставиblockвоСтраницаДиректориум(sectВредност, одредиште_2, големина, СтраницаДиректориумentry)
				}
			}

			continue

			if Equalбајти(sectИме, ([]byte)(".text")) {
				console_2.MПечати(".text")
				console_2.MПечати("[")
				console_2.MUnsignedinteger32Печати(sectheader.shaddress)
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(sectheader.shoffset)
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(sectheader.shГолемина)
				console_2.MПечати("]")
				copy(само.текст[:sectheader.shГолемина], sectВредност[:sectheader.shГолемина])
				само.текстlen = sectheader.shГолемина
			}
			if Equalбајти(sectИме, ([]byte)(".rel.text")) {
				console_2.MПечати(".rel.text")
				console_2.MПечати("[")
				console_2.MUnsignedinteger32Печати(sectheader.shaddress)
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(sectheader.shГолемина)
				console_2.MПечати("]")
				for rt := uint32(0); rt < sectheader.shГолемина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					само.relТекст[rt].offset = offset
					само.relТекст[rt].oaddress = *(*uint32)(Pointer(&само.текст[offset]))
					само.relТекст[rt].number = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					само.relТекстlen++
				}
			}
			if Equalбајти(sectИме, ([]byte)(".dynsym")) {
				console_2.MПечати(".dynsym")
				console_2.MПечати("[")
				console_2.MUnsignedinteger32Печати(sectheader.shaddress)
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(sectheader.shГолемина)
				console_2.MПечати("]")
				for rt := uint32(0); rt < sectheader.shГолемина/8; rt++ {
					offset := *(*uint32)(Pointer(&sectВредност[rt*8]))
					само.relТекст[rt].offset = offset
					само.relТекст[rt].oaddress = *(*uint32)(Pointer(&само.текст[offset]))
					само.relТекст[rt].number = *(*uint32)(Pointer(&sectВредност[rt*8+4]))
					само.relТекстlen++
				}
			}
			if Equalбајти(sectИме, ([]byte)(".dynstr")) {
				console_2.MПечати(".dynstr")
				console_2.MПечати("[")
				console_2.MUnsignedinteger32Печати(sectheader.shaddress)
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(sectheader.shГолемина)
				console_2.MПечати("]")
			}
			if Equalбајти(sectИме, ([]byte)(".strtab")) {
				console_2.MПечати(".strtab")
				console_2.MПечати("[")
				console_2.MUnsignedinteger32Печати(sectheader.shaddress)
				console_2.MПечати("]")
				rt := uint32(0)
				пушти := uint32(0)

				for st := uint32(1); st < sectheader.shГолемина; st++ {
					if sectВредност[st] == 0x0 || sectВредност[st] == ' ' {
						funcИме := sectВредност[пушти+1 : st]
						console_2.MПечати("+")
						console_2.MПечати(funcИме)
						само.strtab[rt] = Бајтиtostring(funcИме)
						пушти = st
						rt++
					}
				}

			}

		}

		console_2.MПечати(([]byte)("<------------"))
		for rt := uint32(0); rt < само.relТекстlen; rt++ {
			console_2.MПечати("[")
			console_2.MПечати(([]byte)(само.strtab[rt]))
			console_2.MПечати(":")
			console_2.MUnsignedinteger32Печати(само.relТекст[rt].number)
			console_2.MПечати(":")

			console_2.MПечати(([]byte)("]"))
		}
		console_2.MПечати(([]byte)("------------>"))

		if текстСтрелка != nil {
			меморијаmanager.Слободни(текстСтрелка)
		}

	}

}
