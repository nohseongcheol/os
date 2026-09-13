package gdt

import . "unsafe"
import "reflect"
import . "konsol"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegKullanıcıcode	uint32	= 0x23
	SegKullanıcıdata	uint32	= 0x2B
	SegKullanıcıgs		uint32	= 0x33
	SegGörevDurum		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	kısıtlaDüşük_2		uint16
	baseDüşük_2		uint16
	baseYüksek_2		uint8
	tür_2			uint8
	imlerKısıtlaYüksek	uint8
	baseveryYüksek		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, kısıtla_2 uint32, tür_2 uint8, imler_2 uint8) {

	self_2.baseDüşük_2 = uint16(base_2 & 0xFFFF)
	self_2.baseYüksek_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryYüksek = uint8((base_2 >> 24) & 0xFF)

	self_2.kısıtlaDüşük_2 = uint16(kısıtla_2 & 0xFFFF)
	self_2.imlerKısıtlaYüksek = uint8((kısıtla_2 >> 24) & 0x0F)
	self_2.imlerKısıtlaYüksek |= (imler_2 & 0xF0)

	self_2.tür_2 = tür_2

}

type TShareddescriptorTablodata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTablodata

type TShareddescriptorTablo struct {
}

func (self_2 *TShareddescriptorTablo) Init() {

	var gdtgirdi TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressDüşük) |
		uint32(gdtdescriptor.GdtaddressYüksek)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtBoyut+1) / Sizeof(gdtgirdi))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	hedef_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&hedef_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	boyut_2 := (*uint16)(Pointer(&hedef_3[0]))
	(*boyut_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&hedef_3)))

	terminal := new(TKonsol)
	terminal.MYazdırxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorTablo) Ayarladescriptor(idx int, base_2 uint32, kısıtla_2 uint32, tür_2 uint8, imler_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, kısıtla_2, tür_2, imler_2)
}

const (
	Kcsİçindekiler	= 1
	Kdsİçindekiler	= 2
	Kgsİçindekiler	= 3

	Kcsselector	= Kcsİçindekiler * 8
	Kdsselector	= Kdsİçindekiler * 8
	Kgsselector	= Kgsİçindekiler * 8

	Seggranbyte	= 0 << 7
	Seggran4kSayfa	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	SegÇalıştır	= 1 << 3

	Privkernel	= 0 << 5
	PrivKullanıcı	= 3 << 5

	SegbigKİP	= 1 << 6

	Mevcut	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescİçindekiler	= 3 << 1
	Udescrxonly		= 1 << 3
	UdescKısıtlaGelenpages	= 1 << 4
	UdescsegnotMevcut	= 1 << 5
	Udescusable		= 1 << 6

	Gdtgirdi	= 256
	TlsBaşlat	= 16
)

var (
	gdtTablo	= [Gdtgirdi]Gdtgirdi_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTablolen	= 0
)

type Gdtgirdi_2 struct {
	kısıtlaDüşük		uint16
	baseDüşük		uint16
	basemid			uint8
	erişim			uint8
	kısıtlaYüksekVEİmler	uint8
	baseYüksek		uint8
}

func (e *Gdtgirdi_2) IsMevcut() bool {
	return e.erişim&Mevcut != 0
}

func (e *Gdtgirdi_2) Fill(base uint32, kısıtla uint32, erişim uint8, imler uint8) {
	e.kısıtlaYüksekVEİmler = uint8((kısıtla >> 16) & 0x000F)
	e.kısıtlaYüksekVEİmler |= imler
	e.erişim = erişim
	e.basemid = uint8(base >> 16)
	e.baseYüksek = uint8(base >> 24)
	e.baseDüşük = uint16(base & 0xFFFF)
	e.kısıtlaDüşük = uint16(kısıtla & 0x0000FFFF)
}

func (e *Gdtgirdi_2) Temizle() {
	e.kısıtlaYüksekVEİmler = 0
	e.erişim = 0
	e.basemid = 0
	e.baseYüksek = 0
	e.baseDüşük = 0
	e.kısıtlaDüşük = 0

}

type Gdtdescriptor struct {
	GdtBoyut		uint16
	GdtaddressDüşük		uint16
	GdtaddressYüksek	uint16
}
type Kullanıcıdescriptor struct {
	GirdiSayı	uint32
	Baseaddress	uint32
	Kısıtla		uint32
	İmler		uint8
}

func Ayarlatlssegment(içindekiler uint32, descriptor *Kullanıcıdescriptor, tablo []Gdtgirdi_2) bool {
	if içindekiler < TlsBaşlat || içindekiler > uint32(len(gdtTablo)) {
		return false
	}

	if descriptor.İmler == Udescrxonly|UdescsegnotMevcut {

		tablo[içindekiler].Temizle()
		return true
	}

	imler := uint8(Seggranbyte)
	if descriptor.İmler&UdescKısıtlaGelenpages != 0 {
		imler = Seggran4kSayfa
	}
	erişim := uint8(PrivKullanıcı | Segnormal | Mevcut)
	if descriptor.İmler&Udescrxonly != 0 {
		erişim |= SegÇalıştır
	} else {
		erişim |= Segw
	}
	if erişim&Segnormal != 0 {
		imler |= SegbigKİP
	}

	tablo[içindekiler].Fill(descriptor.Baseaddress, descriptor.Kısıtla, erişim, imler)
	flushtlsTablo(tablo)

	return true
}

func flushtlsTablo(tablo []Gdtgirdi_2) {
	copy(gdtTablo[TlsBaşlat:], tablo[TlsBaşlat:])
}
func FlushtlsTablo(tablo []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsBaşlat:], tablo[TlsBaşlat:])
}
