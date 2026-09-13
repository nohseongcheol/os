package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUtilizatorcode	uint32	= 0x23
	SegUtilizatordata	uint32	= 0x2B
	SegUtilizatorgs		uint32	= 0x33
	SegtaskStare		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limităScăzută_2			uint16
	baseScăzută_2			uint16
	baseRidicată_2			uint8
	tip				uint8
	indicatoriLimităRidicată	uint8
	baseveryRidicată		uint8
}

func (sine_2 *TSegmentdescriptor) Init(base_2 uint32, limită_2 uint32, tip uint8, indicatori_2 uint8) {

	sine_2.baseScăzută_2 = uint16(base_2 & 0xFFFF)
	sine_2.baseRidicată_2 = uint8((base_2 >> 16) & 0xFF)
	sine_2.baseveryRidicată = uint8((base_2 >> 24) & 0xFF)

	sine_2.limităScăzută_2 = uint16(limită_2 & 0xFFFF)
	sine_2.indicatoriLimităRidicată = uint8((limită_2 >> 24) & 0x0F)
	sine_2.indicatoriLimităRidicată |= (indicatori_2 & 0xF0)

	sine_2.tip = tip

}

type TShareddescriptorTabeldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeldata

type TShareddescriptorTabel struct {
}

func (sine_2 *TShareddescriptorTabel) Init() {

	var gdtînregistrare TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressScăzută) |
		uint32(gdtdescriptor.GdtaddressRidicată)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtMărime+1) / Sizeof(gdtînregistrare))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destinație_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destinație_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	mărime_2 := (*uint16)(Pointer(&destinație_3[0]))
	(*mărime_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destinație_3)))

	terminal := new(TConsole)
	terminal.MTipăreștexy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (sine_2 *TShareddescriptorTabel) Definitdescriptor(idx int, base_2 uint32, limită_2 uint32, tip uint8, indicatori_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limită_2, tip, indicatori_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kPAGINĂ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	SegNormală	= 1 << 4

	Segnoexec	= 0 << 3
	SegExecuție	= 1 << 3

	Privkernel	= 0 << 5
	PrivUtilizator	= 3 << 5

	SegbigMOD	= 1 << 6

	Prezent	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescConținut		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescLimităIntrarepages	= 1 << 4
	UdescsegnotPrezent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtînregistrare	= 256
	TlsPornește	= 16
)

var (
	gdtTabel	= [Gdtînregistrare]Gdtînregistrare_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellen	= 0
)

type Gdtînregistrare_2 struct {
	limităScăzută			uint16
	baseScăzută			uint16
	basemid				uint8
	acces				uint8
	limităRidicatășiIndicatori	uint8
	baseRidicată			uint8
}

func (e *Gdtînregistrare_2) IsPrezent() bool {
	return e.acces&Prezent != 0
}

func (e *Gdtînregistrare_2) Fill(base uint32, limită uint32, acces uint8, indicatori uint8) {
	e.limităRidicatășiIndicatori = uint8((limită >> 16) & 0x000F)
	e.limităRidicatășiIndicatori |= indicatori
	e.acces = acces
	e.basemid = uint8(base >> 16)
	e.baseRidicată = uint8(base >> 24)
	e.baseScăzută = uint16(base & 0xFFFF)
	e.limităScăzută = uint16(limită & 0x0000FFFF)
}

func (e *Gdtînregistrare_2) Golește() {
	e.limităRidicatășiIndicatori = 0
	e.acces = 0
	e.basemid = 0
	e.baseRidicată = 0
	e.baseScăzută = 0
	e.limităScăzută = 0

}

type Gdtdescriptor struct {
	GdtMărime		uint16
	GdtaddressScăzută	uint16
	GdtaddressRidicată	uint16
}
type Utilizatordescriptor struct {
	ÎnregistrareNumăr	uint32
	Baseaddress		uint32
	Limită			uint32
	Indicatori		uint8
}

func Definittlssegment(index uint32, descriptor *Utilizatordescriptor, tabel []Gdtînregistrare_2) bool {
	if index < TlsPornește || index > uint32(len(gdtTabel)) {
		return false
	}

	if descriptor.Indicatori == Udescrxonly|UdescsegnotPrezent {

		tabel[index].Golește()
		return true
	}

	indicatori := uint8(Seggranbyte)
	if descriptor.Indicatori&UdescLimităIntrarepages != 0 {
		indicatori = Seggran4kPAGINĂ
	}
	acces := uint8(PrivUtilizator | SegNormală | Prezent)
	if descriptor.Indicatori&Udescrxonly != 0 {
		acces |= SegExecuție
	} else {
		acces |= Segw
	}
	if acces&SegNormală != 0 {
		indicatori |= SegbigMOD
	}

	tabel[index].Fill(descriptor.Baseaddress, descriptor.Limită, acces, indicatori)
	flushtlsTabel(tabel)

	return true
}

func flushtlsTabel(tabel []Gdtînregistrare_2) {
	copy(gdtTabel[TlsPornește:], tabel[TlsPornește:])
}
func FlushtlsTabel(tabel []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsPornește:], tabel[TlsPornește:])
}
