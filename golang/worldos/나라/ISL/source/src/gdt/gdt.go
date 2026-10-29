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

	SegNotandicode	uint32	= 0x23
	SegNotandidata	uint32	= 0x2B
	SegNotandigs	uint32	= 0x33
	SegVerkStaða	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitLágt_2	uint16
	baseLágt_2	uint16
	baseHátt_2	uint8
	tegund		uint8
	flagslimitHátt	uint8
	baseveryHátt	uint8
}

func (sjálft_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, tegund uint8, flags_2 uint8) {

	sjálft_2.baseLágt_2 = uint16(base_2 & 0xFFFF)
	sjálft_2.baseHátt_2 = uint8((base_2 >> 16) & 0xFF)
	sjálft_2.baseveryHátt = uint8((base_2 >> 24) & 0xFF)

	sjálft_2.limitLágt_2 = uint16(limit_2 & 0xFFFF)
	sjálft_2.flagslimitHátt = uint8((limit_2 >> 24) & 0x0F)
	sjálft_2.flagslimitHátt |= (flags_2 & 0xF0)

	sjálft_2.tegund = tegund

}

type TShareddescriptorTafladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTafladata

type TShareddescriptorTafla struct {
}

func (sjálft_2 *TShareddescriptorTafla) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressLágt) |
		uint32(gdtdescriptor.GdtaddressHátt)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtStærð+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	áfangastaður_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&áfangastaður_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	stærð_2 := (*uint16)(Pointer(&áfangastaður_3[0]))
	(*stærð_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&áfangastaður_3)))

	terminal := new(TConsole)
	terminal.MPrentaxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (sjálft_2 *TShareddescriptorTafla) Setjadescriptor(idx int, base_2 uint32, limit_2 uint32, tegund uint8, flags_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, tegund, flags_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4ksíða	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegKerfis	= 0 << 4
	SegVenjulegur	= 1 << 4

	Segnoexec	= 0 << 3
	SegKeyra	= 1 << 3

	Privkernel	= 0 << 5
	PrivNotandi	= 3 << 5

	SegbigHAMUR	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescInnihald		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitInnpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsRæsa		= 16
)

var (
	gdtTafla	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTaflalen	= 0
)

type Gdtentry_2 struct {
	limitLágt		uint16
	baseLágt		uint16
	basemid			uint8
	aðgangur		uint8
	limitHáttandflags	uint8
	baseHátt		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.aðgangur&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, aðgangur uint8, flags uint8) {
	e.limitHáttandflags = uint8((limit >> 16) & 0x000F)
	e.limitHáttandflags |= flags
	e.aðgangur = aðgangur
	e.basemid = uint8(base >> 16)
	e.baseHátt = uint8(base >> 24)
	e.baseLágt = uint16(base & 0xFFFF)
	e.limitLágt = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Hreinsa() {
	e.limitHáttandflags = 0
	e.aðgangur = 0
	e.basemid = 0
	e.baseHátt = 0
	e.baseLágt = 0
	e.limitLágt = 0

}

type Gdtdescriptor struct {
	GdtStærð	uint16
	GdtaddressLágt	uint16
	GdtaddressHátt	uint16
}
type Notandidescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Flags		uint8
}

func Setjatlssegment(index uint32, descriptor *Notandidescriptor, tafla []Gdtentry_2) bool {
	if index < TlsRæsa || index > uint32(len(gdtTafla)) {
		return false
	}

	if descriptor.Flags == Udescrxonly|Udescsegnotpresent {

		tafla[index].Hreinsa()
		return true
	}

	flags := uint8(Seggranbyte)
	if descriptor.Flags&UdesclimitInnpages != 0 {
		flags = Seggran4ksíða
	}
	aðgangur := uint8(PrivNotandi | SegVenjulegur | Present)
	if descriptor.Flags&Udescrxonly != 0 {
		aðgangur |= SegKeyra
	} else {
		aðgangur |= Segw
	}
	if aðgangur&SegVenjulegur != 0 {
		flags |= SegbigHAMUR
	}

	tafla[index].Fill(descriptor.Baseaddress, descriptor.Limit, aðgangur, flags)
	flushtlsTafla(tafla)

	return true
}

func flushtlsTafla(tafla []Gdtentry_2) {
	copy(gdtTafla[TlsRæsa:], tafla[TlsRæsa:])
}
func FlushtlsTafla(tafla []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsRæsa:], tafla[TlsRæsa:])
}
