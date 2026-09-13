package gdt

import . "unsafe"
import "reflect"
import . "konzola"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKorisnikcode	uint32	= 0x23
	SegKorisnikdata	uint32	= 0x2B
	SegKorisnikgs	uint32	= 0x33
	SegZadatakStanje	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ograničiTiho_2		uint16
	baseTiho_2		uint16
	baseVisoka_2		uint8
	vrsta_2			uint8
	parametriOgraničiVisoka	uint8
	baseveryVisoka		uint8
}

func (isti_2 *TSegmentdescriptor) Init(base_2 uint32, ograniči_2 uint32, vrsta_2 uint8, parametri_3 uint8) {

	isti_2.baseTiho_2 = uint16(base_2 & 0xFFFF)
	isti_2.baseVisoka_2 = uint8((base_2 >> 16) & 0xFF)
	isti_2.baseveryVisoka = uint8((base_2 >> 24) & 0xFF)

	isti_2.ograničiTiho_2 = uint16(ograniči_2 & 0xFFFF)
	isti_2.parametriOgraničiVisoka = uint8((ograniči_2 >> 24) & 0x0F)
	isti_2.parametriOgraničiVisoka |= (parametri_3 & 0xF0)

	isti_2.vrsta_2 = vrsta_2

}

type TShareddescriptorTabeladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeladata

type TShareddescriptorTabela struct {
}

func (isti_2 *TShareddescriptorTabela) Init() {

	var gdtunos TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressTiho) |
		uint32(gdtdescriptor.GdtaddressVisoka)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVeličina+1) / Sizeof(gdtunos))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	odredište_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&odredište_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	veličina_2 := (*uint16)(Pointer(&odredište_3[0]))
	(*veličina_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&odredište_3)))

	terminal := new(TKonzola)
	terminal.MŠtampajxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (isti_2 *TShareddescriptorTabela) Skupdescriptor(idx int, base_2 uint32, ograniči_2 uint32, vrsta_2 uint8, parametri_3 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ograniči_2, vrsta_2, parametri_3)
}

const (
	KcsPopis	= 1
	KdsPopis	= 2
	KgsPopis	= 3

	Kcsselector	= KcsPopis * 8
	Kdsselector	= KdsPopis * 8
	Kgsselector	= KgsPopis * 8

	Seggranbyte	= 0 << 7
	Seggran4kSTRANA	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	Segobične	= 1 << 4

	Segnoexec	= 0 << 3
	Segizvršna	= 1 << 3

	Privkernel	= 0 << 5
	PrivKorisnik	= 3 << 5

	SegbigREŽIM	= 1 << 6

	Prisutna	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSadržaj			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescOgraničiPrimljenopages	= 1 << 4
	UdescsegnotPrisutna		= 1 << 5
	Udescusable			= 1 << 6

	Gdtunos		= 256
	TlsPokreni	= 16
)

var (
	gdtTabela	= [Gdtunos]Gdtunos_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelalen	= 0
)

type Gdtunos_2 struct {
	ograničiTiho			uint16
	baseTiho			uint16
	basemid				uint8
	pristupanje			uint8
	ograničiVisokaandParametri	uint8
	baseVisoka			uint8
}

func (e *Gdtunos_2) IsPrisutna() bool {
	return e.pristupanje&Prisutna != 0
}

func (e *Gdtunos_2) Fill(base uint32, ograniči uint32, pristupanje uint8, parametri uint8) {
	e.ograničiVisokaandParametri = uint8((ograniči >> 16) & 0x000F)
	e.ograničiVisokaandParametri |= parametri
	e.pristupanje = pristupanje
	e.basemid = uint8(base >> 16)
	e.baseVisoka = uint8(base >> 24)
	e.baseTiho = uint16(base & 0xFFFF)
	e.ograničiTiho = uint16(ograniči & 0x0000FFFF)
}

func (e *Gdtunos_2) Očisti() {
	e.ograničiVisokaandParametri = 0
	e.pristupanje = 0
	e.basemid = 0
	e.baseVisoka = 0
	e.baseTiho = 0
	e.ograničiTiho = 0

}

type Gdtdescriptor struct {
	GdtVeličina		uint16
	GdtaddressTiho		uint16
	GdtaddressVisoka	uint16
}
type Korisnikdescriptor struct {
	Unosbroj	uint32
	Baseaddress	uint32
	Ograniči	uint32
	Parametri	uint8
}

func Skuptlssegment(popis uint32, descriptor *Korisnikdescriptor, tabela []Gdtunos_2) bool {
	if popis < TlsPokreni || popis > uint32(len(gdtTabela)) {
		return false
	}

	if descriptor.Parametri == Udescrxonly|UdescsegnotPrisutna {

		tabela[popis].Očisti()
		return true
	}

	parametri := uint8(Seggranbyte)
	if descriptor.Parametri&UdescOgraničiPrimljenopages != 0 {
		parametri = Seggran4kSTRANA
	}
	pristupanje := uint8(PrivKorisnik | Segobične | Prisutna)
	if descriptor.Parametri&Udescrxonly != 0 {
		pristupanje |= Segizvršna
	} else {
		pristupanje |= Segw
	}
	if pristupanje&Segobične != 0 {
		parametri |= SegbigREŽIM
	}

	tabela[popis].Fill(descriptor.Baseaddress, descriptor.Ograniči, pristupanje, parametri)
	flushtlsTabela(tabela)

	return true
}

func flushtlsTabela(tabela []Gdtunos_2) {
	copy(gdtTabela[TlsPokreni:], tabela[TlsPokreni:])
}
func FlushtlsTabela(tabela []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsPokreni:], tabela[TlsPokreni:])
}
