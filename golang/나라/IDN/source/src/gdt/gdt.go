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
	SegTugasStatus	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	batasRendah_2		uint16
	baseRendah_2		uint16
	baseTinggi_2		uint8
	tipe			uint8
	tandaBatasTinggi	uint8
	baseveryTinggi		uint8
}

func (dirisendiri_2 *TSegmentdescriptor) Init(base_2 uint32, batas_2 uint32, tipe uint8, tanda_2 uint8) {

	dirisendiri_2.baseRendah_2 = uint16(base_2 & 0xFFFF)
	dirisendiri_2.baseTinggi_2 = uint8((base_2 >> 16) & 0xFF)
	dirisendiri_2.baseveryTinggi = uint8((base_2 >> 24) & 0xFF)

	dirisendiri_2.batasRendah_2 = uint16(batas_2 & 0xFFFF)
	dirisendiri_2.tandaBatasTinggi = uint8((batas_2 >> 24) & 0x0F)
	dirisendiri_2.tandaBatasTinggi |= (tanda_2 & 0xF0)

	dirisendiri_2.tipe = tipe

}

type TShareddescriptorTabeldata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeldata

type TShareddescriptorTabel struct {
}

func (dirisendiri_2 *TShareddescriptorTabel) Init() {

	var gdtentri TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressRendah) |
		uint32(gdtdescriptor.GdtaddressTinggi)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtUkuran+1) / Sizeof(gdtentri))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	tujuan_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&tujuan_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	ukuran_2 := (*uint16)(Pointer(&tujuan_3[0]))
	(*ukuran_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&tujuan_3)))

	terminal := new(TConsole)
	terminal.MCetakxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (dirisendiri_2 *TShareddescriptorTabel) Aturdescriptor(idx int, base_2 uint32, batas_2 uint32, tipe uint8, tanda_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, batas_2, tipe, tanda_2)
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
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivPengguna	= 3 << 5

	Segbigmode	= 1 << 6

	Ada	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescIsi		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescBatasMasukpages	= 1 << 4
	UdescsegnotAda		= 1 << 5
	Udescusable		= 1 << 6

	Gdtentri	= 256
	TlsMulai	= 16
)

var (
	gdtTabel	= [Gdtentri]Gdtentri_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabellen	= 0
)

type Gdtentri_2 struct {
	batasRendah		uint16
	baseRendah		uint16
	basemid			uint8
	akses			uint8
	batasTinggidanTanda	uint8
	baseTinggi		uint8
}

func (e *Gdtentri_2) IsAda() bool {
	return e.akses&Ada != 0
}

func (e *Gdtentri_2) Fill(base uint32, batas uint32, akses uint8, tanda uint8) {
	e.batasTinggidanTanda = uint8((batas >> 16) & 0x000F)
	e.batasTinggidanTanda |= tanda
	e.akses = akses
	e.basemid = uint8(base >> 16)
	e.baseTinggi = uint8(base >> 24)
	e.baseRendah = uint16(base & 0xFFFF)
	e.batasRendah = uint16(batas & 0x0000FFFF)
}

func (e *Gdtentri_2) Bersihkan() {
	e.batasTinggidanTanda = 0
	e.akses = 0
	e.basemid = 0
	e.baseTinggi = 0
	e.baseRendah = 0
	e.batasRendah = 0

}

type Gdtdescriptor struct {
	GdtUkuran		uint16
	GdtaddressRendah	uint16
	GdtaddressTinggi	uint16
}
type Penggunadescriptor struct {
	EntriNomor	uint32
	Baseaddress	uint32
	Batas		uint32
	Tanda		uint8
}

func Aturtlssegment(indeks uint32, descriptor *Penggunadescriptor, tabel_2 []Gdtentri_2) bool {
	if indeks < TlsMulai || indeks > uint32(len(gdtTabel)) {
		return false
	}

	if descriptor.Tanda == Udescrxonly|UdescsegnotAda {

		tabel_2[indeks].Bersihkan()
		return true
	}

	tanda := uint8(Seggranbyte)
	if descriptor.Tanda&UdescBatasMasukpages != 0 {
		tanda = Seggran4kHalaman
	}
	akses := uint8(PrivPengguna | Segnormal | Ada)
	if descriptor.Tanda&Udescrxonly != 0 {
		akses |= Segexec
	} else {
		akses |= Segw
	}
	if akses&Segnormal != 0 {
		tanda |= Segbigmode
	}

	tabel_2[indeks].Fill(descriptor.Baseaddress, descriptor.Batas, akses, tanda)
	flushtlsTabel(tabel_2)

	return true
}

func flushtlsTabel(tabel_2 []Gdtentri_2) {
	copy(gdtTabel[TlsMulai:], tabel_2[TlsMulai:])
}
func FlushtlsTabel(tabel_2 []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsMulai:], tabel_2[TlsMulai:])
}
