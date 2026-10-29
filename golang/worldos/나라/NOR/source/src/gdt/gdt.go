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

	SegBrukercode		uint32	= 0x23
	SegBrukerdata		uint32	= 0x2B
	SegBrukergs		uint32	= 0x33
	SegOppgaveStatus	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	grenseLav_2	uint16
	baseLav_2	uint16
	baseHøy_2	uint8
	filtype		uint8
	flaggGrenseHøy	uint8
	baseveryHøy	uint8
}

func (selv_2 *TSegmentdescriptor) Init(base_2 uint32, grense_2 uint32, filtype uint8, flagg_2 uint8) {

	selv_2.baseLav_2 = uint16(base_2 & 0xFFFF)
	selv_2.baseHøy_2 = uint8((base_2 >> 16) & 0xFF)
	selv_2.baseveryHøy = uint8((base_2 >> 24) & 0xFF)

	selv_2.grenseLav_2 = uint16(grense_2 & 0xFFFF)
	selv_2.flaggGrenseHøy = uint8((grense_2 >> 24) & 0x0F)
	selv_2.flaggGrenseHøy |= (flagg_2 & 0xF0)

	selv_2.filtype = filtype

}

type TShareddescriptorTabelldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabelldata

type TShareddescriptorTabell struct {
}

func (selv_2 *TShareddescriptorTabell) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	gammelgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressLav) |
		uint32(gdtdescriptor.GdtaddressHøy)<<16)
	gammelgdtlen := int(uintptr(gdtdescriptor.GdtStørrelse+1) / Sizeof(gdtentry))
	gammelgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	gammelgdtlen,
		Cap:	gammelgdtlen,
		Data:	gammelgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], gammelgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	mål_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&mål_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	størrelse_2 := (*uint16)(Pointer(&mål_3[0]))
	(*størrelse_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&mål_3)))

	terminal := new(TConsole)
	terminal.MSkrivutxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (selv_2 *TShareddescriptorTabell) Settdescriptor(idx int, base_2 uint32, grense_2 uint32, filtype uint8, flagg_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, grense_2, filtype, flagg_2)
}

const (
	KcsIndeks	= 1
	KdsIndeks	= 2
	KgsIndeks	= 3

	Kcsselector	= KcsIndeks * 8
	Kdsselector	= KdsIndeks * 8
	Kgsselector	= KgsIndeks * 8

	Seggranbyte	= 0 << 7
	Seggran4kSide	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystem	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	SegKjørbar	= 1 << 3

	Privkernel	= 0 << 5
	PrivBruker	= 3 << 5

	SegStormodus	= 1 << 6

	Tilstede	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescInnhold		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescGrenseInnpages	= 1 << 4
	UdescsegnotTilstede	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsstart	= 16
)

var (
	gdtTabell	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelllen	= 0
)

type Gdtentry_2 struct {
	grenseLav		uint16
	baseLav			uint16
	basemid			uint8
	tilgang			uint8
	grenseHøyogFlagg	uint8
	baseHøy			uint8
}

func (e *Gdtentry_2) IsTilstede() bool {
	return e.tilgang&Tilstede != 0
}

func (e *Gdtentry_2) Fill(base uint32, grense uint32, tilgang uint8, flagg uint8) {
	e.grenseHøyogFlagg = uint8((grense >> 16) & 0x000F)
	e.grenseHøyogFlagg |= flagg
	e.tilgang = tilgang
	e.basemid = uint8(base >> 16)
	e.baseHøy = uint8(base >> 24)
	e.baseLav = uint16(base & 0xFFFF)
	e.grenseLav = uint16(grense & 0x0000FFFF)
}

func (e *Gdtentry_2) Tøm() {
	e.grenseHøyogFlagg = 0
	e.tilgang = 0
	e.basemid = 0
	e.baseHøy = 0
	e.baseLav = 0
	e.grenseLav = 0

}

type Gdtdescriptor struct {
	GdtStørrelse	uint16
	GdtaddressLav	uint16
	GdtaddressHøy	uint16
}
type Brukerdescriptor struct {
	EntryTall	uint32
	Baseaddress	uint32
	Grense		uint32
	Flagg		uint8
}

func Setttlssegment(indeks uint32, descriptor *Brukerdescriptor, tabell_2 []Gdtentry_2) bool {
	if indeks < Tlsstart || indeks > uint32(len(gdtTabell)) {
		return false
	}

	if descriptor.Flagg == Udescrxonly|UdescsegnotTilstede {

		tabell_2[indeks].Tøm()
		return true
	}

	flagg := uint8(Seggranbyte)
	if descriptor.Flagg&UdescGrenseInnpages != 0 {
		flagg = Seggran4kSide
	}
	tilgang := uint8(PrivBruker | Segnormal | Tilstede)
	if descriptor.Flagg&Udescrxonly != 0 {
		tilgang |= SegKjørbar
	} else {
		tilgang |= Segw
	}
	if tilgang&Segnormal != 0 {
		flagg |= SegStormodus
	}

	tabell_2[indeks].Fill(descriptor.Baseaddress, descriptor.Grense, tilgang, flagg)
	flushtlsTabell(tabell_2)

	return true
}

func flushtlsTabell(tabell_2 []Gdtentry_2) {
	copy(gdtTabell[Tlsstart:], tabell_2[Tlsstart:])
}
func FlushtlsTabell(tabell_2 []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], tabell_2[Tlsstart:])
}
