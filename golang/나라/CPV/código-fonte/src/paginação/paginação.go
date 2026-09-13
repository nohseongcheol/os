package paginação

import unsafe "unsafe"
import . "interrupção"
import . "memóriagestor"
import . "utilitário"

type Páginadiretóriopontodeentrada_2 uintptr

const (
	PáginaPresente		uint32	= 0x001
	Páginawritable		uint32	= 0x002
	Páginautilizador	uint32	= 0x004
	Páginaquadro		uint32	= 0xFFFFF000
	Páginacow		uint32	= 0x200
)

func ConjuntooctetoatEndereço(x byte, endereço uint32)
func Conjuntounsignedinteger8atEndereço(x uint8, endereço uint32)
func Conjuntounsignedinteger32atEndereço(x uint32, endereço uint32)

func getcr2() uint32

func conjuntocr3(diretório_de_páginas uint32)
func getcr3() uint32

type Paginação struct {
	TInterrupçãohandler
}
type Tcowquadrogestor struct {
	mem		*TMemóriagestor
	refs		[]uint16
	quadroContar	uint32
}

var (
	Páginadiretóriopontodeentrada	uintptr
	PáginaTabelapontodeentrada	uint32
	pdelen				uint32
	virtlen				uint32
	cowquadrogestor			Tcowquadrogestor
)

func (próprio *Tcowquadrogestor) Init(mem *TMemóriagestor, quadroContar uint32) bool {
	próprio.mem = mem
	próprio.quadroContar = quadroContar
	referencebytes := quadroContar * uint32(unsafe.Sizeof(uint16(0)))
	referencePonteiro := mem.Alocar_memória(referencebytes)
	if referencePonteiro == nil {
		próprio.refs = nil
		próprio.quadroContar = 0
		return false
	}
	próprio.refs = (*[1 << 28]uint16)(referencePonteiro)[:quadroContar:quadroContar]
	for i := uint32(0); i < quadroContar; i++ {
		próprio.refs[i] = 0
	}
	return true
}

func (próprio *Tcowquadrogestor) Reference(quadro uint32) uint16 {
	idx := quadro >> 12
	if idx >= próprio.quadroContar || próprio.refs == nil {
		return 0
	}
	return próprio.refs[idx]
}

func (próprio *Tcowquadrogestor) Increment(quadro uint32) {
	idx := quadro >> 12
	if idx >= próprio.quadroContar || próprio.refs == nil {
		return
	}
	if próprio.refs[idx] == 0 {
		próprio.refs[idx] = 2
	} else {
		próprio.refs[idx]++
	}
}

func (próprio *Tcowquadrogestor) Decrement(quadro uint32) {
	idx := quadro >> 12
	if idx >= próprio.quadroContar || próprio.refs == nil || próprio.refs[idx] == 0 {
		return
	}
	próprio.refs[idx]--
}

func (próprio *Paginação) Init(páginadiretóriopontodeentrada uintptr, páginaTabelapontodeentrada uint32, memóriagestor *TMemóriagestor) {

	Páginadiretóriopontodeentrada = páginadiretóriopontodeentrada
	PáginaTabelapontodeentrada = páginaTabelapontodeentrada

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowquadrogestor.Init(memóriagestor, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			endereçoPonteiro, _ := memóriagestor.Alignedmalloc(0x1000)
			if endereçoPonteiro == nil {
				return
			}
			endereço := uint32(uintptr(endereçoPonteiro))

			Conjuntounsignedinteger32atEndereço(endereço|0x87, uint32(páginadiretóriopontodeentrada)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Conjuntounsignedinteger32atEndereço((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, endereço+pte*4)
			}
		}
		páginadiretóriopontodeentrada = páginadiretóriopontodeentrada + 0x1000
	}

}
func (próprio *Paginação) Sharedmemóriaregion() {

	páginadiretóriopontodeentrada := Páginadiretóriopontodeentrada
	kpáginadiretóriopontodeentrada := Páginadiretóriopontodeentrada

	for i := uint32(1); i <= virtlen; i++ {

		páginadiretóriopontodeentrada = páginadiretóriopontodeentrada + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValor(uint32(kpáginadiretóriopontodeentrada) + pde*4)
			v = (v & 0xFFFFF000)
			Conjuntounsignedinteger32atEndereço(v|0x87, uint32(páginadiretóriopontodeentrada)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValor(uint32(kpáginadiretóriopontodeentrada) + pde*4)
			v = (v & 0xFFFFF000)
			Conjuntounsignedinteger32atEndereço(v|0x87, uint32(páginadiretóriopontodeentrada)+pde*4)

		}

	}
}
func (próprio *Paginação) Páginafalha(gestor *TInterrupçãogestor) {
	interrupçãohandler = manípulopaginaçãointerrupção

	var endereço uintptr
	endereço = uintptr(unsafe.Pointer(&interrupçãohandler))
	próprio.TInterrupçãohandler.Init(0xE, uintptr(unsafe.Pointer(gestor)), endereço)
}

