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

	SegBrugercode	uint32	= 0x23
	SegBrugerdata	uint32	= 0x2B
	SegBrugergs	uint32	= 0x33
	SegOpgaveStatus	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitLav_2	uint16
	baseLav_2	uint16
	baseHøj_2	uint8
	typeVærdi_2	uint8
	flaglimitHøj	uint8
	baseveryHøj	uint8
}

func (selv_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, typeVærdi_2 uint8, flag_2 uint8) {

	selv_2.baseLav_2 = uint16(base_2 & 0xFFFF)
	selv_2.baseHøj_2 = uint8((base_2 >> 16) & 0xFF)
	selv_2.baseveryHøj = uint8((base_2 >> 24) & 0xFF)

	selv_2.limitLav_2 = uint16(limit_2 & 0xFFFF)
	selv_2.flaglimitHøj = uint8((limit_2 >> 24) & 0x0F)
	selv_2.flaglimitHøj |= (flag_2 & 0xF0)

	selv_2.typeVærdi_2 = typeVærdi_2

}

type TShareddescriptorTabeldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeldata

type TShareddescriptorTabel struct {
}

func (selv_2 *TShareddescriptorTabel) Init() {

	var gdtemne TSegmentdescriptor

	gdtdescriptor = *getgdt()
	gammelgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressLav) |
		uint32(gdtdescriptor.GdtaddressHøj)<<16)
	gammelgdtlen := int(uintptr(gdtdescriptor.GdtStørrelse+1) / Sizeof(gdtemne))
	gammelgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	gammelgdtlen,
		Cap:	gammelgdtlen,
		Data:	gammelgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], gammelgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	størrelse_2 := (*uint16)(Pointer(&destination_3[0]))
	(*størrelse_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MUdskrivxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (selv_2 *TShareddescriptorTabel) Satdescriptor(idx int, base_2 uint32, limit_2 uint32, typeVærdi_2 uint8, flag_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, typeVærdi_2, flag_2)
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
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivBruger	= 3 << 5

	SegStortilstand	= 1 << 6

	Tilstedeværende	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescIndhold			= 3 << 1
	Udescrxonly			= 1 << 3
	UdesclimitIndpages		= 1 << 4
	UdescsegIkkeTilstedeværende	= 1 << 5
	Udescusable			= 1 << 6

	Gdtemne		= 256
	TlsBegynd	= 16
)

var (
	gdtTabel	= [Gdtemne]Gdtemne_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellen	= 0
)

type Gdtemne_2 struct {
	limitLav	uint16
	baseLav		uint16
	basemid		uint8
	tilgå		uint8
	limitHøjogFlag	uint8
	baseHøj		uint8
}

func (e *Gdtemne_2) IsTilstedeværende() bool {
	return e.tilgå&Tilstedeværende != 0
}

func (e *Gdtemne_2) Fill(base uint32, limit uint32, tilgå uint8, flag uint8) {
	e.limitHøjogFlag = uint8((limit >> 16) & 0x000F)
	e.limitHøjogFlag |= flag
	e.tilgå = tilgå
	e.basemid = uint8(base >> 16)
	e.baseHøj = uint8(base >> 24)
	e.baseLav = uint16(base & 0xFFFF)
	e.limitLav = uint16(limit & 0x0000FFFF)
}

func (e *Gdtemne_2) Ryd() {
	e.limitHøjogFlag = 0
	e.tilgå = 0
	e.basemid = 0
	e.baseHøj = 0
	e.baseLav = 0
	e.limitLav = 0

}

type Gdtdescriptor struct {
	GdtStørrelse	uint16
	GdtaddressLav	uint16
	GdtaddressHøj	uint16
}
type Brugerdescriptor struct {
	EmneTal		uint32
	Baseaddress	uint32
	Limit		uint32
	Flag		uint8
}

func Sattlssegment(indeks uint32, descriptor *Brugerdescriptor, tabel_2 []Gdtemne_2) bool {
	if indeks < TlsBegynd || indeks > uint32(len(gdtTabel)) {
		return false
	}

	if descriptor.Flag == Udescrxonly|UdescsegIkkeTilstedeværende {

		tabel_2[indeks].Ryd()
		return true
	}

	flag := uint8(Seggranbyte)
	if descriptor.Flag&UdesclimitIndpages != 0 {
		flag = Seggran4kSide
	}
	tilgå := uint8(PrivBruger | Segnormal | Tilstedeværende)
	if descriptor.Flag&Udescrxonly != 0 {
		tilgå |= Segexec
	} else {
		tilgå |= Segw
	}
	if tilgå&Segnormal != 0 {
		flag |= SegStortilstand
	}

	tabel_2[indeks].Fill(descriptor.Baseaddress, descriptor.Limit, tilgå, flag)
	flushtlsTabel(tabel_2)

	return true
}

func flushtlsTabel(tabel_2 []Gdtemne_2) {
	copy(gdtTabel[TlsBegynd:], tabel_2[TlsBegynd:])
}
func FlushtlsTabel(tabel_2 []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsBegynd:], tabel_2[TlsBegynd:])
}
