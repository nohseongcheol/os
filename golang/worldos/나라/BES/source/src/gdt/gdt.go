/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegGebruikercode	uint32	= 0x23
	SegGebruikerdata	uint32	= 0x2B
	SegGebruikergs		uint32	= 0x33
	SegTaakStatus		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	beperkenLaag_2		uint16
	baseLaag_2		uint16
	baseHoog_2		uint8
	soort_2			uint8
	vlaggenBeperkenHoog	uint8
	baseveryHoog		uint8
}

func (zelf_2 *TSegmentdescriptor) Init(base_2 uint32, beperken_2 uint32, soort_2 uint8, vlaggen_2 uint8) {

	zelf_2.baseLaag_2 = uint16(base_2 & 0xFFFF)
	zelf_2.baseHoog_2 = uint8((base_2 >> 16) & 0xFF)
	zelf_2.baseveryHoog = uint8((base_2 >> 24) & 0xFF)

	zelf_2.beperkenLaag_2 = uint16(beperken_2 & 0xFFFF)
	zelf_2.vlaggenBeperkenHoog = uint8((beperken_2 >> 24) & 0x0F)
	zelf_2.vlaggenBeperkenHoog |= (vlaggen_2 & 0xF0)

	zelf_2.soort_2 = soort_2

}

type TShareddescriptorTabeldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeldata

type TShareddescriptorTabel struct {
}

func (zelf_2 *TShareddescriptorTabel) Init() {

	var gdtItem TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oudgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressLaag) |
		uint32(gdtdescriptor.GdtaddressHoog)<<16)
	oudgdtlen := int(uintptr(gdtdescriptor.GdtGrootte+1) / Sizeof(gdtItem))
	oudgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oudgdtlen,
		Cap:	oudgdtlen,
		Data:	oudgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oudgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	bestemming_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&bestemming_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	grootte_2 := (*uint16)(Pointer(&bestemming_3[0]))
	(*grootte_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&bestemming_3)))

	terminal := new(TConsole)
	terminal.MAfdrukkenxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (zelf_2 *TShareddescriptorTabel) Instellendescriptor(idx int, base_2 uint32, beperken_2 uint32, soort_2 uint8, vlaggen_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, beperken_2, soort_2, vlaggen_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kPagina	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSysteem	= 0 << 4
	SegNormaal	= 1 << 4

	Segnoexec	= 0 << 3
	SegUitvoeren	= 1 << 3

	Privkernel	= 0 << 5
	PrivGebruiker	= 3 << 5

	SegGrootmodus	= 1 << 6

	Aanwezig	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescInhoud		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescBeperkeninPaginas	= 1 << 4
	UdescsegNietAanwezig	= 1 << 5
	Udescusable		= 1 << 6

	GdtItem		= 256
	TlsStarten	= 16
)

var (
	gdtTabel	= [GdtItem]GdtItem_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellen	= 0
)

type GdtItem_2 struct {
	beperkenLaag		uint16
	baseLaag		uint16
	basemid			uint8
	toegang			uint8
	beperkenHoogenVlaggen	uint8
	baseHoog		uint8
}

func (e *GdtItem_2) IsAanwezig() bool {
	return e.toegang&Aanwezig != 0
}

func (e *GdtItem_2) Fill(base uint32, beperken uint32, toegang uint8, vlaggen uint8) {
	e.beperkenHoogenVlaggen = uint8((beperken >> 16) & 0x000F)
	e.beperkenHoogenVlaggen |= vlaggen
	e.toegang = toegang
	e.basemid = uint8(base >> 16)
	e.baseHoog = uint8(base >> 24)
	e.baseLaag = uint16(base & 0xFFFF)
	e.beperkenLaag = uint16(beperken & 0x0000FFFF)
}

func (e *GdtItem_2) Wissen() {
	e.beperkenHoogenVlaggen = 0
	e.toegang = 0
	e.basemid = 0
	e.baseHoog = 0
	e.baseLaag = 0
	e.beperkenLaag = 0

}

type Gdtdescriptor struct {
	GdtGrootte	uint16
	GdtaddressLaag	uint16
	GdtaddressHoog	uint16
}
type Gebruikerdescriptor struct {
	ItemGetal	uint32
	Baseaddress	uint32
	Beperken	uint32
	Vlaggen		uint8
}

func Instellentlssegment(index uint32, descriptor *Gebruikerdescriptor, tabel []GdtItem_2) bool {
	if index < TlsStarten || index > uint32(len(gdtTabel)) {
		return false
	}

	if descriptor.Vlaggen == Udescrxonly|UdescsegNietAanwezig {

		tabel[index].Wissen()
		return true
	}

	vlaggen := uint8(Seggranbyte)
	if descriptor.Vlaggen&UdescBeperkeninPaginas != 0 {
		vlaggen = Seggran4kPagina
	}
	toegang := uint8(PrivGebruiker | SegNormaal | Aanwezig)
	if descriptor.Vlaggen&Udescrxonly != 0 {
		toegang |= SegUitvoeren
	} else {
		toegang |= Segw
	}
	if toegang&SegNormaal != 0 {
		vlaggen |= SegGrootmodus
	}

	tabel[index].Fill(descriptor.Baseaddress, descriptor.Beperken, toegang, vlaggen)
	flushtlsTabel(tabel)

	return true
}

func flushtlsTabel(tabel []GdtItem_2) {
	copy(gdtTabel[TlsStarten:], tabel[TlsStarten:])
}
func FlushtlsTabel(tabel []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsStarten:], tabel[TlsStarten:])
}
