/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package formato_eseguibile_e_collegabile

import . "unsafe"

import . "console"
import . "util"
import . "memoriamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTipo		uint16
	emachine	uint16
	eVersione	uint32
	evoce		uint32
	ephoff		uint32
	eshoff		uint32
	eFlag		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNome		uint32
	shTipo		uint32
	shFlag		uint32
	shaddress	uint32
	shoffset	uint32
	shDimensione	uint32
	shCollegamento	uint32
	shInformazioni	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogrammaheader struct {
	pTipo		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pFlag		uint32
	pAllineamento	uint32
}
type Elf32Nota struct {
	nnamesz	uint32
	ndescsz	uint32
	nTipo	uint32
}
type Elf32dyn struct {
	dEtichetta	uint32
	dvalPuntatore	uint32
}
type Elf32rel struct {
	roffset		uint32
	rInformazioni	uint32
}
type Elf32rela struct {
	roffset		uint32
	rInformazioni	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNome		uint32
	stValore	uint32
	stDimensione	uint32
	stInformazioni	uint8
	stAltro		uint8
	stshndx		uint16
}
type relocationTesto struct {
	offset		uint32
	numero		uint32
	oaddress	uint32
}
type Elf struct {
	testo		[]byte
	testolen	uint32
	relTesto	[100]relocationTesto
	relTestolen	uint32
	strtab		[100]string
	Got		uint32
	Dinamico	uint32
}

func (séstesso *Elf) Getvoce(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.evoce
}

func (séstesso *Elf) Parse(data []byte, PAGINACartellavoce uint32) {

	memoriamanager := TMemoriamanager{}
	var testoPuntatore Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderDimensione := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderDimensione*i]))

			var sectNome []byte
			avvia := uint32(strtab.shoffset + sectheader.shNome)
			fine := avvia
			for ; ; fine++ {
				if data[fine] == 0x0 || data[fine] == ' ' {
					break
				}
			}
			sectNome = data[avvia:fine]

			var sectValore []byte
			if sectheader.shTipo != 8 {
				fineoffset := sectheader.shoffset + sectheader.shDimensione
				if fineoffset < sectheader.shoffset || fineoffset > uint32(len(data)) {
					continue
				}
				sectValore = data[sectheader.shoffset:fineoffset]
			}

			if UgualeByte(sectNome, ([]byte)(".got.plt")) {
				console_2.MStampa("[")
				console_2.MStampa(sectNome)
				console_2.MStampa(":")
				séstesso.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Stampa(séstesso.Got)
				console_2.MStampa("]")
			}
			if UgualeByte(sectNome, ([]byte)(".dynamic")) {
				console_2.MStampa("[")
				console_2.MStampa(sectNome)
				console_2.MStampa(":")
				dinamico := sectheader.shaddress
				séstesso.Dinamico = dinamico
				console_2.MUnsignedinteger32Stampa(dinamico)
				console_2.MStampa("]")
			}

			if sectheader.shaddress > 0x1000 {
				dimensione := sectheader.shDimensione
				if sectheader.shTipo == 8 {
					ZeroBloccoIngressoPAGINACartella(sectheader.shaddress, dimensione, PAGINACartellavoce)
				} else {
					destinazione_2 := GetBytefromPuntatore(uintptr(sectheader.shaddress), int(dimensione), int(dimensione))
					ImpostaBloccoIngressoPAGINACartella(sectValore, destinazione_2, dimensione, PAGINACartellavoce)
				}
			}

			continue

			if UgualeByte(sectNome, ([]byte)(".text")) {
				console_2.MStampa(".text")
				console_2.MStampa("[")
				console_2.MUnsignedinteger32Stampa(sectheader.shaddress)
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(sectheader.shoffset)
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(sectheader.shDimensione)
				console_2.MStampa("]")
				copy(séstesso.testo[:sectheader.shDimensione], sectValore[:sectheader.shDimensione])
				séstesso.testolen = sectheader.shDimensione
			}
			if UgualeByte(sectNome, ([]byte)(".rel.text")) {
				console_2.MStampa(".rel.text")
				console_2.MStampa("[")
				console_2.MUnsignedinteger32Stampa(sectheader.shaddress)
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(sectheader.shDimensione)
				console_2.MStampa("]")
				for rt := uint32(0); rt < sectheader.shDimensione/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValore[rt*8]))
					séstesso.relTesto[rt].offset = offset
					séstesso.relTesto[rt].oaddress = *(*uint32)(Pointer(&séstesso.testo[offset]))
					séstesso.relTesto[rt].numero = *(*uint32)(Pointer(&sectValore[rt*8+4]))
					séstesso.relTestolen++
				}
			}
			if UgualeByte(sectNome, ([]byte)(".dynsym")) {
				console_2.MStampa(".dynsym")
				console_2.MStampa("[")
				console_2.MUnsignedinteger32Stampa(sectheader.shaddress)
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(sectheader.shDimensione)
				console_2.MStampa("]")
				for rt := uint32(0); rt < sectheader.shDimensione/8; rt++ {
					offset := *(*uint32)(Pointer(&sectValore[rt*8]))
					séstesso.relTesto[rt].offset = offset
					séstesso.relTesto[rt].oaddress = *(*uint32)(Pointer(&séstesso.testo[offset]))
					séstesso.relTesto[rt].numero = *(*uint32)(Pointer(&sectValore[rt*8+4]))
					séstesso.relTestolen++
				}
			}
			if UgualeByte(sectNome, ([]byte)(".dynstr")) {
				console_2.MStampa(".dynstr")
				console_2.MStampa("[")
				console_2.MUnsignedinteger32Stampa(sectheader.shaddress)
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(sectheader.shDimensione)
				console_2.MStampa("]")
			}
			if UgualeByte(sectNome, ([]byte)(".strtab")) {
				console_2.MStampa(".strtab")
				console_2.MStampa("[")
				console_2.MUnsignedinteger32Stampa(sectheader.shaddress)
				console_2.MStampa("]")
				rt := uint32(0)
				avvia := uint32(0)

				for st := uint32(1); st < sectheader.shDimensione; st++ {
					if sectValore[st] == 0x0 || sectValore[st] == ' ' {
						funcNome := sectValore[avvia+1 : st]
						console_2.MStampa("+")
						console_2.MStampa(funcNome)
						séstesso.strtab[rt] = BytetoStringa(funcNome)
						avvia = st
						rt++
					}
				}

			}

		}

		console_2.MStampa(([]byte)("<------------"))
		for rt := uint32(0); rt < séstesso.relTestolen; rt++ {
			console_2.MStampa("[")
			console_2.MStampa(([]byte)(séstesso.strtab[rt]))
			console_2.MStampa(":")
			console_2.MUnsignedinteger32Stampa(séstesso.relTesto[rt].numero)
			console_2.MStampa(":")

			console_2.MStampa(([]byte)("]"))
		}
		console_2.MStampa(([]byte)("------------>"))

		if testoPuntatore != nil {
			memoriamanager.Libero(testoPuntatore)
		}

	}

}
