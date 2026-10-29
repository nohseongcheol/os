/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "паметmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТип		uint16
	emachine	uint16
	eВерсия		uint32
	eзапис		uint32
	ephoff		uint32
	eshoff		uint32
	eФлагове	uint32
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
	shФлагове	uint32
	shaddress	uint32
	shoffset	uint32
	shРазмер	uint32
	shВръзка	uint32
	shИнформация	uint32
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
	pФлагове	uint32
	pПодравняване	uint32
}
type Elf32Бележка struct {
	nnamesz	uint32
	ndescsz	uint32
	nТип	uint32
}
type Elf32dyn struct {
	dЕтикет		uint32
	dvalПоказалци	uint32
}
type Elf32rel struct {
	roffset		uint32
	rИнформация	uint32
}
type Elf32rela struct {
	roffset		uint32
	rИнформация	uint32
	raddend		uint32
}
type Elf32sym struct {
	stИме		uint32
	stСтойност	uint32
	stРазмер	uint32
	stИнформация	uint8
	stДруги		uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset		uint32
	число		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Динамично	uint32
}

func (себеси *Elf) Getзапис(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eзапис
}

func (себеси *Elf) Parse(data []byte, Страницапапказапис uint32) {

	паметmanager := TПаметmanager{}
	var текстПоказалци Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderРазмер := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderРазмер*i]))

			var sectИме []byte
			стартиране := uint32(strtab.shoffset + sectheader.shИме)
			край := стартиране
			for ; ; край++ {
				if data[край] == 0x0 || data[край] == ' ' {
					break
				}
			}
			sectИме = data[стартиране:край]

			var sectСтойност []byte
			if sectheader.shТип != 8 {
				крайoffset := sectheader.shoffset + sectheader.shРазмер
				if крайoffset < sectheader.shoffset || крайoffset > uint32(len(data)) {
					continue
				}
				sectСтойност = data[sectheader.shoffset:крайoffset]
			}

			if ЕднакъвБайтове(sectИме, ([]byte)(".got.plt")) {
				console_2.MПечат("[")
				console_2.MПечат(sectИме)
				console_2.MПечат(":")
				себеси.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Печат(себеси.Got)
				console_2.MПечат("]")
			}
			if ЕднакъвБайтове(sectИме, ([]byte)(".dynamic")) {
				console_2.MПечат("[")
				console_2.MПечат(sectИме)
				console_2.MПечат(":")
				динамично := sectheader.shaddress
				себеси.Динамично = динамично
				console_2.MUnsignedinteger32Печат(динамично)
				console_2.MПечат("]")
			}

			if sectheader.shaddress > 0x1000 {
				размер := sectheader.shРазмер
				if sectheader.shТип == 8 {
					ZeroБлокВходящСтраницапапка(sectheader.shaddress, размер, Страницапапказапис)
				} else {
					назначение_2 := GetБайтовеfromПоказалци(uintptr(sectheader.shaddress), int(размер), int(размер))
					ЗадайБлокВходящСтраницапапка(sectСтойност, назначение_2, размер, Страницапапказапис)
				}
			}

			continue

			if ЕднакъвБайтове(sectИме, ([]byte)(".text")) {
				console_2.MПечат(".text")
				console_2.MПечат("[")
				console_2.MUnsignedinteger32Печат(sectheader.shaddress)
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(sectheader.shoffset)
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(sectheader.shРазмер)
				console_2.MПечат("]")
				copy(себеси.текст[:sectheader.shРазмер], sectСтойност[:sectheader.shРазмер])
				себеси.текстlen = sectheader.shРазмер
			}
			if ЕднакъвБайтове(sectИме, ([]byte)(".rel.text")) {
				console_2.MПечат(".rel.text")
				console_2.MПечат("[")
				console_2.MUnsignedinteger32Печат(sectheader.shaddress)
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(sectheader.shРазмер)
				console_2.MПечат("]")
				for rt := uint32(0); rt < sectheader.shРазмер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectСтойност[rt*8]))
					себеси.relТекст[rt].offset = offset
					себеси.relТекст[rt].oaddress = *(*uint32)(Pointer(&себеси.текст[offset]))
					себеси.relТекст[rt].число = *(*uint32)(Pointer(&sectСтойност[rt*8+4]))
					себеси.relТекстlen++
				}
			}
			if ЕднакъвБайтове(sectИме, ([]byte)(".dynsym")) {
				console_2.MПечат(".dynsym")
				console_2.MПечат("[")
				console_2.MUnsignedinteger32Печат(sectheader.shaddress)
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(sectheader.shРазмер)
				console_2.MПечат("]")
				for rt := uint32(0); rt < sectheader.shРазмер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectСтойност[rt*8]))
					себеси.relТекст[rt].offset = offset
					себеси.relТекст[rt].oaddress = *(*uint32)(Pointer(&себеси.текст[offset]))
					себеси.relТекст[rt].число = *(*uint32)(Pointer(&sectСтойност[rt*8+4]))
					себеси.relТекстlen++
				}
			}
			if ЕднакъвБайтове(sectИме, ([]byte)(".dynstr")) {
				console_2.MПечат(".dynstr")
				console_2.MПечат("[")
				console_2.MUnsignedinteger32Печат(sectheader.shaddress)
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(sectheader.shРазмер)
				console_2.MПечат("]")
			}
			if ЕднакъвБайтове(sectИме, ([]byte)(".strtab")) {
				console_2.MПечат(".strtab")
				console_2.MПечат("[")
				console_2.MUnsignedinteger32Печат(sectheader.shaddress)
				console_2.MПечат("]")
				rt := uint32(0)
				стартиране := uint32(0)

				for st := uint32(1); st < sectheader.shРазмер; st++ {
					if sectСтойност[st] == 0x0 || sectСтойност[st] == ' ' {
						funcИме := sectСтойност[стартиране+1 : st]
						console_2.MПечат("+")
						console_2.MПечат(funcИме)
						себеси.strtab[rt] = БайтовеtoНиз(funcИме)
						стартиране = st
						rt++
					}
				}

			}

		}

		console_2.MПечат(([]byte)("<------------"))
		for rt := uint32(0); rt < себеси.relТекстlen; rt++ {
			console_2.MПечат("[")
			console_2.MПечат(([]byte)(себеси.strtab[rt]))
			console_2.MПечат(":")
			console_2.MUnsignedinteger32Печат(себеси.relТекст[rt].число)
			console_2.MПечат(":")

			console_2.MПечат(([]byte)("]"))
		}
		console_2.MПечат(([]byte)("------------>"))

		if текстПоказалци != nil {
			паметmanager.Свободно(текстПоказалци)
		}

	}

}
