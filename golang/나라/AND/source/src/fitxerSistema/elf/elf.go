package elf

import . "unsafe"

import . "consola"
import . "util"
import . "memòriamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTipus		uint16
	emachine	uint16
	eVersió		uint32
	eentrada	uint32
	ephoff		uint32
	eshoff		uint32
	eSenyaladors	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNom		uint32
	shTipus		uint32
	shSenyaladors	uint32
	shAdreça	uint32
	shoffset	uint32
	shMida		uint32
	shEnllaç	uint32
	shInformació	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramaheader struct {
	pTipus		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pSenyaladors	uint32
	pAlinea		uint32
}
type Elf32Nota struct {
	nnamesz	uint32
	ndescsz	uint32
	nTipus	uint32
}
type Elf32dyn struct {
	dEtiqueta	uint32
	dvalPunter	uint32
}
type Elf32rel struct {
	roffset		uint32
	rInformació	uint32
}
type Elf32rela struct {
	roffset		uint32
	rInformació	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNom		uint32
	stValor		uint32
	stMida		uint32
	stInformació	uint8
	stAltres	uint8
	stshndx		uint16
}
type relocationtext struct {
	offset	uint32
	nombre	uint32
	oAdreça	uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	reltext		[100]relocationtext
	reltextlen	uint32
	strtab		[100]string
	Got		uint32
	Dinàmic		uint32
}

func (unmateix *Elf) Getentrada(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentrada
}

func (unmateix *Elf) Parse(data []byte, PàginaDirectorientrada uint32) {

	memòriamanager := TMemòriamanager{}
	var textPunter Pointer = nil

	var consola_2 = TConsola{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderMida := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderMida*i]))

			var sectNom []byte
			inicia := uint32(strtab.shoffset + sectheader.shNom)
			final := inicia
			for ; ; final++ {
				if data[final] == 0x0 || data[final] == ' ' {
					break
				}
			}
			sectNom = data[inicia:final]

			var sectValor []byte
			if sectheader.shTipus != 8 {
				finaloffset := sectheader.shoffset + sectheader.shMida
				if finaloffset < sectheader.shoffset || finaloffset > uint32(len(data)) {
					continue
				}
				sectValor = data[sectheader.shoffset:finaloffset]
			}

			if Igualbytes(sectNom, ([]byte)(".got.plt")) {
				consola_2.MImprimeix("[")
				consola_2.MImprimeix(sectNom)
				consola_2.MImprimeix(":")
				unmateix.Got = sectheader.shAdreça
				consola_2.MUnsignedinteger32Imprimeix(unmateix.Got)
				consola_2.MImprimeix("]")
			}
			if Igualbytes(sectNom, ([]byte)(".dynamic")) {
				consola_2.MImprimeix("[")
				consola_2.MImprimeix(sectNom)
				consola_2.MImprimeix(":")
				dinàmic := sectheader.shAdreça
				unmateix.Dinàmic = dinàmic
				consola_2.MUnsignedinteger32Imprimeix(dinàmic)
				consola_2.MImprimeix("]")
			}

			if sectheader.shAdreça > 0x1000 {
				mida := sectheader.shMida
				if sectheader.shTipus == 8 {
					ZeroBlocaPàginaDirectori(sectheader.shAdreça, mida, PàginaDirectorientrada)
				} else {
					destinació_2 := GetbytesdesdePunter(uintptr(sectheader.shAdreça), int(mida), int(mida))
					EstableixBlocaPàginaDirectori(sectValor, destinació_2, mida, PàginaDirectorientrada)
				}
			}

			continue

			if Igualbytes(sectNom, ([]byte)(".text")) {
				consola_2.MImprimeix(".text")
				consola_2.MImprimeix("[")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shAdreça)
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shoffset)
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shMida)
				consola_2.MImprimeix("]")
				copy(unmateix.text[:sectheader.shMida], sectValor[:sectheader.shMida])
				unmateix.textlen = sectheader.shMida
			}
			if Igualbytes(sectNom, ([]byte)(".rel.text")) {
				consola_2.MImprimeix(".rel.text")
				consola_2.MImprimeix("[")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shAdreça)
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shMida)
				consola_2.MImprimeix("]")
				for rt := uint32(0); rt < sectheader.shMida/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValor[rt*8]))
					unmateix.reltext[rt].offset = offset
					unmateix.reltext[rt].oAdreça = *(*uint32)(Pointer(&unmateix.text[offset]))
					unmateix.reltext[rt].nombre = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					unmateix.reltextlen++
				}
			}
			if Igualbytes(sectNom, ([]byte)(".dynsym")) {
				consola_2.MImprimeix(".dynsym")
				consola_2.MImprimeix("[")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shAdreça)
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shMida)
				consola_2.MImprimeix("]")
				for rt := uint32(0); rt < sectheader.shMida/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValor[rt*8]))
					unmateix.reltext[rt].offset = offset
					unmateix.reltext[rt].oAdreça = *(*uint32)(Pointer(&unmateix.text[offset]))
					unmateix.reltext[rt].nombre = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					unmateix.reltextlen++
				}
			}
			if Igualbytes(sectNom, ([]byte)(".dynstr")) {
				consola_2.MImprimeix(".dynstr")
				consola_2.MImprimeix("[")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shAdreça)
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shMida)
				consola_2.MImprimeix("]")
			}
			if Igualbytes(sectNom, ([]byte)(".strtab")) {
				consola_2.MImprimeix(".strtab")
				consola_2.MImprimeix("[")
				consola_2.MUnsignedinteger32Imprimeix(sectheader.shAdreça)
				consola_2.MImprimeix("]")
				rt := uint32(0)
				inicia := uint32(0)

				for st := uint32(1); st < sectheader.shMida; st++ {
					if sectValor[st] == 0x0 || sectValor[st] == ' ' {
						funcNom := sectValor[inicia+1 : st]
						consola_2.MImprimeix("+")
						consola_2.MImprimeix(funcNom)
						unmateix.strtab[rt] = BytestoCadena(funcNom)
						inicia = st
						rt++
					}
				}

			}

		}

		consola_2.MImprimeix(([]byte)("<------------"))
		for rt := uint32(0); rt < unmateix.reltextlen; rt++ {
			consola_2.MImprimeix("[")
			consola_2.MImprimeix(([]byte)(unmateix.strtab[rt]))
			consola_2.MImprimeix(":")
			consola_2.MUnsignedinteger32Imprimeix(unmateix.reltext[rt].nombre)
			consola_2.MImprimeix(":")

			consola_2.MImprimeix(([]byte)("]"))
		}
		consola_2.MImprimeix(([]byte)("------------>"))

		if textPunter != nil {
			memòriamanager.Lliure(textPunter)
		}

	}

}
