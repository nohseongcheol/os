/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package formato_ejecutable_y_enlazable

import . "unsafe"

import . "consola"
import . "utilidad"
import . "memoriagestor"
import . "paginación"

type Elfencabezado struct {
	eident		[16]byte
	etipo		uint16
	emachine	uint16
	eVersión	uint32
	eentrada	uint32
	ephoff		uint32
	eshoff		uint32
	eBanderas	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsecciónencabezado struct {
	shNombre		uint32
	shtipo			uint32
	shBanderas		uint32
	shDirección		uint32
	shDesplazamiento	uint32
	shTamaño		uint32
	shenlace		uint32
	shInformación		uint32
	shaddralign		uint32
	shentsize		uint32
}
type Elfprogramaencabezado struct {
	ptipo		uint32
	pDesplazamiento	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pBanderas	uint32
	pAlinear	uint32
}
type Elf32Nota struct {
	nnamesz	uint32
	ndescsz	uint32
	ntipo	uint32
}
type Elf32dyn struct {
	dEtiqueta	uint32
	dvalPuntero	uint32
}
type Elf32rel struct {
	rDesplazamiento	uint32
	rInformación	uint32
}
type Elf32rela struct {
	rDesplazamiento	uint32
	rInformación	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNombre	uint32
	stValor		uint32
	stTamaño	uint32
	stInformación	uint8
	stOtro		uint8
	stshndx		uint16
}
type relocationtexto struct {
	desplazamiento	uint32
	número		uint32
	oDirección	uint32
}
type Elf struct {
	texto		[]byte
	textolen	uint32
	reltexto	[100]relocationtexto
	reltextolen	uint32
	strtab		[100]string
	Got		uint32
	Dinámico	uint32
}

func (propio *Elf) Getentrada(datos []byte) uint32 {
	elfencabezado := (*Elfencabezado)(Pointer(&datos[0]))
	return elfencabezado.eentrada
}

func (propio *Elf) Parse(datos []byte, Páginadirectorioentrada uint32) {

	memoriagestor := TMemoriagestor{}
	var textoPuntero Pointer = nil

	var consola_2 = TConsola{}

	elfencabezado := (*Elfencabezado)(Pointer(&datos[0]))

	if elfencabezado.eshnum != 0 {
		strtab := (*Elfsecciónencabezado)(Pointer(&datos[elfencabezado.eshoff+uint32(elfencabezado.eshentsize*elfencabezado.eshstrndx)]))
		sectencabezadoTamaño := uint32(Sizeof(Elfsecciónencabezado{}))

		for i := uint32(0); i < uint32(elfencabezado.eshnum); i++ {
			sectencabezado := (*Elfsecciónencabezado)(Pointer(&datos[elfencabezado.eshoff+sectencabezadoTamaño*i]))

			var sectNombre []byte
			iniciar := uint32(strtab.shDesplazamiento + sectencabezado.shNombre)
			fin := iniciar
			for ; ; fin++ {
				if datos[fin] == 0x0 || datos[fin] == ' ' {
					break
				}
			}
			sectNombre = datos[iniciar:fin]

			var sectValor []byte
			if sectencabezado.shtipo != 8 {
				finDesplazamiento := sectencabezado.shDesplazamiento + sectencabezado.shTamaño
				if finDesplazamiento < sectencabezado.shDesplazamiento || finDesplazamiento > uint32(len(datos)) {
					continue
				}
				sectValor = datos[sectencabezado.shDesplazamiento:finDesplazamiento]
			}

			if Igualbytes(sectNombre, ([]byte)(".got.plt")) {
				consola_2.MImprimir("[")
				consola_2.MImprimir(sectNombre)
				consola_2.MImprimir(":")
				propio.Got = sectencabezado.shDirección
				consola_2.MUnsignedinteger32Imprimir(propio.Got)
				consola_2.MImprimir("]")
			}
			if Igualbytes(sectNombre, ([]byte)(".dynamic")) {
				consola_2.MImprimir("[")
				consola_2.MImprimir(sectNombre)
				consola_2.MImprimir(":")
				dinámico := sectencabezado.shDirección
				propio.Dinámico = dinámico
				consola_2.MUnsignedinteger32Imprimir(dinámico)
				consola_2.MImprimir("]")
			}

			if sectencabezado.shDirección > 0x1000 {
				tamaño := sectencabezado.shTamaño
				if sectencabezado.shtipo == 8 {
					CeroBloqueEntradapáginadirectorio(sectencabezado.shDirección, tamaño, Páginadirectorioentrada)
				} else {
					destino_2 := GetbytesdesdePuntero(uintptr(sectencabezado.shDirección), int(tamaño), int(tamaño))
					EstablecerBloqueEntradapáginadirectorio(sectValor, destino_2, tamaño, Páginadirectorioentrada)
				}
			}

			continue

			if Igualbytes(sectNombre, ([]byte)(".text")) {
				consola_2.MImprimir(".text")
				consola_2.MImprimir("[")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDirección)
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDesplazamiento)
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shTamaño)
				consola_2.MImprimir("]")
				copy(propio.texto[:sectencabezado.shTamaño], sectValor[:sectencabezado.shTamaño])
				propio.textolen = sectencabezado.shTamaño
			}
			if Igualbytes(sectNombre, ([]byte)(".rel.text")) {
				consola_2.MImprimir(".rel.text")
				consola_2.MImprimir("[")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDirección)
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shTamaño)
				consola_2.MImprimir("]")
				for rt := uint32(0); rt < sectencabezado.shTamaño/8; rt++ {
					desplazamiento := *(*uint32)(Pointer(&sectValor[rt*8]))
					propio.reltexto[rt].desplazamiento = desplazamiento
					propio.reltexto[rt].oDirección = *(*uint32)(Pointer(&propio.texto[desplazamiento]))
					propio.reltexto[rt].número = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					propio.reltextolen++
				}
			}
			if Igualbytes(sectNombre, ([]byte)(".dynsym")) {
				consola_2.MImprimir(".dynsym")
				consola_2.MImprimir("[")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDirección)
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shTamaño)
				consola_2.MImprimir("]")
				for rt := uint32(0); rt < sectencabezado.shTamaño/8; rt++ {
					desplazamiento := *(*uint32)(Pointer(&sectValor[rt*8]))
					propio.reltexto[rt].desplazamiento = desplazamiento
					propio.reltexto[rt].oDirección = *(*uint32)(Pointer(&propio.texto[desplazamiento]))
					propio.reltexto[rt].número = *(*uint32)(Pointer(&sectValor[rt*8+4]))
					propio.reltextolen++
				}
			}
			if Igualbytes(sectNombre, ([]byte)(".dynstr")) {
				consola_2.MImprimir(".dynstr")
				consola_2.MImprimir("[")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDirección)
				consola_2.MImprimir(":")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shTamaño)
				consola_2.MImprimir("]")
			}
			if Igualbytes(sectNombre, ([]byte)(".strtab")) {
				consola_2.MImprimir(".strtab")
				consola_2.MImprimir("[")
				consola_2.MUnsignedinteger32Imprimir(sectencabezado.shDirección)
				consola_2.MImprimir("]")
				rt := uint32(0)
				iniciar := uint32(0)

				for st := uint32(1); st < sectencabezado.shTamaño; st++ {
					if sectValor[st] == 0x0 || sectValor[st] == ' ' {
						funcNombre := sectValor[iniciar+1 : st]
						consola_2.MImprimir("+")
						consola_2.MImprimir(funcNombre)
						propio.strtab[rt] = BytestoCadena(funcNombre)
						iniciar = st
						rt++
					}
				}

			}

		}

		consola_2.MImprimir(([]byte)("<------------"))
		for rt := uint32(0); rt < propio.reltextolen; rt++ {
			consola_2.MImprimir("[")
			consola_2.MImprimir(([]byte)(propio.strtab[rt]))
			consola_2.MImprimir(":")
			consola_2.MUnsignedinteger32Imprimir(propio.reltexto[rt].número)
			consola_2.MImprimir(":")

			consola_2.MImprimir(([]byte)("]"))
		}
		consola_2.MImprimir(([]byte)("------------>"))

		if textoPuntero != nil {
			memoriagestor.Libre(textoPuntero)
		}

	}

}
