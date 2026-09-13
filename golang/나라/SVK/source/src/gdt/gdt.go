package gdt

import . "unsafe"
import "reflect"
import . "konzola"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegPoužívateľcode	uint32	= 0x23
	SegPoužívateľdata	uint32	= 0x2B
	SegPoužívateľgs		uint32	= 0x33
	SegUlohaStav		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	obmedzenieNízka_2		uint16
	baseNízka_2			uint16
	baseVysoká_2			uint8
	typ_2				uint8
	príznakyObmedzenieVysoká	uint8
	baseveryVysoká			uint8
}

func (vlastný_2 *TSegmentdescriptor) Init(base_2 uint32, obmedzenie_2 uint32, typ_2 uint8, príznaky_2 uint8) {

	vlastný_2.baseNízka_2 = uint16(base_2 & 0xFFFF)
	vlastný_2.baseVysoká_2 = uint8((base_2 >> 16) & 0xFF)
	vlastný_2.baseveryVysoká = uint8((base_2 >> 24) & 0xFF)

	vlastný_2.obmedzenieNízka_2 = uint16(obmedzenie_2 & 0xFFFF)
	vlastný_2.príznakyObmedzenieVysoká = uint8((obmedzenie_2 >> 24) & 0x0F)
	vlastný_2.príznakyObmedzenieVysoká |= (príznaky_2 & 0xF0)

	vlastný_2.typ_2 = typ_2

}

type TShareddescriptorTabuľkadata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabuľkadata

type TShareddescriptorTabuľka struct {
}

func (vlastný_2 *TShareddescriptorTabuľka) Init() {

	var gdtpoložka TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressNízka) |
		uint32(gdtdescriptor.GdtaddressVysoká)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVeľkosť+1) / Sizeof(gdtpoložka))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	cieľ_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&cieľ_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	veľkosť_2 := (*uint16)(Pointer(&cieľ_3[0]))
	(*veľkosť_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&cieľ_3)))

	terminal := new(TKonzola)
	terminal.MTlačiťxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (vlastný_2 *TShareddescriptorTabuľka) Sadadescriptor(idx int, base_2 uint32, obmedzenie_2 uint32, typ_2 uint8, príznaky_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, obmedzenie_2, typ_2, príznaky_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kSTRANA	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSystém	= 0 << 4
	SegNormálna	= 1 << 4

	Segnoexec	= 0 << 3
	SegSpúšťanie	= 1 << 3

	Privkernel	= 0 << 5
	PrivPoužívateľ	= 3 << 5

	Segbigrežim	= 1 << 6

	Prítomné	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescObsah		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescObmedzenienaStrany	= 1 << 4
	UdescsegnotPrítomné	= 1 << 5
	Udescusable		= 1 << 6

	Gdtpoložka	= 256
	TlsSpustiť	= 16
)

var (
	gdtTabuľka	= [Gdtpoložka]Gdtpoložka_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabuľkalen	= 0
)

type Gdtpoložka_2 struct {
	obmedzenieNízka			uint16
	baseNízka			uint16
	basemid				uint8
	prístup				uint8
	obmedzenieVysokáaPríznaky	uint8
	baseVysoká			uint8
}

func (e *Gdtpoložka_2) IsPrítomné() bool {
	return e.prístup&Prítomné != 0
}

func (e *Gdtpoložka_2) Fill(base uint32, obmedzenie uint32, prístup uint8, príznaky uint8) {
	e.obmedzenieVysokáaPríznaky = uint8((obmedzenie >> 16) & 0x000F)
	e.obmedzenieVysokáaPríznaky |= príznaky
	e.prístup = prístup
	e.basemid = uint8(base >> 16)
	e.baseVysoká = uint8(base >> 24)
	e.baseNízka = uint16(base & 0xFFFF)
	e.obmedzenieNízka = uint16(obmedzenie & 0x0000FFFF)
}

func (e *Gdtpoložka_2) Vyčistiť() {
	e.obmedzenieVysokáaPríznaky = 0
	e.prístup = 0
	e.basemid = 0
	e.baseVysoká = 0
	e.baseNízka = 0
	e.obmedzenieNízka = 0

}

type Gdtdescriptor struct {
	GdtVeľkosť		uint16
	GdtaddressNízka		uint16
	GdtaddressVysoká	uint16
}
type Používateľdescriptor struct {
	PoložkaČíslo	uint32
	Baseaddress	uint32
	Obmedzenie	uint32
	Príznaky	uint8
}

func Sadatlssegment(index uint32, descriptor *Používateľdescriptor, tabuľka []Gdtpoložka_2) bool {
	if index < TlsSpustiť || index > uint32(len(gdtTabuľka)) {
		return false
	}

	if descriptor.Príznaky == Udescrxonly|UdescsegnotPrítomné {

		tabuľka[index].Vyčistiť()
		return true
	}

	príznaky := uint8(Seggranbyte)
	if descriptor.Príznaky&UdescObmedzenienaStrany != 0 {
		príznaky = Seggran4kSTRANA
	}
	prístup := uint8(PrivPoužívateľ | SegNormálna | Prítomné)
	if descriptor.Príznaky&Udescrxonly != 0 {
		prístup |= SegSpúšťanie
	} else {
		prístup |= Segw
	}
	if prístup&SegNormálna != 0 {
		príznaky |= Segbigrežim
	}

	tabuľka[index].Fill(descriptor.Baseaddress, descriptor.Obmedzenie, prístup, príznaky)
	flushtlsTabuľka(tabuľka)

	return true
}

func flushtlsTabuľka(tabuľka []Gdtpoložka_2) {
	copy(gdtTabuľka[TlsSpustiť:], tabuľka[TlsSpustiť:])
}
func FlushtlsTabuľka(tabuľka []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsSpustiť:], tabuľka[TlsSpustiť:])
}
