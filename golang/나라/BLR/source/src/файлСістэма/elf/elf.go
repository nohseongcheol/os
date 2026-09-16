/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "памяцьmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТып		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eСцяжкі		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shНазва		uint32
	shТып		uint32
	shСцяжкі	uint32
	shaddress	uint32
	shoffset	uint32
	shПамер		uint32
	shСпасылка	uint32
	shІнф		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпраграмаheader struct {
	pТып		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pСцяжкі		uint32
	pШыхтаванне	uint32
}
type Elf32Заўвага struct {
	nnamesz	uint32
	ndescsz	uint32
	nТып	uint32
}
type Elf32dyn struct {
	dТэг		uint32
	dvalПаказальнік	uint32
}
type Elf32rel struct {
	roffset	uint32
	rІнф	uint32
}
type Elf32rela struct {
	roffset	uint32
	rІнф	uint32
	raddend	uint32
}
type Elf32sym struct {
	stНазва		uint32
	stЗначэнне	uint32
	stПамер		uint32
	stІнф		uint8
	stЙньшы		uint8
	stshndx		uint16
}
type relocationТэкст struct {
	offset		uint32
	нУМАР		uint32
	oaddress	uint32
}
type Elf struct {
	тэкст		[]byte
	тэкстlen	uint32
	relТэкст	[100]relocationТэкст
	relТэкстlen	uint32
	strtab		[100]string
	Got		uint32
	Данамічна	uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, СтаронкаКаталогentry uint32) {

	памяцьmanager := TПамяцьmanager{}
	var тэкстПаказальнік Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderПамер := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderПамер*i]))

			var sectНазва []byte
			уключыць := uint32(strtab.shoffset + sectheader.shНазва)
			канец := уключыць
			for ; ; канец++ {
				if data[канец] == 0x0 || data[канец] == ' ' {
					break
				}
			}
			sectНазва = data[уключыць:канец]

			var sectЗначэнне []byte
			if sectheader.shТып != 8 {
				канецoffset := sectheader.shoffset + sectheader.shПамер
				if канецoffset < sectheader.shoffset || канецoffset > uint32(len(data)) {
					continue
				}
				sectЗначэнне = data[sectheader.shoffset:канецoffset]
			}

			if АднолькавыБайтаў(sectНазва, ([]byte)(".got.plt")) {
				console_2.MДрукаваць("[")
				console_2.MДрукаваць(sectНазва)
				console_2.MДрукаваць(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Друкаваць(self.Got)
				console_2.MДрукаваць("]")
			}
			if АднолькавыБайтаў(sectНазва, ([]byte)(".dynamic")) {
				console_2.MДрукаваць("[")
				console_2.MДрукаваць(sectНазва)
				console_2.MДрукаваць(":")
				данамічна := sectheader.shaddress
				self.Данамічна = данамічна
				console_2.MUnsignedinteger32Друкаваць(данамічна)
				console_2.MДрукаваць("]")
			}

			if sectheader.shaddress > 0x1000 {
				памер := sectheader.shПамер
				if sectheader.shТып == 8 {
					ZeroБлокуСтаронкаКаталог(sectheader.shaddress, памер, СтаронкаКаталогentry)
				} else {
					destination_2 := GetБайтаўfromПаказальнік(uintptr(sectheader.shaddress), int(памер), int(памер))
					ВызначанаБлокуСтаронкаКаталог(sectЗначэнне, destination_2, памер, СтаронкаКаталогentry)
				}
			}

			continue

			if АднолькавыБайтаў(sectНазва, ([]byte)(".text")) {
				console_2.MДрукаваць(".text")
				console_2.MДрукаваць("[")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shaddress)
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shoffset)
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shПамер)
				console_2.MДрукаваць("]")
				copy(self.тэкст[:sectheader.shПамер], sectЗначэнне[:sectheader.shПамер])
				self.тэкстlen = sectheader.shПамер
			}
			if АднолькавыБайтаў(sectНазва, ([]byte)(".rel.text")) {
				console_2.MДрукаваць(".rel.text")
				console_2.MДрукаваць("[")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shaddress)
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shПамер)
				console_2.MДрукаваць("]")
				for rt := uint32(0); rt < sectheader.shПамер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначэнне[rt*8]))
					self.relТэкст[rt].offset = offset
					self.relТэкст[rt].oaddress = *(*uint32)(Pointer(&self.тэкст[offset]))
					self.relТэкст[rt].нУМАР = *(*uint32)(Pointer(&sectЗначэнне[rt*8+4]))
					self.relТэкстlen++
				}
			}
			if АднолькавыБайтаў(sectНазва, ([]byte)(".dynsym")) {
				console_2.MДрукаваць(".dynsym")
				console_2.MДрукаваць("[")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shaddress)
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shПамер)
				console_2.MДрукаваць("]")
				for rt := uint32(0); rt < sectheader.shПамер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначэнне[rt*8]))
					self.relТэкст[rt].offset = offset
					self.relТэкст[rt].oaddress = *(*uint32)(Pointer(&self.тэкст[offset]))
					self.relТэкст[rt].нУМАР = *(*uint32)(Pointer(&sectЗначэнне[rt*8+4]))
					self.relТэкстlen++
				}
			}
			if АднолькавыБайтаў(sectНазва, ([]byte)(".dynstr")) {
				console_2.MДрукаваць(".dynstr")
				console_2.MДрукаваць("[")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shaddress)
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shПамер)
				console_2.MДрукаваць("]")
			}
			if АднолькавыБайтаў(sectНазва, ([]byte)(".strtab")) {
				console_2.MДрукаваць(".strtab")
				console_2.MДрукаваць("[")
				console_2.MUnsignedinteger32Друкаваць(sectheader.shaddress)
				console_2.MДрукаваць("]")
				rt := uint32(0)
				уключыць := uint32(0)

				for st := uint32(1); st < sectheader.shПамер; st++ {
					if sectЗначэнне[st] == 0x0 || sectЗначэнне[st] == ' ' {
						funcНазва := sectЗначэнне[уключыць+1 : st]
						console_2.MДрукаваць("+")
						console_2.MДрукаваць(funcНазва)
						self.strtab[rt] = БайтаўtoРадок(funcНазва)
						уключыць = st
						rt++
					}
				}

			}

		}

		console_2.MДрукаваць(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relТэкстlen; rt++ {
			console_2.MДрукаваць("[")
			console_2.MДрукаваць(([]byte)(self.strtab[rt]))
			console_2.MДрукаваць(":")
			console_2.MUnsignedinteger32Друкаваць(self.relТэкст[rt].нУМАР)
			console_2.MДрукаваць(":")

			console_2.MДрукаваць(([]byte)("]"))
		}
		console_2.MДрукаваць(([]byte)("------------>"))

		if тэкстПаказальнік != nil {
			памяцьmanager.Вольна(тэкстПаказальнік)
		}

	}

}
