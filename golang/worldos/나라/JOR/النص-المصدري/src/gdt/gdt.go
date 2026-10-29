/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "طرفية"

const (
	Segنواةcode	uint32	= 0x08
	Segنواةبيانات	uint32	= 0x10
	Segنواةgs	uint32	= 0x18

	Segمستخدمcode	uint32	= 0x23
	Segمستخدمبيانات	uint32	= 0x2B
	Segمستخدمgs	uint32	= 0x33
	Segمهمةالحالة	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	تحديدمنخفض_2		uint16
	baseمنخفض_2		uint16
	baseعالية_2		uint8
	نوع			uint8
	خياراتتحديدعالية	uint8
	baseveryعالية		uint8
}

func (نفسه_2 *TSegmentdescriptor) Init(base_2 uint32, تحديد_2 uint32, نوع uint8, خيارات_3 uint8) {

	نفسه_2.baseمنخفض_2 = uint16(base_2 & 0xFFFF)
	نفسه_2.baseعالية_2 = uint8((base_2 >> 16) & 0xFF)
	نفسه_2.baseveryعالية = uint8((base_2 >> 24) & 0xFF)

	نفسه_2.تحديدمنخفض_2 = uint16(تحديد_2 & 0xFFFF)
	نفسه_2.خياراتتحديدعالية = uint8((تحديد_2 >> 24) & 0x0F)
	نفسه_2.خياراتتحديدعالية |= (خيارات_3 & 0xF0)

	نفسه_2.نوع = نوع

}

type TShareddescriptorجدولبيانات struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var بيانات_2 TShareddescriptorجدولبيانات

type TShareddescriptorجدول struct {
}

func (نفسه_2 *TShareddescriptorجدول) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressمنخفض) |
		uint32(gdtdescriptor.Gdtaddressعالية)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtالحجم+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(بيانات_2.segmentdescriptor[:], oldgdt)

	بيانات_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	بيانات_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	بيانات_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	المقصد_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&المقصد_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&بيانات_2)))

	الحجم_2 := (*uint16)(Pointer(&المقصد_3[0]))
	(*الحجم_2) = (uint16)((Sizeof(بيانات_2)))

	gdtfunc(uintptr(Pointer(&المقصد_3)))

	terminal := new(Tطرفية)
	terminal.Mاطبعxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32اطبع(uint32(uintptr(Pointer(&بيانات_2.segmentdescriptor[3]))))

}
func (نفسه_2 *TShareddescriptorجدول) Sتحديدdescriptor(idx int, base_2 uint32, تحديد_2 uint32, نوع uint8, خيارات_3 uint8) {
	بيانات_2.segmentdescriptor[idx].Init(base_2, تحديد_2, نوع, خيارات_3)
}

const (
	Kcsفهرس	= 1
	Kdsفهرس	= 2
	Kgsفهرس	= 3

	Kcsselector	= Kcsفهرس * 8
	Kdsselector	= Kdsفهرس * 8
	Kgsselector	= Kgsفهرس * 8

	Seggranبايت	= 0 << 7
	Seggran4kصفحة	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segنظام	= 0 << 4
	Segعادي	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privنواة	= 0 << 5
	Privمستخدم	= 3 << 5

	Segbigوضع	= 1 << 6

	Pالحالي	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescالمحتويات		= 3 << 1
	Udescrxفقط		= 1 << 3
	Udescتحديدداخلصفحات	= 1 << 4
	Udescsegnotالحالي	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsابدأ		= 16
)

var (
	gdtجدول		= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtجدولlen	= 0
)

type Gdtentry_2 struct {
	تحديدمنخفض		uint16
	baseمنخفض		uint16
	basemid			uint8
	نفاذ			uint8
	تحديدعاليةandخيارات	uint8
	baseعالية		uint8
}

func (e *Gdtentry_2) Isالحالي() bool {
	return e.نفاذ&Pالحالي != 0
}

func (e *Gdtentry_2) Fill(base uint32, تحديد uint32, نفاذ uint8, خيارات uint8) {
	e.تحديدعاليةandخيارات = uint8((تحديد >> 16) & 0x000F)
	e.تحديدعاليةandخيارات |= خيارات
	e.نفاذ = نفاذ
	e.basemid = uint8(base >> 16)
	e.baseعالية = uint8(base >> 24)
	e.baseمنخفض = uint16(base & 0xFFFF)
	e.تحديدمنخفض = uint16(تحديد & 0x0000FFFF)
}

func (e *Gdtentry_2) Cامح() {
	e.تحديدعاليةandخيارات = 0
	e.نفاذ = 0
	e.basemid = 0
	e.baseعالية = 0
	e.baseمنخفض = 0
	e.تحديدمنخفض = 0

}

type Gdtdescriptor struct {
	Gdtالحجم	uint16
	Gdtaddressمنخفض	uint16
	Gdtaddressعالية	uint16
}
type Uمستخدمdescriptor struct {
	Entryالأرقام	uint32
	Baseaddress	uint32
	Lتحديد		uint32
	Fخيارات		uint8
}

func Sتحديدtlssegment(فهرس uint32, descriptor *Uمستخدمdescriptor, جدول []Gdtentry_2) bool {
	if فهرس < Tlsابدأ || فهرس > uint32(len(gdtجدول)) {
		return false
	}

	if descriptor.Fخيارات == Udescrxفقط|Udescsegnotالحالي {

		جدول[فهرس].Cامح()
		return true
	}

	خيارات := uint8(Seggranبايت)
	if descriptor.Fخيارات&Udescتحديدداخلصفحات != 0 {
		خيارات = Seggran4kصفحة
	}
	نفاذ := uint8(Privمستخدم | Segعادي | Pالحالي)
	if descriptor.Fخيارات&Udescrxفقط != 0 {
		نفاذ |= Segexec
	} else {
		نفاذ |= Segw
	}
	if نفاذ&Segعادي != 0 {
		خيارات |= Segbigوضع
	}

	جدول[فهرس].Fill(descriptor.Baseaddress, descriptor.Lتحديد, نفاذ, خيارات)
	flushtlsجدول(جدول)

	return true
}

func flushtlsجدول(جدول []Gdtentry_2) {
	copy(gdtجدول[Tlsابدأ:], جدول[Tlsابدأ:])
}
func Flushtlsجدول(جدول []TSegmentdescriptor) {
	copy(بيانات_2.segmentdescriptor[Tlsابدأ:], جدول[Tlsابدأ:])
}
