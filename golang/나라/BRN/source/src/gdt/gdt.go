package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegPenggunacode	uint32	= 0x23
	SegPenggunadata	uint32	= 0x2B
	SegPenggunags	uint32	= 0x33
	SegTugasKeadaan	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	hadRendah_2		uint16
	baseRendah_2		uint16
	baseTinggi_2		uint8
	jenis			uint8
	benderaHadTinggi	uint8
	baseveryTinggi		uint8
}

func (diri_2 *TSegmentdescriptor) Init(base_2 uint32, had_2 uint32, jenis uint8, bendera_2 uint8) {

	diri_2.baseRendah_2 = uint16(base_2 & 0xFFFF)
	diri_2.baseTinggi_2 = uint8((base_2 >> 16) & 0xFF)
	diri_2.baseveryTinggi = uint8((base_2 >> 24) & 0xFF)

	diri_2.hadRendah_2 = uint16(had_2 & 0xFFFF)
	diri_2.benderaHadTinggi = uint8((had_2 >> 24) & 0x0F)
	diri_2.benderaHadTinggi |= (bendera_2 & 0xF0)

	diri_2.jenis = jenis

}

type TShareddescriptorJadualdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorJadualdata

type TShareddescriptorJadual struct {
}

func (diri_2 *TShareddescriptorJadual) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressRendah) |
		uint32(gdtdescriptor.GdtaddressTinggi)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtSaiz+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	saiz_2 := (*uint16)(Pointer(&destination_3[0]))
	(*saiz_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MCetakxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (diri_2 *TShareddescriptorJadual) Tetapkandescriptor(idx int, base_2 uint32, had_2 uint32, jenis uint8, bendera_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, had_2, jenis, bendera_2)
}

const (
	KcsIndeks	= 1
	KdsIndeks	= 2
	KgsIndeks	= 3

	Kcsselector	= KcsIndeks * 8
	Kdsselector	= KdsIndeks * 8
	Kgsselector	= KgsIndeks * 8

	Seggranbyte		= 0 << 7
	Seggran4kHalaman	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	SegBiasa	= 1 << 4

	Segnoexec	= 0 << 3
	SegJalankan	= 1 << 3

	Privkernel	= 0 << 5
	PrivPengguna	= 3 << 5

	Segbigmod	= 1 << 6

	Hadir	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescKandungan		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescHadMasukHalaman	= 1 << 4
	UdescsegnotHadir	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsMula		= 16
)

var (
	gdtJadual	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtJaduallen	= 0
)

type Gdtentry_2 struct {
	hadRendah		uint16
	baseRendah		uint16
	basemid			uint8
	capai			uint8
	hadTinggiandBendera	uint8
	baseTinggi		uint8
}

func (e *Gdtentry_2) IsHadir() bool {
	return e.capai&Hadir != 0
}

func (e *Gdtentry_2) Fill(base uint32, had uint32, capai uint8, bendera uint8) {
	e.hadTinggiandBendera = uint8((had >> 16) & 0x000F)
	e.hadTinggiandBendera |= bendera
	e.capai = capai
	e.basemid = uint8(base >> 16)
	e.baseTinggi = uint8(base >> 24)
	e.baseRendah = uint16(base & 0xFFFF)
	e.hadRendah = uint16(had & 0x0000FFFF)
}

func (e *Gdtentry_2) Kosongkan() {
	e.hadTinggiandBendera = 0
	e.capai = 0
	e.basemid = 0
	e.baseTinggi = 0
	e.baseRendah = 0
	e.hadRendah = 0

}

type Gdtdescriptor struct {
	GdtSaiz			uint16
	GdtaddressRendah	uint16
	GdtaddressTinggi	uint16
}
type Penggunadescriptor struct {
	EntryNOMBOR	uint32
	Baseaddress	uint32
	Had		uint32
	Bendera		uint8
}

func Tetapkantlssegment(indeks uint32, descriptor *Penggunadescriptor, jadual []Gdtentry_2) bool {
	if indeks < TlsMula || indeks > uint32(len(gdtJadual)) {
		return false
	}

	if descriptor.Bendera == Udescrxonly|UdescsegnotHadir {

		jadual[indeks].Kosongkan()
		return true
	}

	bendera := uint8(Seggranbyte)
	if descriptor.Bendera&UdescHadMasukHalaman != 0 {
		bendera = Seggran4kHalaman
	}
	capai := uint8(PrivPengguna | SegBiasa | Hadir)
	if descriptor.Bendera&Udescrxonly != 0 {
		capai |= SegJalankan
	} else {
		capai |= Segw
	}
	if capai&SegBiasa != 0 {
		bendera |= Segbigmod
	}

	jadual[indeks].Fill(descriptor.Baseaddress, descriptor.Had, capai, bendera)
	flushtlsJadual(jadual)

	return true
}

func flushtlsJadual(jadual []Gdtentry_2) {
	copy(gdtJadual[TlsMula:], jadual[TlsMula:])
}
func FlushtlsJadual(jadual []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsMula:], jadual[TlsMula:])
}
