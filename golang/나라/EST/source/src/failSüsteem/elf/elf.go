package elf

import . "unsafe"

import . "console"
import . "util"
import . "mälumanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eLiik		uint16
	emachine	uint16
	eVersioon	uint32
	ekirje		uint32
	ephoff		uint32
	eshoff		uint32
	eLipud		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNimi		uint32
	shLiik		uint32
	shLipud		uint32
	shaddress	uint32
	shoffset	uint32
	shSuurus	uint32
	shViit		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogrammheader struct {
	pLiik		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pLipud		uint32
	pJoondus	uint32
}
type Elf32Märkus struct {
	nnamesz	uint32
	ndescsz	uint32
	nLiik	uint32
}
type Elf32dyn struct {
	dSilt		uint32
	dvalKursor	uint32
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
	stNimi		uint32
	stVäärtus	uint32
	stSuurus	uint32
	stinfo		uint8
	stMuu		uint8
	stshndx		uint16
}
type relocationTekst struct {
	offset		uint32
	arv		uint32
	oaddress	uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dünaamiline	uint32
}

func (ise *Elf) Getkirje(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.ekirje
}

func (ise *Elf) Parse(data []byte, LehekülgKataloogkirje uint32) {

	mälumanager := TMälumanager{}
	var tekstKursor Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderSuurus := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderSuurus*i]))

			var sectNimi []byte
			käivita := uint32(strtab.shoffset + sectheader.shNimi)
			lõpp := käivita
			for ; ; lõpp++ {
				if data[lõpp] == 0x0 || data[lõpp] == ' ' {
					break
				}
			}
			sectNimi = data[käivita:lõpp]

			var sectVäärtus []byte
			if sectheader.shLiik != 8 {
				lõppoffset := sectheader.shoffset + sectheader.shSuurus
				if lõppoffset < sectheader.shoffset || lõppoffset > uint32(len(data)) {
					continue
				}
				sectVäärtus = data[sectheader.shoffset:lõppoffset]
			}

			if Võrdnebaiti(sectNimi, ([]byte)(".got.plt")) {
				console_2.MPrindi("[")
				console_2.MPrindi(sectNimi)
				console_2.MPrindi(":")
				ise.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Prindi(ise.Got)
				console_2.MPrindi("]")
			}
			if Võrdnebaiti(sectNimi, ([]byte)(".dynamic")) {
				console_2.MPrindi("[")
				console_2.MPrindi(sectNimi)
				console_2.MPrindi(":")
				dünaamiline := sectheader.shaddress
				ise.Dünaamiline = dünaamiline
				console_2.MUnsignedinteger32Prindi(dünaamiline)
				console_2.MPrindi("]")
			}

			if sectheader.shaddress > 0x1000 {
				suurus := sectheader.shSuurus
				if sectheader.shLiik == 8 {
					ZeroKastSisseLehekülgKataloog(sectheader.shaddress, suurus, LehekülgKataloogkirje)
				} else {
					sihtfail_2 := GetbaitifromKursor(uintptr(sectheader.shaddress), int(suurus), int(suurus))
					MääraKastSisseLehekülgKataloog(sectVäärtus, sihtfail_2, suurus, LehekülgKataloogkirje)
				}
			}

			continue

			if Võrdnebaiti(sectNimi, ([]byte)(".text")) {
				console_2.MPrindi(".text")
				console_2.MPrindi("[")
				console_2.MUnsignedinteger32Prindi(sectheader.shaddress)
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(sectheader.shoffset)
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(sectheader.shSuurus)
				console_2.MPrindi("]")
				copy(ise.tekst[:sectheader.shSuurus], sectVäärtus[:sectheader.shSuurus])
				ise.tekstlen = sectheader.shSuurus
			}
			if Võrdnebaiti(sectNimi, ([]byte)(".rel.text")) {
				console_2.MPrindi(".rel.text")
				console_2.MPrindi("[")
				console_2.MUnsignedinteger32Prindi(sectheader.shaddress)
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(sectheader.shSuurus)
				console_2.MPrindi("]")
				for rt := uint32(0); rt < sectheader.shSuurus/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVäärtus[rt*8]))
					ise.relTekst[rt].offset = offset
					ise.relTekst[rt].oaddress = *(*uint32)(Pointer(&ise.tekst[offset]))
					ise.relTekst[rt].arv = *(*uint32)(Pointer(&sectVäärtus[rt*8+4]))
					ise.relTekstlen++
				}
			}
			if Võrdnebaiti(sectNimi, ([]byte)(".dynsym")) {
				console_2.MPrindi(".dynsym")
				console_2.MPrindi("[")
				console_2.MUnsignedinteger32Prindi(sectheader.shaddress)
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(sectheader.shSuurus)
				console_2.MPrindi("]")
				for rt := uint32(0); rt < sectheader.shSuurus/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVäärtus[rt*8]))
					ise.relTekst[rt].offset = offset
					ise.relTekst[rt].oaddress = *(*uint32)(Pointer(&ise.tekst[offset]))
					ise.relTekst[rt].arv = *(*uint32)(Pointer(&sectVäärtus[rt*8+4]))
					ise.relTekstlen++
				}
			}
			if Võrdnebaiti(sectNimi, ([]byte)(".dynstr")) {
				console_2.MPrindi(".dynstr")
				console_2.MPrindi("[")
				console_2.MUnsignedinteger32Prindi(sectheader.shaddress)
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(sectheader.shSuurus)
				console_2.MPrindi("]")
			}
			if Võrdnebaiti(sectNimi, ([]byte)(".strtab")) {
				console_2.MPrindi(".strtab")
				console_2.MPrindi("[")
				console_2.MUnsignedinteger32Prindi(sectheader.shaddress)
				console_2.MPrindi("]")
				rt := uint32(0)
				käivita := uint32(0)

				for st := uint32(1); st < sectheader.shSuurus; st++ {
					if sectVäärtus[st] == 0x0 || sectVäärtus[st] == ' ' {
						funcNimi := sectVäärtus[käivita+1 : st]
						console_2.MPrindi("+")
						console_2.MPrindi(funcNimi)
						ise.strtab[rt] = Baititostring(funcNimi)
						käivita = st
						rt++
					}
				}

			}

		}

		console_2.MPrindi(([]byte)("<------------"))
		for rt := uint32(0); rt < ise.relTekstlen; rt++ {
			console_2.MPrindi("[")
			console_2.MPrindi(([]byte)(ise.strtab[rt]))
			console_2.MPrindi(":")
			console_2.MUnsignedinteger32Prindi(ise.relTekst[rt].arv)
			console_2.MPrindi(":")

			console_2.MPrindi(([]byte)("]"))
		}
		console_2.MPrindi(([]byte)("------------>"))

		if tekstKursor != nil {
			mälumanager.Vaba(tekstKursor)
		}

	}

}
