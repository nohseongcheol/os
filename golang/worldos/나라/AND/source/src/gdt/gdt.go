/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "consola"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUsuaricode	uint32	= 0x23
	SegUsuaridata	uint32	= 0x2B
	SegUsuarigs	uint32	= 0x33
	SegTascaEstat	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	límitBaixa_2		uint16
	baseBaixa_2		uint16
	baseAlta_2		uint8
	tipus			uint8
	senyaladorsLímitAlta	uint8
	baseveryAlta		uint8
}

func (unmateix_2 *TSegmentdescriptor) Init(base_2 uint32, límit_2 uint32, tipus uint8, senyaladors_2 uint8) {

	unmateix_2.baseBaixa_2 = uint16(base_2 & 0xFFFF)
	unmateix_2.baseAlta_2 = uint8((base_2 >> 16) & 0xFF)
	unmateix_2.baseveryAlta = uint8((base_2 >> 24) & 0xFF)

	unmateix_2.límitBaixa_2 = uint16(límit_2 & 0xFFFF)
	unmateix_2.senyaladorsLímitAlta = uint8((límit_2 >> 24) & 0x0F)
	unmateix_2.senyaladorsLímitAlta |= (senyaladors_2 & 0xF0)

	unmateix_2.tipus = tipus

}

type TShareddescriptorTauladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTauladata

type TShareddescriptorTaula struct {
}

func (unmateix_2 *TShareddescriptorTaula) Init() {

	var gdtentrada TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtAdreça := uintptr(uint32(gdtdescriptor.GdtAdreçaBaixa) |
		uint32(gdtdescriptor.GdtAdreçaAlta)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtMida+1) / Sizeof(gdtentrada))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtAdreça,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destinació_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseAdreça := (*uint32)(Pointer(&destinació_3[2]))
	(*baseAdreça) = uint32(uintptr(Pointer(&data_2)))

	mida_2 := (*uint16)(Pointer(&destinació_3[0]))
	(*mida_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destinació_3)))

	terminal := new(TConsola)
	terminal.MImprimeixxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (unmateix_2 *TShareddescriptorTaula) Estableixdescriptor(idx int, base_2 uint32, límit_2 uint32, tipus uint8, senyaladors_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, límit_2, tipus, senyaladors_2)
}

const (
	KcsÍndex	= 1
	KdsÍndex	= 2
	KgsÍndex	= 3

	Kcsselector	= KcsÍndex * 8
	Kdsselector	= KdsÍndex * 8
	Kgsselector	= KgsÍndex * 8

	Seggranbyte	= 0 << 7
	Seggran4kPàgina	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistema	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	SegExecució	= 1 << 3

	Privkernel	= 0 << 5
	PrivUsuari	= 3 << 5

	Segbigmode	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescContinguts		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescLímitaPàgines	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentrada	= 256
	TlsInicia	= 16
)

var (
	gdtTaula	= [Gdtentrada]Gdtentrada_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTaulalen	= 0
)

type Gdtentrada_2 struct {
	límitBaixa		uint16
	baseBaixa		uint16
	basemid			uint8
	accés			uint8
	límitAltaiSenyaladors	uint8
	baseAlta		uint8
}

func (e *Gdtentrada_2) Ispresent() bool {
	return e.accés&Present != 0
}

func (e *Gdtentrada_2) Fill(base uint32, límit uint32, accés uint8, senyaladors uint8) {
	e.límitAltaiSenyaladors = uint8((límit >> 16) & 0x000F)
	e.límitAltaiSenyaladors |= senyaladors
	e.accés = accés
	e.basemid = uint8(base >> 16)
	e.baseAlta = uint8(base >> 24)
	e.baseBaixa = uint16(base & 0xFFFF)
	e.límitBaixa = uint16(límit & 0x0000FFFF)
}

func (e *Gdtentrada_2) Neteja() {
	e.límitAltaiSenyaladors = 0
	e.accés = 0
	e.basemid = 0
	e.baseAlta = 0
	e.baseBaixa = 0
	e.límitBaixa = 0

}

type Gdtdescriptor struct {
	GdtMida		uint16
	GdtAdreçaBaixa	uint16
	GdtAdreçaAlta	uint16
}
type Usuaridescriptor struct {
	EntradaNombre	uint32
	BaseAdreça	uint32
	Límit		uint32
	Senyaladors	uint8
}

func Estableixtlssegment(índex uint32, descriptor *Usuaridescriptor, taula []Gdtentrada_2) bool {
	if índex < TlsInicia || índex > uint32(len(gdtTaula)) {
		return false
	}

	if descriptor.Senyaladors == Udescrxonly|Udescsegnotpresent {

		taula[índex].Neteja()
		return true
	}

	senyaladors := uint8(Seggranbyte)
	if descriptor.Senyaladors&UdescLímitaPàgines != 0 {
		senyaladors = Seggran4kPàgina
	}
	accés := uint8(PrivUsuari | Segnormal | Present)
	if descriptor.Senyaladors&Udescrxonly != 0 {
		accés |= SegExecució
	} else {
		accés |= Segw
	}
	if accés&Segnormal != 0 {
		senyaladors |= Segbigmode
	}

	taula[índex].Fill(descriptor.BaseAdreça, descriptor.Límit, accés, senyaladors)
	flushtlsTaula(taula)

	return true
}

func flushtlsTaula(taula []Gdtentrada_2) {
	copy(gdtTaula[TlsInicia:], taula[TlsInicia:])
}
func FlushtlsTaula(taula []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsInicia:], taula[TlsInicia:])
}
