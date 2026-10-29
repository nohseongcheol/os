/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "konsola"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUżytkownikcode	uint32	= 0x23
	SegUżytkownikdata	uint32	= 0x2B
	SegUżytkownikgs		uint32	= 0x33
	SegZadanieStan		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitNiski_2		uint16
	baseNiski_2		uint16
	baseWysoki_2		uint8
	typ			uint8
	znacznikilimitWysoki	uint8
	baseveryWysoki		uint8
}

func (bieżący_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, typ uint8, znaczniki_2 uint8) {

	bieżący_2.baseNiski_2 = uint16(base_2 & 0xFFFF)
	bieżący_2.baseWysoki_2 = uint8((base_2 >> 16) & 0xFF)
	bieżący_2.baseveryWysoki = uint8((base_2 >> 24) & 0xFF)

	bieżący_2.limitNiski_2 = uint16(limit_2 & 0xFFFF)
	bieżący_2.znacznikilimitWysoki = uint8((limit_2 >> 24) & 0x0F)
	bieżący_2.znacznikilimitWysoki |= (znaczniki_2 & 0xF0)

	bieżący_2.typ = typ

}

type TShareddescriptorTabeladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeladata

type TShareddescriptorTabela struct {
}

func (bieżący_2 *TShareddescriptorTabela) Init() {

	var gdtwpis TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtAdres := uintptr(uint32(gdtdescriptor.GdtAdresNiski) |
		uint32(gdtdescriptor.GdtAdresWysoki)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtRozmiar+1) / Sizeof(gdtwpis))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtAdres,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	cel_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseAdres := (*uint32)(Pointer(&cel_3[2]))
	(*baseAdres) = uint32(uintptr(Pointer(&data_2)))

	rozmiar_2 := (*uint16)(Pointer(&cel_3[0]))
	(*rozmiar_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&cel_3)))

	terminal := new(TKonsola)
	terminal.MWydrukujxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (bieżący_2 *TShareddescriptorTabela) Zbiórdescriptor(idx int, base_2 uint32, limit_2 uint32, typ uint8, znaczniki_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, typ, znaczniki_2)
}

const (
	KcsIndeks	= 1
	KdsIndeks	= 2
	KgsIndeks	= 3

	Kcsselector	= KcsIndeks * 8
	Kdsselector	= KdsIndeks * 8
	Kgsselector	= KgsIndeks * 8

	Seggranbyte	= 0 << 7
	Seggran4kStrona	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSystemowe	= 0 << 4
	SegZwykły	= 1 << 4

	Segnoexec	= 0 << 3
	SegUruchomienie	= 1 << 3

	Privkernel	= 0 << 5
	PrivUżytkownik	= 3 << 5

	SegbigTRYB	= 1 << 6

	Obecny	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSpistreści			= 3 << 1
	Udescrxonly			= 1 << 3
	UdesclimitWchodzącypages	= 1 << 4
	UdescsegnotObecny		= 1 << 5
	Udescusable			= 1 << 6

	Gdtwpis		= 256
	TlsUruchom	= 16
)

var (
	gdtTabela	= [Gdtwpis]Gdtwpis_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelalen	= 0
)

type Gdtwpis_2 struct {
	limitNiski			uint16
	baseNiski			uint16
	basemid				uint8
	dostępu				uint8
	limitWysokiorazZnaczniki	uint8
	baseWysoki			uint8
}

func (e *Gdtwpis_2) IsObecny() bool {
	return e.dostępu&Obecny != 0
}

func (e *Gdtwpis_2) Fill(base uint32, limit uint32, dostępu uint8, znaczniki uint8) {
	e.limitWysokiorazZnaczniki = uint8((limit >> 16) & 0x000F)
	e.limitWysokiorazZnaczniki |= znaczniki
	e.dostępu = dostępu
	e.basemid = uint8(base >> 16)
	e.baseWysoki = uint8(base >> 24)
	e.baseNiski = uint16(base & 0xFFFF)
	e.limitNiski = uint16(limit & 0x0000FFFF)
}

func (e *Gdtwpis_2) Wyczyść() {
	e.limitWysokiorazZnaczniki = 0
	e.dostępu = 0
	e.basemid = 0
	e.baseWysoki = 0
	e.baseNiski = 0
	e.limitNiski = 0

}

type Gdtdescriptor struct {
	GdtRozmiar	uint16
	GdtAdresNiski	uint16
	GdtAdresWysoki	uint16
}
type Użytkownikdescriptor struct {
	WpisLiczba	uint32
	BaseAdres	uint32
	Limit		uint32
	Znaczniki	uint8
}

func Zbiórtlssegment(indeks uint32, descriptor *Użytkownikdescriptor, tabela []Gdtwpis_2) bool {
	if indeks < TlsUruchom || indeks > uint32(len(gdtTabela)) {
		return false
	}

	if descriptor.Znaczniki == Udescrxonly|UdescsegnotObecny {

		tabela[indeks].Wyczyść()
		return true
	}

	znaczniki := uint8(Seggranbyte)
	if descriptor.Znaczniki&UdesclimitWchodzącypages != 0 {
		znaczniki = Seggran4kStrona
	}
	dostępu := uint8(PrivUżytkownik | SegZwykły | Obecny)
	if descriptor.Znaczniki&Udescrxonly != 0 {
		dostępu |= SegUruchomienie
	} else {
		dostępu |= Segw
	}
	if dostępu&SegZwykły != 0 {
		znaczniki |= SegbigTRYB
	}

	tabela[indeks].Fill(descriptor.BaseAdres, descriptor.Limit, dostępu, znaczniki)
	flushtlsTabela(tabela)

	return true
}

func flushtlsTabela(tabela []Gdtwpis_2) {
	copy(gdtTabela[TlsUruchom:], tabela[TlsUruchom:])
}
func FlushtlsTabela(tabela []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsUruchom:], tabela[TlsUruchom:])
}
