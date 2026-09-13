package formato_executável_e_ligável

import . "unsafe"
import . "console"

import mem "memóriagestor"

type Ligação struct {
	Dinâmico	uintptr
	Previous	*Ligação
	Seguinte	*Ligação
}
type Ligaçãomapa struct {
	First	*Ligação
	Última	*Ligação

	Tamanho_2	int

	mem	*mem.TMemóriagestor
}

func (próprio *Ligaçãomapa) Init(mem *mem.TMemóriagestor) {
	próprio.mem = mem
}
func (próprio *Ligaçãomapa) Clone() Ligaçãomapa {
	var ligaçãomapa Ligaçãomapa

	ligaçãomapa.Init(próprio.mem)

	Ligação := próprio.First

	for ; Ligação != nil; Ligação = Ligação.Seguinte {
		ligaçãomapa.Adicionar_ao_fim_da_lista(Ligação.Dinâmico)
	}
	return ligaçãomapa
}
func (próprio *Ligaçãomapa) Adicionar_ao_início_da_lista(Dinâmico uintptr) {
	novoligação := (*Ligação)(próprio.mem.Alocar_memória(uint32(Sizeof(Ligação{}))))
	novoligação.Dinâmico = Dinâmico
	novoligação.Seguinte = próprio.First
	próprio.First = novoligação
	próprio.Tamanho_2++

	if próprio.First.Seguinte == nil {
		próprio.Última = próprio.First
	}
}
func (próprio *Ligaçãomapa) Adicionar_ao_fim_da_lista(Dinâmico uintptr) {
	if Dinâmico == 0 {
		return
	}

	if próprio.Tamanho_2 == 0 {
		próprio.Adicionar_ao_início_da_lista(Dinâmico)
	} else {
		novoligação := (*Ligação)(próprio.mem.Alocar_memória(uint32(Sizeof(Ligação{}))))
		novoligação.Dinâmico = Dinâmico
		novoligação.Seguinte = nil
		próprio.Última.Seguinte = novoligação
		próprio.Última = novoligação
		próprio.Tamanho_2++
	}
}
func (próprio *Ligaçãomapa) Imprimir(x uint16, y uint16) {
	Ligação := próprio.First
	console_2 := TConsole{}
	console_2.MImprimirxy("linkmap : ", x, y)
	for ; Ligação != nil; Ligação = Ligação.Seguinte {
		console_2.MUnsignedinteger32Imprimir(uint32(Ligação.Dinâmico))
		console_2.MImprimir("+")

	}
}
