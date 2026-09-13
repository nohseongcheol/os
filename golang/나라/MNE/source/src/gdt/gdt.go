package gdt

import . "unsafe"
import "reflect"
import . "конзола"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKorisnikcode	uint32	= 0x23
	SegKorisnikdata	uint32	= 0x2B
	SegKorisnikgs	uint32	= 0x33
	SegЗадатакСтање	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ограничиTiho_2		uint16
	baseTiho_2		uint16
	baseВисока_2		uint8
	врста_2			uint8
	parametriОграничиВисока	uint8
	baseveryВисока		uint8
}

func (isti_2 *TSegmentdescriptor) Init(base_2 uint32, ограничи_2 uint32, врста_2 uint8, parametri_2 uint8) {

	isti_2.baseTiho_2 = uint16(base_2 & 0xFFFF)
	isti_2.baseВисока_2 = uint8((base_2 >> 16) & 0xFF)
	isti_2.baseveryВисока = uint8((base_2 >> 24) & 0xFF)

	isti_2.ограничиTiho_2 = uint16(ограничи_2 & 0xFFFF)
	isti_2.parametriОграничиВисока = uint8((ограничи_2 >> 24) & 0x0F)
	isti_2.parametriОграничиВисока |= (parametri_2 & 0xF0)

	isti_2.врста_2 = врста_2

}

type TShareddescriptorTabeladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeladata

type TShareddescriptorTabela struct {
}

func (isti_2 *TShareddescriptorTabela) Init() {

	var gdtунос TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressTiho) |
		uint32(gdtdescriptor.GdtaddressВисока)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtВеличина+1) / Sizeof(gdtунос))
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

	величина_2 := (*uint16)(Pointer(&odredište_3[0]))
	(*величина_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&odredište_3)))

	terminal := new(TКонзола)
	terminal.MŠtampajxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (isti_2 *TShareddescriptorTabela) Скупdescriptor(idx int, base_2 uint32, ограничи_2 uint32, врста_2 uint8, parametri_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ограничи_2, врста_2, parametri_2)
}

const (
	KcsPopis	= 1
	KdsPopis	= 2
	KgsPopis	= 3

	Kcsselector	= KcsPopis * 8
	Kdsselector	= KdsPopis * 8
	Kgsselector	= KgsPopis * 8

	Seggranbyte	= 0 << 7
	Seggran4klist	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистем	= 0 << 4
	Segобичне	= 1 << 4

	Segnoexec	= 0 << 3
	Segizvršna	= 1 << 3

	Privkernel	= 0 << 5
	PrivKorisnik	= 3 << 5

	SegbigREŽIM	= 1 << 6

	Prisutno	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescСадржај			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescОграничиПримљеноpages	= 1 << 4
	UdescsegnotPrisutno		= 1 << 5
	Udescusable			= 1 << 6

	Gdtунос		= 256
	TlsPokreni	= 16
)

var (
	gdtTabela	= [Gdtунос]Gdtунос_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelalen	= 0
)

type Gdtунос_2 struct {
	ограничиTiho			uint16
	baseTiho			uint16
	basemid				uint8
	приступање			uint8
	ограничиВисокаandParametri	uint8
	baseВисока			uint8
}

func (e *Gdtунос_2) IsPrisutno() bool {
	return e.приступање&Prisutno != 0
}

func (e *Gdtунос_2) Fill(base uint32, ограничи uint32, приступање uint8, parametri uint8) {
	e.ограничиВисокаandParametri = uint8((ограничи >> 16) & 0x000F)
	e.ограничиВисокаandParametri |= parametri
	e.приступање = приступање
	e.basemid = uint8(base >> 16)
	e.baseВисока = uint8(base >> 24)
	e.baseTiho = uint16(base & 0xFFFF)
	e.ограничиTiho = uint16(ограничи & 0x0000FFFF)
}

func (e *Gdtунос_2) Очисти() {
	e.ограничиВисокаandParametri = 0
	e.приступање = 0
	e.basemid = 0
	e.baseВисока = 0
	e.baseTiho = 0
	e.ограничиTiho = 0

}

type Gdtdescriptor struct {
	GdtВеличина		uint16
	GdtaddressTiho		uint16
	GdtaddressВисока	uint16
}
type Korisnikdescriptor struct {
	Уносброј	uint32
	Baseaddress	uint32
	Ограничи	uint32
	Parametri	uint8
}

func Скупtlssegment(popis uint32, descriptor *Korisnikdescriptor, tabela []Gdtунос_2) bool {
	if popis < TlsPokreni || popis > uint32(len(gdtTabela)) {
		return false
	}

	if descriptor.Parametri == Udescrxonly|UdescsegnotPrisutno {

		tabela[popis].Очисти()
		return true
	}

	parametri := uint8(Seggranbyte)
	if descriptor.Parametri&UdescОграничиПримљеноpages != 0 {
		parametri = Seggran4klist
	}
	приступање := uint8(PrivKorisnik | Segобичне | Prisutno)
	if descriptor.Parametri&Udescrxonly != 0 {
		приступање |= Segizvršna
	} else {
		приступање |= Segw
	}
	if приступање&Segобичне != 0 {
		parametri |= SegbigREŽIM
	}

	tabela[popis].Fill(descriptor.Baseaddress, descriptor.Ограничи, приступање, parametri)
	flushtlsTabela(tabela)

	return true
}

func flushtlsTabela(tabela []Gdtунос_2) {
	copy(gdtTabela[TlsPokreni:], tabela[TlsPokreni:])
}
func FlushtlsTabela(tabela []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsPokreni:], tabela[TlsPokreni:])
}
