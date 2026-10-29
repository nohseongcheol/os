/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package suoritettava_ja_linkitettävä_muoto

import . "unsafe"

import . "konsoli"
import . "util"
import . "muistimanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTyyppi		uint16
	emachine	uint16
	eVersio		uint32
	ehakusana	uint32
	ephoff		uint32
	eshoff		uint32
	eLiput		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNimi		uint32
	shTyyppi	uint32
	shLiput		uint32
	shaddress	uint32
	shoffset	uint32
	shKoko		uint32
	shLinkki	uint32
	shTieto		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfohjelmaheader struct {
	pTyyppi	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pLiput	uint32
	pTasaus	uint32
}
type Elf32Huomautus struct {
	nnamesz	uint32
	ndescsz	uint32
	nTyyppi	uint32
}
type Elf32dyn struct {
	dTunniste	uint32
	dvalOsoitin	uint32
}
type Elf32rel struct {
	roffset	uint32
	rTieto	uint32
}
type Elf32rela struct {
	roffset	uint32
	rTieto	uint32
	raddend	uint32
}
type Elf32sym struct {
	stNimi	uint32
	stArvo	uint32
	stKoko	uint32
	stTieto	uint8
	stMuu	uint8
	stshndx	uint16
}
type relocationTeksti struct {
	offset		uint32
	numero		uint32
	oaddress	uint32
}
type Elf struct {
	teksti		[]byte
	tekstilen	uint32
	relTeksti	[100]relocationTeksti
	relTekstilen	uint32
	strtab		[100]string
	Got		uint32
	Dynaaminen	uint32
}

func (itse *Elf) Gethakusana(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.ehakusana
}

func (itse *Elf) Parse(data []byte, SivuKansiohakusana uint32) {

	muistimanager := TMuistimanager{}
	var tekstiOsoitin Pointer = nil

	var konsoli_2 = TKonsoli{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderKoko := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderKoko*i]))

			var sectNimi []byte
			käynnistä := uint32(strtab.shoffset + sectheader.shNimi)
			loppuajankohta := käynnistä
			for ; ; loppuajankohta++ {
				if data[loppuajankohta] == 0x0 || data[loppuajankohta] == ' ' {
					break
				}
			}
			sectNimi = data[käynnistä:loppuajankohta]

			var sectArvo []byte
			if sectheader.shTyyppi != 8 {
				loppuajankohtaoffset := sectheader.shoffset + sectheader.shKoko
				if loppuajankohtaoffset < sectheader.shoffset || loppuajankohtaoffset > uint32(len(data)) {
					continue
				}
				sectArvo = data[sectheader.shoffset:loppuajankohtaoffset]
			}

			if Samankokoinentavua(sectNimi, ([]byte)(".got.plt")) {
				konsoli_2.MTulosta("[")
				konsoli_2.MTulosta(sectNimi)
				konsoli_2.MTulosta(":")
				itse.Got = sectheader.shaddress
				konsoli_2.MUnsignedinteger32Tulosta(itse.Got)
				konsoli_2.MTulosta("]")
			}
			if Samankokoinentavua(sectNimi, ([]byte)(".dynamic")) {
				konsoli_2.MTulosta("[")
				konsoli_2.MTulosta(sectNimi)
				konsoli_2.MTulosta(":")
				dynaaminen := sectheader.shaddress
				itse.Dynaaminen = dynaaminen
				konsoli_2.MUnsignedinteger32Tulosta(dynaaminen)
				konsoli_2.MTulosta("]")
			}

			if sectheader.shaddress > 0x1000 {
				koko := sectheader.shKoko
				if sectheader.shTyyppi == 8 {
					ZeroLohkoSaapuvaSivuKansio(sectheader.shaddress, koko, SivuKansiohakusana)
				} else {
					kohde_2 := GettavualähteestäOsoitin(uintptr(sectheader.shaddress), int(koko), int(koko))
					AsetaLohkoSaapuvaSivuKansio(sectArvo, kohde_2, koko, SivuKansiohakusana)
				}
			}

			continue

			if Samankokoinentavua(sectNimi, ([]byte)(".text")) {
				konsoli_2.MTulosta(".text")
				konsoli_2.MTulosta("[")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shaddress)
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shoffset)
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shKoko)
				konsoli_2.MTulosta("]")
				copy(itse.teksti[:sectheader.shKoko], sectArvo[:sectheader.shKoko])
				itse.tekstilen = sectheader.shKoko
			}
			if Samankokoinentavua(sectNimi, ([]byte)(".rel.text")) {
				konsoli_2.MTulosta(".rel.text")
				konsoli_2.MTulosta("[")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shaddress)
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shKoko)
				konsoli_2.MTulosta("]")
				for rt := uint32(0); rt < sectheader.shKoko/8; rt++ {
					offset := *(*uint32)(Pointer(&sectArvo[rt*8]))
					itse.relTeksti[rt].offset = offset
					itse.relTeksti[rt].oaddress = *(*uint32)(Pointer(&itse.teksti[offset]))
					itse.relTeksti[rt].numero = *(*uint32)(Pointer(&sectArvo[rt*8+4]))
					itse.relTekstilen++
				}
			}
			if Samankokoinentavua(sectNimi, ([]byte)(".dynsym")) {
				konsoli_2.MTulosta(".dynsym")
				konsoli_2.MTulosta("[")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shaddress)
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shKoko)
				konsoli_2.MTulosta("]")
				for rt := uint32(0); rt < sectheader.shKoko/8; rt++ {
					offset := *(*uint32)(Pointer(&sectArvo[rt*8]))
					itse.relTeksti[rt].offset = offset
					itse.relTeksti[rt].oaddress = *(*uint32)(Pointer(&itse.teksti[offset]))
					itse.relTeksti[rt].numero = *(*uint32)(Pointer(&sectArvo[rt*8+4]))
					itse.relTekstilen++
				}
			}
			if Samankokoinentavua(sectNimi, ([]byte)(".dynstr")) {
				konsoli_2.MTulosta(".dynstr")
				konsoli_2.MTulosta("[")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shaddress)
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shKoko)
				konsoli_2.MTulosta("]")
			}
			if Samankokoinentavua(sectNimi, ([]byte)(".strtab")) {
				konsoli_2.MTulosta(".strtab")
				konsoli_2.MTulosta("[")
				konsoli_2.MUnsignedinteger32Tulosta(sectheader.shaddress)
				konsoli_2.MTulosta("]")
				rt := uint32(0)
				käynnistä := uint32(0)

				for st := uint32(1); st < sectheader.shKoko; st++ {
					if sectArvo[st] == 0x0 || sectArvo[st] == ' ' {
						funcNimi := sectArvo[käynnistä+1 : st]
						konsoli_2.MTulosta("+")
						konsoli_2.MTulosta(funcNimi)
						itse.strtab[rt] = TavuatoMerkkijono(funcNimi)
						käynnistä = st
						rt++
					}
				}

			}

		}

		konsoli_2.MTulosta(([]byte)("<------------"))
		for rt := uint32(0); rt < itse.relTekstilen; rt++ {
			konsoli_2.MTulosta("[")
			konsoli_2.MTulosta(([]byte)(itse.strtab[rt]))
			konsoli_2.MTulosta(":")
			konsoli_2.MUnsignedinteger32Tulosta(itse.relTeksti[rt].numero)
			konsoli_2.MTulosta(":")

			konsoli_2.MTulosta(([]byte)("]"))
		}
		konsoli_2.MTulosta(([]byte)("------------>"))

		if tekstiOsoitin != nil {
			muistimanager.Vapaana(tekstiOsoitin)
		}

	}

}
