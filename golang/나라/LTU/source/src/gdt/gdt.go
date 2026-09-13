package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegNaudotojascode	uint32	= 0x23
	SegNaudotojasdata	uint32	= 0x2B
	SegNaudotojasgs		uint32	= 0x33
	SegUžduotisBūsena	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ribaŽemas_2		uint16
	baseŽemas_2		uint16
	baseAukštas_2		uint8
	tipas			uint8
	parametraiRibaAukštas	uint8
	baseveryAukštas		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, riba_2 uint32, tipas uint8, parametrai_3 uint8) {

	self_2.baseŽemas_2 = uint16(base_2 & 0xFFFF)
	self_2.baseAukštas_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryAukštas = uint8((base_2 >> 24) & 0xFF)

	self_2.ribaŽemas_2 = uint16(riba_2 & 0xFFFF)
	self_2.parametraiRibaAukštas = uint8((riba_2 >> 24) & 0x0F)
	self_2.parametraiRibaAukštas |= (parametrai_3 & 0xF0)

	self_2.tipas = tipas

}

type TShareddescriptorLentelėdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorLentelėdata

type TShareddescriptorLentelė struct {
}

func (self_2 *TShareddescriptorLentelė) Init() {

	var gdtįrašas TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressŽemas) |
		uint32(gdtdescriptor.GdtaddressAukštas)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtDydis+1) / Sizeof(gdtįrašas))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	tikslas_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&tikslas_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	dydis_2 := (*uint16)(Pointer(&tikslas_3[0]))
	(*dydis_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&tikslas_3)))

	terminal := new(TConsole)
	terminal.MSpausdintixy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorLentelė) Nustatytadescriptor(idx int, base_2 uint32, riba_2 uint32, tipas uint8, parametrai_3 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, riba_2, tipas, parametrai_3)
}

const (
	KcsRodyklė	= 1
	KdsRodyklė	= 2
	KgsRodyklė	= 3

	Kcsselector	= KcsRodyklė * 8
	Kdsselector	= KdsRodyklė * 8
	Kgsselector	= KgsRodyklė * 8

	Seggranbyte		= 0 << 7
	Seggran4kPuslapis	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistema	= 0 << 4
	SegNormalus	= 1 << 4

	Segnoexec	= 0 << 3
	SegVykdyti	= 1 << 3

	Privkernel	= 0 << 5
	PrivNaudotojas	= 3 << 5

	SegbigREŽIMAS	= 1 << 6

	Yra	= 1 << 7

	Udesc32seg	= 1 << 0
	UdescTurinys	= 3 << 1
	Udescrxonly	= 1 << 3
	UdescRibaĮpages	= 1 << 4
	UdescsegnotYra	= 1 << 5
	Udescusable	= 1 << 6

	Gdtįrašas	= 256
	TlsPaleisti	= 16
)

var (
	gdtLentelė	= [Gdtįrašas]Gdtįrašas_2{}
	gdtdescriptor	Gdtdescriptor
	gdtLentelėlen	= 0
)

type Gdtįrašas_2 struct {
	ribaŽemas		uint16
	baseŽemas		uint16
	basemid			uint8
	prieiti			uint8
	ribaAukštasirParametrai	uint8
	baseAukštas		uint8
}

func (e *Gdtįrašas_2) IsYra() bool {
	return e.prieiti&Yra != 0
}

func (e *Gdtįrašas_2) Fill(base uint32, riba uint32, prieiti uint8, parametrai uint8) {
	e.ribaAukštasirParametrai = uint8((riba >> 16) & 0x000F)
	e.ribaAukštasirParametrai |= parametrai
	e.prieiti = prieiti
	e.basemid = uint8(base >> 16)
	e.baseAukštas = uint8(base >> 24)
	e.baseŽemas = uint16(base & 0xFFFF)
	e.ribaŽemas = uint16(riba & 0x0000FFFF)
}

func (e *Gdtįrašas_2) Išvalyti() {
	e.ribaAukštasirParametrai = 0
	e.prieiti = 0
	e.basemid = 0
	e.baseAukštas = 0
	e.baseŽemas = 0
	e.ribaŽemas = 0

}

type Gdtdescriptor struct {
	GdtDydis		uint16
	GdtaddressŽemas		uint16
	GdtaddressAukštas	uint16
}
type Naudotojasdescriptor struct {
	ĮrašasSkaičius	uint32
	Baseaddress	uint32
	Riba		uint32
	Parametrai	uint8
}

func Nustatytatlssegment(rodyklė uint32, descriptor *Naudotojasdescriptor, lentelė []Gdtįrašas_2) bool {
	if rodyklė < TlsPaleisti || rodyklė > uint32(len(gdtLentelė)) {
		return false
	}

	if descriptor.Parametrai == Udescrxonly|UdescsegnotYra {

		lentelė[rodyklė].Išvalyti()
		return true
	}

	parametrai := uint8(Seggranbyte)
	if descriptor.Parametrai&UdescRibaĮpages != 0 {
		parametrai = Seggran4kPuslapis
	}
	prieiti := uint8(PrivNaudotojas | SegNormalus | Yra)
	if descriptor.Parametrai&Udescrxonly != 0 {
		prieiti |= SegVykdyti
	} else {
		prieiti |= Segw
	}
	if prieiti&SegNormalus != 0 {
		parametrai |= SegbigREŽIMAS
	}

	lentelė[rodyklė].Fill(descriptor.Baseaddress, descriptor.Riba, prieiti, parametrai)
	flushtlsLentelė(lentelė)

	return true
}

func flushtlsLentelė(lentelė []Gdtįrašas_2) {
	copy(gdtLentelė[TlsPaleisti:], lentelė[TlsPaleisti:])
}
func FlushtlsLentelė(lentelė []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsPaleisti:], lentelė[TlsPaleisti:])
}