var interrupçãohandler func(uint32) uint32

func manípulopaginaçãointerrupção(esp uint32) uint32 {
	if Resolvercopiaraoescreverfalha() {
		return esp
	}
	return Manípulofatalinterrupçãoquadro(esp, 0x0E)
}

func CloneEndereçoEspaçocow(origempáginadiretório uint32) uint32 {
	if Ativomemóriagestor == nil || origempáginadiretório == 0 {
		return 0
	}
	destinoPonteiro, _ := Ativomemóriagestor.Alignedmalloc(0x1000)
	if destinoPonteiro == nil {
		return 0
	}
	destinopáginadiretório := uint32(uintptr(destinoPonteiro))
	for i := uint32(0); i < 1024; i++ {
		Conjuntounsignedinteger32atEndereço(0, destinopáginadiretório+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		origempdeEndereço := origempáginadiretório + pde*4
		origempde := GetValor(origempdeEndereço)
		if (origempde & PáginaPresente) == 0 {
			continue
		}
		if issharedpde(pde) {
			Conjuntounsignedinteger32atEndereço(origempde, destinopáginadiretório+pde*4)
			continue
		}

		destinoptPonteiro, _ := Ativomemóriagestor.Alignedmalloc(0x1000)
		if destinoptPonteiro == nil {
			continue
		}
		origempt := origempde & Páginaquadro
		destinopt := uint32(uintptr(destinoptPonteiro))
		Conjuntounsignedinteger32atEndereço((destinopt | (origempde & 0xFFF)), destinopáginadiretório+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteEndereço := origempt + pte*4
			pontodeentrada := GetValor(pteEndereço)
			if (pontodeentrada & PáginaPresente) != 0 {
				if (pontodeentrada & Páginawritable) != 0 {
					pontodeentrada = (pontodeentrada &^ Páginawritable) | Páginacow
					Conjuntounsignedinteger32atEndereço(pontodeentrada, pteEndereço)
					cowquadrogestor.Increment(pontodeentrada & Páginaquadro)
				} else if (pontodeentrada & Páginacow) != 0 {
					cowquadrogestor.Increment(pontodeentrada & Páginaquadro)
				}
			}
			Conjuntounsignedinteger32atEndereço(pontodeentrada, destinopt+pte*4)
		}
	}
	recarregarcr3()
	return destinopáginadiretório
}

func Resolvercopiaraoescreverfalha() bool {
	if Ativomemóriagestor == nil {
		return false
	}
	falhaEndereço := getcr2()
	diretório_de_páginas := getcr3()
	pdeEndereço := diretório_de_páginas + ((falhaEndereço>>22)&0x3FF)*4
	pde := GetValor(pdeEndereço)
	if (pde & PáginaPresente) == 0 {
		return false
	}
	pt := pde & Páginaquadro
	pteEndereço := pt + ((falhaEndereço>>12)&0x3FF)*4
	pte := GetValor(pteEndereço)
	if (pte&Páginacow) == 0 || (pte&PáginaPresente) == 0 {
		return false
	}
	oldquadro := pte & Páginaquadro
	if cowquadrogestor.Reference(oldquadro) <= 1 {
		Conjuntounsignedinteger32atEndereço((pte|Páginawritable)&^Páginacow, pteEndereço)
		recarregarcr3()
		return true
	}

	novoPonteiro, _ := Ativomemóriagestor.Alignedmalloc(0x1000)
	if novoPonteiro == nil {
		return false
	}
	novoquadro := uint32(uintptr(novoPonteiro)) & Páginaquadro

	origem_2 := GetbytesdePonteiro(uintptr(falhaEndereço&Páginaquadro), 0x1000, 0x1000)
	destino_2 := GetbytesdePonteiro(uintptr(novoquadro), 0x1000, 0x1000)
	copy(destino_2, origem_2)
	cowquadrogestor.Decrement(oldquadro)
	Conjuntounsignedinteger32atEndereço((novoquadro|(pte&0xFFF)|Páginawritable)&^Páginacow, pteEndereço)
	recarregarcr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func recarregarcr3() {
	cr3 := getcr3()
	conjuntocr3(cr3)
}

func ConjuntooctetoEntradapáginadiretório(x byte, endereço uint32, diretório_de_páginas uint32) {
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	ConjuntooctetoatEndereço(x, endereço)
	conjuntocr3(oldcr3)
}

func ConjuntoBlocoEntradapáginadiretório(origem_2 []byte, destino_2 []byte, tamanho uint32, diretório_de_páginas uint32) {
	if tamanho == 0 || diretório_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	makeIntervaloPrivadowritableAtual(diretório_de_páginas, uint32(uintptr(unsafe.Pointer(&destino_2[0]))), tamanho)

	for i := uint32(0); i < tamanho; i++ {
		destino_2[i] = origem_2[i]
	}
	conjuntocr3(oldcr3)
}

func ZeroBlocoEntradapáginadiretório(endereço uint32, tamanho uint32, diretório_de_páginas uint32) {
	if tamanho == 0 || diretório_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	makeIntervaloPrivadowritableAtual(diretório_de_páginas, endereço, tamanho)
	destino_2 := GetbytesdePonteiro(uintptr(endereço), int(tamanho), int(tamanho))
	for i := uint32(0); i < tamanho; i++ {
		destino_2[i] = 0
	}
	conjuntocr3(oldcr3)
}

func makepáginaPrivadowritableAtual(diretório_de_páginas uint32, virtualEndereço uint32) bool {
	pde := GetValor(diretório_de_páginas + ((virtualEndereço>>22)&0x3FF)*4)
	if (pde & PáginaPresente) == 0 {
		return false
	}
	pteEndereço := (pde & Páginaquadro) + ((virtualEndereço>>12)&0x3FF)*4
	pte := GetValor(pteEndereço)
	if (pte & PáginaPresente) == 0 {
		return false
	}
	if (pte & Páginacow) == 0 {
		return (pte & Páginawritable) != 0
	}
	if Ativomemóriagestor == nil {
		return false
	}
	novoPonteiro, _ := Ativomemóriagestor.Alignedmalloc(0x1000)
	if novoPonteiro == nil {
		return false
	}
	novoquadro := uint32(uintptr(novoPonteiro)) & Páginaquadro
	origem_2 := GetbytesdePonteiro(uintptr(virtualEndereço&Páginaquadro), 0x1000, 0x1000)
	destino_2 := GetbytesdePonteiro(uintptr(novoquadro), 0x1000, 0x1000)
	copy(destino_2, origem_2)
	cowquadrogestor.Decrement(pte & Páginaquadro)
	Conjuntounsignedinteger32atEndereço((novoquadro|(pte&0xFFF)|Páginawritable)&^Páginacow, pteEndereço)
	// Publish the new physical frame before writing through its virtual address.
	recarregarcr3()
	return true
}

func makeIntervaloPrivadowritableAtual(diretório_de_páginas uint32, endereço uint32, tamanho uint32) bool {
	if tamanho == 0 {
		return true
	}
	última := endereço + tamanho - 1
	if última < endereço {
		return false
	}
	for página := endereço & Páginaquadro; ; página += 0x1000 {
		if !makepáginaPrivadowritableAtual(diretório_de_páginas, página) {
			return false
		}
		if página == (última & Páginaquadro) {
			break
		}
	}
	return true
}

func MakeIntervaloPrivadowritable(diretório_de_páginas uint32, endereço uint32, tamanho uint32) bool {
	if diretório_de_páginas == 0 {
		return false
	}
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	aceitar := makeIntervaloPrivadowritableAtual(diretório_de_páginas, endereço, tamanho)
	conjuntocr3(oldcr3)
	return aceitar
}

func Conjuntounsignedinteger32Entradapáginadiretório(x uint32, endereço uint32, diretório_de_páginas uint32) {
	if diretório_de_páginas == 0 {
		return
	}
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	Conjuntounsignedinteger32atEndereço(x, endereço)
	conjuntocr3(oldcr3)
}

func GetValor(endereço uint32) uint32 {
	var orgValor uint32 = *(*uint32)(unsafe.Pointer(uintptr(endereço)))
	return orgValor
}
func GetValorEntradapáginadiretório(endereço uint32, diretório_de_páginas uint32) uint32 {
	if diretório_de_páginas == 0 {
		return 0
	}
	oldcr3 := getcr3()
	conjuntocr3(diretório_de_páginas)
	v := GetValor(endereço)
	conjuntocr3(oldcr3)
	return v
}

var v uint32 = 0

func CopiarpáginaquadroBloco(xpáginadiretório uint32, ypáginadiretório uint32, vEndereço uint32) {
	if xpáginadiretório == 0 || ypáginadiretório == 0 {
		return
	}
	oldcr3 := getcr3()
	conjuntocr3(xpáginadiretório)
	v = GetValor(vEndereço)
	Conjuntounsignedinteger32Entradapáginadiretório(v, vEndereço, ypáginadiretório)

	conjuntocr3(oldcr3)
}
