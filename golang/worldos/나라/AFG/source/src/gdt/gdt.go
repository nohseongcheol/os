/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	Segکاربرcode	uint32	= 0x23
	Segکاربرdata	uint32	= 0x2B
	Segکاربرgs	uint32	= 0x33
	Segtaskحالت	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitاندک_2	uint16
	baseاندک_2	uint16
	baseزیاد_2	uint8
	نوع		uint8
	flagslimitزیاد	uint8
	baseveryزیاد	uint8
}

func (خود_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, نوع uint8, flags_2 uint8) {

	خود_2.baseاندک_2 = uint16(base_2 & 0xFFFF)
	خود_2.baseزیاد_2 = uint8((base_2 >> 16) & 0xFF)
	خود_2.baseveryزیاد = uint8((base_2 >> 24) & 0xFF)

	خود_2.limitاندک_2 = uint16(limit_2 & 0xFFFF)
	خود_2.flagslimitزیاد = uint8((limit_2 >> 24) & 0x0F)
	خود_2.flagslimitزیاد |= (flags_2 & 0xF0)

	خود_2.نوع = نوع

}

type TShareddescriptorجدولdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorجدولdata

type TShareddescriptorجدول struct {
}

func (خود_2 *TShareddescriptorجدول) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressاندک) |
		uint32(gdtdescriptor.Gdtaddressزیاد)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtاندازه+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	مقصد_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&مقصد_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	اندازه_2 := (*uint16)(Pointer(&مقصد_3[0]))
	(*اندازه_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&مقصد_3)))

	terminal := new(TConsole)
	terminal.Mچاپxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (خود_2 *TShareddescriptorجدول) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, نوع uint8, flags_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, نوع, flags_2)
}

const (
	Kcsنمایه	= 1
	Kdsنمایه	= 2
	Kgsنمایه	= 3

	Kcsselector	= Kcsنمایه * 8
	Kdsselector	= Kdsنمایه * 8
	Kgsselector	= Kgsنمایه * 8

	Seggranbyte	= 0 << 7
	Seggran4kصفحه	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segسیستم	= 0 << 4
	Segعادی		= 1 << 4

	Segnoexec	= 0 << 3
	Segاجرا		= 1 << 3

	Privkernel	= 0 << 5
	Privکاربر	= 3 << 5

	Segbigحالت	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescمحتویات		= 3 << 1
	Udescrxonly		= 1 << 3
	Udesclimitداخلpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsstart	= 16
)

var (
	gdtجدول		= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtجدولlen	= 0
)

type Gdtentry_2 struct {
	limitاندک		uint16
	baseاندک		uint16
	basemid			uint8
	access			uint8
	limitزیادandflags	uint8
	baseزیاد		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, flags uint8) {
	e.limitزیادandflags = uint8((limit >> 16) & 0x000F)
	e.limitزیادandflags |= flags
	e.access = access
	e.basemid = uint8(base >> 16)
	e.baseزیاد = uint8(base >> 24)
	e.baseاندک = uint16(base & 0xFFFF)
	e.limitاندک = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Cپاککردن() {
	e.limitزیادandflags = 0
	e.access = 0
	e.basemid = 0
	e.baseزیاد = 0
	e.baseاندک = 0
	e.limitاندک = 0

}

type Gdtdescriptor struct {
	Gdtاندازه	uint16
	Gdtaddressاندک	uint16
	Gdtaddressزیاد	uint16
}
type Uکاربرdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Flags		uint8
}

func Settlssegment(نمایه uint32, descriptor *Uکاربرdescriptor, جدول []Gdtentry_2) bool {
	if نمایه < Tlsstart || نمایه > uint32(len(gdtجدول)) {
		return false
	}

	if descriptor.Flags == Udescrxonly|Udescsegnotpresent {

		جدول[نمایه].Cپاککردن()
		return true
	}

	flags := uint8(Seggranbyte)
	if descriptor.Flags&Udesclimitداخلpages != 0 {
		flags = Seggran4kصفحه
	}
	access := uint8(Privکاربر | Segعادی | Present)
	if descriptor.Flags&Udescrxonly != 0 {
		access |= Segاجرا
	} else {
		access |= Segw
	}
	if access&Segعادی != 0 {
		flags |= Segbigحالت
	}

	جدول[نمایه].Fill(descriptor.Baseaddress, descriptor.Limit, access, flags)
	flushtlsجدول(جدول)

	return true
}

func flushtlsجدول(جدول []Gdtentry_2) {
	copy(gdtجدول[Tlsstart:], جدول[Tlsstart:])
}
func Flushtlsجدول(جدول []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], جدول[Tlsstart:])
}
