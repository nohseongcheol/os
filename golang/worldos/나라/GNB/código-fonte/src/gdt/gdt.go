/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segnúcleocode	uint32	= 0x08
	Segnúcleodados	uint32	= 0x10
	Segnúcleogs	uint32	= 0x18

	Segutilizadorcode	uint32	= 0x23
	Segutilizadordados	uint32	= 0x2B
	Segutilizadorgs		uint32	= 0x33
	SegtarefaEstado		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limiteBaixo_2		uint16
	baseBaixo_2		uint16
	baseAlto_2		uint8
	tipo_2			uint8
	parâmetrosLimiteAlto	uint8
	baseveryAlto		uint8
}

func (próprio_2 *TSegmentdescriptor) Init(base_2 uint32, limite_2 uint32, tipo_2 uint8, parâmetros_3 uint8) {

	próprio_2.baseBaixo_2 = uint16(base_2 & 0xFFFF)
	próprio_2.baseAlto_2 = uint8((base_2 >> 16) & 0xFF)
	próprio_2.baseveryAlto = uint8((base_2 >> 24) & 0xFF)

	próprio_2.limiteBaixo_2 = uint16(limite_2 & 0xFFFF)
	próprio_2.parâmetrosLimiteAlto = uint8((limite_2 >> 24) & 0x0F)
	próprio_2.parâmetrosLimiteAlto |= (parâmetros_3 & 0xF0)

	próprio_2.tipo_2 = tipo_2

}

type TShareddescriptorTabeladados struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var dados_2 TShareddescriptorTabeladados

type TShareddescriptorTabela struct {
}

func (próprio_2 *TShareddescriptorTabela) Init() {

	var gdtpontodeentrada TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtEndereço := uintptr(uint32(gdtdescriptor.GdtEndereçoBaixo) |
		uint32(gdtdescriptor.GdtEndereçoAlto)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtTamanho+1) / Sizeof(gdtpontodeentrada))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtEndereço,
	}))
	copy(dados_2.segmentdescriptor[:], oldgdt)

	dados_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	dados_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	dados_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destino_4 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseEndereço := (*uint32)(Pointer(&destino_4[2]))
	(*baseEndereço) = uint32(uintptr(Pointer(&dados_2)))

	tamanho_2 := (*uint16)(Pointer(&destino_4[0]))
	(*tamanho_2) = (uint16)((Sizeof(dados_2)))

	gdtfunc(uintptr(Pointer(&destino_4)))

	terminal := new(TConsole)
	terminal.MImprimirxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&dados_2.segmentdescriptor[3]))))

}
func (próprio_2 *TShareddescriptorTabela) Conjuntodescriptor(idx int, base_2 uint32, limite_2 uint32, tipo_2 uint8, parâmetros_3 uint8) {
	dados_2.segmentdescriptor[idx].Init(base_2, limite_2, tipo_2, parâmetros_3)
}

const (
	KcsÍndice	= 1
	KdsÍndice	= 2
	KgsÍndice	= 3

	Kcsselector	= KcsÍndice * 8
	Kdsselector	= KdsÍndice * 8
	Kgsselector	= KgsÍndice * 8

	Seggranocteto	= 0 << 7
	Seggran4kpágina	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsistema	= 0 << 4
	SegNormais	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privnúcleo	= 0 << 5
	Privutilizador	= 3 << 5

	Segbigmodo	= 1 << 6

	Presente	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescConteúdo		= 3 << 1
	Udescrxsomente		= 1 << 3
	UdescLimiteEntradapages	= 1 << 4
	UdescsegnotPresente	= 1 << 5
	Udescusable		= 1 << 6

	Gdtpontodeentrada	= 256
	TlsIniciar		= 16
)

var (
	gdtTabela	= [Gdtpontodeentrada]Gdtpontodeentrada_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelalen	= 0
)

type Gdtpontodeentrada_2 struct {
	limiteBaixo		uint16
	baseBaixo		uint16
	basemid			uint8
	acesso			uint8
	limiteAltoeParâmetros	uint8
	baseAlto		uint8
}

func (e *Gdtpontodeentrada_2) IsPresente() bool {
	return e.acesso&Presente != 0
}

func (e *Gdtpontodeentrada_2) Fill(base uint32, limite uint32, acesso uint8, parâmetros uint8) {
	e.limiteAltoeParâmetros = uint8((limite >> 16) & 0x000F)
	e.limiteAltoeParâmetros |= parâmetros
	e.acesso = acesso
	e.basemid = uint8(base >> 16)
	e.baseAlto = uint8(base >> 24)
	e.baseBaixo = uint16(base & 0xFFFF)
	e.limiteBaixo = uint16(limite & 0x0000FFFF)
}

func (e *Gdtpontodeentrada_2) Limpar() {
	e.limiteAltoeParâmetros = 0
	e.acesso = 0
	e.basemid = 0
	e.baseAlto = 0
	e.baseBaixo = 0
	e.limiteBaixo = 0

}

type Gdtdescriptor struct {
	GdtTamanho		uint16
	GdtEndereçoBaixo	uint16
	GdtEndereçoAlto		uint16
}
type Utilizadordescriptor struct {
	PontodeentradaNúmero	uint32
	BaseEndereço		uint32
	Limite			uint32
	Parâmetros		uint8
}

func Conjuntotlssegment(índice uint32, descriptor *Utilizadordescriptor, tabela []Gdtpontodeentrada_2) bool {
	if índice < TlsIniciar || índice > uint32(len(gdtTabela)) {
		return false
	}

	if descriptor.Parâmetros == Udescrxsomente|UdescsegnotPresente {

		tabela[índice].Limpar()
		return true
	}

	parâmetros := uint8(Seggranocteto)
	if descriptor.Parâmetros&UdescLimiteEntradapages != 0 {
		parâmetros = Seggran4kpágina
	}
	acesso := uint8(Privutilizador | SegNormais | Presente)
	if descriptor.Parâmetros&Udescrxsomente != 0 {
		acesso |= Segexec
	} else {
		acesso |= Segw
	}
	if acesso&SegNormais != 0 {
		parâmetros |= Segbigmodo
	}

	tabela[índice].Fill(descriptor.BaseEndereço, descriptor.Limite, acesso, parâmetros)
	flushtlsTabela(tabela)

	return true
}

func flushtlsTabela(tabela []Gdtpontodeentrada_2) {
	copy(gdtTabela[TlsIniciar:], tabela[TlsIniciar:])
}
func FlushtlsTabela(tabela []TSegmentdescriptor) {
	copy(dados_2.segmentdescriptor[TlsIniciar:], tabela[TlsIniciar:])
}
