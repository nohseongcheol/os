package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	Segصارفcode	uint32	= 0x23
	Segصارفdata	uint32	= 0x2B
	Segصارفgs	uint32	= 0x33
	Segtaskحالت	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	حدکم_2		uint16
	baseکم_2	uint16
	baseاونچا_2	uint8
	نوعیت		uint8
	جھنڈیاںحداونچا	uint8
	baseveryاونچا	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, حد_2 uint32, نوعیت uint8, جھنڈیاں_2 uint8) {

	self_2.baseکم_2 = uint16(base_2 & 0xFFFF)
	self_2.baseاونچا_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryاونچا = uint8((base_2 >> 24) & 0xFF)

	self_2.حدکم_2 = uint16(حد_2 & 0xFFFF)
	self_2.جھنڈیاںحداونچا = uint8((حد_2 >> 24) & 0x0F)
	self_2.جھنڈیاںحداونچا |= (جھنڈیاں_2 & 0xF0)

	self_2.نوعیت = نوعیت

}

type TShareddescriptorجدولdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorجدولdata

type TShareddescriptorجدول struct {
}

func (self_2 *TShareddescriptorجدول) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressکم) |
		uint32(gdtdescriptor.Gdtaddressاونچا)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtحجم+1) / Sizeof(gdtentry))
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

	حجم_2 := (*uint16)(Pointer(&destination_3[0]))
	(*حجم_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.Mچھاپیںxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorجدول) Sسیٹdescriptor(idx int, base_2 uint32, حد_2 uint32, نوعیت uint8, جھنڈیاں_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, حد_2, نوعیت, جھنڈیاں_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kصفحہ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segنظام	= 0 << 4
	Segسادہ	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	Privصارف	= 3 << 5

	Segbigmode	= 1 << 6

	Pموجود	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescہدایاتکےموضوعات	= 3 << 1
	Udescrxonly		= 1 << 3
	Udescحداندرpages	= 1 << 4
	Udescsegnotموجود	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsچلائیں	= 16
)

var (
	gdtجدول		= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtجدولlen	= 0
)

type Gdtentry_2 struct {
	حدکم			uint16
	baseکم			uint16
	basemid			uint8
	رسائی			uint8
	حداونچاandجھنڈیاں	uint8
	baseاونچا		uint8
}

func (e *Gdtentry_2) Isموجود() bool {
	return e.رسائی&Pموجود != 0
}

func (e *Gdtentry_2) Fill(base uint32, حد uint32, رسائی uint8, جھنڈیاں uint8) {
	e.حداونچاandجھنڈیاں = uint8((حد >> 16) & 0x000F)
	e.حداونچاandجھنڈیاں |= جھنڈیاں
	e.رسائی = رسائی
	e.basemid = uint8(base >> 16)
	e.baseاونچا = uint8(base >> 24)
	e.baseکم = uint16(base & 0xFFFF)
	e.حدکم = uint16(حد & 0x0000FFFF)
}

func (e *Gdtentry_2) Cصاف() {
	e.حداونچاandجھنڈیاں = 0
	e.رسائی = 0
	e.basemid = 0
	e.baseاونچا = 0
	e.baseکم = 0
	e.حدکم = 0

}

type Gdtdescriptor struct {
	Gdtحجم		uint16
	Gdtaddressکم	uint16
	Gdtaddressاونچا	uint16
}
type Uصارفdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Lحد		uint32
	Fجھنڈیاں	uint8
}

func Sسیٹtlssegment(index uint32, descriptor *Uصارفdescriptor, جدول []Gdtentry_2) bool {
	if index < Tlsچلائیں || index > uint32(len(gdtجدول)) {
		return false
	}

	if descriptor.Fجھنڈیاں == Udescrxonly|Udescsegnotموجود {

		جدول[index].Cصاف()
		return true
	}

	جھنڈیاں := uint8(Seggranbyte)
	if descriptor.Fجھنڈیاں&Udescحداندرpages != 0 {
		جھنڈیاں = Seggran4kصفحہ
	}
	رسائی := uint8(Privصارف | Segسادہ | Pموجود)
	if descriptor.Fجھنڈیاں&Udescrxonly != 0 {
		رسائی |= Segexec
	} else {
		رسائی |= Segw
	}
	if رسائی&Segسادہ != 0 {
		جھنڈیاں |= Segbigmode
	}

	جدول[index].Fill(descriptor.Baseaddress, descriptor.Lحد, رسائی, جھنڈیاں)
	flushtlsجدول(جدول)

	return true
}

func flushtlsجدول(جدول []Gdtentry_2) {
	copy(gdtجدول[Tlsچلائیں:], جدول[Tlsچلائیں:])
}
func Flushtlsجدول(جدول []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsچلائیں:], جدول[Tlsچلائیں:])
}
