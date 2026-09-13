package gdt

import . "unsafe"
import "reflect"
import . "konsol"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegAnvändarecode	uint32	= 0x23
	SegAnvändaredata	uint32	= 0x2B
	SegAnvändaregs		uint32	= 0x33
	SegAktivitetTillstånd	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	gränsLåg_2	uint16
	baseLåg_2	uint16
	baseHög_2	uint8
	typ		uint8
	flaggorGränsHög	uint8
	baseveryHög	uint8
}

func (själv_2 *TSegmentdescriptor) Init(base_2 uint32, gräns_2 uint32, typ uint8, flaggor_2 uint8) {

	själv_2.baseLåg_2 = uint16(base_2 & 0xFFFF)
	själv_2.baseHög_2 = uint8((base_2 >> 16) & 0xFF)
	själv_2.baseveryHög = uint8((base_2 >> 24) & 0xFF)

	själv_2.gränsLåg_2 = uint16(gräns_2 & 0xFFFF)
	själv_2.flaggorGränsHög = uint8((gräns_2 >> 24) & 0x0F)
	själv_2.flaggorGränsHög |= (flaggor_2 & 0xF0)

	själv_2.typ = typ

}

type TShareddescriptorTabelldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabelldata

type TShareddescriptorTabell struct {
}

func (själv_2 *TShareddescriptorTabell) Init() {

	var gdtpost TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtAdress := uintptr(uint32(gdtdescriptor.GdtAdressLåg) |
		uint32(gdtdescriptor.GdtAdressHög)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtStorlek+1) / Sizeof(gdtpost))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtAdress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	mål_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseAdress := (*uint32)(Pointer(&mål_3[2]))
	(*baseAdress) = uint32(uintptr(Pointer(&data_2)))

	storlek_2 := (*uint16)(Pointer(&mål_3[0]))
	(*storlek_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&mål_3)))

	terminal := new(TKonsol)
	terminal.MSkrivutxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (själv_2 *TShareddescriptorTabell) Mängddescriptor(idx int, base_2 uint32, gräns_2 uint32, typ uint8, flaggor_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, gräns_2, typ, flaggor_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kSida	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystem	= 0 << 4
	SegNormalt	= 1 << 4

	Segnoexec	= 0 << 3
	SegKör		= 1 << 3

	Privkernel	= 0 << 5
	PrivAnvändare	= 3 << 5

	SegbigLÄGE	= 1 << 6

	Ansluten	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescInnehåll		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescGränsipages	= 1 << 4
	UdescsegnotAnsluten	= 1 << 5
	Udescusable		= 1 << 6

	Gdtpost		= 256
	TlsStarta	= 16
)

var (
	gdtTabell	= [Gdtpost]Gdtpost_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelllen	= 0
)

type Gdtpost_2 struct {
	gränsLåg		uint16
	baseLåg			uint16
	basemid			uint8
	åtkomst			uint8
	gränsHögochFlaggor	uint8
	baseHög			uint8
}

func (e *Gdtpost_2) IsAnsluten() bool {
	return e.åtkomst&Ansluten != 0
}

func (e *Gdtpost_2) Fill(base uint32, gräns uint32, åtkomst uint8, flaggor uint8) {
	e.gränsHögochFlaggor = uint8((gräns >> 16) & 0x000F)
	e.gränsHögochFlaggor |= flaggor
	e.åtkomst = åtkomst
	e.basemid = uint8(base >> 16)
	e.baseHög = uint8(base >> 24)
	e.baseLåg = uint16(base & 0xFFFF)
	e.gränsLåg = uint16(gräns & 0x0000FFFF)
}

func (e *Gdtpost_2) Töm() {
	e.gränsHögochFlaggor = 0
	e.åtkomst = 0
	e.basemid = 0
	e.baseHög = 0
	e.baseLåg = 0
	e.gränsLåg = 0

}

type Gdtdescriptor struct {
	GdtStorlek	uint16
	GdtAdressLåg	uint16
	GdtAdressHög	uint16
}
type Användaredescriptor struct {
	PostNummer	uint32
	BaseAdress	uint32
	Gräns		uint32
	Flaggor		uint8
}

func Mängdtlssegment(index uint32, descriptor *Användaredescriptor, tabell []Gdtpost_2) bool {
	if index < TlsStarta || index > uint32(len(gdtTabell)) {
		return false
	}

	if descriptor.Flaggor == Udescrxonly|UdescsegnotAnsluten {

		tabell[index].Töm()
		return true
	}

	flaggor := uint8(Seggranbyte)
	if descriptor.Flaggor&UdescGränsipages != 0 {
		flaggor = Seggran4kSida
	}
	åtkomst := uint8(PrivAnvändare | SegNormalt | Ansluten)
	if descriptor.Flaggor&Udescrxonly != 0 {
		åtkomst |= SegKör
	} else {
		åtkomst |= Segw
	}
	if åtkomst&SegNormalt != 0 {
		flaggor |= SegbigLÄGE
	}

	tabell[index].Fill(descriptor.BaseAdress, descriptor.Gräns, åtkomst, flaggor)
	flushtlsTabell(tabell)

	return true
}

func flushtlsTabell(tabell []Gdtpost_2) {
	copy(gdtTabell[TlsStarta:], tabell[TlsStarta:])
}
func FlushtlsTabell(tabell []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsStarta:], tabell[TlsStarta:])
}
