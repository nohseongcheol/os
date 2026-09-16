/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "konzol"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegFelhasználócode	uint32	= 0x23
	SegFelhasználódata	uint32	= 0x2B
	SegFelhasználógs	uint32	= 0x33
	SegFeladatÁllapot	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	korlátozásAlacsony_2	uint16
	baseAlacsony_2		uint16
	baseMagas_2		uint8
	típus			uint8
	flagekKorlátozásMagas	uint8
	baseveryMagas		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, korlátozás_2 uint32, típus uint8, flagek_2 uint8) {

	self_2.baseAlacsony_2 = uint16(base_2 & 0xFFFF)
	self_2.baseMagas_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryMagas = uint8((base_2 >> 24) & 0xFF)

	self_2.korlátozásAlacsony_2 = uint16(korlátozás_2 & 0xFFFF)
	self_2.flagekKorlátozásMagas = uint8((korlátozás_2 >> 24) & 0x0F)
	self_2.flagekKorlátozásMagas |= (flagek_2 & 0xF0)

	self_2.típus = típus

}

type TShareddescriptorTáblázatdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTáblázatdata

type TShareddescriptorTáblázat struct {
}

func (self_2 *TShareddescriptorTáblázat) Init() {

	var gdtbejegyzés TSegmentdescriptor

	gdtdescriptor = *getgdt()
	öreggdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressAlacsony) |
		uint32(gdtdescriptor.GdtaddressMagas)<<16)
	öreggdtlen := int(uintptr(gdtdescriptor.GdtMéret+1) / Sizeof(gdtbejegyzés))
	öreggdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	öreggdtlen,
		Cap:	öreggdtlen,
		Data:	öreggdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], öreggdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	cél_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&cél_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	méret_2 := (*uint16)(Pointer(&cél_3[0]))
	(*méret_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&cél_3)))

	terminal := new(TKonzol)
	terminal.MNyomtatásxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorTáblázat) Halmazdescriptor(idx int, base_2 uint32, korlátozás_2 uint32, típus uint8, flagek_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, korlátozás_2, típus, flagek_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kOldal	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegRendszer	= 0 << 4
	SegNormál	= 1 << 4

	Segnoexec	= 0 << 3
	SegFuttatás	= 1 << 3

	Privkernel	= 0 << 5
	PrivFelhasználó	= 3 << 5

	SegNagymód	= 1 << 6

	Jelenvan	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescTartalom		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescKorlátozásBepages	= 1 << 4
	UdescsegNemJelenvan	= 1 << 5
	Udescusable		= 1 << 6

	Gdtbejegyzés	= 256
	TlsIndítás	= 16
)

var (
	gdtTáblázat	= [Gdtbejegyzés]Gdtbejegyzés_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTáblázatlen	= 0
)

type Gdtbejegyzés_2 struct {
	korlátozásAlacsony	uint16
	baseAlacsony		uint16
	basemid			uint8
	elérés			uint8
	korlátozásMagasÉSFlagek	uint8
	baseMagas		uint8
}

func (e *Gdtbejegyzés_2) IsJelenvan() bool {
	return e.elérés&Jelenvan != 0
}

func (e *Gdtbejegyzés_2) Fill(base uint32, korlátozás uint32, elérés uint8, flagek uint8) {
	e.korlátozásMagasÉSFlagek = uint8((korlátozás >> 16) & 0x000F)
	e.korlátozásMagasÉSFlagek |= flagek
	e.elérés = elérés
	e.basemid = uint8(base >> 16)
	e.baseMagas = uint8(base >> 24)
	e.baseAlacsony = uint16(base & 0xFFFF)
	e.korlátozásAlacsony = uint16(korlátozás & 0x0000FFFF)
}

func (e *Gdtbejegyzés_2) Törlés() {
	e.korlátozásMagasÉSFlagek = 0
	e.elérés = 0
	e.basemid = 0
	e.baseMagas = 0
	e.baseAlacsony = 0
	e.korlátozásAlacsony = 0

}

type Gdtdescriptor struct {
	GdtMéret		uint16
	GdtaddressAlacsony	uint16
	GdtaddressMagas		uint16
}
type Felhasználódescriptor struct {
	BejegyzésSzám	uint32
	Baseaddress	uint32
	Korlátozás	uint32
	Flagek		uint8
}

func Halmaztlssegment(index uint32, descriptor *Felhasználódescriptor, táblázat []Gdtbejegyzés_2) bool {
	if index < TlsIndítás || index > uint32(len(gdtTáblázat)) {
		return false
	}

	if descriptor.Flagek == Udescrxonly|UdescsegNemJelenvan {

		táblázat[index].Törlés()
		return true
	}

	flagek := uint8(Seggranbyte)
	if descriptor.Flagek&UdescKorlátozásBepages != 0 {
		flagek = Seggran4kOldal
	}
	elérés := uint8(PrivFelhasználó | SegNormál | Jelenvan)
	if descriptor.Flagek&Udescrxonly != 0 {
		elérés |= SegFuttatás
	} else {
		elérés |= Segw
	}
	if elérés&SegNormál != 0 {
		flagek |= SegNagymód
	}

	táblázat[index].Fill(descriptor.Baseaddress, descriptor.Korlátozás, elérés, flagek)
	flushtlsTáblázat(táblázat)

	return true
}

func flushtlsTáblázat(táblázat []Gdtbejegyzés_2) {
	copy(gdtTáblázat[TlsIndítás:], táblázat[TlsIndítás:])
}
func FlushtlsTáblázat(táblázat []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsIndítás:], táblázat[TlsIndítás:])
}
