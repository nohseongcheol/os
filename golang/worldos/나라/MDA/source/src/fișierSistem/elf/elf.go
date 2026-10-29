/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "memoriemanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTip		uint16
	emachine	uint16
	eVersiune	uint32
	eînregistrare	uint32
	ephoff		uint32
	eshoff		uint32
	eIndicatori	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNume		uint32
	shTip		uint32
	shIndicatori	uint32
	shaddress	uint32
	shoffset	uint32
	shMărime	uint32
	shLegătură	uint32
	shDetaliat	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTip		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pIndicatori	uint32
	pAliniere	uint32
}
type Elf32Notă struct {
	nnamesz	uint32
	ndescsz	uint32
	nTip	uint32
}
type Elf32dyn struct {
	dEtichetă	uint32
	dvalIndicator	uint32
}
type Elf32rel struct {
	roffset		uint32
	rDetaliat	uint32
}
type Elf32rela struct {
	roffset		uint32
	rDetaliat	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNume		uint32
	stValoare	uint32
	stMărime	uint32
	stDetaliat	uint8
	stAltele	uint8
	stshndx		uint16
}
type relocationtext struct {
	offset		uint32
	număr		uint32
	oaddress	uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	reltext		[100]relocationtext
	reltextlen	uint32
	strtab		[100]string
	Got		uint32
	Dinamică	uint32
}

func (sine *Elf) Getînregistrare(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eînregistrare
}

func (sine *Elf) Parse(data []byte, PAGINĂDirectorînregistrare uint32) {

	memoriemanager := TMemoriemanager{}
	var textIndicator Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderMărime := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderMărime*i]))

			var sectNume []byte
			pornește := uint32(strtab.shoffset + sectheader.shNume)
			sfârșit := pornește
			for ; ; sfârșit++ {
				if data[sfârșit] == 0x0 || data[sfârșit] == ' ' {
					break
				}
			}
			sectNume = data[pornește:sfârșit]

			var sectValoare []byte
			if sectheader.shTip != 8 {
				sfârșitoffset := sectheader.shoffset + sectheader.shMărime
				if sfârșitoffset < sectheader.shoffset || sfârșitoffset > uint32(len(data)) {
					continue
				}
				sectValoare = data[sectheader.shoffset:sfârșitoffset]
			}

			if EqualOcteți(sectNume, ([]byte)(".got.plt")) {
				console_2.MTipărește("[")
				console_2.MTipărește(sectNume)
				console_2.MTipărește(":")
				sine.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Tipărește(sine.Got)
				console_2.MTipărește("]")
			}
			if EqualOcteți(sectNume, ([]byte)(".dynamic")) {
				console_2.MTipărește("[")
				console_2.MTipărește(sectNume)
				console_2.MTipărește(":")
				dinamică := sectheader.shaddress
				sine.Dinamică = dinamică
				console_2.MUnsignedinteger32Tipărește(dinamică)
				console_2.MTipărește("]")
			}

			if sectheader.shaddress > 0x1000 {
				mărime := sectheader.shMărime
				if sectheader.shTip == 8 {
					ZeroBlocIntrarePAGINĂDirector(sectheader.shaddress, mărime, PAGINĂDirectorînregistrare)
				} else {
					destinație_2 := GetOctețifromIndicator(uintptr(sectheader.shaddress), int(mărime), int(mărime))
					DefinitBlocIntrarePAGINĂDirector(sectValoare, destinație_2, mărime, PAGINĂDirectorînregistrare)
				}
			}

			continue

			if EqualOcteți(sectNume, ([]byte)(".text")) {
				console_2.MTipărește(".text")
				console_2.MTipărește("[")
				console_2.MUnsignedinteger32Tipărește(sectheader.shaddress)
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(sectheader.shoffset)
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(sectheader.shMărime)
				console_2.MTipărește("]")
				copy(sine.text[:sectheader.shMărime], sectValoare[:sectheader.shMărime])
				sine.textlen = sectheader.shMărime
			}
			if EqualOcteți(sectNume, ([]byte)(".rel.text")) {
				console_2.MTipărește(".rel.text")
				console_2.MTipărește("[")
				console_2.MUnsignedinteger32Tipărește(sectheader.shaddress)
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(sectheader.shMărime)
				console_2.MTipărește("]")
				for rt := uint32(0); rt < sectheader.shMărime/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValoare[rt*8]))
					sine.reltext[rt].offset = offset
					sine.reltext[rt].oaddress = *(*uint32)(Pointer(&sine.text[offset]))
					sine.reltext[rt].număr = *(*uint32)(Pointer(&sectValoare[rt*8+4]))
					sine.reltextlen++
				}
			}
			if EqualOcteți(sectNume, ([]byte)(".dynsym")) {
				console_2.MTipărește(".dynsym")
				console_2.MTipărește("[")
				console_2.MUnsignedinteger32Tipărește(sectheader.shaddress)
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(sectheader.shMărime)
				console_2.MTipărește("]")
				for rt := uint32(0); rt < sectheader.shMărime/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValoare[rt*8]))
					sine.reltext[rt].offset = offset
					sine.reltext[rt].oaddress = *(*uint32)(Pointer(&sine.text[offset]))
					sine.reltext[rt].număr = *(*uint32)(Pointer(&sectValoare[rt*8+4]))
					sine.reltextlen++
				}
			}
			if EqualOcteți(sectNume, ([]byte)(".dynstr")) {
				console_2.MTipărește(".dynstr")
				console_2.MTipărește("[")
				console_2.MUnsignedinteger32Tipărește(sectheader.shaddress)
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(sectheader.shMărime)
				console_2.MTipărește("]")
			}
			if EqualOcteți(sectNume, ([]byte)(".strtab")) {
				console_2.MTipărește(".strtab")
				console_2.MTipărește("[")
				console_2.MUnsignedinteger32Tipărește(sectheader.shaddress)
				console_2.MTipărește("]")
				rt := uint32(0)
				pornește := uint32(0)

				for st := uint32(1); st < sectheader.shMărime; st++ {
					if sectValoare[st] == 0x0 || sectValoare[st] == ' ' {
						funcNume := sectValoare[pornește+1 : st]
						console_2.MTipărește("+")
						console_2.MTipărește(funcNume)
						sine.strtab[rt] = OctețitoȘir(funcNume)
						pornește = st
						rt++
					}
				}

			}

		}

		console_2.MTipărește(([]byte)("<------------"))
		for rt := uint32(0); rt < sine.reltextlen; rt++ {
			console_2.MTipărește("[")
			console_2.MTipărește(([]byte)(sine.strtab[rt]))
			console_2.MTipărește(":")
			console_2.MUnsignedinteger32Tipărește(sine.reltext[rt].număr)
			console_2.MTipărește(":")

			console_2.MTipărește(([]byte)("]"))
		}
		console_2.MTipărește(([]byte)("------------>"))

		if textIndicator != nil {
			memoriemanager.Liber(textIndicator)
		}

	}

}
