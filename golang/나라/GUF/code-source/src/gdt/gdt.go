package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segnoyaucode	uint32	= 0x08
	Segnoyaudonnées	uint32	= 0x10
	Segnoyaugs	uint32	= 0x18

	Segutilisateurcode	uint32	= 0x23
	Segutilisateurdonnées	uint32	= 0x2B
	Segutilisateurgs	uint32	= 0x33
	SegtâcheÉtat		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limiteBasse_2		uint16
	baseBasse_2		uint16
	baseÉlevée_2		uint8
	typeValeur_2		uint8
	attributsLimiteÉlevée	uint8
	baseveryÉlevée		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limite_2 uint32, typeValeur_2 uint8, attributs_3 uint8) {

	self_2.baseBasse_2 = uint16(base_2 & 0xFFFF)
	self_2.baseÉlevée_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryÉlevée = uint8((base_2 >> 24) & 0xFF)

	self_2.limiteBasse_2 = uint16(limite_2 & 0xFFFF)
	self_2.attributsLimiteÉlevée = uint8((limite_2 >> 24) & 0x0F)
	self_2.attributsLimiteÉlevée |= (attributs_3 & 0xF0)

	self_2.typeValeur_2 = typeValeur_2

}

type TShareddescriptorTableaudonnées struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var données_2 TShareddescriptorTableaudonnées

type TShareddescriptorTableau struct {
}

func (self_2 *TShareddescriptorTableau) Init() {

	var gdtélément TSegmentdescriptor

	gdtdescriptor = *getgdt()
	vieuxgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressBasse) |
		uint32(gdtdescriptor.GdtaddressÉlevée)<<16)
	vieuxgdtlen := int(uintptr(gdtdescriptor.GdtTaille+1) / Sizeof(gdtélément))
	vieuxgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	vieuxgdtlen,
		Cap:	vieuxgdtlen,
		Data:	vieuxgdtaddress,
	}))
	copy(données_2.segmentdescriptor[:], vieuxgdt)

	données_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	données_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	données_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&données_2)))

	taille_2 := (*uint16)(Pointer(&destination_3[0]))
	(*taille_2) = (uint16)((Sizeof(données_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MImprimerxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(&données_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorTableau) Ensembledescriptor(idx int, base_2 uint32, limite_2 uint32, typeValeur_2 uint8, attributs_3 uint8) {
	données_2.segmentdescriptor[idx].Init(base_2, limite_2, typeValeur_2, attributs_3)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranoctet	= 0 << 7
	Seggran4kpage	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystème	= 0 << 4
	SegNormale	= 1 << 4

	Segnoexec	= 0 << 3
	SegExécution	= 1 << 3

	Privnoyau	= 0 << 5
	Privutilisateur	= 3 << 5

	SegÉlevémode	= 1 << 6

	Présente	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSommaire			= 3 << 1
	Udescrxseulement		= 1 << 3
	UdescLimiteEntrantepages	= 1 << 4
	UdescsegNonPrésente		= 1 << 5
	Udescusable			= 1 << 6

	Gdtélément	= 256
	TlsDémarrer	= 16
)

var (
	gdtTableau	= [Gdtélément]Gdtélément_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTableaulen	= 0
)

type Gdtélément_2 struct {
	limiteBasse		uint16
	baseBasse		uint16
	basemid			uint8
	accès			uint8
	limiteÉlevéeetAttributs	uint8
	baseÉlevée		uint8
}

func (e *Gdtélément_2) IsPrésente() bool {
	return e.accès&Présente != 0
}

func (e *Gdtélément_2) Fill(base uint32, limite uint32, accès uint8, attributs_2 uint8) {
	e.limiteÉlevéeetAttributs = uint8((limite >> 16) & 0x000F)
	e.limiteÉlevéeetAttributs |= attributs_2
	e.accès = accès
	e.basemid = uint8(base >> 16)
	e.baseÉlevée = uint8(base >> 24)
	e.baseBasse = uint16(base & 0xFFFF)
	e.limiteBasse = uint16(limite & 0x0000FFFF)
}

func (e *Gdtélément_2) Effacer() {
	e.limiteÉlevéeetAttributs = 0
	e.accès = 0
	e.basemid = 0
	e.baseÉlevée = 0
	e.baseBasse = 0
	e.limiteBasse = 0

}

type Gdtdescriptor struct {
	GdtTaille		uint16
	GdtaddressBasse		uint16
	GdtaddressÉlevée	uint16
}
type Utilisateurdescriptor struct {
	ÉlémentNombre	uint32
	Baseaddress	uint32
	Limite		uint32
	Attributs	uint8
}

func Ensembletlssegment(index uint32, descriptor *Utilisateurdescriptor, tableau_2 []Gdtélément_2) bool {
	if index < TlsDémarrer || index > uint32(len(gdtTableau)) {
		return false
	}

	if descriptor.Attributs == Udescrxseulement|UdescsegNonPrésente {

		tableau_2[index].Effacer()
		return true
	}

	attributs_2 := uint8(Seggranoctet)
	if descriptor.Attributs&UdescLimiteEntrantepages != 0 {
		attributs_2 = Seggran4kpage
	}
	accès := uint8(Privutilisateur | SegNormale | Présente)
	if descriptor.Attributs&Udescrxseulement != 0 {
		accès |= SegExécution
	} else {
		accès |= Segw
	}
	if accès&SegNormale != 0 {
		attributs_2 |= SegÉlevémode
	}

	tableau_2[index].Fill(descriptor.Baseaddress, descriptor.Limite, accès, attributs_2)
	flushtlsTableau(tableau_2)

	return true
}

func flushtlsTableau(tableau_2 []Gdtélément_2) {
	copy(gdtTableau[TlsDémarrer:], tableau_2[TlsDémarrer:])
}
func FlushtlsTableau(tableau_2 []TSegmentdescriptor) {
	copy(données_2.segmentdescriptor[TlsDémarrer:], tableau_2[TlsDémarrer:])
}
