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

	SegUporabnikcode	uint32	= 0x23
	SegUporabnikdata	uint32	= 0x2B
	SegUporabnikgs		uint32	= 0x33
	SegNalogaStanje		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitNizko_2		uint16
	baseNizko_2		uint16
	baseVisoko_2		uint8
	vrsta_2			uint8
	zastavicelimitVisoko	uint8
	baseveryVisoko		uint8
}

func (sam_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, vrsta_2 uint8, zastavice_2 uint8) {

	sam_2.baseNizko_2 = uint16(base_2 & 0xFFFF)
	sam_2.baseVisoko_2 = uint8((base_2 >> 16) & 0xFF)
	sam_2.baseveryVisoko = uint8((base_2 >> 24) & 0xFF)

	sam_2.limitNizko_2 = uint16(limit_2 & 0xFFFF)
	sam_2.zastavicelimitVisoko = uint8((limit_2 >> 24) & 0x0F)
	sam_2.zastavicelimitVisoko |= (zastavice_2 & 0xF0)

	sam_2.vrsta_2 = vrsta_2

}

type TShareddescriptorPreglednicadata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorPreglednicadata

type TShareddescriptorPreglednica struct {
}

func (sam_2 *TShareddescriptorPreglednica) Init() {

	var gdtvnos TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressNizko) |
		uint32(gdtdescriptor.GdtaddressVisoko)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVelikost+1) / Sizeof(gdtvnos))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	cilj_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&cilj_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	velikost_2 := (*uint16)(Pointer(&cilj_3[0]))
	(*velikost_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&cilj_3)))

	terminal := new(TConsole)
	terminal.MNatisnixy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (sam_2 *TShareddescriptorPreglednica) Množicadescriptor(idx int, base_2 uint32, limit_2 uint32, vrsta_2 uint8, zastavice_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, vrsta_2, zastavice_2)
}

const (
	KcsKazalo	= 1
	KdsKazalo	= 2
	KgsKazalo	= 3

	Kcsselector	= KcsKazalo * 8
	Kdsselector	= KdsKazalo * 8
	Kgsselector	= KgsKazalo * 8

	Seggranbyte	= 0 << 7
	Seggran4kStran	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	SegObičajno	= 1 << 4

	Segnoexec	= 0 << 3
	SegIzvedljivo	= 1 << 3

	Privkernel	= 0 << 5
	PrivUporabnik	= 3 << 5

	SegbigNAČIN	= 1 << 6

	Prisotnost	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescVsebina		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitVhodnopages	= 1 << 4
	UdescsegnotPrisotnost	= 1 << 5
	Udescusable		= 1 << 6

	Gdtvnos		= 256
	TlsZačni	= 16
)

var (
	gdtPreglednica		= [Gdtvnos]Gdtvnos_2{}
	gdtdescriptor		Gdtdescriptor
	gdtPreglednicalen	= 0
)

type Gdtvnos_2 struct {
	limitNizko		uint16
	baseNizko		uint16
	basemid			uint8
	dostop			uint8
	limitVisokoandZastavice	uint8
	baseVisoko		uint8
}

func (e *Gdtvnos_2) IsPrisotnost() bool {
	return e.dostop&Prisotnost != 0
}

func (e *Gdtvnos_2) Fill(base uint32, limit uint32, dostop uint8, zastavice uint8) {
	e.limitVisokoandZastavice = uint8((limit >> 16) & 0x000F)
	e.limitVisokoandZastavice |= zastavice
	e.dostop = dostop
	e.basemid = uint8(base >> 16)
	e.baseVisoko = uint8(base >> 24)
	e.baseNizko = uint16(base & 0xFFFF)
	e.limitNizko = uint16(limit & 0x0000FFFF)
}

func (e *Gdtvnos_2) Počisti() {
	e.limitVisokoandZastavice = 0
	e.dostop = 0
	e.basemid = 0
	e.baseVisoko = 0
	e.baseNizko = 0
	e.limitNizko = 0

}

type Gdtdescriptor struct {
	GdtVelikost		uint16
	GdtaddressNizko		uint16
	GdtaddressVisoko	uint16
}
type Uporabnikdescriptor struct {
	VnosŠtevilka	uint32
	Baseaddress	uint32
	Limit		uint32
	Zastavice	uint8
}

func Množicatlssegment(kazalo uint32, descriptor *Uporabnikdescriptor, preglednica []Gdtvnos_2) bool {
	if kazalo < TlsZačni || kazalo > uint32(len(gdtPreglednica)) {
		return false
	}

	if descriptor.Zastavice == Udescrxonly|UdescsegnotPrisotnost {

		preglednica[kazalo].Počisti()
		return true
	}

	zastavice := uint8(Seggranbyte)
	if descriptor.Zastavice&UdesclimitVhodnopages != 0 {
		zastavice = Seggran4kStran
	}
	dostop := uint8(PrivUporabnik | SegObičajno | Prisotnost)
	if descriptor.Zastavice&Udescrxonly != 0 {
		dostop |= SegIzvedljivo
	} else {
		dostop |= Segw
	}
	if dostop&SegObičajno != 0 {
		zastavice |= SegbigNAČIN
	}

	preglednica[kazalo].Fill(descriptor.Baseaddress, descriptor.Limit, dostop, zastavice)
	flushtlsPreglednica(preglednica)

	return true
}

func flushtlsPreglednica(preglednica []Gdtvnos_2) {
	copy(gdtPreglednica[TlsZačni:], preglednica[TlsZačni:])
}
func FlushtlsPreglednica(preglednica []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsZačni:], preglednica[TlsZačni:])
}
