package gdt

import . "unsafe"
import "reflect"
import . "konsoli"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKäyttäjäcode	uint32	= 0x23
	SegKäyttäjädata	uint32	= 0x2B
	SegKäyttäjägs	uint32	= 0x33
	SegTehtäväTila	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	rajoitusMatala_2	uint16
	baseMatala_2		uint16
	baseKorkea_2		uint8
	tyyppi			uint8
	liputRajoitusKorkea	uint8
	baseveryKorkea		uint8
}

func (itse_2 *TSegmentdescriptor) Init(base_2 uint32, rajoitus_2 uint32, tyyppi uint8, liput_2 uint8) {

	itse_2.baseMatala_2 = uint16(base_2 & 0xFFFF)
	itse_2.baseKorkea_2 = uint8((base_2 >> 16) & 0xFF)
	itse_2.baseveryKorkea = uint8((base_2 >> 24) & 0xFF)

	itse_2.rajoitusMatala_2 = uint16(rajoitus_2 & 0xFFFF)
	itse_2.liputRajoitusKorkea = uint8((rajoitus_2 >> 24) & 0x0F)
	itse_2.liputRajoitusKorkea |= (liput_2 & 0xF0)

	itse_2.tyyppi = tyyppi

}

type TShareddescriptorTaulukkodata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTaulukkodata

type TShareddescriptorTaulukko struct {
}

func (itse_2 *TShareddescriptorTaulukko) Init() {

	var gdthakusana TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressMatala) |
		uint32(gdtdescriptor.GdtaddressKorkea)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtKoko+1) / Sizeof(gdthakusana))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	kohde_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&kohde_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	koko_2 := (*uint16)(Pointer(&kohde_3[0]))
	(*koko_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&kohde_3)))

	terminal := new(TKonsoli)
	terminal.MTulostaxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (itse_2 *TShareddescriptorTaulukko) Asetadescriptor(idx int, base_2 uint32, rajoitus_2 uint32, tyyppi uint8, liput_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, rajoitus_2, tyyppi, liput_2)
}

const (
	KcsHakemisto	= 1
	KdsHakemisto	= 2
	KgsHakemisto	= 3

	Kcsselector	= KcsHakemisto * 8
	Kdsselector	= KdsHakemisto * 8
	Kgsselector	= KgsHakemisto * 8

	Seggranbyte	= 0 << 7
	Seggran4kSivu	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegJärjestelmä	= 0 << 4
	SegNormaali	= 1 << 4

	Segnoexec	= 0 << 3
	SegSuoritus	= 1 << 3

	Privkernel	= 0 << 5
	PrivKäyttäjä	= 3 << 5

	SegbigTILA	= 1 << 6

	Liitetty	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSisältö			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescRajoitusSaapuvapages	= 1 << 4
	UdescsegnotLiitetty		= 1 << 5
	Udescusable			= 1 << 6

	Gdthakusana	= 256
	TlsKäynnistä	= 16
)

var (
	gdtTaulukko	= [Gdthakusana]Gdthakusana_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTaulukkolen	= 0
)

type Gdthakusana_2 struct {
	rajoitusMatala		uint16
	baseMatala		uint16
	basemid			uint8
	pääsy			uint8
	rajoitusKorkeaandLiput	uint8
	baseKorkea		uint8
}

func (e *Gdthakusana_2) IsLiitetty() bool {
	return e.pääsy&Liitetty != 0
}

func (e *Gdthakusana_2) Fill(base uint32, rajoitus uint32, pääsy uint8, liput uint8) {
	e.rajoitusKorkeaandLiput = uint8((rajoitus >> 16) & 0x000F)
	e.rajoitusKorkeaandLiput |= liput
	e.pääsy = pääsy
	e.basemid = uint8(base >> 16)
	e.baseKorkea = uint8(base >> 24)
	e.baseMatala = uint16(base & 0xFFFF)
	e.rajoitusMatala = uint16(rajoitus & 0x0000FFFF)
}

func (e *Gdthakusana_2) Tyhjennä() {
	e.rajoitusKorkeaandLiput = 0
	e.pääsy = 0
	e.basemid = 0
	e.baseKorkea = 0
	e.baseMatala = 0
	e.rajoitusMatala = 0

}

type Gdtdescriptor struct {
	GdtKoko			uint16
	GdtaddressMatala	uint16
	GdtaddressKorkea	uint16
}
type Käyttäjädescriptor struct {
	HakusanaNumero	uint32
	Baseaddress	uint32
	Rajoitus	uint32
	Liput		uint8
}

func Asetatlssegment(hakemisto uint32, descriptor *Käyttäjädescriptor, taulukko_2 []Gdthakusana_2) bool {
	if hakemisto < TlsKäynnistä || hakemisto > uint32(len(gdtTaulukko)) {
		return false
	}

	if descriptor.Liput == Udescrxonly|UdescsegnotLiitetty {

		taulukko_2[hakemisto].Tyhjennä()
		return true
	}

	liput := uint8(Seggranbyte)
	if descriptor.Liput&UdescRajoitusSaapuvapages != 0 {
		liput = Seggran4kSivu
	}
	pääsy := uint8(PrivKäyttäjä | SegNormaali | Liitetty)
	if descriptor.Liput&Udescrxonly != 0 {
		pääsy |= SegSuoritus
	} else {
		pääsy |= Segw
	}
	if pääsy&SegNormaali != 0 {
		liput |= SegbigTILA
	}

	taulukko_2[hakemisto].Fill(descriptor.Baseaddress, descriptor.Rajoitus, pääsy, liput)
	flushtlsTaulukko(taulukko_2)

	return true
}

func flushtlsTaulukko(taulukko_2 []Gdthakusana_2) {
	copy(gdtTaulukko[TlsKäynnistä:], taulukko_2[TlsKäynnistä:])
}
func FlushtlsTaulukko(taulukko_2 []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsKäynnistä:], taulukko_2[TlsKäynnistä:])
}
