package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKorisnikcode		uint32	= 0x23
	SegKorisnikdata		uint32	= 0x2B
	SegKorisnikgs		uint32	= 0x33
	SegZadatakStanje	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ograničenjeNIsko_2		uint16
	baseNIsko_2			uint16
	baseVisoko_2			uint8
	vrsta				uint8
	zastaviceOgraničenjeVisoko	uint8
	baseveryVisoko			uint8
}

func (sam_2 *TSegmentdescriptor) Init(base_2 uint32, ograničenje_2 uint32, vrsta uint8, zastavice_2 uint8) {

	sam_2.baseNIsko_2 = uint16(base_2 & 0xFFFF)
	sam_2.baseVisoko_2 = uint8((base_2 >> 16) & 0xFF)
	sam_2.baseveryVisoko = uint8((base_2 >> 24) & 0xFF)

	sam_2.ograničenjeNIsko_2 = uint16(ograničenje_2 & 0xFFFF)
	sam_2.zastaviceOgraničenjeVisoko = uint8((ograničenje_2 >> 24) & 0x0F)
	sam_2.zastaviceOgraničenjeVisoko |= (zastavice_2 & 0xF0)

	sam_2.vrsta = vrsta

}

type TShareddescriptorTablicadata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTablicadata

type TShareddescriptorTablica struct {
}

func (sam_2 *TShareddescriptorTablica) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressNIsko) |
		uint32(gdtdescriptor.GdtaddressVisoko)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVeličina+1) / Sizeof(gdtentry))
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

	terminal := new(TConsole)
	terminal.MIspisxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (sam_2 *TShareddescriptorTablica) Postavidescriptor(idx int, base_2 uint32, ograničenje_2 uint32, vrsta uint8, zastavice_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ograničenje_2, vrsta, zastavice_2)
}

const (
	KcsKazalo	= 1
	KdsKazalo	= 2
	KgsKazalo	= 3

	Kcsselector	= KcsKazalo * 8
	Kdsselector	= KdsKazalo * 8
	Kgsselector	= KgsKazalo * 8

	Seggranbyte		= 0 << 7
	Seggran4kStranica	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSustav	= 0 << 4
	SegNormalno	= 1 << 4

	Segnoexec	= 0 << 3
	SegIzvrši	= 1 << 3

	Privkernel	= 0 << 5
	PrivKorisnik	= 3 << 5

	SegbigNAČIN	= 1 << 6

	Prisutno	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSadržaj			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescOgraničenjePovećajStranice	= 1 << 4
	UdescsegnotPrisutno		= 1 << 5
	Udescusable			= 1 << 6

	Gdtentry	= 256
	TlsPokreni	= 16
)

var (
	gdtTablica	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTablicalen	= 0
)

type Gdtentry_2 struct {
	ograničenjeNIsko		uint16
	baseNIsko			uint16
	basemid				uint8
	pristup				uint8
	ograničenjeVisokoandZastavice	uint8
	baseVisoko			uint8
}

func (e *Gdtentry_2) IsPrisutno() bool {
	return e.pristup&Prisutno != 0
}

func (e *Gdtentry_2) Fill(base uint32, ograničenje uint32, pristup uint8, zastavice uint8) {
	e.ograničenjeVisokoandZastavice = uint8((ograničenje >> 16) & 0x000F)
	e.ograničenjeVisokoandZastavice |= zastavice
	e.pristup = pristup
	e.basemid = uint8(base >> 16)
	e.baseVisoko = uint8(base >> 24)
	e.baseNIsko = uint16(base & 0xFFFF)
	e.ograničenjeNIsko = uint16(ograničenje & 0x0000FFFF)
}

func (e *Gdtentry_2) Očisti() {
	e.ograničenjeVisokoandZastavice = 0
	e.pristup = 0
	e.basemid = 0
	e.baseVisoko = 0
	e.baseNIsko = 0
	e.ograničenjeNIsko = 0

}

type Gdtdescriptor struct {
	GdtVeličina		uint16
	GdtaddressNIsko		uint16
	GdtaddressVisoko	uint16
}
type Korisnikdescriptor struct {
	EntryBROJ	uint32
	Baseaddress	uint32
	Ograničenje	uint32
	Zastavice	uint8
}

func Postavitlssegment(kazalo uint32, descriptor *Korisnikdescriptor, tablica []Gdtentry_2) bool {
	if kazalo < TlsPokreni || kazalo > uint32(len(gdtTablica)) {
		return false
	}

	if descriptor.Zastavice == Udescrxonly|UdescsegnotPrisutno {

		tablica[kazalo].Očisti()
		return true
	}

	zastavice := uint8(Seggranbyte)
	if descriptor.Zastavice&UdescOgraničenjePovećajStranice != 0 {
		zastavice = Seggran4kStranica
	}
	pristup := uint8(PrivKorisnik | SegNormalno | Prisutno)
	if descriptor.Zastavice&Udescrxonly != 0 {
		pristup |= SegIzvrši
	} else {
		pristup |= Segw
	}
	if pristup&SegNormalno != 0 {
		zastavice |= SegbigNAČIN
	}

	tablica[kazalo].Fill(descriptor.Baseaddress, descriptor.Ograničenje, pristup, zastavice)
	flushtlsTablica(tablica)

	return true
}

func flushtlsTablica(tablica []Gdtentry_2) {
	copy(gdtTablica[TlsPokreni:], tablica[TlsPokreni:])
}
func FlushtlsTablica(tablica []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsPokreni:], tablica[TlsPokreni:])
}
