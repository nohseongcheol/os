package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKasutajacode	uint32	= 0x23
	SegKasutajadata	uint32	= 0x2B
	SegKasutajags	uint32	= 0x33
	SegtaskOlek	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	piirMadal_2	uint16
	baseMadal_2	uint16
	baseKõrge_2	uint8
	liik_2		uint8
	lipudPiirKõrge	uint8
	baseveryKõrge	uint8
}

func (ise_2 *TSegmentdescriptor) Init(base_2 uint32, piir_2 uint32, liik_2 uint8, lipud_2 uint8) {

	ise_2.baseMadal_2 = uint16(base_2 & 0xFFFF)
	ise_2.baseKõrge_2 = uint8((base_2 >> 16) & 0xFF)
	ise_2.baseveryKõrge = uint8((base_2 >> 24) & 0xFF)

	ise_2.piirMadal_2 = uint16(piir_2 & 0xFFFF)
	ise_2.lipudPiirKõrge = uint8((piir_2 >> 24) & 0x0F)
	ise_2.lipudPiirKõrge |= (lipud_2 & 0xF0)

	ise_2.liik_2 = liik_2

}

type TShareddescriptorTabeldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeldata

type TShareddescriptorTabel struct {
}

func (ise_2 *TShareddescriptorTabel) Init() {

	var gdtkirje TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressMadal) |
		uint32(gdtdescriptor.GdtaddressKõrge)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtSuurus+1) / Sizeof(gdtkirje))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	sihtfail_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&sihtfail_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	suurus_2 := (*uint16)(Pointer(&sihtfail_3[0]))
	(*suurus_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&sihtfail_3)))

	terminal := new(TConsole)
	terminal.MPrindixy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (ise_2 *TShareddescriptorTabel) Määradescriptor(idx int, base_2 uint32, piir_2 uint32, liik_2 uint8, lipud_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, piir_2, liik_2, lipud_2)
}

const (
	KcsSisukord	= 1
	KdsSisukord	= 2
	KgsSisukord	= 3

	Kcsselector	= KcsSisukord * 8
	Kdsselector	= KdsSisukord * 8
	Kgsselector	= KgsSisukord * 8

	Seggranbyte		= 0 << 7
	Seggran4kLehekülg	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSüsteem	= 0 << 4
	SegTavaline	= 1 << 4

	Segnoexec	= 0 << 3
	SegKäivitamine	= 1 << 3

	Privkernel	= 0 << 5
	PrivKasutaja	= 3 << 5

	SegbigREŽIIM	= 1 << 6

	Olemas	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescSisukord		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescPiirSissepages	= 1 << 4
	UdescsegnotOlemas	= 1 << 5
	Udescusable		= 1 << 6

	Gdtkirje	= 256
	TlsKäivita	= 16
)

var (
	gdtTabel	= [Gdtkirje]Gdtkirje_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellen	= 0
)

type Gdtkirje_2 struct {
	piirMadal		uint16
	baseMadal		uint16
	basemid			uint8
	ligipääs		uint8
	piirKõrgejaLipud	uint8
	baseKõrge		uint8
}

func (e *Gdtkirje_2) IsOlemas() bool {
	return e.ligipääs&Olemas != 0
}

func (e *Gdtkirje_2) Fill(base uint32, piir uint32, ligipääs uint8, lipud uint8) {
	e.piirKõrgejaLipud = uint8((piir >> 16) & 0x000F)
	e.piirKõrgejaLipud |= lipud
	e.ligipääs = ligipääs
	e.basemid = uint8(base >> 16)
	e.baseKõrge = uint8(base >> 24)
	e.baseMadal = uint16(base & 0xFFFF)
	e.piirMadal = uint16(piir & 0x0000FFFF)
}

func (e *Gdtkirje_2) Puhasta() {
	e.piirKõrgejaLipud = 0
	e.ligipääs = 0
	e.basemid = 0
	e.baseKõrge = 0
	e.baseMadal = 0
	e.piirMadal = 0

}

type Gdtdescriptor struct {
	GdtSuurus	uint16
	GdtaddressMadal	uint16
	GdtaddressKõrge	uint16
}
type Kasutajadescriptor struct {
	KirjeArv	uint32
	Baseaddress	uint32
	Piir		uint32
	Lipud		uint8
}

func Määratlssegment(sisukord uint32, descriptor *Kasutajadescriptor, tabel []Gdtkirje_2) bool {
	if sisukord < TlsKäivita || sisukord > uint32(len(gdtTabel)) {
		return false
	}

	if descriptor.Lipud == Udescrxonly|UdescsegnotOlemas {

		tabel[sisukord].Puhasta()
		return true
	}

	lipud := uint8(Seggranbyte)
	if descriptor.Lipud&UdescPiirSissepages != 0 {
		lipud = Seggran4kLehekülg
	}
	ligipääs := uint8(PrivKasutaja | SegTavaline | Olemas)
	if descriptor.Lipud&Udescrxonly != 0 {
		ligipääs |= SegKäivitamine
	} else {
		ligipääs |= Segw
	}
	if ligipääs&SegTavaline != 0 {
		lipud |= SegbigREŽIIM
	}

	tabel[sisukord].Fill(descriptor.Baseaddress, descriptor.Piir, ligipääs, lipud)
	flushtlsTabel(tabel)

	return true
}

func flushtlsTabel(tabel []Gdtkirje_2) {
	copy(gdtTabel[TlsKäivita:], tabel[TlsKäivita:])
}
func FlushtlsTabel(tabel []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsKäivita:], tabel[TlsKäivita:])
}
