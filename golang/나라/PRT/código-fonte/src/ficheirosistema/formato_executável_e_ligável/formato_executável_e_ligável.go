/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package formato_executável_e_ligável

import . "unsafe"

import . "console"
import . "utilitário"
import . "memóriagestor"
import . "paginação"

type Elfcabeçalho struct {
	eident		[16]byte
	etipo		uint16
	emachine	uint16
	eVersão		uint32
	epontodeentrada	uint32
	ephoff		uint32
	eshoff		uint32
	eParâmetros	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsecçãocabeçalho struct {
	shNome		uint32
	shtipo		uint32
	shParâmetros	uint32
	shEndereço	uint32
	shDeslocamento	uint32
	shTamanho	uint32
	shligação	uint32
	shInformações	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramacabeçalho struct {
	ptipo		uint32
	pDeslocamento	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pParâmetros	uint32
	pAlinhamento	uint32
}
type Elf32Nota struct {
	nnamesz	uint32
	ndescsz	uint32
	ntipo	uint32
}
type Elf32dyn struct {
	dMarca		uint32
	dvalPonteiro	uint32
}
type Elf32rel struct {
	rDeslocamento	uint32
	rInformações	uint32
}
type Elf32rela struct {
	rDeslocamento	uint32
	rInformações	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNome		uint32
	stValor		uint32
	stTamanho	uint32
	stInformações	uint8
	stOutro		uint8
	stshndx		uint16
}
type relocationtexto struct {
	deslocamento	uint32
	número		uint32
	oEndereço	uint32
}
type Elf struct {
	texto		[]byte
	textolen	uint32
	reltexto	[100]relocationtexto
	reltextolen	uint32
	strtab		[100]string
	Got		uint32
	Dinâmico	uint32
}

func (próprio *Elf) Getpontodeentrada(dados []byte) uint32 {
	elfcabeçalho := (*Elfcabeçalho)(Pointer(&dados[0]))
	return elfcabeçalho.epontodeentrada
}

func (próprio *Elf) Parse(dados []byte, Páginadiretóriopontodeentrada uint32) {

	memóriagestor := TMemóriagestor{}
	var textoPonteiro Pointer = nil

	var console_2 = TConsole{}

	elfcabeçalho := (*Elfcabeçalho)(Pointer(&dados[0]))

	if elfcabeçalho.eshnum != 0 {
		strtab := (*Elfsecçãocabeçalho)(Pointer(&dados[elfcabeçalho.eshoff+uint32(elfcabeçalho.eshentsize*elfcabeçalho.eshstrndx)]))
		sectcabeçalhoTamanho := uint32(Sizeof(Elfsecçãocabeçalho{}))

		for i := uint32(0); i < uint32(elfcabeçalho.eshnum); i++ {
			sectcabeçalho := (*Elfsecçãocabeçalho)(Pointer(&dados[elfcabeçalho.eshoff+sectcabeçalhoTamanho*i]))

			var sectNome []byte
			iniciar := uint32(strtab.shDeslocamento + sectcabeçalho.shNome)
			fim := iniciar
			for ; ; fim++ {
				if dados[fim] == 0x0 || dados[fim] == ' ' {
					break
				}
			}
			sectNome = dados[iniciar:fim]

			var sectValor []byte
			if sectcabeçalho.shtipo != 8 {
				fimDeslocamento := sectcabeçalho.shDeslocamento + sectcabeçalho.shTamanho
				if fimDeslocamento < sectcabeçalho.shDeslocamento || fimDeslocamento > uint32(len(dados)) {
					continue
				}
				sectValor = dados[sectcabeçalho.shDeslocamento:fimDeslocamento]
			}

			if Igualbytes(sectNome, ([]byte)(".got.plt")) {
				console_2.MImprimir("[")
				console_2.MImprimir(sectNome)
				console_2.MImprimir(":")
				próprio.Got = sectcabeçalho.shEndereço
				console_2.MUnsignedinteger32Imprimir(próprio.Got)
				console_2.MImprimir("]")
			}
			if Igualbytes(sectNome, ([]byte)(".dynamic")) {
				console_2.MImprimir("[")
				console_2.MImprimir(sectNome)
				console_2.MImprimir(":")
				dinâmico := sectcabeçalho.shEndereço
				próprio.Dinâmico = dinâmico
				console_2.MUnsignedinteger32Imprimir(dinâmico)
				console_2.MImprimir("]")
			}

			if sectcabeçalho.shEndereço > 0x1000 {
				tamanho := sectcabeçalho.shTamanho
				if sectcabeçalho.shtipo == 8 {
					ZeroBlocoEntradapáginadiretório(sectcabeçalho.shEndereço, tamanho, Páginadiretóriopontodeentrada)
				} else {
					destino_2 := GetbytesdePonteiro(uintptr(sectcabeçalho.shEndereço), int(tamanho), int(tamanho))
					ConjuntoBlocoEntradapáginadiretório(sectValor, destino_2, tamanho, Páginadiretóriopontodeentrada)
				}
			}

			continue

			if Igualbytes(sectNome, ([]byte)(".text")) {
				console_2.MImprimir(".text")
				console_2.MImprimir("[")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shEndereço)
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shDeslocamento)
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shTamanho)
				console_2.MImprimir("]")
				copy(próprio.texto[:sectcabeçalho.shTamanho], sectValor[:sectcabeçalho.shTamanho])
				próprio.textolen = sectcabeçalho.shTamanho
			}
			if Igualbytes(sectNome, ([]byte)(".rel.text")) {
				console_2.MImprimir(".rel.text")
				console_2.MImprimir("[")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shEndereço)
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shTamanho)
				console_2.MImprimir("]")
				for rt := uint32(0); rt < sectcabeçalho.shTamanho/8; rt++ {
					deslocamento := *(*uint32)(Pointer(&sectValor[rt*8]))
					próprio.reltexto[rt].deslocamento = deslocamento
					próprio.reltexto[rt].oEndereço = *(*uint32)(Pointer(&próprio.texto[deslocamento]))
					próprio.reltexto[rt].número = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					próprio.reltextolen++
				}
			}
			if Igualbytes(sectNome, ([]byte)(".dynsym")) {
				console_2.MImprimir(".dynsym")
				console_2.MImprimir("[")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shEndereço)
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shTamanho)
				console_2.MImprimir("]")
				for rt := uint32(0); rt < sectcabeçalho.shTamanho/8; rt++ {
					deslocamento := *(*uint32)(Pointer(&sectValor[rt*8]))
					próprio.reltexto[rt].deslocamento = deslocamento
					próprio.reltexto[rt].oEndereço = *(*uint32)(Pointer(&próprio.texto[deslocamento]))
					próprio.reltexto[rt].número = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					próprio.reltextolen++
				}
			}
			if Igualbytes(sectNome, ([]byte)(".dynstr")) {
				console_2.MImprimir(".dynstr")
				console_2.MImprimir("[")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shEndereço)
				console_2.MImprimir(":")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shTamanho)
				console_2.MImprimir("]")
			}
			if Igualbytes(sectNome, ([]byte)(".strtab")) {
				console_2.MImprimir(".strtab")
				console_2.MImprimir("[")
				console_2.MUnsignedinteger32Imprimir(sectcabeçalho.shEndereço)
				console_2.MImprimir("]")
				rt := uint32(0)
				iniciar := uint32(0)

				for st := uint32(1); st < sectcabeçalho.shTamanho; st++ {
					if sectValor[st] == 0x0 || sectValor[st] == ' ' {
						funcNome := sectValor[iniciar+1 : st]
						console_2.MImprimir("+")
						console_2.MImprimir(funcNome)
						próprio.strtab[rt] = Bytesparalinha(funcNome)
						iniciar = st
						rt++
					}
				}

			}

		}

		console_2.MImprimir(([]byte)("<------------"))
		for rt := uint32(0); rt < próprio.reltextolen; rt++ {
			console_2.MImprimir("[")
			console_2.MImprimir(([]byte)(próprio.strtab[rt]))
			console_2.MImprimir(":")
			console_2.MUnsignedinteger32Imprimir(próprio.reltexto[rt].número)
			console_2.MImprimir(":")

			console_2.MImprimir(([]byte)("]"))
		}
		console_2.MImprimir(([]byte)("------------>"))

		if textoPonteiro != nil {
			memóriagestor.Livre(textoPonteiro)
		}

	}

}
