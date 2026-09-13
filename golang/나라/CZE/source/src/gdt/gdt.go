package gdt

import . "unsafe"
import "reflect"
import . "konzole"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUživatelcode	uint32	= 0x23
	SegUživateldata	uint32	= 0x2B
	SegUživatelgs	uint32	= 0x33
	SegÚlohaStav	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	omezeníNízká_2		uint16
	baseNízká_2		uint16
	baseVysoká_2		uint8
	typ_2			uint8
	příznakyOmezeníVysoká	uint8
	baseveryVysoká		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, omezení_2 uint32, typ_2 uint8, příznaky_2 uint8) {

	self_2.baseNízká_2 = uint16(base_2 & 0xFFFF)
	self_2.baseVysoká_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryVysoká = uint8((base_2 >> 24) & 0xFF)

	self_2.omezeníNízká_2 = uint16(omezení_2 & 0xFFFF)
	self_2.příznakyOmezeníVysoká = uint8((omezení_2 >> 24) & 0x0F)
	self_2.příznakyOmezeníVysoká |= (příznaky_2 & 0xF0)

	self_2.typ_2 = typ_2

}

type TShareddescriptorTabulkadata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabulkadata

type TShareddescriptorTabulka struct {
}

func (self_2 *TShareddescriptorTabulka) Init() {

	var gdtZáznam TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtAdresa := uintptr(uint32(gdtdescriptor.GdtAdresaNízká) |
		uint32(gdtdescriptor.GdtAdresaVysoká)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVelikost+1) / Sizeof(gdtZáznam))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtAdresa,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	cíl_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseAdresa := (*uint32)(Pointer(&cíl_3[2]))
	(*baseAdresa) = uint32(uintptr(Pointer(&data_2)))

	velikost_2 := (*uint16)(Pointer(&cíl_3[0]))
	(*velikost_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&cíl_3)))

	terminal := new(TKonzole)
	terminal.MTisknoutxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorTabulka) Nastavitdescriptor(idx int, base_2 uint32, omezení_2 uint32, typ_2 uint8, příznaky_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, omezení_2, typ_2, příznaky_2)
}

const (
	KcsRejstřík	= 1
	KdsRejstřík	= 2
	KgsRejstřík	= 3

	Kcsselector	= KcsRejstřík * 8
	Kdsselector	= KdsRejstřík * 8
	Kgsselector	= KgsRejstřík * 8

	Seggranbyte		= 0 << 7
	Seggran4kStránka	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSystém	= 0 << 4
	SegNormální	= 1 << 4

	Segnoexec	= 0 << 3
	SegVykonání	= 1 << 3

	Privkernel	= 0 << 5
	PrivUživatel	= 3 << 5

	SegbigMÓD	= 1 << 6

	Současný	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescObsah		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescOmezeníVstuppages	= 1 << 4
	UdescsegnotSoučasný	= 1 << 5
	Udescusable		= 1 << 6

	GdtZáznam	= 256
	TlsSpustit	= 16
)

var (
	gdtTabulka	= [GdtZáznam]GdtZáznam_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabulkalen	= 0
)

type GdtZáznam_2 struct {
	omezeníNízká		uint16
	baseNízká		uint16
	basemid			uint8
	přístup			uint8
	omezeníVysokáaPříznaky	uint8
	baseVysoká		uint8
}

func (e *GdtZáznam_2) IsSoučasný() bool {
	return e.přístup&Současný != 0
}

func (e *GdtZáznam_2) Fill(base uint32, omezení uint32, přístup uint8, příznaky uint8) {
	e.omezeníVysokáaPříznaky = uint8((omezení >> 16) & 0x000F)
	e.omezeníVysokáaPříznaky |= příznaky
	e.přístup = přístup
	e.basemid = uint8(base >> 16)
	e.baseVysoká = uint8(base >> 24)
	e.baseNízká = uint16(base & 0xFFFF)
	e.omezeníNízká = uint16(omezení & 0x0000FFFF)
}

func (e *GdtZáznam_2) Vyčistit() {
	e.omezeníVysokáaPříznaky = 0
	e.přístup = 0
	e.basemid = 0
	e.baseVysoká = 0
	e.baseNízká = 0
	e.omezeníNízká = 0

}

type Gdtdescriptor struct {
	GdtVelikost	uint16
	GdtAdresaNízká	uint16
	GdtAdresaVysoká	uint16
}
type Uživateldescriptor struct {
	ZáznamČíslo	uint32
	BaseAdresa	uint32
	Omezení		uint32
	Příznaky	uint8
}

func Nastavittlssegment(rejstřík uint32, descriptor *Uživateldescriptor, tabulka []GdtZáznam_2) bool {
	if rejstřík < TlsSpustit || rejstřík > uint32(len(gdtTabulka)) {
		return false
	}

	if descriptor.Příznaky == Udescrxonly|UdescsegnotSoučasný {

		tabulka[rejstřík].Vyčistit()
		return true
	}

	příznaky := uint8(Seggranbyte)
	if descriptor.Příznaky&UdescOmezeníVstuppages != 0 {
		příznaky = Seggran4kStránka
	}
	přístup := uint8(PrivUživatel | SegNormální | Současný)
	if descriptor.Příznaky&Udescrxonly != 0 {
		přístup |= SegVykonání
	} else {
		přístup |= Segw
	}
	if přístup&SegNormální != 0 {
		příznaky |= SegbigMÓD
	}

	tabulka[rejstřík].Fill(descriptor.BaseAdresa, descriptor.Omezení, přístup, příznaky)
	flushtlsTabulka(tabulka)

	return true
}

func flushtlsTabulka(tabulka []GdtZáznam_2) {
	copy(gdtTabulka[TlsSpustit:], tabulka[TlsSpustit:])
}
func FlushtlsTabulka(tabulka []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsSpustit:], tabulka[TlsSpustit:])
}
